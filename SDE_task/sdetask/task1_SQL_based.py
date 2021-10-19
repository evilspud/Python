#!/usr/bin/env python3

"""test_db_creation.py

Author: Matthew Southerington

Create summary CSV report
    Total number of accounts by product type
    Sum of account balances by product type

    The report contains the following 3 columns:

    - product_type (based on PRODUCTS.PD_PRODUCT_TYPE)
    - total_accounts
    - total_balance (based on ACCOUNTS.A_ACCOUNT_BALANCE)

Returns file 'product_summary_report.csv'.
"""

import csv
import sqlite3

# set connection to named database
conn = sqlite3.connect('SDE_task/sdetask/data/mortgages.db')

# create a cursor for passing commands to the database
c = conn.cursor()

# join accounts to products by product number
c.execute("""SELECT DISTINCT
                products.pd_product_type as product_type
                ,count(accounts.a_account_number) as total_accounts
                ,sum(accounts.a_account_balance) as total_balance
            FROM accounts
            LEFT JOIN products
            ON accounts.a_product_number = products.pd_product_number
            GROUP BY products.pd_product_type

"""
          )

# CSV export
# use with statement so that csv path only remains open when being used
# open csv in write mode
with open('SDE_task/sdetask/output/product_summary_report.csv', 'w') as f:

    # create the csv writer
    writer = csv.writer(f)

    # get headings from the cursor description of last executed statement
    # Use first list index as headers
    writer.writerow(information[0] for information in c.description)

    # write results of the last execution i.e. cursor (c) to the csv file
    writer.writerows(c)

# close connection
conn.close()
