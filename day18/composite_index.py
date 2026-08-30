import sqlite3
import time

conn = sqlite3.connect("users.db")
cur = conn.cursor()

# Composite index: order matters (leftmost prefix rule)
cur.execute("CREATE INDEX IF NOT EXISTS idx_city_status_amount ON orders(city, status, amount)")
conn.commit()
print("Composite index created.\n")

def profile(label, query):
    print(f"--- {label} ---")
    print("Query:", query)
    for row in cur.execute(f"EXPLAIN QUERY PLAN {query}"):
        print("Plan:", row)
    start = time.time()
    results = cur.execute(query).fetchall()
    elapsed = (time.time() - start) * 1000
    print(f"Rows: {len(results)} | Time: {elapsed:.2f} ms\n")

# Uses all 3 columns in order — should use the composite index fully
profile("Uses full leftmost prefix", "SELECT * FROM orders WHERE city = 'Karachi' AND status = 'pending' AND amount > 4000")

# Uses only the first column — still uses the index (leftmost prefix still matches)
profile("Uses only first column", "SELECT * FROM orders WHERE city = 'Karachi'")

# Skips the first column — index CANNOT be used efficiently
profile("Skips leftmost column", "SELECT * FROM orders WHERE status = 'pending' AND amount > 4000")

conn.close()