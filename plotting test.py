import geopandas as gpd
import geopandas as gpd
import requests
from io import BytesIO
import zipfile
import tempfile
import gdown
import os

# Correctly formatted URL
url = "https://drive.google.com/uc?id=YOUR_FILE_ID&export=download"

# Create a temporary directory
temp_dir = tempfile.mkdtemp()

# Define output file path in the temporary directory
output = os.path.join(temp_dir, 'shapefile.zip')

# Download the file using gdown
gdown.download(url, output, quiet=False)

# Extract the ZIP file
with zipfile.ZipFile(output, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# Find the .shp file and load it into GeoDataFrame
for file in os.listdir(temp_dir):
    if file.endswith('.shp'):
        shapefile_path = os.path.join(temp_dir, file)
        gdf = gpd.read_file(shapefile_path)
        break

# Now gdf contains your GeoDataFrame

# Optional: Clean up the temporary directory
import shutil
shutil.rmtree(temp_dir)


#https://drive.google.com/file/d/1Ei-rD6W6P1WzQ20H5-z9NBhXwCG_wD4l/view?usp=drive_link