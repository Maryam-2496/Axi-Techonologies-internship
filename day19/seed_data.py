import sqlite3
import random
import time

DB_PATH = "users.db"

FIRST_NAMES = ["Ali", "Sara", "Hamza", "Ayesha", "Bilal", "Zara", "Omar", "Mariam", "Usman", "Hina"]
CITIES = ["Islamabad", "Lahore", "Karachi", "Peshawar", "Multan", "Quetta", "Faisalabad"]

def seed(n=500_000):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            city TEXT NOT NULL,
            status TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    print(f"Seeding {n} rows... this may take a minute.")
    start = time.time()

    batch = []
    for i in range(n):
        name = random.choice(FIRST_NAMES)
        city = random.choice(CITIES)
        status = random.choice(["pending", "shipped", "delivered", "cancelled"])
        amount = round(random.uniform(5, 5000), 2)
        created_at = f"2026-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        batch.append((name, city, status, amount, created_at))

        if len(batch) >= 10000:
            cur.executemany(
                "INSERT INTO orders (customer_name, city, status, amount, created_at) VALUES (?, ?, ?, ?, ?)",
                batch,
            )
            batch = []
            print(f"  {i+1} rows inserted...")

    if batch:
        cur.executemany(
            "INSERT INTO orders (customer_name, city, status, amount, created_at) VALUES (?, ?, ?, ?, ?)",
            batch,
        )

    conn.commit()
    conn.close()
    print(f"Done in {time.time() - start:.1f}s")

if __name__ == "__main__":
    seed()