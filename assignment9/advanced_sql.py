import sqlite3
db = sqlite3.connect('../db/lesson.db')
db.execute("PRAGMA foreign_keys = 1")

# Task 1
cursor = db.cursor()
sql = """
SELECT o.order_id, SUM(p.price * li.quantity) as total_price
FROM orders o
JOIN line_items li ON o.order_id = li.order_id
JOIN products p ON li.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id
LIMIT 5
"""
cursor.execute(sql)
results = cursor.fetchall()
print("Order ID | Total Price")
print("-" * 25)
for row in results:
    order_id, total_price = row
    print(f"{order_id:8} | ${total_price:.2f}")

# Task 2
print("\n\nTask 2: Average Order Price per Customer")
print("=" * 50)
sql2 = """
SELECT c.customer_name, AVG(subquery.total_price) as average_total_price
FROM (
    SELECT o.customer_id as customer_id_b, SUM(p.price * li.quantity) as total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.customer_id
) as subquery
LEFT JOIN customers c ON c.customer_id = subquery.customer_id_b
GROUP BY c.customer_id
ORDER BY c.customer_name
"""
cursor.execute(sql2)
results2 = cursor.fetchall()
print("Customer Name        | Average Order Price")
print("-" * 50)
for row in results2:
    name, avg_price = row
    if name is None:
        continue
    print(f"{name:20} | ${avg_price:.2f}")

# Task 3
print("\n\nTask 3: Insert Transaction for New Order")
print("=" * 50)
cursor.execute("SELECT customer_id FROM customers WHERE customer_name = ?", ("Perez and Sons",))
customer_id = cursor.fetchone()[0]
print(f"Customer ID for 'Perez and Sons': {customer_id}")
cursor.execute("SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?", ("Miranda", "Harris"))
employee_id = cursor.fetchone()[0]
print(f"Employee ID for 'Miranda Harris': {employee_id}")
cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
product_ids = [row[0] for row in cursor.fetchall()]
print(f"5 least expensive product IDs: {product_ids}")
try:
    cursor.execute(
        """INSERT INTO orders (customer_id, employee_id, date)
           VALUES (?, ?, date('now'))
           RETURNING order_id""",
        (customer_id, employee_id)
    )
    order_id = cursor.fetchone()[0]
    print(f"Created order with ID: {order_id}")
    for product_id in product_ids:
        cursor.execute(
            """INSERT INTO line_items (order_id, product_id, quantity)
               VALUES (?, ?, ?)""",
            (order_id, product_id, 10)
        )
    db.commit()
    print("Transaction committed successfully!")
    print("\n\nLine Items for Order:", order_id)
    print("-" * 60)
    select_query = """
    SELECT li.line_item_id, li.quantity, p.product_name
    FROM line_items li
    JOIN products p ON li.product_id = p.product_id
    WHERE li.order_id = ?
    ORDER BY li.line_item_id
    """
    cursor.execute(select_query, (order_id,))
    line_items = cursor.fetchall()
    print("Line Item ID | Quantity | Product Name")
    print("-" * 60)
    for row in line_items:
        line_item_id, quantity, product_name = row
        print(f"{line_item_id:12} | {quantity:8} | {product_name}")
except Exception as e:
    db.rollback()
    print(f"Error during transaction: {e}")

# Task 4
print("\n\nTask 4: Employees with More Than 5 Orders")
print("=" * 50)
sql4 = """
SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) as order_count
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
GROUP BY e.employee_id
HAVING COUNT(o.order_id) > 5
ORDER BY e.first_name, e.last_name
"""
cursor.execute(sql4)
results4 = cursor.fetchall()
print("Employee ID | First Name       | Last Name        | Order Count")
print("-" * 65)
for row in results4:
    employee_id, first_name, last_name, order_count = row
    print(f"{employee_id:11} | {first_name:16} | {last_name:16} | {order_count:11}")
db.close()
