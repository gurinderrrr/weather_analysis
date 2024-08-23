import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.graph_objects as go

# Load shapefile
shapefile_path = 'C:\\Users\\hp\\Desktop\\gurinder\\python test\\maharashtra district excluding vidarbha.shp'
gdf = gpd.read_file(shapefile_path)

# Example DataFrame for rainfall data (30 days of data)
dates = pd.date_range(start='2024-08-01', end='2024-08-30')

# Generate 50 random stations with lat/long spread across the map
num_stations = 50
np.random.seed(42)  # For reproducibility

stations = [f'Station_{i}' for i in range(1, num_stations + 1)]
types = np.random.choice(['AWS', 'ARG', 'UR'], num_stations)  # Randomly assign types

# Generate random lat/long within specified bounds (Maharashtra region roughly)
lats = np.random.uniform(18, 22, num_stations)  # Latitude range for Maharashtra
longs = np.random.uniform(72, 79, num_stations)  # Longitude range for Maharashtra

# Sort stations by longitude to simulate rain movement from west to northeast
station_coords = sorted(zip(stations, lats, longs, types), key=lambda x: x[2])  # Sort by longitude

# Simulate rainfall data showing movement from left to right (west to northeast)
rainfall_data = []
front_width = 1.5  # Width of the rain front in degrees

for day, date in enumerate(dates):
    # Determine the current position of the rain front
    rain_front_start = 72 + (day / len(dates)) * (79 - 72)  # Start at 72 longitude and move towards 79
    rain_front_end = rain_front_start + front_width
    
    for station, lat, lon, station_type in station_coords:
        if rain_front_start <= lon <= rain_front_end:
            rf = np.random.uniform(10, 100)  # Random rainfall within the rain front
        else:
            rf = 0  # No rain outside the front

        rainfall_data.append({
            'DATE': date,
            'STATION': station,
            'TYPE': station_type,
            'RF': rf,
            'LAT': lat,
            'LONG': lon
        })

# Create DataFrame
df = pd.DataFrame(rainfall_data)

# Function to get custom color based on rainfall value
def get_custom_color(rf):
    if pd.isna(rf):
        return 'black'
    elif rf == 0:
        return 'silver'
    elif 0 < rf <= 2.5:
        return '#98FB98'
    elif 2.6 <= rf <= 15.5:
        return '#7FFF00'
    elif 15.6 <= rf <= 64.5:
        return '#228B22'
    elif 64.6 <= rf <= 115.5:
        return '#FFFF00'
    elif 115.6 <= rf <= 204.5:
        return '#FF8C00'
    elif rf > 204.5:
        return '#FF0000'
    else:
        return '#00008B'

# Generate the base map figure
fig = go.Figure()

# Add shapefile boundaries to the figure
for _, row in gdf.iterrows():
    geom_type = row.geometry.geom_type
    if geom_type == 'Polygon':
        coords = np.array(row.geometry.exterior.coords.xy)
        fig.add_trace(go.Scattermapbox(
            lon=coords[0].tolist(),
            lat=coords[1].tolist(),
            mode='lines',
            line=dict(width=1, color='black'),
            showlegend=False
        ))
    elif geom_type == 'MultiPolygon':
        for polygon in row.geometry.geoms:
            coords = np.array(polygon.exterior.coords.xy)
            fig.add_trace(go.Scattermapbox(
                lon=coords[0].tolist(),
                lat=coords[1].tolist(),
                mode='lines',
                line=dict(width=1, color='black'),
                showlegend=False
            ))

# Create animation frames for each date
frames = []
for date in dates:
    date_data = df[df['DATE'] == date]
    frame_data = go.Scattermapbox(
        lon=date_data['LONG'].tolist(),
        lat=date_data['LAT'].tolist(),
        mode='markers',
        marker=dict(
            size=10,
            color=[get_custom_color(rf) for rf in date_data['RF']],
            opacity=0.7
        ),
        text=[f"{station} ({rf:.1f} mm)" for station, rf in zip(date_data['STATION'], date_data['RF'])],  # Enhanced hover info
        hoverinfo='text'
    )
    frames.append(go.Frame(data=[frame_data], name=str(date)))

fig.frames = frames

# Update layout to center the map and adjust zoom to show entire area
fig.update_layout(
    mapbox=dict(
        style='white-bg',
        zoom=6.3,  # Adjust zoom level to fit the map properly
        center=dict(lat=20, lon=75),  # Center the map to fit Maharashtra region
        layers=[]  # To make sure no additional layers obstruct the map
    ),
    # Commenting out the sliders parameter to hide the slider
    # sliders=[{
    #     "steps": [
    #         {"args": [[str(date)], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate"}],
    #          "label": str(date), "method": "animate"}
    #         for date in dates
    #     ],
    #     "active": 0,
    #     "x": 0.1,
    #     "y": 0,
    #     "xanchor": "left",
    #     "yanchor": "top"
    # }],
    updatemenus=[{
        "buttons": [
            {"args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
             "label": "Play", "method": "animate"},
            {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
             "label": "Pause", "method": "animate"}
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }]
)

# Save the animated figure to an HTML file
fig.write_html('C:\\Users\\hp\\Desktop\\gurinder\\python test\\RF_PLOT_shapefile_animation_50stations_30days_moving_rain_no_slider.html')