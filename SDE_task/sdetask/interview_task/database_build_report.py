#!/usr/bin/env python3

"""database_build_report.py

Author: Matthew Southerington

Gather information on the output of the following code snippet:
    sqlite3 data/mortgages.db < bin/create_db.sql

Written as it has to be assumed that CSV or other input data may not be
    visible in future.

To inform the new user of:
    Content and structure of tables
    Sample Data
    Success of build

Output: Printed to terminal
"""

import sqlite3

from set_parameters import db_path

print("database_build_report.py starts")

# Database connection
conn = sqlite3.connect(db_path)

# Cursor
c = conn.cursor()

# List of database tables
c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
table_names = c.fetchall()

# Table Structure Report
print("TABLES:")
for table_name in table_names:
    print(table_name[0], "\n")

    # Column Attributes - Meaning
    c.execute("SELECT * FROM pragma_table_info")
    column_attribute_headers = [descriptor[0] for descriptor in c.description]
    print(column_attribute_headers)

    # Column Attributes
    c.execute("pragma table_info('%s')" % table_name)
    column_attributes = c.fetchall()

    for column_attribute in column_attributes:
        print(column_attribute)
    print("\n")

    # Data Sample
    c.execute("SELECT * FROM '%s'" % table_name)
    datalines = c.fetchmany(20)
    for dataline in datalines:
        print(dataline)
    print("\n")

conn.close()

print("database_build_report.py ends")
