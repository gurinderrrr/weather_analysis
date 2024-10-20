import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import json

# Step 1: Define the color_range function
def color_range(rf_value):
    if pd.isna(rf_value):  # Handle NaN values
        return '#FFFFFF'
    elif 0 <= rf_value <= 0.9:  # Low rainfall
        return '#FFFFFF' 
    elif 1 <= rf_value <= 2.4:  # Low rainfall
        return '#ADFF2F' 
    elif 2.5 <= rf_value <= 15.5:  # Moderate rainfall
        return '#00FF00'
    elif 15.6 <= rf_value <= 64.4:  # High rainfall
        return '#00FFFF'
    elif 64.5 <= rf_value <= 115.5:  # Very high rainfall
        return '#FFFF00'
    elif 115.6 <= rf_value <= 204.4:  # Very high rainfall
        return '#FFA500'
    elif rf_value > 204.4:  # Extreme high rainfall
        return '#FF0000'
    else:
        return '#FFFFFF'

# Load the Excel file
file_path = 'C:\\Users\\hp\\Desktop\\AUGUST 2024 edited aa.xls'  # Path to the file
df = pd.read_excel(file_path)





# Filter out rows with invalid lat/long (e.g., 0.00 or 99.99)
df_filtered = df[((df['LAT'] != 0) & (df['LONG'] != 0)) & ((df['LAT'] != 99.99) & (df['LONG'] != 99.99))]

df=df_filtered.copy()
del df_filtered


# Assign day numbers as column headers for the 31 rainfall columns
day_columns = list(range(1, 32))  # Days 1 to 31 for August
df.columns = ['Station'] + day_columns + ['LAT', 'LONG']

# Melt the DataFrame from wide to long format
df_melted = df.melt(id_vars=['Station', 'LAT', 'LONG'], 
                    value_vars=day_columns, 
                    var_name='Date', 
                    value_name='RF')

# Convert 'Date' to actual date format (August 1-31, 2024) and keep only the date part
df_melted['Date'] = pd.to_datetime(df_melted['Date'], format='%d').map(lambda x: x.replace(month=8, year=2024)).dt.date

# Ensure lat and long are numeric
df_melted['LAT'] = pd.to_numeric(df_melted['LAT'], errors='coerce')
df_melted['LONG'] = pd.to_numeric(df_melted['LONG'], errors='coerce')
df_melted['RF'] = pd.to_numeric(df_melted['RF'], errors='coerce')

# Save the transformed data to an Excel file
output_file = 'C:\\Users\\hp\\Desktop\\august_2024_rainfall_long_format.xlsx'
df_melted.to_excel(output_file, index=False)

# Step 3: Create a new column in DataFrame for colors based on RF values
df_melted['color'] = df_melted['RF'].apply(color_range)

# Step 1: Read the Excel file
excel_file_path = 'C:\\Users\\hp\\Desktop\\august_2024_rainfall_long_format.xlsx'
df = pd.read_excel(excel_file_path)

# Step 2: Read the shapefile
shapefile_path = "C:\\Users\\hp\\Desktop\\gurinder\\filtered shape files\\maharashtra district excluding vidarbha.shp"
gdf = gpd.read_file(shapefile_path)

# Convert the GeoDataFrame to GeoJSON format
geojson = json.loads(gdf.to_json())

# Calculate the centroid of each district polygon
gdf['centroid'] = gdf.geometry.centroid
gdf['centroid_lon'] = gdf.centroid.x
gdf['centroid_lat'] = gdf.centroid.y


    # Plot using Plotly Graph Objects
fig = go.Figure()

    # Add shapefile boundaries
for feature in geojson['features']:
        coords = feature['geometry']['coordinates']
        if feature['geometry']['type'] == 'Polygon':
            lon, lat = zip(*coords[0])
            fig.add_trace(go.Scattermapbox(
                lon=lon,
                lat=lat,
                mode='lines',
                line=dict(width=1, color='black'),
                fill='toself',
                fillcolor='rgba(0,100,80,0.2)',
                showlegend=False  # Hide the legend
            ))
        elif feature['geometry']['type'] == 'MultiPolygon':
            for polygon in coords:
                lon, lat = zip(*polygon[0])
                fig.add_trace(go.Scattermapbox(
                    lon=lon,
                    lat=lat,
                    mode='lines',
                    line=dict(width=1, color='black'),
                    fill='toself',
                    fillcolor='rgba(0,100,80,0.2)',
                    showlegend=False  # Hide the legend
                ))

    # Add district names as text annotations
for _, row in gdf.iterrows():
        fig.add_trace(go.Scattermapbox(
            lon=[row['centroid_lon']],
            lat=[row['centroid_lat']],
            mode='text',
            text=row['DISTRICT'],
            showlegend=False,
            textfont=dict(size=10, color='black')  # Adjust text size and color as needed
        ))



# Step 4: Process the data and plot for each day
for date in df_melted['Date'].unique():
    daily_data = df_melted[df_melted['Date'] == date]



     # Create the plot using latitude and longitude directly from the Excel data
    fig = px.scatter_mapbox(
        daily_data,
        lat='LAT',
        lon='LONG',
        hover_name='Station',  # Show station names on hover
        hover_data={'RF': True, 'LAT': False, 'LONG': False, 'color': False},  # Show only RF and Station in hover
        mapbox_style='white-bg',
        center={'lat': gdf.geometry.centroid.y.mean(), 'lon': gdf.geometry.centroid.x.mean()},
        zoom=5,  # Adjust the zoom level
        opacity=1
    )

    # Manually specify the color for each marker using the 'color' column
    fig.update_traces(marker=dict(color=daily_data['color'], size=8))  # Adjust size as needed

    # Save the plot as an HTML file, ensuring the date is formatted properly
    fig.write_html(f'C:\\Users\\hp\\Desktop\\PLOTS\\rainfall_plot_{pd.to_datetime(date).strftime("%Y_%m_%d")}.html')