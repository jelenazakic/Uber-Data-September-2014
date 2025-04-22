import sqlite3

conn = sqlite3.connect("uber.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS uber_pickups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime TEXT,
    lat REAL,
    lon REAL,
    base TEXT,
    hour INTEGER,
    day INTEGER,
    weekday INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Uber table created in 'uber.db'")

