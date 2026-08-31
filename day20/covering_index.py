import sqlite3
import time

conn = sqlite3.connect("users.db")
cur = conn.cursor()

# Covering index: includes every column this specific query needs
cur.execute("CREATE INDEX IF NOT EXISTS idx_covering_city_amount ON orders(city, amount)")
conn.commit()
print("Covering index created.\n")

def profile(label, query):
    print(f"--- {label} ---")
    print("Query:", query)
    for row in cur.execute(f"EXPLAIN QUERY PLAN {query}"):
        print("Plan:", row)
    start = time.time()
    results = cur.execute(query).fetchall()
    elapsed = (time.time() - start) * 1000
    print(f"Rows: {len(results)} | Time: {elapsed:.2f} ms\n")

# This query ONLY needs city + amount — both are in the index, so SQLite
# never has to fetch the full row from the table (a "covering" query)
profile("Covering index (no heap fetch needed)", "SELECT city, amount FROM orders WHERE city = 'Multan'")

# Compare: same filter, but SELECT * forces it to fetch full rows anyway
profile("Same filter, SELECT * (heap fetch required)", "SELECT * FROM orders WHERE city = 'Multan'")

conn.close()