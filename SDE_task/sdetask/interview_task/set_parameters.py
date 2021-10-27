#!/usr/bin/env python3

"""set_parameters.py

Author: Matthew Southerington

Set necessary user-defined parameters. Return an error is an invalid filepath
is defined.
"""
import os
import errno

root_dir = "SDE_task/sdetask/"

db_location = "data/mortgages.db"
db_path = root_dir + db_location

# File existence
if not os.path.exists(db_path):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), db_path)
