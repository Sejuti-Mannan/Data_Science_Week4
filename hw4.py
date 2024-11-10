# Sejuti Mannan
# NYU Tandon Data Science Bootcamp
# Week 4 (10/23) SQL Fundamentals

'''
TABLE INFO :
SALES – Date, Order_id, Item_id, Customer_id, Quantity, Revenue
ITEMS – Item_id, Item_name, price, department
CUSTOMERS- customer_id, first_name,last_name,Address
'''

import sqlite3
import pandas as pd

# SET UP DATABASE AND TABLES
# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create tables based on your structure
cursor.execute('''
CREATE TABLE SALES (
    Date DATE,
    Order_id INTEGER,
    Item_id INTEGER,
    Customer_id INTEGER,
    Quantity INTEGER,
    Revenue REAL
)
''')

cursor.execute('''
CREATE TABLE ITEMS (
    Item_id INTEGER PRIMARY KEY,
    Item_name TEXT,
    Price REAL,
    Department TEXT
)
''')

cursor.execute('''
CREATE TABLE CUSTOMERS (
    Customer_id INTEGER PRIMARY KEY,
    First_name TEXT,
    Last_name TEXT,
    Address TEXT
)
''')
conn.commit()

# Customers
customers_data = [
    (1001, "John", "Doe", "123 Elm St"),
    (1002, "Jane", "Smith", "456 Oak St"),
    (1003, "Alice", "Johnson", "789 Maple Ave"),
    (1004, "John", "Doe", "321 Pine St"),
]
cursor.executemany("INSERT INTO CUSTOMERS VALUES (?, ?, ?, ?)", customers_data)

# Items
items_data = [
    (101, "Laptop", 1200.0, "Electronics"),
    (102, "Headphones", 200.0, "Electronics"),
    (103, "Coffee Maker", 100.0, "Home Appliances"),
    (104, "Blender", 150.0, "Home Appliances"),
    (105, "Notebook", 5.0, "Stationery"),
]
cursor.executemany("INSERT INTO ITEMS VALUES (?, ?, ?, ?)", items_data)

# Sales
sales_data = [
    ("2023-03-18", 1, 101, 1001, 1, 1200.0),
    ("2023-03-18", 2, 102, 1002, 1, 200.0),
    ("2023-01-15", 3, 103, 1003, 2, 200.0),
    ("2023-01-20", 4, 104, 1001, 1, 150.0),
    ("2022-11-22", 5, 105, 1002, 10, 50.0),
    ("2022-12-10", 6, 101, 1004, 1, 1200.0),
    ("2022-08-05", 7, 103, 1003, 1, 100.0),
    ("2023-01-10", 8, 102, 1002, 1, 200.0),
]
cursor.executemany("INSERT INTO SALES VALUES (?, ?, ?, ?, ?, ?)", sales_data)

conn.commit()

# Pull total number of orders that were completed on 18th March 2023
query1 = '''
SELECT COUNT(*) as total_orders
FROM SALES
WHERE Date = '2023-03-18'
'''
result1 = pd.read_sql_query(query1, conn)
print(result1)

# Pull total number of orders that were completed on 18th March 2023 with the first name ‘John’ and last name Doe’
query2 = '''
SELECT COUNT(*) as total_orders
FROM SALES AS s
LEFT JOIN CUSTOMERS AS c
ON s.Customer_id = c.Customer_id
WHERE Date = '2023-03-18' AND First_name = 'John' AND Last_name = 'Doe'
'''
result2 = pd.read_sql_query(query2, conn)
print(result2)

# Pull total number of customers that purchased in January 2023 and the average amount spend per customer
query3 = '''
SELECT COUNT(DISTINCT Customer_id) AS total_customers,
       AVG(total_spent) AS avg_spent_per_customer
FROM (
    SELECT Customer_id, SUM(Revenue) AS total_spent
    FROM SALES
    WHERE Date LIKE '2023-01-%' 
    GROUP BY Customer_id
);
'''
result3 = pd.read_sql_query(query3, conn)
print(result3)

# Pull the departments that generated less than $600 in 2022
query4 = '''
SELECT Department, SUM(s.Revenue) AS total_revenue
FROM SALES AS s 
INNER JOIN ITEMS AS i ON s.Item_id = i.Item_id
WHERE Date LIKE  '2022-%-%'
GROUP BY i.Department 
HAVING total_revenue < 600
'''

# What is the most and least revenue we have generated by an order
query5 = '''
SELECT MAX(Revenue) AS max_revenue, MIN(Revenue) AS min_revenue
FROM SALES
'''

# What were the orders that were purchased in our most lucrative order
query6 = '''
SELECT *
FROM SALES
WHERE Revenue = (SELECT MAX(Revenue) FROM SALES)
'''