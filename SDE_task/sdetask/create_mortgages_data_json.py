#!/usr/bin/env python3

"""create_mortgages_data_json.py

Author: Matthew Southerington

Extract data from the SQLite3 mortgages database and create a JSON file
called mortgages_data.json

JSON output fields:
    months_in_arrears
    in_possession
    in_default
    customer_position
    is_bankrupt
    is_deceased
"""


import json
import math
import sqlite3


def yn_bool(yn_flag: str) -> bool:
    """Coverts a Y/N string field to boolean

    Args:
    yn_flag (str): A string of (ideally) Y and N flags. Flags will be converted
    to upper case.

    Any flag which is not Y will be returned as False. (In reality you may
    wish to return an error to highlight invalid data)

    Returns:
    bool: yn_bool
    """

    return True if yn_flag.upper() == 'Y' else False


def months_in_arrears(
        arrears_balance: float,
        regular_payment_amount: float) -> float:
    """Absolute arrears balance for an account divided by the
        regular monthly payment amount. The value should be rounded to 1
        decimal place. The minimum value should be 0.

    Args:
    arrears_balance (float): Absolute arrears balance
    regular_payment_amount (float): Regular monthly payment amount

    Returns:
    float: Months in Arrears to one decimal place, floored at zero.
    """

    if regular_payment_amount in (0, math.isnan):
        return 0
    else:
        return max(round(arrears_balance/regular_payment_amount, 1), 0)


def is_deceased(deceased_date: str) -> bool:
    """Boolean to indicate if customer deceased date is populated

    Args:
    deceased_date (str): Deceased date as string

    Returns:
    bool: is_deceased
    """
    return False if deceased_date == '' else True


def in_default(
        customer_bankruptcy_flags: list, in_possession: bool,
        months_in_arrears: float) -> bool:
    """A boolean to indicate if the account is in default

    An account is said to be in default in the following circumstances:
        1. The account is in possession
        2. The account is 3 months or more in arrears and either customer 1 or
            customer 2 is bankrupt
        3. The account is more than 6 months in arrears

    Args:
    customer_bankruptcy_flags (list): A list of booleans representing the
        bankruptcy status of the selected customers
    in_possession (bool): A boolean representing whether the account is in
        possession
    months_in_arrars (float): Total arrears balance divided by regular monthly
        payment, floored at zero

    Returns:
    bool: in_default
    """

    is_account_bankrupt = any(customer_bankruptcy_flags)

    return (
        (is_account_bankrupt and months_in_arrears >= 3)
        or months_in_arrears >= 6
        or in_possession
    )


# set connection to named database
conn = sqlite3.connect('SDE_task/sdetask/data/mortgages.db')

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

# Account Derivations
json_output = {"accounts": []}

for account in accounts_sql_output:
    (a_account_number, arrears_balance, regular_payment_amount,
        in_possession_yn) = account

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

    # Months In Arrears
    months_arrears = months_in_arrears(arrears_balance, regular_payment_amount)

    # In Possession
    in_posssesion = yn_bool(in_possession_yn)

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

with open("SDE_task/sdetask/output/mortgages_data.json", "w") as json_file:
    json.dump(json_output, json_file, indent=4)
