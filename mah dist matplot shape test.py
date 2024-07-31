import geopandas as gpd
import matplotlib.pyplot as plt

shapefile_path='C:\\Users\\hp\\Desktop\\gurinder\\filtered shape files\\maharashtra district excluding vidarbha.shp'

gdf=gpd.read_file(shapefile_path)

# Plot the shapefile
fig, ax = plt.subplots(figsize=(22, 10))
gdf.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=1)


# Add taluka names
for x, y, dist in zip(gdf.centroid.geometry.x, gdf.centroid.geometry.y, gdf['DISTRICT']):
    ax.text(x, y, dist, ha='center', va='center', fontsize=4, color='black')

#gdf.plot()
plt.show()



