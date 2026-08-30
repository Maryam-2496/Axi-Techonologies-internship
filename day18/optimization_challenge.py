import sqlite3
import time

conn = sqlite3.connect("users.db")
cur = conn.cursor()

target_query = "SELECT id, amount FROM orders WHERE customer_name = 'Ali' AND status = 'pending'"

def profile(label, query):
    for row in cur.execute(f"EXPLAIN QUERY PLAN {query}"):
        print("Plan:", row)
    start = time.time()
    results = cur.execute(query).fetchall()
    elapsed = (time.time() - start) * 1000
    print(f"{label}: {len(results)} rows, {elapsed:.2f} ms\n")

print("--- BEFORE optimization (no index on customer_name) ---")
profile("Before", target_query)

# Optimal index: customer_name first (most selective, filters hardest),
# then status, then include amount so it's a covering index too
cur.execute("CREATE INDEX IF NOT EXISTS idx_optimal_name_status_amount ON orders(customer_name, status, amount)")
conn.commit()

print("--- AFTER optimization (composite covering index created) ---")
profile("After", target_query)

conn.close()