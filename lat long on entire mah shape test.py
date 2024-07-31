import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px

# Load the shapefile for Pune district
shapefile_path = 'C:\\Users\\HP\\Desktop\\guri\\python test\\maharashtra tehsil excluding vidharbha.shp'
district_data = gpd.read_file(shapefile_path)

# Read latitude and longitude data from Excel
excel_file = 'C:\\Users\\HP\\Desktop\\guri\\python test\\metadata with observatory 22-07-2024.xlsx'
lat_lon_data = pd.read_excel(excel_file)

# Convert latitude and longitude data to GeoDataFrame
geometry = gpd.points_from_xy(lat_lon_data['LONG'], lat_lon_data['LAT'])
lat_lon_gdf = gpd.GeoDataFrame(lat_lon_data, geometry=geometry, crs=district_data.crs)

# Convert district_data to GeoJSON format
district_geojson = district_data.to_json()

# Create the figure
fig = go.Figure()

# Add the shapefile data as a trace
fig.add_trace(go.Choroplethmapbox(
    geojson=district_geojson,
    locations=[0],  # dummy value
    z=[0],  # dummy value
    showscale=False,
    marker=dict(opacity=0.5, line=dict(width=1))
))

# Add RIMC points
if 'RIMC' in lat_lon_gdf['TYPE'].values:
    rimc_data = lat_lon_gdf[lat_lon_gdf['TYPE'] == 'RIMC']
    fig.add_trace(go.Scattermapbox(
        lat=rimc_data['LAT'],
        lon=rimc_data['LONG'],
        mode='markers',
        marker=dict(size=10, color='red'),
        name='RIMC'
    ))

# Add OBSERVATORY points
if 'OBSERVATORY' in lat_lon_gdf['TYPE'].values:
    observatory_data = lat_lon_gdf[lat_lon_gdf['TYPE'] == 'OBSERVATORY']
    fig.add_trace(go.Scattermapbox(
        lat=observatory_data['LAT'],
        lon=observatory_data['LONG'],
        mode='markers',
        marker=dict(size=10, color='blue'),
        name='OBSERVATORY'
    ))

# Set layout
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=district_data.geometry.centroid.y.mean(), lon=district_data.geometry.centroid.x.mean()),
        zoom=8
    ),
    title='AWS and ARG Location on Pune Tehsil Level Map',
    margin=dict(l=0, r=0, t=50, b=0)
)

# Show the plot
fig.show()