import pandas as pd
import numpy as np
import os
from datetime import date,datetime
from datetime import timedelta
import os
import time

# Get today's date
t_day = date.today()
d1 = t_day.strftime("%Y-%m-%d")
d1_2 = t_day.strftime("%d-%m-%Y")
y_day=t_day-timedelta(days=1)
d0=y_day.strftime("%Y-%m-%d")
d0_2 = y_day.strftime("%d-%m-%Y")

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

df = pd.read_csv(f'http://www.ogimet.com/cgi-bin/getsynop?begin={year_str}{month_str}010300&end={year_str}{month_str}220300&state=Ind&lang=eng', header=None)

# Assign your custom column names
df.columns = ['WMO INDEX', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'REPORT']

# Filter rows where 'REPORT' does not start with 'BBXX' and 'date' equals '03'
df = df[~df['REPORT'].str.startswith('BBXX') & (df['date'] == 03)]



                        #choose columns to include in combine_tday_mh
df=df[['WMO INDEX','REPORT']]

print(df)
exit()

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


#print(df_full_combined)
#print(df_full_combined.info())

#df_full_combined.to_excel('C:\\Users\\hp\\Desktop\\test ogi final.xlsx', index=False)





























                     #generate list of aws and STATIONS
aws_mh=["MUMBAI_COLABA","MUMBAI_SANTA_CRUZ",'RATNAGIRI','MAHABALESHWAR','SATARA','SOLAPUR']
#Merge with all_mh to include all stations
aws_mh_df = pd.DataFrame({'STATIONS': aws_mh})



#Collect today's data (adjust your URLs accordingly)
today_03_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e={d1}&f={d1}&g=03&h=00')[0]
arg_today_03_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=ARG&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e={d1}&f={d1}&g=03&h=00')[0]

#Combine the dataframes
combine_tday_03_mh = pd.concat([today_03_mh, arg_today_03_mh], ignore_index=True)

                            #drop vidarbha stations
mah_drop_03_today = combine_tday_03_mh[(combine_tday_03_mh['DISTRICT'] == 'AKOLA') | (combine_tday_03_mh['DISTRICT'] == 'AMRAVATI')|
(combine_tday_03_mh['DISTRICT'] == 'BHANDARA') | (combine_tday_03_mh['DISTRICT'] == 'BULDHANA')|
(combine_tday_03_mh['DISTRICT'] == 'CHANDRAPUR') | (combine_tday_03_mh['DISTRICT'] == 'GADCHIROLI')|
(combine_tday_03_mh['DISTRICT'] == 'GONDIA') | (combine_tday_03_mh['DISTRICT'] == 'NAGPUR')|
(combine_tday_03_mh['DISTRICT'] == 'YAVATMAL') | (combine_tday_03_mh['DISTRICT'] == 'WARDHA')|
(combine_tday_03_mh['DISTRICT'] == 'WASHIM')].index
combine_tday_03_mh.drop(mah_drop_03_today, inplace=True)


                        #choose columns to include in combine_tday_mh
combine_tday_03_mh=combine_tday_03_mh[['STATION','RAIN FALL CUM. SINCE 0300 UTC (mm)','TEMP DAY MIN. (\'C)','MSLP (hPa / gpm)']]


                       #replace names
combine_tday_03_mh.columns =combine_tday_03_mh.columns.str.replace('STATION', 'STATIONS',regex=False)
combine_tday_03_mh.columns =combine_tday_03_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
combine_tday_03_mh.columns =combine_tday_03_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)



combined_all_03_stations = aws_mh_df.merge(combine_tday_03_mh, on='STATIONS', how='left')

#print(combined_all_03_stations)
























            #collect yesterdays aws tabular data
yesterday_mh=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+d0+'&f='+d0+'&g=12&h=00')
dfy_mh=yesterday_mh[0]
             #collect yesterdays arg tabular data
arg_yesterday_mh=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=ARG&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+d0+'&f='+d0+'&g=12&h=00')
arg_dfy_mh=arg_yesterday_mh[0]


                                #combine the two dataframes
combine_yday_mh=pd.concat([dfy_mh,arg_dfy_mh], ignore_index=True)



                                #drop vidarbha stations
mah_drop_yesterday = combine_yday_mh[(combine_yday_mh['DISTRICT'] == 'AKOLA') | (combine_yday_mh['DISTRICT'] == 'AMRAVATI')|
               (combine_yday_mh['DISTRICT'] == 'BHANDARA') | (combine_yday_mh['DISTRICT'] == 'BULDHANA')|
               (combine_yday_mh['DISTRICT'] == 'CHANDRAPUR') | (combine_yday_mh['DISTRICT'] == 'GADCHIROLI')|
               (combine_yday_mh['DISTRICT'] == 'GONDIA') | (combine_yday_mh['DISTRICT'] == 'NAGPUR')|
               (combine_yday_mh['DISTRICT'] == 'YAVATMAL') | (combine_yday_mh['DISTRICT'] == 'WARDHA')|
               (combine_yday_mh['DISTRICT'] == 'WASHIM')].index
combine_yday_mh.drop(mah_drop_yesterday, inplace=True)


                            #choose columns to include in combine_yday_mh
combine_yday_mh=combine_yday_mh[['STATION','TEMP DAY MAX. (\'C)']]


                           #replace names
combine_yday_mh.columns =combine_yday_mh.columns.str.replace('STATION', 'STATIONS',regex=False)
combine_yday_mh.columns =combine_yday_mh.columns.str.replace('TEMP DAY MAX. (\'C)', 'MAX T',regex=False)




combined_all_12_stations = aws_mh_df.merge(combine_yday_mh, on='STATIONS', how='left')

#print(combined_all_12_stations)


combine_final=combined_all_03_stations.merge(combined_all_12_stations, on='STATIONS', how='left')



























final_combined = df_full_combined.merge(combine_final, on='STATIONS', how='left')

final_combined=final_combined[['STATIONS','Observatory Rainfall (mm)','RF','Observatory Min Temp (°C)','MIN T','Observatory Max Temp (°C)','MAX T','Observatory Pressure (hPa)','MSLP (hPa / gpm)']]




print(final_combined)
print(final_combined.info())

final_combined.to_excel('C:\\Users\\hp\\Desktop\\comparison.xlsx', index=False)



exit()