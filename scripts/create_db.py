import sqlite3

def create_uber_database(db_name = "uber.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rating REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS riders (
    rider_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id INTEGER,
    rider_id INTEGER,
    pickup_datetime TEXT,
    dropoff_datetime TEXT,
    price REAL,
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
    FOREIGN KEY (rider_id) REFERENCES riders(rider_id)
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Database and tables created.")

if __name__ == "__main__":
    create_uber_database()
