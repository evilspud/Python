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
                a.a_account_number as account_number
                ,min(0,round(a.a_arrears_balance/a.a_regular_payment_amount,1)) as months_in_arrears
                ,case when pt.pt_in_possession = 'Y' then True else False end as in_possession
                ,acl.acl_customer_pos as customer_position
                ,case when c.c_bankruptcy_ind = 'Y' then True else False end as is_bankrupt
                ,case when c.c_deceased_date = Null then False else True end as is_deceased
            FROM accounts a
            LEFT JOIN accounts_customer_link acl
                ON a.a_account_number = acl.acl_account_number
            LEFT JOIN customers c
                ON acl.acl_customer_number = c.c_customer_number
            LEFT JOIN properties pt
                ON a.a_property_number = pt.pt_property_number
"""
          )


results = c.fetchall()

print(results)


with open("SDE_task/sdetask/output/mortgages_data.json", "w") as json_file:
    json.dump(results, json_file)

# close connection
conn.close()
"""

## Task 2
Create a Python process to extract data from the SQLite3 mortgages database
(data/mortgages.db) and create a JSON file in the below format:
```JSON
{
    "accounts": [
        {
            "account_number": 1,
            "months_in_arrears": 17.1,
            "in_possession": false,
            "in_default": true,
            "customers": [
                {
                    "customer_position": 1,
                    "is_bankrupt": false,
                    "is_deceased": false
                },
                {
                    "customer_position": 2,
                    "is_bankrupt": false,
                    "is_deceased": false
                }
            ]
        },
        {
            "account_number": 2,
            "months_in_arrears": 3.3,
            "in_possession": false,
            "in_default": false,
            "customers": [
                {
                    "customer_position": 1,
                    "is_bankrupt": false,
                    "is_deceased": false
                },
                {
                    "customer_position": 2,
                    "is_bankrupt": false,
                    "is_deceased": false
                }
            ]
        },
        ...
    ]
}
```
- The JSON file should be named 'mortgages_data.json'.
- The "accounts" list should contain an entry for each account in the ACCOUNTS
table in the mortgages database.
- Each acccount entry should contain a list of all customers attached to the
account


"""
