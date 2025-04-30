import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import FastMarkerCluster

st.set_page_config(page_title="Uber Data Dashboard", layout="wide")
st.title("Uber Pickups in September 2014")

# --- Load data from SQLite ---
with sqlite3.connect("uber.db") as conn:
    df = pd.read_sql_query("SELECT * FROM uber_pickups", conn)

df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df['hour'] = df['datetime'].dt.hour
df['weekday'] = df['datetime'].dt.day_name()
df['month'] = df['datetime'].dt.month_name()

base_info = {
    "B02512": {"name": "Unter", "location": "636 W 28th St, New York, NY"},
    "B02598": {"name": "Hinter", "location": "New York, NY"},
    "B02617": {"name": "Weiter", "location": "New York, NY"},
    "B02682": {"name": "Schmecken", "location": "New York, NY"},
    "B02764": {"name": "Danach-NY", "location": "New York, NY"}
}

st.metric(label="📦 Total Pickups", value=f"{len(df):,}")

# --- Sidebar Filters ---
selected_date = st.sidebar.date_input("Select a date", value=df['date'].min())

# Base filter
name_to_code = {info["name"]: code for code, info in base_info.items()}
selected_base_names = st.sidebar.multiselect(
    "Select base(s)", name_to_code.keys(), default=list(name_to_code.keys())
)
selected_base_codes = [name_to_code[name] for name in selected_base_names]

if not selected_base_codes:
    st.warning("Please select at least one base.")
    st.stop()

filtered_df = df[(df['date'] == selected_date) & (df['base'].isin(selected_base_codes))]

# --- Hour Range Slider ---
st.sidebar.header("Filter by Hour Range")
hour_range = st.sidebar.slider(
    "Select hour range", min_value=0, max_value=23, value=(0, 23), step=1
)
filtered_df = filtered_df[(filtered_df['hour'] >= hour_range[0]) & (filtered_df['hour'] <= hour_range[1])]

# --- Base Details Helper ---
def get_base_details(base_code):
    return base_info.get(base_code, {"name": "Unknown", "location": "Unknown"})

# --- Filter Summary ---
st.markdown("### 📊 Filter Summary")
st.markdown(f"- **📅 Date:** {selected_date.strftime('%A, %B %d, %Y')}")
st.markdown(f"- **⏰ Hour Range:** {hour_range[0]}:00 to {hour_range[1]}:00")
st.markdown("- **🚖 Base(s):**")
for base in selected_base_codes:
    info = get_base_details(base)
    st.markdown(f"  - {base} – **{info['name']}** ({info['location']})")

st.info(f"🔎 Showing {len(filtered_df):,} pickups based on current filters.")

# --- Map ---
st.markdown("### 🗺️ Map of Uber Pickups")
if not filtered_df.empty:
    ny_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
    FastMarkerCluster(data=filtered_df[['lat', 'lon']].values.tolist()).add_to(ny_map)
    st.components.v1.html(ny_map._repr_html_(), height=500)
else:
    st.warning("No pickup data available for the selected filters.")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Pickups by Hour", "Pickups by Hour (Line Plot)", "Pickups by Base", "Heatmap"
])

with tab1:
    st.subheader("Pickups by Hour")
    if not filtered_df.empty:
        fig, ax = plt.subplots()
        filtered_df.groupby('hour').size().plot(kind='bar', ax=ax)
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both'))
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)
    else:
        st.info("No data to display.")

with tab2:
    st.subheader("Pickups by Hour (Line Plot)")
    if not filtered_df.empty:
        fig1, ax1 = plt.subplots()
        filtered_df.groupby('hour').size().plot(kind='line', ax=ax1, marker='o')
        st.pyplot(fig1)
    else:
        st.info("No data to display.")

with tab3:
    st.subheader("Pickups by Base")
    if not filtered_df.empty:
        fig2, ax2 = plt.subplots()
        filtered_df['base'].value_counts().plot(kind='bar', ax=ax2)
        st.pyplot(fig2)
    else:
        st.info("No data to display.")

with tab4:
    st.subheader("Heatmap: Pickups by Hour and Base")
    if not filtered_df.empty:
        heatmap_data = filtered_df.groupby(['base', 'hour']).size().unstack(fill_value=0)
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax3)
        st.pyplot(fig3)
    else:
        st.info("No data to display.")

