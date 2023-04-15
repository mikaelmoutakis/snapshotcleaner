#!/usr/bin/env python

"""snapshotcleaner: Cleans up old zfs snapshots

Usage:
  snapshotcleaner <end_date> <dataset> [-R --recursive] [--dry-run]
  snapshotcleaner -h | --help

Options:
  -h --help            Shows this help text.
  -R, --recursive      Remove snapshots from child datasets recursively
  --dry-run            Show which snapshots to remove, but don't remove them
"""

# Import required libraries
from docopt import docopt
import subprocess
from datetime import datetime
import re


# Function to validate the date format
def is_valid_date(date_string):
    try:
        datetime.fromisoformat(date_string)
        return True
    except ValueError:
        return False


# Function to check if the dataset is valid
def is_valid_dataset(dataset):
    result = subprocess.run(
        ["zfs", "list", dataset], stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    return result.returncode == 0


# Function to remove snapshots based on the given parameters
def remove_snapshots(end_date, dataset, recursive=False, dry_run=False):
    end_date = datetime.fromisoformat(
        end_date
    )  # Convert the end_date string to a datetime object
    # Prepare the command to list snapshots
    list_snapshots_command = [
        "zfs",
        "list",
        "-t",
        "snapshot",
        "-o",
        "name,creation",
        "-s",
        "creation",
    ]
    if recursive:
        list_snapshots_command.append("-r")
    list_snapshots_command.append(dataset)

    # Execute the command and decode the output
    snapshot_list_output = subprocess.check_output(list_snapshots_command).decode(
        "utf-8"
    )
    snapshot_lines = snapshot_list_output.strip().split("\n")[
        1:
    ]  # Split the output into lines and skip the header

    snapshots_to_remove = []
    for snapshot_line in snapshot_lines:
        # Split the line into snapshot name and creation date
        snapshot_name, snapshot_creation = re.split(
            r"\s+", snapshot_line.strip(), maxsplit=1
        )
        # Convert the snapshot creation date string to a datetime object
        snapshot_creation_date = datetime.fromisoformat(snapshot_creation)
        # Check if the snapshot creation date is before the end_date
        if snapshot_creation_date < end_date:
            snapshots_to_remove.append(snapshot_name)

    # Perform dry-run or actual removal based on the option
    if dry_run:
        for snapshot_name in snapshots_to_remove:
            print("Would remove snapshot:", snapshot_name)
    else:
        for snapshot_name in snapshots_to_remove:
            print("Removing snapshot:", snapshot_name)
            subprocess.run(["zfs", "destroy", snapshot_name])


# Main script entry point
if __name__ == "__main__":
    arguments = docopt(
        __doc__, version="0.1"
    )  # Parse command-line arguments using docopt

    # Validate end_date and dataset input
    if not is_valid_date(arguments["<end_date>"]):
        print("Error: Invalid end_date. Please provide a valid ISO date.")
        exit(1)

    if not is_valid_dataset(arguments["<dataset>"]):
        print("Error: Invalid dataset. Please provide a valid zfs dataset.")
        exit(1)

    # Call the remove_snapshots function with the parsed arguments
    remove_snapshots(
        arguments["<end_date>"],
        arguments["<dataset>"],
        arguments["--recursive"],
        arguments["--dry-run"],
    )
