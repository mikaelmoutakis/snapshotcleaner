# Snapshotcleaner
A command line application in Python that clean up old zfs snapshots. 

The application should have the following command line interface:

```
  snapshotcleaner: Cleans up old zfs snapshots

  Usage:
    snapshotcleaner <end_date> <dataset>
    snapshotcleaner -h


  Options:
    -h --help     		Shows this help text.
    -R, --recursive		Remove snapshots from child datasets recursively
    --dry-run				Show which snapshots to remove, but don"t remove them
```

The command "snapshotcleaner <end_date> <dataset>" removes all snapshots of
dataset "<dataset>" taken before the date "<end_date>". 

For example, "snapshotcleaner 2022-04-05 poolname/mydata" removes all zfs snapshots
of the dataset "poolname/mydata" taken before 2022-04-05 (the fifth of April, 2022). 

Before removing the snapshot, "snapshotcleaner" checks that the variable "<end_date>"
is a valid ISO date, and that the variable "<dataset>" refers to a valid zfs dataset. 
dddd
Running "snapshotcleaner" with the command-line option "--dry-run" means that the program
prints all snapshots that will be deleted, but without deleting them. 

Running "snapshotcleaner" with the command-line option "--recursive" means that the program
deletes zfs snapshots from the child datasets of "<dataset>". 


## Installation:
Clone the repository:
  
  git clone https://github.com/mikaelmoutakis/snapshotcleaner
  cd snapshotcleaner
  python3 setup.py install
  
Running `python3 setyp.py install` installs the program file at "/usr/local/bin/snapshotcleaner" and all its python libraries at the directory "/usr/local/lib/snapshotcleaner/".
