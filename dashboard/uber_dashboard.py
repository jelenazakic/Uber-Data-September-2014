import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# --- Title ---
st.set_page_config(page_title = "Uber Data Dashboard", layout = "wide")
st.title ("Uber Pickups in September 2014")

# --- Load data from SQLite --
with sqlite3.connect("uber.db") as conn:
     df = pd.read_sql_query("SELECT * FROM uber_pickups", conn)

df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df['hour'] = df['datetime'].dt.hour
df['weekday'] = df['datetime'].dt.day_name()
df['month'] =  df['datetime'].dt.month_name()

st.metric(label="📦 Total Pickups", value=f"{len(df):,}")

# --- Plotting filtered data ---
selected_date = st.sidebar.date_input("Select a date", value = df['date'].min())
selected_base = st.sidebar.multiselect("Select base(s)", df['base'].unique(), default = list(df['base'].unique()))
filtered_df = df[(df['date'] == selected_date) & (df['base'].isin(selected_base))]

# --- Slider to filter by hour range ---
st.sidebar.header("Filter by Hour Range")
hour_range = st.sidebar.slider("Select hour range", min_value = 0, max_value = 23,value = (0,23), step = 1)
filtered_df_hour = filtered_df[(filtered_df['hour'] >= hour_range[0]) & (filtered_df['hour']<= hour_range[1])]
filtered_df = filtered_df_hour

# --- Display filter summary ---
st.markdown(f"""
### 📊 Filter Summary
- **📅 Date:** {selected_date.strftime('%A, %B %d, %Y')}
- **⏰ Hour Range:** {hour_range[0]}:00 to {hour_range[1]}:00
- **🚖 Base(s):** {', '.join(selected_base)}
""")
st.info(f"🔎 Showing {len(filtered_df):,} pickups based on current filters.")

# --- Tabs for visualizations ---
tab1, tab2, tab3, tab4 = st.tabs(["Pickups by Hour","Pickups by Hour (Line Plot)", "Pickups by Base", "Heatmap"])

with tab1:
    st.subheader("Pickups by Hour")
    fig, ax = plt.subplots()
    filtered_df.groupby('hour').size().plot(kind='bar', ax=ax)
    st.pyplot(fig)
    
with tab2:
    st.subheader("Pickups by Hour (Line Plot)")
    fig1, ax1 = plt.subplots()
    filtered_df.groupby('hour').size().plot(kind = 'line', ax = ax1, marker = 'o')
    st.pyplot(fig1)
    
with tab3:
    st.subheader("Pickups by Base")
    fig2, ax2 = plt.subplots()
    filtered_df['base'].value_counts().plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

with tab4:
    st.subheader("Heatmap: Pickups by Hour and Base")
    heatmap_data = filtered_df.groupby(['base', 'hour']).size().unstack(fill_value=0)
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax3)
    st.pyplot(fig3)
