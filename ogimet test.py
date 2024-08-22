import pandas as pd
import numpy as np
import os
from datetime import date,datetime
from datetime import timedelta
import os
import time

# Get today's date
t_day = date.today()
y_day=t_day-timedelta(days=1)

# Separate year, month, and day as strings
year_str = t_day.strftime("%Y")  # Year as a string
month_str = t_day.strftime("%m")  # Month as a string
day_str = t_day.strftime("%d")    # Day as a string
# Separate year, month, and day as strings
ytday_year_str = y_day.strftime("%Y")  # Year as a string
ytday_month_str = y_day.strftime("%m")  # Month as a string
ytday_day_str = y_day.strftime("%d")    # Day as a string

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
df_combined['Observatory Pressure (hPa)'] = df_combined['Pressure'].apply(convert_pressure)



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
df_combined['Observatory Min Temp (°C)'] = df_combined['Min Temp Code'].apply(convert_min_temp)



# Define the regex pattern for rainfall (matches either the code or nothing)
rainfall_pattern = r'\b555(?:\s(0\d{4}))?\b'

# Extract the rainfall group from the REPORT column
df_combined['Rainfall Code'] = df_combined['REPORT'].str.extract(rainfall_pattern)

# Convert to actual rainfall, or default to 0.0 mm if missing
def convert_rainfall(code):
    if pd.isna(code):
        return 0.0  # Default to 0.0 mm if the rainfall code is missing
    return float(code) / 10  # Convert the code to rainfall in mm

# Apply the conversion function
df_combined['Observatory Rainfall (mm)'] = df_combined['Rainfall Code'].apply(convert_rainfall)


df_combined=df_combined[['STATIONS','Observatory Rainfall (mm)','Observatory Min Temp (°C)','Observatory Pressure (hPa)']]


#print(df_combined)
#print(df_combined.info())

#df_combined.to_excel('C:\\Users\\hp\\Desktop\\test ogi.xlsx', index=False)















dfy = pd.read_csv(f'http://www.ogimet.com/cgi-bin/getsynop?begin={ytday_year_str}{ytday_month_str}{ytday_day_str}1200&end={ytday_year_str}{ytday_month_str}{ytday_day_str}1200&state=Ind&lang=eng', header=None)

# Assign your custom column names
dfy.columns = ['WMO INDEX', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'REPORT']

                        #choose columns to include in combine_tday_mh
dfy=dfy[['WMO INDEX','REPORT']]


dfy_combined = all_index_df.merge(dfy, on='WMO INDEX', how='left')


def dfy_map_sta_to_index_mh(row):
    dfy_station_to_index = {
        43057: 'MUMBAI_COLABA',
        43003: 'MUMBAI_SANTA_CRUZ',
        43110: 'RATNAGIRI',
        43111: 'MAHABALESHWAR',
        43113: 'SATARA',
        43117: 'SOLAPUR',
    }
    
    dfy_index = row['WMO INDEX']
    if dfy_index in dfy_station_to_index:
        return dfy_station_to_index[dfy_index]
    else:
        return ''


dfy_combined['STATIONS']=dfy_combined.apply(dfy_map_sta_to_index_mh, axis=1)




# Reorder columns as needed
dfy_combined = dfy_combined[['WMO INDEX','STATIONS', 'REPORT']]




# Define the regex pattern for minimum temperature
max_temp_pattern = r'\b333\s(10\d{3})\b'

# Extract the min temperature group from the REPORT column
dfy_combined['Max Temp Code'] = dfy_combined['REPORT'].str.extract(max_temp_pattern)

# Convert to actual temperature
def convert_max_temp(code):
    if pd.isna(code):
        return None  # Handle NaN values
    return float(code[2:]) / 10  # Convert the last three digits to temperature

# Apply the conversion function
dfy_combined['Observatory Max Temp (°C)'] = dfy_combined['Max Temp Code'].apply(convert_max_temp)


dfy_combined=dfy_combined[['STATIONS','Observatory Max Temp (°C)']]


df_full_combined = df_combined.merge(dfy_combined, on='STATIONS', how='left')

df_full_combined=df_full_combined[['STATIONS','Observatory Rainfall (mm)','Observatory Min Temp (°C)','Observatory Max Temp (°C)','Observatory Pressure (hPa)']]


print(df_full_combined)
print(df_full_combined.info())

df_full_combined.to_excel('C:\\Users\\hp\\Desktop\\test ogi final.xlsx', index=False)








exit()