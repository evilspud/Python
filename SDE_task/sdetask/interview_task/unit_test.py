#!/usr/bin/env python3

"""unit_test.py

Author: Matthew Southerington

Define test functions to pass parameters through the functions for the report
production.
"""

import math

from functions import in_default
from functions import is_deceased
from functions import months_in_arrears
from functions import yn_bool


print("Unit_test.py starts")


# NB renamed months_in_arrears to avoid clash with function of same name
def test_in_default(
        customer_bankruptcy_flags, in_possession,
        mia, expected):
    assert in_default(
        customer_bankruptcy_flags, in_possession,
        mia) is expected


# customer_bankruptcy tests
test_in_default([True, True], False, 3, True)
test_in_default([True, False], False, 3, True)
test_in_default([False], False, 3, False)

# customer_bankrupcy and 3+ months tests
test_in_default([True], False, 3, True)
test_in_default([True], False, 2.9, False)

# in_possession tests
test_in_default([False, False], True, 3, True)
test_in_default([False, False], False, 3, False)

# months_in_arrears tests
test_in_default([False, False], False, 6.1, True)
test_in_default([False, False], False, 6, False)


def test_is_deceased(deceased_date, expected):
    assert is_deceased(deceased_date) is expected


# deceased date population
test_is_deceased('', False)
test_is_deceased('Jan-21', True)


def test_months_in_arrears(arrears_balance, regular_payment_amount, expected):
    assert months_in_arrears(
        arrears_balance, regular_payment_amount
    ) == expected


test_months_in_arrears(921.05, 0, 0)
test_months_in_arrears(921.05, math.nan, 0)
test_months_in_arrears(921.05, 100, 9.2)
test_months_in_arrears(-921.05, 100, 0)
test_months_in_arrears(921.05, -100, 0)


def test_yn_bool(yn_flag, expected):
    assert yn_bool(
        yn_flag
    ) is expected


test_yn_bool("Y", True)
test_yn_bool("N", False)
test_yn_bool("y", True)
test_yn_bool("n", False)
test_yn_bool(None, False)
test_yn_bool("j", False)

print("Unit_test.py ends")
