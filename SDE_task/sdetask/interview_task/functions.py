#!/usr/bin/env python3

"""test_db_creation.py

Author: Matthew Southerington

Define functions
"""

import math

print("functions.py starts")


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


def is_deceased(deceased_date: str) -> bool:
    """Boolean to indicate if customer deceased date is populated

    Args:
    deceased_date (str): Deceased date as string

    Returns:
    bool: is_deceased
    """
    return False if deceased_date == '' else True


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


print("functions.py ends")
