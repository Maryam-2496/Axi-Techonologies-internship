import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

total = cur.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
print(f"Total rows: {total}\n")

for column, value in [("city", "Karachi"), ("status", "pending"), ("city", "Multan")]:
    count = cur.execute(f"SELECT COUNT(*) FROM orders WHERE {column} = ?", (value,)).fetchone()[0]
    selectivity = count / total
    print(f"{column} = '{value}': {count} rows ({selectivity:.1%} of table) — {'LOW selectivity, index may not help' if selectivity > 0.05 else 'HIGH selectivity, index helps a lot'}")

conn.close()