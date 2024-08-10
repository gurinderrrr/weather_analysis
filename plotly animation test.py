import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.graph_objects as go

# Load shapefile
shapefile_path = 'C:\\Users\\hp\\Desktop\\gurinder\\python test\\maharashtra district excluding vidarbha.shp'
gdf = gpd.read_file(shapefile_path)

# Example DataFrame for rainfall data (10 days of data)
dates = pd.date_range(start='2024-08-01', end='2024-08-10')
stations = ['Station_A', 'Station_B', 'Station_C']
types = ['AWS', 'ARG', 'UR']
data = {
    'DATE': np.repeat(dates, len(stations)),
    'STATION': stations * len(dates),
    'TYPE': types * len(dates),
    'RF': np.random.rand(len(dates) * len(stations)) * 100,  # Random rainfall data
    'LAT': np.random.uniform(18, 20, len(dates) * len(stations)),
    'LONG': np.random.uniform(73, 75, len(dates) * len(stations))
}

df = pd.DataFrame(data)

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
        for polygon in row.geometry.geoms:  # Access individual polygons
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
    frames.append(go.Frame(
        data=[go.Scattermapbox(
            lon=date_data['LONG'].tolist(),  # Convert to list
            lat=date_data['LAT'].tolist(),   # Convert to list
            mode='markers',
            marker=dict(
                size=10,
                color='blue',  # Example color, you can use your custom color function here
                opacity=0.7
            ),
            text=date_data['STATION'],
            hoverinfo='text'
        )],
        name=str(date)
    ))

fig.frames = frames

# Add slider
fig.update_layout(
    mapbox=dict(
        style='white-bg',
        zoom=5,
        center=dict(lat=19, lon=74)
    ),
    sliders=[{
        "steps": [
            {"args": [[str(date)], {"frame": {"duration": 1000, "redraw": True}, "mode": "immediate"}],
             "label": str(date), "method": "animate"}
            for date in dates
        ],
        "active": 0,
        "x": 0.1,
        "y": 0,
        "xanchor": "left",
        "yanchor": "top"
    }],
    updatemenus=[{
        "buttons": [
            {"args": [None, {"frame": {"duration": 1000, "redraw": True}, "fromcurrent": True}],
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
fig.write_html('C:\\Users\\hp\\Desktop\\gurinder\\python test\\RF_PLOT_shapefile_animation.html')