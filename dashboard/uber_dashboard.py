import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title = "Uber Data Dashboard", layout = "wide")
st.title ("Uber Pickups Dashboard")

conn = sqlite3.connect("uber.db")
df = pd.read_sql_query("SELECT * FROM uber_pickups", conn)
conn.close()

df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df['hour'] = df['datetime'].dt.hour
df['weekday'] = df['datetime'].dt.day_name()
df['month'] =  df['datetime'].dt.month_name()

st.sidebar.header("Filters")
selected_date = st.sidebar.date_input("Select a date", value = df['date'].min())

selected_base = st.sidebar.multiselect("Select base(s)", df['base'].unique(), default = list(df['base'].unique()))

filtered_df = df[(df['date'] == selected_date) & (df['base'].isin(selected_base))]

st.write(f"Showing date for **{selected_date}** and base(s): {','.join(selected_base)}")
st.write(f"Number of pickups: {len(filtered_df)}")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Pickups by Hour")
    fig, ax = plt.subplots()
    filtered_df.groupby('hour').size().plot(kind = 'bar', ax=ax)
    st.pyplot(fig)
with col2:
    st.subheader("Pickups by Base")
    fig2, ax2 = plt.subplots()
    filtered_df['base'].value_counts().plot(kind = 'bar', ax = ax2)
    st.pyplot(fig2)

st.subheader("Heatmap: Pickups by Hour and Base")
heatmap_data = filtered_df.groupby(['base', 'hour']).size().unstack(fill_value = 0)
fig3, ax3 = plt.subplots(figsize = (10,5))
sns.heatmap(heatmap_data, cmap ="YlGnBu", ax = ax3)
st.pyplot(fig3)


