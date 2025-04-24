import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#--- Setup ---
plt.style.use("ggplot")
sns.set_palette("Set2")
os.makedirs("plots", exist_ok=True)

# --- Load Data ---
with sqlite3.connect("uber.db") as conn:
    df = pd.read_sql_query("SELECT * FROM uber_pickups", conn)

# --- Preprocessing ---
df['datetime'] = pd.to_datetime(df['datetime'])
df['hour'] = df['datetime'].dt.hour
df['day'] = df['datetime'].dt.day
df['weekday_name'] = df['datetime'].dt.day_name()
df['is_weekend'] = df['weekday'] >= 5

# --- Pickups by hour ---
plt.figure(figsize=(10, 5))
df.groupby('hour').size().plot(kind = 'bar')
plt.title("Uber Pickups by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Pickups")
plt.tight_layout()
plt.savefig("plots/pickups_by_hour.png")
plt.close()

# --- Pickups by weekday ---
plt.figure(figsize=(10, 5))
order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['weekday_name'] = pd.Categorical(df['weekday_name'], categories = order, ordered = True)
df['weekday_name'].value_counts().loc[order].plot(kind = 'bar')
plt.title("Uber Pickups by Weekday")
plt.xlabel("Day of Week")
plt.ylabel("Number of Pickups")
plt.tight_layout()
plt.savefig("plots/pickups_by_weekday.png")
plt.close()

# --- Pickups by base ---
plt.figure(figsize = (10, 5))
df['base'].value_counts().plot(kind = 'bar')
plt.title(" Uber Pickups by Base")
plt.xlabel("Base")
plt.ylabel("Number of Pickups")
plt.tight_layout()
plt.savefig("plots/pickups_by_base.png")
plt.close()

# --- Heatmap of pickups by day and hour ---
heatmap_data = df.groupby(['day', 'hour']).size().unstack(fill_value=0)
plt.figure(figsize = (12, 7))
sns.heatmap(heatmap_data, cmap = "YlGnBu")
plt.title(" Heatmap: Pickups by Day & Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Day of Month")
plt.tight_layout()
plt.savefig("plots/pickups_heatmap_day_hour.png")
plt.close()

# --- Weekday vs Weekend comparison ---
df['day_type'] = df['weekday_name'].apply(lambda x: 'Weekday' if x in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else 'Weekend')
pickups_by_day_type = df.groupby('day_type').size()
num_weekdays = df[df['day_type'] == 'Weekday']['datetime'].dt.date.nunique()
num_weekends = df[df['day_type'] == 'Weekend']['datetime'].dt.date.nunique()
avg_weekday = pickups_by_day_type['Weekday'] / num_weekdays
avg_weekend = pickups_by_day_type['Weekend'] / num_weekends

# --- Compare ---
percentage_difference = ((avg_weekday - avg_weekend) / avg_weekend) * 100
print(f"Average pickups on weekdays: {avg_weekday:.2f}")
print(f"Average pickups on weekends: {avg_weekend:.2f}")
print(f"Weekday pickups are ~{percentage_difference:.1f}% higher than weekends.")

plt.figure(figsize = (6, 5))
df['is_weekend'].replace({True: 'Weekend', False: 'Weekday'}).value_counts().plot(kind='bar')
plt.title("Weekday vs Weekend Pickups")
plt.ylabel("Pickups")
plt.tight_layout()
plt.savefig("plots/weekday_vs_weekend.png")
plt.close()

print("All plots saved in the 'plots/' folder.")

