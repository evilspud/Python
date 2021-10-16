
"""insert a record into the table"""
c.execute("INSERT INTO employees VALUES ('Mary', 'Schafer', 50000)")

"""insert a record into the table using positions from the class method lists"""
c.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))

"""insert a record into the table using a dictionary"""
c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", 
    {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay,})

conn.commit()

"""select results from the table"""
c.execute("SELECT * FROM employees WHERE last='Doe'")

"""or using dictionary and placeholder"""
c.execute("SELECT * FROM employees WHERE last=:last", {'last': 'Doe'})



"""
fetch the results of the query
fetch one, fetch many(x), fetch all - into a list of tuples
"""

print(c.fetchall())

conn.commit()