import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.transforms as transforms

shapefile_path='C:\\Users\\hp\\Desktop\\gurinder\\filtered shape files\\maharashtra district excluding vidarbha.shp'

gdf=gpd.read_file(shapefile_path)



# Plot the shapefile
fig, ax = plt.subplots(figsize=(22, 10))
gdf.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=1)


# Add taluka names
for x, y, dist in zip(gdf.centroid.geometry.x, gdf.centroid.geometry.y, gdf['DISTRICT']):
    ax.text(x, y, dist, ha='center', va='center', fontsize=4, color='black')


# Set the axes to cover the entire figure
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Optional for exact fit
ax.set_position([0, 0, 1, 1])  # Stretch the axes to cover the entire figure

#gdf.plot()
plt.show()



