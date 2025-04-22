import pandas as pd
import sqlite3

df = pd.read_csv("data/uber_cleaned_sep14.csv")

conn = sqlite3.connect("uber.db")

df.to_sql("uber_pickups", conn, if_exists="append", index=False)

conn.close()

print("✅ Data inserted into 'uber_pickups' table!")

