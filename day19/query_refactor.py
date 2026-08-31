import sqlite3
import time

conn = sqlite3.connect("users.db")
cur = conn.cursor()

def profile(label, query):
    start = time.time()
    results = cur.execute(query).fetchall()
    elapsed = (time.time() - start) * 1000
    print(f"{label}: {len(results)} rows, {elapsed:.2f} ms")

print("=== SELECT * vs specific columns ===")
profile("SELECT * (bad)", "SELECT * FROM orders WHERE city = 'Karachi'")
profile("SELECT specific cols (better)", "SELECT id, amount FROM orders WHERE city = 'Karachi'")

print("\n=== Unindexed OR vs UNION of indexed lookups ===")
profile("OR across columns (bad — can't use one index well)",
        "SELECT * FROM orders WHERE city = 'Karachi' OR status = 'delivered'")
profile("Rewritten as UNION (better — each half uses its own index)",
        """SELECT * FROM orders WHERE city = 'Karachi'
           UNION
           SELECT * FROM orders WHERE status = 'delivered'""")

print("\n=== N+1 simulation vs single batched query ===")
cities = ["Lahore", "Karachi", "Multan"]

start = time.time()
for c in cities:
    cur.execute("SELECT COUNT(*) FROM orders WHERE city = ?", (c,)).fetchone()
elapsed = (time.time() - start) * 1000
print(f"N+1 pattern (3 separate queries): {elapsed:.2f} ms")

start = time.time()
cur.execute("SELECT city, COUNT(*) FROM orders WHERE city IN (?,?,?) GROUP BY city", cities).fetchall()
elapsed = (time.time() - start) * 1000
print(f"Single batched query (GROUP BY): {elapsed:.2f} ms")

conn.close()