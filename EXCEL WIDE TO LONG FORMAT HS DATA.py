import pandas as pd

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

# Display the first few rows of the transformed data
#df_melted.head()