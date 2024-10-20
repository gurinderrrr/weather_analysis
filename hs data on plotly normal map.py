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
        return ''

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
shapefile_path = "C:\\Users\\hp\\Desktop\\gurinder\\filtered shape files\\maharashtra all districts.shp"
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



     # Plot rainfall data points using latitude and longitude from the Excel data
    fig.add_trace(go.Scattermapbox(
        lat=daily_data['LAT'],
        lon=daily_data['LONG'],
        mode='markers',
        marker=dict(
            color=daily_data['color'],  # Color based on RF values
            size=10  # Marker size
        ),
        text=daily_data.apply(
        lambda row: (
            f"Station: {row['Station']}<br>"
            f"Rainfall: {'DATA NOT AVAILABLE' if pd.isna(row['RF']) else f'{row['RF']} mm'}"
        ), 
        axis=1
    ),
    hoverinfo='text',
    name="Rainfall Data Legend"  # Name this trace for the legend
    ))
    # Manually specify the color for each marker using the 'color' column
    fig.update_traces(marker=dict(color=daily_data['color'], size=8))  # Adjust size as needed

        # Add dummy traces for the legend with fixed colors
    legend_colors = {
        '<b>0mm <= RF <= 0.9mm</b>': '#71797E',
        '<b>1mm <= RF <= 2.4mm</b>': '#ADFF2F',
        '<b>2.5mm <= RF <= 15.5mm</b>': '#00FF00',
        '<b>15.6mm <= RF <= 64.4mm</b>': '#00FFFF',
        '<b>64.5mm <= RF <= 115.5mm</b>': '#FFFF00',
        '<b>115.6mm <= RF <= 204.4mm</b>': '#FFA500',
        '<b>RF > 204.4mm</b>': '#FF0000',
        '<b>Data Not Available</b>': '#000000',
        
    }


    # Add each color category as a dummy trace to the legend
    for label, color in legend_colors.items():
        fig.add_trace(go.Scattermapbox(
            lon=[None],  # No actual points for these dummy traces
            lat=[None],
            mode='markers',
            marker=dict(size=10, color=color),  # Use the specific color for each label
            showlegend=True,
            name=label
        ))

        # Center of the bounding box
    bounds = gdf.total_bounds
    center_lon = (bounds[0] + bounds[2]) / 2
    center_lat = (bounds[1] + bounds[3]) / 2

    # Set map layout
    fig.update_layout(
        mapbox=dict(
            style='white-bg',  # No external map background
            center=dict(lat=center_lat, lon=center_lon),
        zoom=5.8  # Adjust the zoom level as needed
        ),
        showlegend=True,
        margin={"r":0,"t":30,"l":0,"b":0},  # Adjusted top margin to make room for the title
        #height=700  # Set height for better view
        title={
        'text': "Custom Map of GeoDataFrame",
        'y':0.98,  # Adjust title position
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }   
    )

    # Save the plot as an HTML file, ensuring the date is formatted properly
    fig.write_html(f'C:\\Users\\hp\\Desktop\\PLOTS\\rainfall_plot_{pd.to_datetime(date).strftime("%Y_%m_%d")}.html')