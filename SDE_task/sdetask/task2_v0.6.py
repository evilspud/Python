#!/usr/bin/env python3

"""xxxxxxxxxx.py

Author: Matthew Southerington

Extract data from the SQLite3 mortgages database (data/mortgages.db)
and create a JSON file called mortgages_data.json

JSON output fields:

    _months_in_arrears_
    _in_possession_
    _in_default_
        An account is said to be in default in (any of) the following
        circumstances:
            2. The account is 3 months or more in arrears and either customer 1
                or customer 2 is bankrupt

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
    regular_payment_amount: float
    ) -> float:
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

# Account Derivations
dict_json_output = {"accounts": []}

for account in accounts_sql_output:
    (a_account_number, arrears_balance, regular_payment_amount,
        in_possession_yn) = account

    # In Possession
    in_possession = yn_bool(in_possession_yn)

    # Months in Arrears
    months_arrears = months_in_arrears(arrears_balance, regular_payment_amount)
    
    account_dict = {
        "account_number": a_account_number,
        "months_in_arrears": months_arrears,
        "in_possession": in_possession,
        "customers": []
    }

    # List of Customers

    customers_by_account = [{
        "customer_position": customer[1],
        "is_bankrupt": yn_bool(customer[2]),
        "is_deceased": is_deceased(customer[3])
        }
        for customer in customers_sql_output if customer[0] == a_account_number
    ]

    # In Default

print(customers_by_account)

    ##### for customers in customers_by_account list,
    # 
    # bring back a list of the values of  


    # in_default = any(
    #     in_possession,
    #     months_arrears > 6,
        

    # )
    
    # print(in_default)





    #     if account_dict["account_number"] == c_account_number:
    #         account_dict["customers"].append(customer_dict)

    # dict_json_output["accounts"].append(account_dict)


with open("SDE_task/sdetask/output/mortgages_data.json", "w") as json_file:
    json.dump(dict_json_output, json_file, indent=4)

conn.close()
