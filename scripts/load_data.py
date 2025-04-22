
import sqlite3
import pandas as pd


conn = sqlite3.connect("uber.db")


df = pd.read_csv("data/Uber-Jan-Feb-FOIL.csv")


df.to_sql("Uber-Jan-Feb-FOIL.csv", conn, if_exists="append", index=False)

conn.close()

