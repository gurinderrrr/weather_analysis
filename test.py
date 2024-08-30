import pandas as pd
import numpy as np
import os
from datetime import date,datetime
from datetime import timedelta
import os
import time
import itertools

# Get today's date
t_day = date.today()
d1 = t_day.strftime("%Y-%m-%d")
d1_2 = t_day.strftime("%d-%m-%Y")
y_day=t_day-timedelta(days=7)
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

print(day_str,ytday_day_str)















                #generate list of aws and STATIONS
aws_mh=["MUMBAI_COLABA","MUMBAI_SANTA_CRUZ",'RATNAGIRI','MAHABALESHWAR','SATARA','SOLAPUR']
#Merge with all_mh to include all stations
aws_mh_df = pd.DataFrame({'STATIONS': aws_mh})



#Collect today's data (adjust your URLs accordingly)
today_03_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e={d0}&f={d1}&g=ALL_HOUR&h=ALL_MINUTE')[0]



                            #drop vidarbha stations
mah_drop_03_today = today_03_mh[(today_03_mh['DISTRICT'] == 'AKOLA') | (today_03_mh['DISTRICT'] == 'AMRAVATI')|
(today_03_mh['DISTRICT'] == 'BHANDARA') | (today_03_mh['DISTRICT'] == 'BULDHANA')|
(today_03_mh['DISTRICT'] == 'CHANDRAPUR') | (today_03_mh['DISTRICT'] == 'GADCHIROLI')|
(today_03_mh['DISTRICT'] == 'GONDIA') | (today_03_mh['DISTRICT'] == 'NAGPUR')|
(today_03_mh['DISTRICT'] == 'YAVATMAL') | (today_03_mh['DISTRICT'] == 'WARDHA')|
(today_03_mh['DISTRICT'] == 'WASHIM')].index
today_03_mh.drop(mah_drop_03_today, inplace=True)


                        #choose columns to include in combine_tday_mh
today_03_mh=today_03_mh[['STATION','DATE(YYYY-MM-DD)','TIME (UTC)','RAIN FALL CUM. SINCE 0300 UTC (mm)','TEMP. (\'C)','TEMP DAY MIN. (\'C)','TEMP DAY MAX. (\'C)','MSLP (hPa / gpm)']]


                       #replace names
today_03_mh.columns =today_03_mh.columns.str.replace('STATION', 'STATIONS',regex=False)
today_03_mh.columns=today_03_mh.columns.str.replace('DATE(YYYY-MM-DD)', 'DATE',regex=False)
today_03_mh.columns =today_03_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
today_03_mh.columns =today_03_mh.columns.str.replace('TEMP. (\'C)', 'TEMP',regex=False)
today_03_mh.columns =today_03_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)
today_03_mh.columns =today_03_mh.columns.str.replace('TEMP DAY MAX. (\'C)', 'MAX T',regex=False)
today_03_mh.columns =today_03_mh.columns.str.replace('MSLP (hPa / gpm)', 'MSLP',regex=False)

#print(today_03_mh)
#exit()

# Filter rows where 'REPORT' does not start with 'BBXX' and 'date' equals '03'
today_03_mh = today_03_mh[(today_03_mh['TIME (UTC)'] == '00:00:00')|(today_03_mh['TIME (UTC)'] == '03:00:00')|(today_03_mh['TIME (UTC)'] == '06:00:00')|(today_03_mh['TIME (UTC)'] == '09:00:00')|(today_03_mh['TIME (UTC)'] == '12:00:00')|(today_03_mh['TIME (UTC)'] == '15:00:00')|(today_03_mh['TIME (UTC)'] == '18:00:00')]



combined_all_03_stations = aws_mh_df.merge(today_03_mh, on='STATIONS', how='left')

#print(combined_all_03_stations)
#exit()



combined_all_03_stations['DATE'] = pd.to_datetime(combined_all_03_stations['DATE'],format='%Y-%m-%d')
combined_all_03_stations['DATE'] = combined_all_03_stations['DATE'].dt.strftime('%d-%m-%Y')

combined_all_03_stations['TIME (UTC)'] = pd.to_datetime(combined_all_03_stations['TIME (UTC)'],format='%H:%M:%S')
combined_all_03_stations['TIME (UTC)'] = combined_all_03_stations['TIME (UTC)'].dt.strftime('%H:%M')

#print(df)




# Combine DATE and TIME (UTC) columns into DATETIME (UTC) 
combined_all_03_stations['DATETIME (UTC)'] = combined_all_03_stations['DATE']+" "+ combined_all_03_stations['TIME (UTC)']



combined_all_03_stations = combined_all_03_stations.drop(columns=['DATE','TIME (UTC)'])

#print(df)
#print('unique stations in df: ',df['STATIONS'].nunique())
#print('unique datetime in df: ',df['DATETIME (UTC)'].nunique())





#print(df)


#print('unique stations in df: ',df['STATION'].nunique())
#print('unique datetime in df: ',df['DATETIME (UTC)'].nunique())






#Define the start date, end date, and frequency
start_datetime = d0 + ' 00:00'
end_datetime = d1 + ' 00:00'
frequency = '3H'

#Create a datetime range
datetime_range = pd.date_range(start=start_datetime, end=end_datetime, freq=frequency).strftime('%d-%m-%Y %H:%M')



# Reverse the order
#datetime_range = datetime_range[::-1]

#print(datetime_range)







# Create a DataFrame with the datetime range
datetime_df = pd.DataFrame(datetime_range, columns=['DATETIME (UTC)'])


print(datetime_df)
print('rows in datetime_df: ',len(datetime_df))


# Extract unique values
stations = combined_all_03_stations['STATIONS'].unique()
datetimes = datetime_df['DATETIME (UTC)'].unique()

# Create a DataFrame with all combinations of 'station' and 'datetime'
all_combinations = pd.DataFrame(list(itertools.product(stations, datetimes)), columns=['STATIONS', 'DATETIME (UTC)'])

# Merge with the original df to include all stations and all datetimes
complete_combined = pd.merge(all_combinations, combined_all_03_stations, on=['STATIONS', 'DATETIME (UTC)'], how='left')


















combined_all_03_stations.to_excel('C:\\Users\\hp\\Desktop\\test rimc ogi.xlsx', index=False)

exit()

final_combined = df_full_combined.merge(combine_final, on='STATIONS', how='left')

final_combined=final_combined[['STATIONS','Observatory Rainfall (mm)','RF','Observatory Min Temp (°C)','MIN T','Observatory Max Temp (°C)','MAX T','Observatory Pressure (hPa)','MSLP (hPa / gpm)']]




print(final_combined)
print(final_combined.info())

final_combined.to_excel('C:\\Users\\hp\\Desktop\\comparison.xlsx', index=False)






















print(final_combined)
print(final_combined.info())

final_combined.to_excel('C:\\Users\\hp\\Desktop\\comparison.xlsx', index=False)



exit()






















                     #generate list of aws and STATIONS
aws_mh=["MUMBAI_COLABA","MUMBAI_SANTA_CRUZ",'RATNAGIRI','MAHABALESHWAR','SATARA','SOLAPUR']
#Merge with all_mh to include all stations
aws_mh_df = pd.DataFrame({'STATIONS': aws_mh})



#Collect today's data (adjust your URLs accordingly)
today_03_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e={d0}&f={d1}&g=ALL_HOUR&h=00')[0]



                            #drop vidarbha stations
mah_drop_03_today = today_03_mh[(today_03_mh['DISTRICT'] == 'AKOLA') | (today_03_mh['DISTRICT'] == 'AMRAVATI')|
(today_03_mh['DISTRICT'] == 'BHANDARA') | (today_03_mh['DISTRICT'] == 'BULDHANA')|
(today_03_mh['DISTRICT'] == 'CHANDRAPUR') | (today_03_mh['DISTRICT'] == 'GADCHIROLI')|
(today_03_mh['DISTRICT'] == 'GONDIA') | (today_03_mh['DISTRICT'] == 'NAGPUR')|
(today_03_mh['DISTRICT'] == 'YAVATMAL') | (today_03_mh['DISTRICT'] == 'WARDHA')|
(today_03_mh['DISTRICT'] == 'WASHIM')].index
today_03_mh.drop(mah_drop_03_today, inplace=True)


                        #choose columns to include in combine_tday_mh
today_03_mh=today_03_mh[['STATION','RAIN FALL CUM. SINCE 0300 UTC (mm)','TEMP DAY MIN. (\'C)','MSLP (hPa / gpm)']]


                       #replace names
today_03_mh.columns =today_03_mh.columns.str.replace('STATION', 'STATIONS',regex=False)
today_03_mh.columns =today_03_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
today_03_mh.columns =today_03_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)



combined_all_03_stations = aws_mh_df.merge(today_03_mh, on='STATIONS', how='left')

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




























exit()