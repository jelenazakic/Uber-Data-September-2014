import pandas as pd
import sqlite3 
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

conn = sqlite.connect("uber.db")
df = pd.read_query("SELECT * FROM uber_pickups",conn)
conn.close()

df['date_time'] = pd.to_time(dt['date_time'])
df['hour'] = df['datetime'].dt.hour
df['day'] = df['datetime'].dt.day
df['weekday'] = df['datetime'].dt.weekday

#Pickups per hour
hourly = df.groupby('hour').size()
plt.figure(figsize=(10, 5))
hourly.plot(kind='bar')
plt.title("Uber Pickups by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Pickups")
plt.tight_layout()
plt.savefig("plots/pickups_by_hour.png")
plt.close()

# Pickups per day 
weekday_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
df['weekday_name'] = df['weekday'].map(weekday_map)
weekday = df['weekday_name'].value_counts().reindex(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.figure(figsize=(10, 5))
weekday.plot(kind='bar')
plt.title("Uber Pickups by Weekday")
plt.xlabel("Day of Week")
plt.ylabel("Number of Pickups")
plt.tight_layout()
plt.savefig("plots/pickups_by_weekday.png")
plt.close()

#Pickups per base
base = df['base'].value_counts()
plt.figure(figsize=(10, 5))
base.plot(kind='bar')
plt.title("Uber Pickups by Base")
plt.xlabel("Base")
plt.ylabel("Number of Pickups")
plt.tight_layout()
plt.savefig("plots/pickups_by_base.png")
plt.close()

#Heatmap: Hour vs. Day
heatmap_data = df.groupby(['day', 'hour']).size().unstack(fill_value=0)
plt.figure(figsize=(12, 7))
sns.heatmap(heatmap_data, cmap="YlGnBu")
plt.title("Heatmap of Uber Pickups by Day and Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Day of Month")
plt.tight_layout()
plt.savefig("plots/pickups_heatmap.png")
plt.close()

print("✅ All plots saved in the 'plots/' folder.")


