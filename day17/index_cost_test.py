import sqlite3
import time
import os

conn = sqlite3.connect("users.db")
cur = conn.cursor()

# Check database file size (includes indexes)
size_mb = os.path.getsize("users.db") / (1024 * 1024)
print(f"Database file size: {size_mb:.2f} MB")

# Measure insert speed WITH indexes present
start = time.time()
for i in range(1000):
    cur.execute(
        "INSERT INTO orders (customer_name, city, status, amount, created_at) VALUES (?, ?, ?, ?, ?)",
        ("Test User", "Lahore", "pending", 99.99, "2026-08-11"),
    )
conn.commit()
elapsed = (time.time() - start) * 1000
print(f"Time to insert 1000 rows (with indexes): {elapsed:.2f} ms")

conn.close()