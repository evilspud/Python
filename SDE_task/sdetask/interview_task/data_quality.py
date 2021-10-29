#!/usr/bin/env python3

"""data_quality.py

Author: Matthew Southerington

SQL check queries to better understand data issues.
"""

import sqlite3
from set_parameters import db_path

print("data_quality.py starts")

# Database connection
conn = sqlite3.connect(db_path)

# Cursor
c = conn.cursor()

# list of deceased customer numbers
c.execute("""
SELECT DISTINCT c_customer_number
FROM customers
WHERE c_deceased_date != ''
""")
output = c.fetchall()
print("Deceased: \n\n", output, "\n")

# regular payment is zero or missing
c.execute("""
SELECT a_account_number, a_regular_payment_amount
FROM accounts
WHERE a_regular_payment_amount in (0, null)
""")
output = c.fetchall()
print("Regular Payment Zero/Missing: \n\n", output, "\n")

# No primary key on accounts_customer_link - meaning you might get
# multiple customers in each account position - TRUE
c.execute("""
SELECT DISTINCT
    acl_account_number,
    acl_customer_pos,
    count(acl_customer_number) as count_cust
FROM accounts_customer_link
GROUP BY acl_account_number,
         acl_customer_pos
HAVING count_cust > 1
""")
output = c.fetchall()
print("Accounts with multiple customers in a position: \n\n", output, "\n")


# Y/N flags which are not Y or N
def dq_yn_check(id, variable, table) -> list:
    with conn:
        c.execute(f"""SELECT
                        {id}
                        ,{variable}
                    FROM {table}
                    WHERE {variable} not in ("Y", "N")
                    """)
        output = c.fetchall()
        print(f"Y/N flags are not Y/N: {variable}: \n\n", output, "\n")


dq_yn_check('c_customer_number', 'c_bankruptcy_ind', 'customers')
# dq_yn_check('pd_product_number', 'pd_product_fixed_ind', 'products')
# dq_yn_check('pd_product_number', 'pd_product_flexible_ind', 'products')
# dq_yn_check('pd_product_number', 'pd_product_tracker_ind', 'products')
# dq_yn_check('pd_product_number', 'pd_product_variable_ind', 'products')
# dq_yn_check('pd_product_number', 'pd_product_capped_ind', 'products')
# dq_yn_check('pd_product_number', 'pd_product_discount_ind', 'products')
dq_yn_check('pt_property_number', 'pt_in_possession', 'properties')

conn.close()

print("data_quality.py ends")
