#!/usr/bin/env python3

"""set_parameters.py

Author: Matthew Southerington

Set necessary user-defined parameters. Return an error if an invalid filepath
is defined.
"""

import errno
import os

print("Set_parameters.py starts")


def path_existence(path: str):
    """Test the existence of the specified path
    Args: path (str): A string representing the path to be tested

    Returns: Message if file exists, or raises error if not
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path
        )
    return print(f"Path {path} exists.")


root_dir = "SDE_task/sdetask/"

db_location = "data/mortgages.db"
db_path = root_dir + db_location

# Test path
path_existence(db_path)

# Proposed output locations - not tested as will not exist yet
# Test for directory existence could be added
csv_location = "output/product_summary_report.csv"
csv_path = root_dir + csv_location

json_location = "output/mortgages_data.json"
json_path = root_dir + json_location

print("Set_parameters.py ends")
