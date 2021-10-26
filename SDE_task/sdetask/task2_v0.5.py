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
import math
import sqlite3

# set connection to named database
conn = sqlite3.connect('SDE_task/sdetask/data/mortgages.db')

with conn:
    # create a cursor for passing commands to the database
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

# Account Derivations
dict_json_output = {"accounts": []}

for account in accounts_sql_output:
    (a_account_number, arrears_balance, regular_payment_amount,
        in_possession_yn) = account

    # Months in Arrears
    if regular_payment_amount in (0, math.isnan):
        months_in_arrears = 0
    else:
        months_in_arrears = max(
            round(arrears_balance/regular_payment_amount, 1), 0)

    # In Possession
    if in_possession_yn == 'Y':
        in_possession = True
    else:
        in_possession = False

    account_dict = {
            "account_number": a_account_number,
            "months_in_arrears": months_in_arrears,
            "in_possession": in_possession,
            "in_default": False,
            "customers": []
    }

    # find matching customers

    # Customer Derivations
    for customer in customers_sql_output:
        (c_account_number, customer_position, is_bankrupt_yn,
            deceased_date) = customer

        # Is Bankrupt
        if is_bankrupt_yn == 'Y':
            is_bankrupt = True
        else:
            is_bankrupt = False

        # Is Deceased
        if deceased_date != '':
            is_deceased = True
        else:
            is_deceased = False

        customer_dict = {
                "customer_position": customer_position,
                "is_bankrupt": is_bankrupt,
                "is_deceased": is_deceased
            }

        if account_dict["account_number"] == c_account_number:
            account_dict["customers"].append(customer_dict)

    dict_json_output["accounts"].append(account_dict)


with open("SDE_task/sdetask/output/mortgages_data.json", "w") as json_file:
    json.dump(dict_json_output, json_file, indent=4)

conn.close()
