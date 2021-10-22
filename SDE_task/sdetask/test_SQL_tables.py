import sqlite3

# set connection to named database
conn = sqlite3.connect('SDE_task/sdetask/data/mortgages.db')

# create a cursor for passing commands to the database
c = conn.cursor()

# deceased customer date format
c.execute("""
SELECT DISTINCT c_deceased_date FROM customers
""")
output = c.fetchall()
# print(output)

# list of deceased customer numbers
c.execute("""
SELECT DISTINCT c_customer_number
FROM customers
WHERE c_deceased_date != ''
""")
output = c.fetchall()
# print(output)

# list of accounts where regular payment is zero or missing
c.execute("""
SELECT a_account_number, a_regular_payment_amount
FROM accounts
WHERE a_regular_payment_amount in (0, null)
""")
output = c.fetchall()
# print(output)

# Accounts Customer Link
c.execute("""
SELECT *
FROM accounts_customer_link
""")
output = c.fetchall()
print(output)

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
# print(output)


conn.close()
