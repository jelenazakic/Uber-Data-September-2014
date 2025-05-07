
# 🚕 Uber Pickups Dashboard

This is an interactive Streamlit app that visualizes Uber pickup data by hour, base, and more. You can filter by date and base and explore trends easily.

👉 **[Try the live app here](https://uber-data-september-2014-edlgwlcfleerfxkpgpadx2.streamlit.app/)**

## Features

- Filter by date and base
- Visualizations for:
  - Top 5 Busiest Hours Per Base
  - Pickups by hour
  - Pickups by base
  - Heatmap (base vs. hour)
  - Interactive New York City Map with pickup points
  - Pickup Density Heatmap

The app includes an interactive map showing all pickup points across NYC for the selected time period. This gives a quick overview of activity hotspots and trends.

- Built using  `folium`
- Shows pickup **density** and **distribution** over the city
- Helps identify high-traffic zones (e.g., Midtown, Downtown)

## Dataset

Stored in a local SQLite database (`uber.db`). Comes from the [Uber pickups NYC dataset](https://www.kaggle.com/datasets/fivethirtyeight/uber-pickups-in-new-york-city).



