import pandas as pd
import plotly.graph_objects as go

# Load the Excel file using openpyxl
df = pd.read_excel('C:\\Users\\hp\\Desktop\\gurinder\\python test\\metadata test.xlsx', engine='openpyxl')

# Ensure 'RF' and 'ALTITUDE' columns are treated as strings
df['RF'] = df['RF'].astype(str)
df['ALTITUDE'] = df['ALTITUDE'].astype(str)

# Clean 'RF' and 'ALTITUDE' columns
df['RF'] = df['RF'].str.replace(r'[^\d.]+', '', regex=True)
df['ALTITUDE'] = df['ALTITUDE'].str.replace(r'[^\d.]+', '', regex=True)

# Convert cleaned columns to numeric
df['RF'] = pd.to_numeric(df['RF'], errors='coerce')
df['ALTITUDE'] = pd.to_numeric(df['ALTITUDE'], errors='coerce')

# Define the hover text with the desired information
df['HoverText'] = (
    df['STATION'] + '<br>' +
    'Altitude: ' + df['ALTITUDE'].astype(str) + '<br>' +
    'Rainfall: ' + df['RF'].astype(str)
)

# Create the 3D scatter plot
fig = go.Figure()

# Add the data points
fig.add_trace(go.Scatter3d(
    x=df['LONG'],          # Longitude
    y=df['LAT'],           # Latitude
    z=df['ALTITUDE'],      # Altitude
    mode='markers',
    marker=dict(
        size=5,            # Fixed size for all markers
        color=df['RF'],    # Color by Rainfall
        colorscale='Viridis',
        colorbar=dict(title='Rainfall')
    ),
    text=df['HoverText'],  # Hover text with the desired info
    hoverinfo='text'      # Display only the custom hover text
))

# Update layout to use Carto Positron as the map style
fig.update_layout(
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Altitude'
    ),
    title='3D Map of Stations with Rainfall',
    scene_camera=dict(
        eye=dict(x=1.5, y=1.5, z=1.5)  # Adjust camera position if needed
    ),
    mapbox=dict(
        style='carto-positron',  # Use Carto Positron as the base map style
        center=dict(
            lat=df['LAT'].mean(),  # Center the map on the average latitude
            lon=df['LONG'].mean()  # Center the map on the average longitude
        ),
        zoom=10,  # Adjust zoom level if needed
        accesstoken='pk.eyJ1IjoiZ3VyaW5kZXJuIiwiYSI6ImNsemllMm0xbDBmYmsya3MxNTZraWU3eWoifQ.jeOv2rXt-XphBQDTlBII-g'  # Replace with your Mapbox access token
    )
)

# Show the plot
fig.show()