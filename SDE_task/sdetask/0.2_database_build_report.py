#!/usr/bin/env python3

"""test_db_creation.py

Author: Matthew Southerington

Gather information on the output of the following code snippet:
    sqlite3 data/mortgages.db < bin/create_db.sql

Written as it has to be assumed that CSV or other input data may not be
    visible in future.

To inform the new user of:
    Content and structure of tables
    Sample Data
    Success of build
"""


import sqlite3

# Database connection
conn = sqlite3.connect('SDE_task/sdetask/data/mortgages.db')

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
    # Variable Descriptors
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
