import geopandas as gpd
import matplotlib.pyplot as plt

shapefile_path='C:\\Users\\hp\\Desktop\\gurinder\\python test\\maharashtra district excluding vidarbha.shp'

gdf=gpd.read_file(shapefile_path)

print(gdf.geometry.type)
print(gdf.crs)



#gdf = gdf.to_crs(epsg=4263)

# Calculate bounding box
x_min, y_min, x_max, y_max = gdf.total_bounds



# Plot the shapefile
fig, ax = plt.subplots(figsize=(22, 10))
gdf.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=1)



# Add taluka names
for x, y, dist in zip(gdf.centroid.geometry.x, gdf.centroid.geometry.y, gdf['DISTRICT']):
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
plt.show()




