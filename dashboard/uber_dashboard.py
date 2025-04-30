import streamlit as st
import pandas as pd
import sqlite3
import folium
from folium.plugins import FastMarkerCluster
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Uber Data Dashboard", layout="wide")
st.title("Uber Pickups in September 2014")

# --- Load data from SQLite --
with sqlite3.connect("uber.db") as conn:
    df = pd.read_sql_query("SELECT * FROM uber_pickups", conn)

df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df['hour'] = df['datetime'].dt.hour
df['weekday'] = df['datetime'].dt.day_name()
df['month'] = df['datetime'].dt.month_name()

# Base info and color mapping
base_info = {
    "B02512": {"name": "Unter", "location": "636 W 28th St, New York, NY", "color": "#1f77b4"},  # Blue
    "B02598": {"name": "Hinter", "location": "New York, NY", "color": "#ff7f0e"},  # Orange
    "B02617": {"name": "Weiter", "location": "New York, NY", "color": "#2ca02c"},  # Green
    "B02682": {"name": "Schmecken", "location": "New York, NY", "color": "#d62728"},  # Red
    "B02764": {"name": "Danach-NY", "location": "New York, NY", "color": "#9467bd"}  # Purple
}

st.metric(label="📦 Total Pickups", value=f"{len(df):,}")

# --- Plotting filtered data ---
selected_date = st.sidebar.date_input("Select a date", value=df['date'].min())
base_codes = [code for code in df['base'].unique() if code in base_info]

name_to_code = {info["name"]: code for code, info in base_info.items()}
selected_base_names = st.sidebar.multiselect("Select base(s)", name_to_code)
selected_base = [name_to_code[name] for name in selected_base_names]
selected_base_codes = [name_to_code[name] for name in selected_base_names]
code_to_color = {code: info["color"] for code, info in base_info.items()}
if selected_base_names:
    for name in selected_base_names:
        code = name_to_code[name]
        color = code_to_color[code]
        st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center; margin-bottom: 8px;">
        <div style="width: 15px; height: 15px; border-radius: 50%; background-color: {color}; margin-right: 8px;"></div>
        <span style="font-weight: 600; color: {color};">{name}</span>
    </div>
    """,
    unsafe_allow_html=True
    )
filtered_df = df[(df['date'] == selected_date) & (df['base'].isin(selected_base_codes))]

def get_base_details(base_code):
    return base_info.get(base_code, {"name": "Unknown", "location": "Unknown", "color": "#000000"})

# --- New York's map ---
st.markdown("### Map of Uber Pickups")
ny_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

for _, row in filtered_df.iterrows():
    base_code = row['base']
    color = code_to_color.get(base_code, "#000000")
    base_details = get_base_details(base_code)
    base_color = base_details['color']
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5,
        color=base_color,          fill=True,
        fill_color=base_color,
        fill_opacity=0.6
    ).add_to(ny_map)

st.components.v1.html(ny_map._repr_html_(), height=500)

# --- Slider to filter by hour range ---
st.sidebar.header("Filter by Hour Range")
hour_range = st.sidebar.slider("Select hour range", min_value=0, max_value=23, value=(0, 23), step=1)
filtered_df_hour = filtered_df[(filtered_df['hour'] >= hour_range[0]) & (filtered_df['hour'] <= hour_range[1])]
filtered_df = filtered_df_hour

# --- Display filter summary ---
st.markdown("### 📊 Filter Summary")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**📅 Date**")
    st.markdown(f"{selected_date.strftime('%A, %B %d, %Y')}")

with col2:
    st.markdown("**⏰ Hour Range**")
    st.markdown(f"{hour_range[0]}:00 — {hour_range[1]}:00")

st.markdown("**🚖 Selected Base(s):**")
for base in selected_base_codes:
    info = get_base_details(base)
    st.markdown(
        f"""
        <div style="padding: 8px; margin-bottom: 5px; border-radius: 8px;">
            <strong>{info['name']}</strong> ({base})<br>
            <span style="color: gray;">📍 {info['location']}</span>
        </div>
        """, unsafe_allow_html=True
    )

st.info(f"🔎 Showing **{len(filtered_df):,}** pickups based on current filters.")

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
