import sqlite3
from employee import employee

"""
create a connection to a 
specific database file (or memory location)
"""

conn = sqlite3.connect(':memory:')
# conn = sqlite3.connect('mysqlite3file.db')

"""create a cursor for interacting with the database"""
c = conn.cursor()

"""create a table"""
c.execute("""CREATE TABLE employees (
    first text,
    last text,
    pay integer
    )""")

"""create specific functions to undertake tasks in the database"""
def insert_emp(emp):
    """By using the with statement, we can employ context management to allocate and 
    release the resource as necessary. We no longer need to use the commit statement"""
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", 
            {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


""" select statements never need to be committed, so we do not need WITH (context manager)"""
def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return c.fetchall()

def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees 
            SET pay = :pay
            WHERE first = :first AND last = :last""", 
            {'first': emp.first, 'last': emp.last, 'pay': pay}
        )

def remove_emp(emp):
    with conn:
        c.execute("""
        DELETE from employees WHERE first = :first and last = :last
        """,
        {'first': emp.first, 'last': emp.last})



emp_1 = employee('John', 'Doe', 80000)
emp_2 = employee('Jane', 'Doe', 90000)

"""
use functions to insert employees
"""

insert_emp(emp_1)
insert_emp(emp_2)

"""
Find employees with specified last name
"""
emps = get_emps_by_name('Doe')
print(emps)

update_pay(emp_2, 95000)

remove_emp(emp_1)


emps = get_emps_by_name('Doe')
print(emps)

conn.close()
