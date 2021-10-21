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

# set connection to named database
conn = sqlite3.connect('SDE_task/sdetask/data/mortgages.db')

# create a cursor for passing commands to the database
c = conn.cursor()

# print list of database tables from SQLite default master table
c.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
table_names = c.fetchall()

# create report
# header
print("TABLES:")
# For each table, print name, list of column attributes and sample data
for table_name in table_names:
    print(table_name[0], "\n")

    # print meaning of column attributes by getting
    # info of SQLite pragma table itself
    c.execute("SELECT * FROM pragma_table_info")
    # use cursor description to list variable names
    column_attribute_headers = [variable[0] for variable in c.description]
    print(column_attribute_headers)

    # column attributes
    # insert table name into SQLite statement
    c.execute("pragma table_info('%s')" % table_name)
    column_attributes = c.fetchall()
    # list comprehension for easy reading
    for column_attribute in column_attributes:
        print(column_attribute)
    # line break
    print("\n")

    # show sample of data
    c.execute("SELECT * FROM '%s'" % table_name)
    datalines = c.fetchmany(10)
    for dataline in datalines:
        print(dataline)
    # line break
    print("\n")

# close connection
conn.close()
