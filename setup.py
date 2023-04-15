from setuptools import setup, find_packages
import os

# Create the shell script content
shell_script = """#!/bin/sh
python3 /usr/local/lib/snapshotcleaner/snapshotcleaner.py "$@"
"""

# Create the shell script file
with open("snapshotcleaner.sh", "w") as f:
    f.write(shell_script)

# Make the shell script executable
os.chmod("snapshotcleaner.sh", 0o755)

setup(
    name="snapshotcleaner",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "docopt",
    ],
    entry_points={
        "console_scripts": [
            "snapshotcleaner = snapshotcleaner:snapshotcleaner",
        ],
    },
    data_files=[
        ("/usr/local/lib/snapshotcleaner", ["snapshotcleaner.py"]),
        ("/usr/local/bin", ["snapshotcleaner.sh"]),
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
