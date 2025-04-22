import pandas as pd

df = pd.read_csv("data/uber-raw-data-sep14.csv")

print("✅ Loaded CSV!")
print("\n📊 Columns:")
print(df.columns)

print("\n🧪 Preview of the first 5 rows:")
print(df.head())

print("\n🔎 Dataset shape (rows, columns):")
print(df.shape)
