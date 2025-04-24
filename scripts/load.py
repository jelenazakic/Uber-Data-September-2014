import pandas as pd

df = pd.read_csv("data/uber-raw-data-sep14.csv")

print("Loaded CSV!")
print("Columns:")
print(df.columns)

print("Preview of the first 5 rows:")
print(df.head())

print("Dataset shape (rows, columns):")
print(df.shape)
