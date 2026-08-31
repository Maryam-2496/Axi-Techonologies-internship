import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

# Basic B-Tree index on a single column
cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_city ON orders(city)")

# Partial index — only indexes rows matching a condition (smaller, faster for that specific filter)
cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_orders_pending
    ON orders(status)
    WHERE status = 'pending'
""")

conn.commit()
print("Indexes created.")

for row in cur.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"):
    print(row)

conn.close()