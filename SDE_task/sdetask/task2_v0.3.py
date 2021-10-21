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

import sqlite3

# set connection to named database
conn = sqlite3.connect('SDE_task/sdetask/data/mortgages.db')

with conn:
    # create a cursor for passing commands to the database
    c = conn.cursor()

# join accounts to customers and properties
# calculate

c.execute("""
    SELECT
        a.a_account_number
        ,a.a_arrears_balance
        ,a.a_regular_payment_amount
        ,pt.pt_in_possession
    FROM accounts a
    LEFT JOIN properties pt
        ON a.a_property_number = pt.pt_property_number
""")

accounts = c.fetchmany(2)
print(accounts)

for account in accounts:
    (account_number, arrears_balance, regular_payment_amount,
        in_possession_YN) = account

    months_in_arrears = max(
        round(arrears_balance/regular_payment_amount, 1), 0)

    if in_possession_YN == 'Y':
        in_possession = True
    else:
        in_possession = False

dict_accounts = {"accounts": {
    "account_number": account_number,
    "months_in_arrears": months_in_arrears,
    "in_possession": in_possession,
    "in_default": "xxx",
    }
}

print(dict_accounts)



conn.close()









"""
c.execute(
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
