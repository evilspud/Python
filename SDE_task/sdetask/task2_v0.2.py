#!/usr/bin/env python3

"""xxxxxxxxxx.py

Author: Matthew Southerington

Extract data from the SQLite3 mortgages database (data/mortgages.db)
and create a JSON file called mortgages_data.json

JSON output fields:

    _months_in_arrears_:
        Defined as the absolute arrears balance for an account divided by the
        regular monthly payment amount. The value should be rounded to 1
        decimal place. The minimum value should be 0

    _in_possession_:
        A boolean flag derived from PROPERTIES.PT_IN_POSSESSION

    _in_default_:
        An account is said to be in default in (any of) the following
        circumstances:
            1. The account is in possession
            2. The account is 3 months or more in arrears and either customer 1
                or customer 2 is bankrupt
            3. The account is more than 6 months in arrears

    _customer_position_:
        Derived from ACCOUNTS_CUSTOMERS_LINK.ACL_CUSTOMER_POSITION

    _is_bankrupt_:
        A boolean flag derived from CUSTOMERS.C_BANKRUPTCY_IND

    _is_deceased_:
        This should be set to 'true' if the CUSTOMERS.C_DECEASED_DATE is
        populated

"""

import json
import sqlite3

# set connection to named database
conn = sqlite3.connect('SDE_task/sdetask/data/mortgages.db')

with conn:
    # create a cursor for passing commands to the database
    c = conn.cursor()

# join accounts to customers and properties
# calculate

c.execute("""SELECT
                a.a_account_number
                ,a.a_arrears_balance
                ,a.a_regular_payment_amount
                ,pt.pt_in_possession
                ,acl.acl_customer_pos
                ,c.c_bankruptcy_ind
                ,c.c_deceased_date
            FROM accounts a
            LEFT JOIN accounts_customer_link acl
                ON a.a_account_number = acl.acl_account_number
            LEFT JOIN customers c
                ON acl.acl_customer_number = c.c_customer_number
            LEFT JOIN properties pt
                ON a.a_property_number = pt.pt_property_number
"""
          )

# list of tuples
results = c.fetchmany(2)


for result in results:
    # get tuple data into separate variables for calculations
    (a_account_number, a_arrears_balance, a_regular_payment_amount,
        pt_in_possession, acl_customer_pos, c_bankruptcy_ind,
        c_deceased_date) = result

    # calculate months_in_arrears
    months_in_arrears_raw = a_arrears_balance / a_regular_payment_amount
    floor = 0
    months_in_arrears_floored = max(months_in_arrears_raw, floor)
    months_in_arrears = round(months_in_arrears_floored, 1)

    # in possession
    if pt_in_possession == 'Y':
        in_possession = True
    else:
        in_possession = False

    # in default
    if in_possession:
        in_default = True
    elif months_in_arrears > 6:
        in_default = True
    elif months_in_arrears >= 3:

        """
        Add if either customer is bankrupt
        This whole data stream will need to be a dictionary before starting 
        account[customer][]

        maybe we need to get the individual tables out and put into separate 
        dictionaries

        find a way to join/structure in python
        """

print(result, months_in_arrears, in_possession)



"""
- The JSON file should be named 'mortgages_data.json'.
- The "accounts" list should contain an entry for each account in the ACCOUNTS
table in the mortgages database.
- Each acccount entry should contain a list of all customers attached to the
account


"""
