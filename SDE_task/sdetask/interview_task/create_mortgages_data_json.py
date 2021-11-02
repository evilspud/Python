#!/usr/bin/env python3

"""create_mortgages_data_json.py

Author: Matthew Southerington

Import packages, functions and parameters.

Create a database connection and extract data from the SQLite3 mortgages
database.

Find accounts and join properties.

Find customers and account link information.

For each account:
    Derive variables
    Get customer information for customers who share the account number
    Of those customers, find bankrupt customers
    Build individual account dictionary
    Append dictionary to overall output

Create/overwrite JSON file

JSON output fields:
    account_number
    months_in_arrears
    in_possession
    in_default
    customer_position
    is_bankrupt
    is_deceased

Inputs: mortgages.db
Outputs: mortgages_data.json
"""

import json
import sqlite3

from functions import in_default
from functions import is_deceased
from functions import months_in_arrears
from functions import yn_bool

from set_parameters import db_path
from set_parameters import json_path
from set_parameters import path_existence

print("Create_mortgages_data_json.py starts")

# Database connection
conn = sqlite3.connect(db_path)

# Cursor
c = conn.cursor()

# Accounts and Properties
c.execute("""
    SELECT
        a.a_account_number
        ,a.a_arrears_balance
        ,a.a_regular_payment_amount
        ,pt.pt_in_possession
    FROM accounts a
    LEFT JOIN properties pt
        ON a.a_property_number = pt.pt_property_number
    ORDER BY a_account_number
""")

accounts_sql_output = c.fetchall()

# Customers and Account Link
c.execute("""
    SELECT
        acl.acl_account_number
        ,acl.acl_customer_pos
        ,c.c_bankruptcy_ind
        ,c.c_deceased_date
    FROM customers c
    LEFT JOIN accounts_customer_link acl
    ON acl.acl_customer_number = c.c_customer_number
    ORDER BY acl_account_number
""")

customers_sql_output = c.fetchall()

conn.close()

json_output = {"accounts": []}

# Account Derivations
for account in accounts_sql_output:
    (a_account_number, arrears_balance, regular_payment_amount,
        in_possession_yn) = account

    # Months In Arrears
    months_arrears = months_in_arrears(arrears_balance, regular_payment_amount)

    # In Possession
    in_posssesion = yn_bool(in_possession_yn)

    # Associated Customers
    associated_customers = [{
        "customer_position": customer[1],
        "is_bankrupt": yn_bool(customer[2]),
        "is_deceased": is_deceased(customer[3])
        }
        for customer in customers_sql_output if customer[0] == a_account_number
    ]

    # Customer bankruptcy flags
    customer_bankruptcy_flags = [
        customers["is_bankrupt"]
        for customers in associated_customers
    ]

    # Account Derivations
    account_dict = {
        "account_number": a_account_number,
        "months_in_arrears": months_arrears,
        "in_possession": in_posssesion,
        "in_default": in_default(
            customer_bankruptcy_flags,
            in_posssesion,
            months_arrears
        ),
        "customers": associated_customers
    }

    json_output["accounts"].append(account_dict)

with open(json_path, "w") as json_file:
    json.dump(json_output, json_file, indent=4)

# Test Creation
path_existence(json_path)

print("Create_mortgages_data_json.py ends")
