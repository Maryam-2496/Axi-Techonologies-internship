import sqlite3
import time

conn = sqlite3.connect("users.db")
cur = conn.cursor()

query = "SELECT * FROM orders WHERE city = 'Lahore' AND status = 'pending'"

# Show the execution plan
print("--- EXPLAIN QUERY PLAN ---")
for row in cur.execute(f"EXPLAIN QUERY PLAN {query}"):
    print(row)

# Time the actual query
start = time.time()
results = cur.execute(query).fetchall()
elapsed = (time.time() - start) * 1000
print(f"\n--- RESULTS ---")
print(f"Rows returned: {len(results)}")
print(f"Time taken: {elapsed:.2f} ms")

conn.close()