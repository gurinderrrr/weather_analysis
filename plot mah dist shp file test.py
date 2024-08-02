import geopandas as gpd
import matplotlib.pyplot as plt

# Path to the shapefile
shapefile_path = 'C:\\Users\\hp\\Desktop\\gurinder\\python test\\maharashtra district excluding vidarbha.shp'

# Load the shapefile
gdf = gpd.read_file(shapefile_path)

# Print CRS and geometry type for verification
#print(gdf.geometry.type)
#print(gdf.crs)

# Re-project to UTM Zone 43N
#gdf = gdf.to_crs(epsg=32643)

# Calculate centroids
gdf['centroid'] = gdf.geometry.centroid

# Calculate bounding box
x_min, y_min, x_max, y_max = gdf.total_bounds

# Plot the shapefile
fig, ax = plt.subplots(figsize=(22, 10))
gdf.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=1)

# Add district names at centroid locations
for x, y, dist in zip(gdf['centroid'].x, gdf['centroid'].y, gdf['DISTRICT']):
    ax.text(x, y, dist, ha='center', va='center', fontsize=8, color='black')

# Adjust plot limits to fit the data exactly
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Set aspect ratio to be equal
ax.set_aspect('auto')

# Remove axis
ax.axis('off')

# Adjust subplot parameters to minimize extra space
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Show the plot
plt.show()