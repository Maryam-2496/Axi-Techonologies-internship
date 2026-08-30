import sqlite3
import time

conn = sqlite3.connect("users.db")
cur = conn.cursor()

def profile(label, query):
    print(f"\n--- {label} ---")
    print("Query:", query)
    for row in cur.execute(f"EXPLAIN QUERY PLAN {query}"):
        print("Plan:", row)
    start = time.time()
    results = cur.execute(query).fetchall()
    elapsed = (time.time() - start) * 1000
    print(f"Rows: {len(results)} | Time: {elapsed:.2f} ms")

# 1. Sequential/full scan (no usable index — filtering on amount, not indexed)
profile("Sequential Scan", "SELECT * FROM orders WHERE amount > 4000")

# 2. Index scan (city is indexed)
profile("Index Scan", "SELECT * FROM orders WHERE city = 'Karachi'")

# 3. Covering-ish scan on the partial index
profile("Partial Index Match", "SELECT * FROM orders WHERE status = 'pending'")

conn.close()