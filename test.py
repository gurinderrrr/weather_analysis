import pandas as pd
import plotly.graph_objects as go

# Sample data for testing
data = {
    'LAT': [19.0, 19.1, 19.2, 19.3, 19.4, 19.5, 19.6],
    'LONG': [75.0, 75.1, 75.2, 75.3, 75.4, 75.5, 75.6],
    'RF': [10, 20, 30, 40, 50, 60, 70],
    'TYPE': ['AWS', 'ARG', 'AWS', 'ARG', 'OBSERVATORY', 'AWS', 'ARG']
}
df = pd.DataFrame(data)

# Define marker shapes for each type
shape_map = {
    'AWS': 'triangle-up',
    'ARG': 'triangle-down',
    'OBSERVATORY': 'circle'
}

# Define your map styles
map_styles = {
    'light': "carto-positron",
    'dark': "carto-darkmatter",
    'satellite': "open-street-map",
    'terrain': "stamen-terrain",
    'toner': "stamen-toner",
    'watercolor': "stamen-watercolor"
}

def create_map(style, file_name):
    fig = go.Figure()

    # Iterate over each type and create a trace with the corresponding shape
    for t, shape in shape_map.items():
        subset = df[df['TYPE'] == t]
        
        # Print debugging information
        print(f"Creating trace for type: {t}, shape: {shape}")
        print(f"Subset size: {len(subset)}")
        
        fig.add_trace(go.Scattermapbox(
            lat=subset['LAT'],
            lon=subset['LONG'],
            mode='markers',
            marker=dict(
                size=10,
                symbol=shape,  # Set the marker shape
                color=subset['RF'],  # Use the rainfall column for color
                colorscale='Viridis',  # Choose a color scale
                colorbar=dict(title='Rainfall (mm)')  # Add a colorbar with title
            ),
            text=subset['TYPE'],
            hovertemplate='<b>Type:</b> %{text}<br>Rainfall: %{marker.color:.2f} mm<br>Latitude: %{lat}<br>Longitude: %{lon}<extra></extra>',
            name=t
        ))

    fig.update_layout(
        mapbox=dict(
            style=style,
            zoom=5,  # Adjust zoom level as needed
            center={"lat": 19.7515, "lon": 75.7139}  # Centered on Maharashtra
        ),
        margin={"r":0,"t":0,"l":0,"b":0}  # Optional: remove extra margins
    )

    fig.write_html(file_name)  # Save the map to an HTML file

# Use a specific map style and save to HTML
selected_style = map_styles['satellite']  # Choose the style you want
output_file = f"C:\\Users\\HP\\Desktop\\{selected_style}.html"  # Define the output file name
create_map(selected_style, output_file)