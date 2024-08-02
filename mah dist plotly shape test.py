import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

shapefile_path='C:\\Users\\hp\\Desktop\\gurinder\\python test\\maharashtra district excluding vidarbha.shp'

gdf=gpd.read_file(shapefile_path)

# Convert GeoDataFrame to GeoJSON format
geojson = gdf.to_json()

# Create a Plotly figure with graph_objects
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson,
    locations=gdf.index,
    marker_opacity=0.5,
    marker_line_width=0
))

# Update layout for Mapbox style
fig.update_layout(
    mapbox_style="carto-positron",
)

# Save the plot as an image
fig.write_image("C:\\Users\\hp\\Desktop\\plot.png")  # Save as PNG