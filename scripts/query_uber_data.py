import sqlite3
import pandas as pd

conn = sqlite3.connect("uber.db")

def run_query(query):
	df = pd.read_sql_query(query, conn)
	print(df)

query = "SELECT COUNT(*) as total_pickups FROM uber_pickups"
run_query(query)

conn.close()
