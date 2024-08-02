import pandas as pd
import plotly.express as px
import numpy as np
import plotly.io as pio

# Define the color range function
def color_range(rf_value):
    if pd.isna(rf_value):  # Handle NaN values
        return 'black'
    elif rf_value % 0.5 != 0:  # if not multiple of 0.5
        return 'pink'
    elif rf_value == 0:  # if 0
        return 'silver'
    elif 0 < rf_value <= 2.5:  # vlr
        return '#98FB98'
    elif 2.6 <= rf_value <= 15.5:  # lr
        return '#7FFF00'
    elif 15.6 <= rf_value <= 64.5:  # mr
        return '#228B22'
    elif 64.6 <= rf_value <= 115.5:  # hr
        return '#FFFF00'
    elif 115.6 <= rf_value <= 204.5:  # vhr
        return '#FF8C00'
    elif rf_value > 204.5:  # ehr
        return '#FF0000'
    else:
        return 'blue'

# Define the columns
columns = ['STATION', 'TYPE', 'LAT', 'LONG', 'RF']

# Define data for the columns
stations = ['Station' + str(i) for i in range(1, 11)]
types = np.random.choice(['AWS', 'ARG', 'OBSERVATORY'], 10)
lats = np.random.uniform(16.0, 22.0, 10)  # Latitude range for Maharashtra
longs = np.random.uniform(72.0, 80.0, 10)  # Longitude range for Maharashtra

# Define specific rainfall values
rainfall = [10.3, 20.5, np.nan, 5.0, 15.5, np.nan, 30.0, 0.6, 25.0, 40.0]  # 6 multiples of 0.5, 2 non-multiples of 0.5, and 2 NaN values

# Create the dataframe
df = pd.DataFrame({
    'STATION': stations,
    'TYPE': types,
    'LAT': lats,
    'LONG': longs,
    'RF': rainfall
})

# Apply the color range function to create a new color column
df['COLOR'] = df['RF'].apply(color_range)

# Replace NaN values with a fixed size for the size column
df['SIZE'] = df['RF'].fillna(10)  # Set a fixed size for NaN values

# Create the plot
fig = px.scatter_mapbox(
    df,
    lat='LAT',
    lon='LONG',
    size='SIZE',
    hover_name='STATION',
    hover_data={'TYPE': True, 'RF': True, 'LAT': False, 'LONG': False, 'COLOR': False, 'SIZE': False},
    size_max=15,
    zoom=4,
    title='Rainfall Data for Stations in Maharashtra'
)

# Update marker colors
fig.update_traces(marker=dict(color=df['COLOR'], showscale=False))

# Update layout for map style
fig.update_layout(
    mapbox_style='open-street-map',
    margin={'r':0,'t':0,'l':0,'b':0}
)

# Save the plot as an HTML file
pio.write_html(fig, file='rainfall_data_map.html', auto_open=True)