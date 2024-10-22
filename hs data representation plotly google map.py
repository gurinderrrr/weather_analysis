import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go  # Import Plotly's graph objects


# Step 1: Define the color_range function
def color_range(rf_value):
    if pd.isna(rf_value):  # Handle NaN values
        return '#FFFFFF'
    elif 0 <= rf_value <= 0.9:  # Low rainfall
        return '#000000' 
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
        return '#000000'

# Load the Excel file
file_path = 'C:\\Users\\hp\\Desktop\\AUGUST 2024 edited aa.xls'  # Path to the file
df = pd.read_excel(file_path)





# Filter out rows with invalid lat/long (e.g., 0.00 or 9999 or nan)
df_filtered = df[
    ((df['LAT'] != 0) & (df['LONG'] != 0)) &
    ((df['LAT'] != 9999) & (df['LONG'] != 9999)) &
    (pd.notna(df['LAT']) & pd.notna(df['LONG']))
    
]
df=df_filtered.copy()
del df_filtered

df['LAT_FILTERED']=df['LAT']/100
df['LONG_FILTERED']=df['LONG']/100

del df['LAT']
del df['LONG']


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

df_rf_filtered = df_melted[(pd.notna(df_melted['RF']))]

df_melted=df_rf_filtered.copy()
del df_rf_filtered



# Ensure lat and long are numeric
df_melted['LAT'] = pd.to_numeric(df_melted['LAT'], errors='coerce')
df_melted['LONG'] = pd.to_numeric(df_melted['LONG'], errors='coerce')
df_melted['RF'] = pd.to_numeric(df_melted['RF'], errors='coerce')



# Save the transformed data to an Excel file
output_file = 'C:\\Users\\hp\\Desktop\\august_2024_rainfall_long_format.xlsx'
df_melted.to_excel(output_file, index=False)

# Step 3: Create a new column in DataFrame for colors based on RF values
df_melted['color'] = df_melted['RF'].apply(color_range)


# Step 4: Create a dictionary to map RF value ranges to labels for legends
rf_legend_labels = {
    '#000000': '0-0.9 mm',
    '#ADFF2F': '1-2.4 mm',
    '#00FF00': '2.5-15.5 mm',
    '#00FFFF': '15.6-64.4 mm',
    '#FFFF00': '64.5-115.5 mm',
    '#FFA500': '115.6-204.4 mm',
    '#FF0000': '>204.4 mm'
}

# Step 1: Read the Excel file
excel_file_path = 'C:\\Users\\hp\\Desktop\\august_2024_rainfall_long_format.xlsx'
df = pd.read_excel(excel_file_path)

# Step 2: Read the shapefile
shapefile_path = "C:\\Users\\hp\\Desktop\\gurinder\\filtered shape files\\maharashtra all districts.shp"
gdf = gpd.read_file(shapefile_path)


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
        mapbox_style='carto-positron',
        center={'lat': gdf.geometry.centroid.y.mean(), 'lon': gdf.geometry.centroid.x.mean()},
        zoom=5,  # Adjust the zoom level
        opacity=1
    )

    # Manually specify the color for each marker using the 'color' column
    fig.update_traces(marker=dict(color=daily_data['color'], size=8))  # Adjust size as needed

    # Add a custom legend for rainfall values using the rf_legend_labels dictionary
    for color_code, label in rf_legend_labels.items():
        # Add dummy scatter points for legend entries
        fig.add_trace(go.Scattermapbox(
            lat=[None], lon=[None],  # Dummy data to only show the legend
            mode='markers',
            marker=go.scattermapbox.Marker(size=20, color=color_code),
            showlegend=True,
            name=label  # Legend label
        ))

    # Save the plot as an HTML file, ensuring the date is formatted properly
    fig.write_html(f'C:\\Users\\hp\\Desktop\\PLOTS\\rainfall_plot_{pd.to_datetime(date).strftime("%Y_%m_%d")}.html')