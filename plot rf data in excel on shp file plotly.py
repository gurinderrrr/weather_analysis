import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go

# Load Excel data
excel_file = "C:\\Users\\hp\\Desktop\\ARWIND.xlsx"
df = pd.read_excel(excel_file)

df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
df['LONG'] = pd.to_numeric(df['LONG'], errors='coerce')

# Filter out rows with invalid lat/long (e.g., 0.00 or 99.99)
df_filtered = df[((df['LAT'] != 0) & (df['LONG'] != 0)) & ((df['LAT'] != 99.99) & (df['LONG'] != 99.99))]

# Custom function to assign colors based on rainfall value
def color_range(rf_value):
    if pd.isna(rf_value):  # Handle NaN values
        return '#FFFFFF'
    elif 1 <= rf_value <= 2.4:  # Light Rain
        return '#ADFF2F'  # GreenYellow
    elif 2.5 <= rf_value <= 15.5:  # Moderate Rain
        return '#00FF00'  # Lime
    elif 15.6 <= rf_value <= 64.4:  # Heavy Rain
        return '#00FFFF'  # Aqua
    elif 64.5 <= rf_value <= 115.5:  # Very Heavy Rain
        return '#FFFF00'  # Yellow
    elif 115.6 <= rf_value <= 204.4:  # Very Heavy Rain
        return '#FFA500'  # Orange
    elif rf_value > 204.4:  # Extremely Heavy Rain
        return '#FF0000'  # Red
    else:
        return '#FFFFFF'  # Default white for no rainfall

# Apply color function to the rainfall data
df_filtered['color'] = df_filtered['RF'].apply(color_range)


df=df_filtered.copy()
del df_filtered

# Check if there are any NaNs in lat/long and print a sample of the data
print(df[['STATION', 'LAT', 'LONG', 'RF']].head())
print(df.isna().sum())  # Ensure no missing values in important columns

# Load the shapefile
shapefile = "C:\\Users\\hp\\Desktop\\gurinder\\filtered shape files\\maharashtra district excluding vidarbha.shp"
gdf = gpd.read_file(shapefile)

# Convert the geodataframe to GeoJSON format for Plotly
geojson = gdf.__geo_interface__

# Create a hover text with both station name and rainfall amount
df['hover_info'] = df['STATION'] + '<br>Rainfall: ' + df['RF'].astype(str) + ' mm'

# Create a scatter plot for rainfall data using lat, long, and RF
fig = go.Figure()

# Plot the rainfall data from Excel as scatter points with hover information
fig.add_trace(go.Scattermapbox(
    lon=df['LONG'],
    lat=df['LAT'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=10,
        color=df['color'],  # Use custom colors based on rainfall
        showscale=False
    ),
    hovertext=df['hover_info'],  # Custom hover text with station name and rainfall
    hoverinfo='text'  # Ensure hover info displays custom text
))

# Use the "open-street-map" style, which doesn't require a token
fig.update_layout(
    mapbox_style='open-street-map',  # No token required for this style
    mapbox_zoom=5,  # Adjust zoom level
    mapbox_center={"lat": df['LAT'].mean(), "lon": df['LONG'].mean()},
    margin={"r":0,"t":0,"l":0,"b":0}
)

# Save the plot as an HTML file
fig.write_html("rainfall_map_with_hover.html")

# Optionally, show the plot in the browser
#fig.show()