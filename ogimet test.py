import pandas as pd
import numpy as np
import os
from datetime import date,datetime
from datetime import timedelta
import os
import time

# Get today's date
t_day = date.today()

# Separate year, month, and day as strings
year_str = t_day.strftime("%Y")  # Year as a string
month_str = t_day.strftime("%m")  # Month as a string
day_str = t_day.strftime("%d")    # Day as a string


                     #generate list of aws and STATIONS
all_index=[ 43057,
        43003,
        43110,
        43111,
        43113,
        43117]

#Merge with all_mh to include all stations
all_index_df = pd.DataFrame({'WMO INDEX': all_index})
all_index_df['WMO INDEX'] = all_index_df['WMO INDEX'].astype(np.int64)




# Reading the HTML table into a DataFrame
#df = pd.read_html(f'https://www.ogimet.com/cgi-bin/gsynres?lang=en&ord=DIR&ndays=1&ano={year_str}&mes={month_str}&day={day_str}&hora=03&state=India')[2]

#df = pd.read_html(f'https://www.ogimet.com/display_synops2.php?lang=en&lugar=43057&tipo=ALL&ord=REV&ano=2024&mes=08&day=19&hora=03&anof=2024&mesf=08&dayf=19&horaf=03')[2]

df = pd.read_csv(f'http://www.ogimet.com/cgi-bin/getsynop?begin={year_str}{month_str}{day_str}0300&end={year_str}{month_str}{day_str}0300&state=Ind&lang=eng', header=None)

# Assign your custom column names
df.columns = ['WMO INDEX', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'REPORT']

                        #choose columns to include in combine_tday_mh
df=df[['WMO INDEX','REPORT']]

df_combined = all_index_df.merge(df, on='WMO INDEX', how='left')

def map_sta_to_index_mh(row):
    station_to_index = {
        43057: 'MUMBAI_COLABA',
        43003: 'MUMBAI_SANTA_CRUZ',
        43110: 'RATNAGIRI',
        43111: 'MAHABALESHWAR',
        43113: 'SATARA',
        43117: 'SOLAPUR',
    }
    
    index = row['WMO INDEX']
    if index in station_to_index:
        return station_to_index[index]
    else:
        return ''


df_combined['STATIONS']=df_combined.apply(map_sta_to_index_mh, axis=1)

# Reorder columns as needed
df_combined = df_combined[['WMO INDEX','STATIONS', 'REPORT']]


# Adding a capture group to the regex pattern
pressure_pattern = r'\b(4[09]\d{3})\b'

# Extracting the pressure group from the REPORT column
df_combined['Pressure'] = df_combined['REPORT'].str.extract(pressure_pattern)

def convert_pressure(code):
    if pd.isna(code):
        return None  # Handle NaN values
    code = str(code)  # Convert to string if not already
    if code.startswith('40'):
        return 1000 + float(code[1:]) / 10
    elif code.startswith('49'):
        return 900 + float(code[1:]) / 10
    return None

# Apply the function to the 'Pressure' column
df_combined['Obs. Pressure (hPa)'] = df_combined['Pressure'].apply(convert_pressure)



# Define the regex pattern for minimum temperature
min_temp_pattern = r'\b333\s(20\d{3})\b'

# Extract the min temperature group from the REPORT column
df_combined['Min Temp Code'] = df_combined['REPORT'].str.extract(min_temp_pattern)

# Convert to actual temperature
def convert_min_temp(code):
    if pd.isna(code):
        return None  # Handle NaN values
    return float(code[2:]) / 10  # Convert the last three digits to temperature

# Apply the conversion function
df_combined['Obs. Min Temp (°C)'] = df_combined['Min Temp Code'].apply(convert_min_temp)


print(df_combined)
print(df_combined.info())

df_combined.to_excel('C:\\Users\\hp\\Desktop\\test ogi.xlsx', index=False)
exit()
# Extracting the 4th group for pressure
pressure_group = df[3].str.split().str[5]

print(pressure_group)
#print(df.info())
exit()




# Correct column selection based on the actual structure of the DataFrame
# Inspecting the columns first
#print(df.columns)



# Selecting the specific columns
selected_columns = df.loc[:, [('Station', 'Station'), 
                              ('Temperature (C)', 'Max'), 
                              ('Temperature (C)', 'Min'), 
                              ('Prec. (mm)', 'Prec. (mm)')
                              ]]

# Flattening the MultiIndex columns
selected_columns.columns = ['Station', 'Max', 'Min', 'RF']

                        #choose columns to include in combine_tday_mh
#selected_columns.columns =selected_columns.columns.str.replace('DATE(YYYY-MM-DD)', 'DATE',regex=False)

print(selected_columns)
print(selected_columns.info())

selected_columns.to_excel(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads\\ogimet may test.xlsx'),index=False)