import os
import requests
import zipfile
import geopandas as gpd
import plotly.express as px
import pandas as pd

# Example rainfall data points with district names
rainfall_data = [
    {"district": "Mumbai", "lat": 19.0760, "lon": 72.8777, "rainfall": 100},
    {"district": "Pune", "lat": 18.5204, "lon": 73.8567, "rainfall": 120},
    {"district": "Nagpur", "lat": 21.1458, "lon": 79.0882, "rainfall": 90}
]

# Convert to DataFrame
df = pd.DataFrame(rainfall_data)

# Define the shapefile URL and local path
shapefile_url = "https://github.com/datameet/maps/raw/master/Districts/india_districts.zip"
shapefile_dir = "india_districts"
shapefile_path = os.path.join(shapefile_dir, "india_districts.shp")

# Download and extract the shapefile if not already done
if not os.path.exists(shapefile_path):
    os.makedirs(shapefile_dir, exist_ok=True)
    zip_path = os.path.join(shapefile_dir, "india_districts.zip")
    
    # Download the shapefile
    with requests.get(shapefile_url, stream=True) as r:
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    # Extract the shapefile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(shapefile_dir)

# Load the India districts shapefile
gdf = gpd.read_file(shapefile_path)

# Create a GeoDataFrame with rainfall data
gdf_rainfall = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))

# Plot the map
fig = px.choropleth_mapbox(
    gdf,
    geojson=gdf.geometry,
    locations=gdf.index,
    mapbox_style="carto-positron",
    center={"lat": 20.5937, "lon": 78.9629},
    zoom=4,
    title="Rainfall Data in Indian Districts"
)

# Add rainfall data points to the map
fig.add_scattermapbox(
    lat=df["lat"],
    lon=df["lon"],
    mode="markers",
    marker=px.scatter_mapbox(size=df["rainfall"], color=df["rainfall"], colorscale="Viridis", showscale=True),
    text=df["district"],
    name="Rainfall"
)

fig.show()