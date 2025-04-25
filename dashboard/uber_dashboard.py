import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import FastMarkerCluster

# --- Title ---
st.set_page_config(page_title = "Uber Data Dashboard", layout = "wide")
st.title ("Uber Pickups in September 2014")

# --- Load data from SQLite --
with sqlite3.connect("uber.db") as conn:
     df = pd.read_sql_query("SELECT * FROM uber_pickups", conn)
     
locations = df[['lat', 'lon']].values.tolist()
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df['hour'] = df['datetime'].dt.hour
df['weekday'] = df['datetime'].dt.day_name()
df['month'] =  df['datetime'].dt.month_name()

# --- New York's map ---
ny_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
FastMarkerCluster(data=locations).add_to(ny_map)
st.subheader("Uber Pickups in New York")
st.write("Here are the Uber pickup locations in New York City.")
st.markdown("### Map of Uber Pickups")
st.components.v1.html(ny_map._repr_html_(), height=500)

# --- Base info ---
base_name_map = {
    "B02512": "Unter",
    "B02598": "Hinter",
    "B02617": "Weiter",
    "B02682": "Schmecken",
    "B02764": "Danach-NY"
}

base_info = {
    "B02512": {"name": "Unter", "location": "636 W 28th St, New York, NY"},
    "B02598": {"name": "Hinter", "location": "New York, NY"},
    "B02617": {"name": "Weiter", "location": "New York, NY"},
    "B02682": {"name": "Schmecken", "location": "New York, NY"},
    "B02764": {"name": "Danach-NY", "location": "New York, NY"}
}

base_colors = {
    'B02512': 'red',
    'B02598': 'blue',
    'B02617': 'green',
    'B02682': 'purple',
    'B02764': 'orange',
    'B02765': 'yellow'
}

def get_base_details(base_code):
    return base_info.get(base_code, {"name": "Unknown", "location": "Unknown"})

st.metric(label="📦 Total Pickups", value=f"{len(df):,}")

# --- Plotting filtered data ---
selected_date = st.sidebar.date_input("Select a date", value = df['date'].min())
base_names = [base_name_map[code] for code in df['base'].unique()]
selected_base = st.sidebar.multiselect("Select base(s)", base_names, default = base_names)
name_to_code = {v: k for k, v in base_name_map.items()}
selected_base = [name_to_code[name] for name in selected_base]
filtered_df = df[(df['date'] == selected_date) & (df['base'].isin(selected_base))]

# --- Slider to filter by hour range ---
st.sidebar.header("Filter by Hour Range")
hour_range = st.sidebar.slider("Select hour range", min_value = 0, max_value = 23,value = (0,23), step = 1)
filtered_df_hour = filtered_df[(filtered_df['hour'] >= hour_range[0]) & (filtered_df['hour']<= hour_range[1])]
filtered_df = filtered_df_hour

# --- Display filter summary ---
st.markdown("### 📊 Filter Summary")
st.markdown(f"- **📅 Date:** {selected_date.strftime('%A, %B %d, %Y')}")
st.markdown(f"- **⏰ Hour Range:** {hour_range[0]}:00 to {hour_range[1]}:00")
st.markdown("- **🚖 Base(s):**")
for base in selected_base:
    info = get_base_details(base)
    st.markdown(f"  - `{base}` – **{info['name']}** ({info['location']})")

st.info(f"🔎 Showing {len(filtered_df):,} pickups based on current filters.")

# --- Tabs for visualizations ---
tab1, tab2, tab3, tab4 = st.tabs(["Pickups by Hour","Pickups by Hour (Line Plot)", "Pickups by Base", "Heatmap"])

with tab1:
    st.subheader("Pickups by Hour")
    fig, ax = plt.subplots()
    filtered_df.groupby('hour').size().plot(kind='bar', ax=ax)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both'))
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
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
