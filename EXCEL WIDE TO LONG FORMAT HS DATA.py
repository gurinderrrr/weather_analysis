import pandas as pd

# Load the Excel file
df = pd.read_excel('C:\\Users\\hp\\Desktop\\AUGUST 2024 edited aa.xls')

# Assume the first column is station names, and the rest are rainfall values for 31 days
station_column = 'Station'
lat_column = 'LAT'
long_column = 'LONG'
rainfall_columns = df.columns[3:]  # Rainfall data starts from the 4th column

# Melt the dataframe to get each station's rainfall per date
df_melted = df.melt(id_vars=[station_column, lat_column, long_column], 
                    value_vars=rainfall_columns, 
                    var_name='Date', value_name='Rainfall')

# Add a datetime column if your original columns are named as 1, 2, 3, ... 31 for August
df_melted['Date'] = pd.to_datetime(df_melted['Date'], format='%d').map(lambda x: x.replace(month=8, year=2023))

# Rearrange columns: Station, Date, Rainfall, Lat, Long
df_melted = df_melted[[station_column, 'Date', 'Rainfall', lat_column, long_column]]

# Save df_melted as an Excel file
df_melted.to_excel('C:\\Users\\hp\\Desktop\\transformed_data.xlsx', index=False)  # Adjust file name/path as needed

# View the transformed DataFrame
#print(df_melted)

# Now, df_melted contains the desired column order: Station, Date, Rainfall, Lat, and Long
