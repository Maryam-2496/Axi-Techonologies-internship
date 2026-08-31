import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS orders")
conn.commit()
conn.close()
print("Old orders table dropped.")