import pandas as pd

df = pd.read_csv("data/uber-raw-data-sep14.csv")

df.columns = ['datetime', 'lat', 'lon', 'base']

df['datetime'] = pd.to_datetime(df['datetime'], format = "%m/%d/%Y %H:%M:%S")

df.to_csv("data/uber_cleaned_sep14.csv", index=False)

print("✅ Data cleaned and saved to 'data/uber_cleaned_sep14.csv'")
