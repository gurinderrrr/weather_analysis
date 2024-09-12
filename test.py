print('Importing required libraries.')
# import libraries
import pandas as pd
import numpy as np
from datetime import date,datetime
from datetime import timedelta
import os
import time
from win32com import client
import warnings
from collections import Counter
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Alignment
#warnings.filterwarnings("ignore")
import pdfkit
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import re


print('Creating required date and time')

#Create today's and yesterday's date
t_day = date.today()
d1 = t_day.strftime("%Y-%m-%d")
d1_2 = t_day.strftime("%d-%m-%Y")
d1_22 = t_day.strftime("%d-%m")
d1_year = t_day.strftime("%Y")
d1_month = t_day.strftime("%m-%Y")
#print(d1_22)

y_day=t_day-timedelta(days=1)
d0=y_day.strftime("%Y-%m-%d")
d0_2 = y_day.strftime("%d-%m-%Y")
d0_22 = y_day.strftime("%d-%m")
#print(d0_22)


# Get the path to the OneDrive
analysis_path = os.path.join(os.path.expanduser("~"), 'OneDrive')

# Define the path to the "daily data" folder
daily_data_path = os.path.join(analysis_path, "daily data")

# Check if the "daily data" folder exists and create it if not
if not os.path.exists(daily_data_path):
    os.makedirs(daily_data_path)





# Define the path to the "daily data" folder
daily_year_path = os.path.join(daily_data_path, d1_year)

# Check if the "daily data" folder exists and create it if not
if not os.path.exists(daily_year_path):
    os.makedirs(daily_year_path)





# Define the path to the "daily data" folder
daily_month_path = os.path.join(daily_year_path, d1_month)

# Check if the "daily data" folder exists and create it if not
if not os.path.exists(daily_month_path):
    os.makedirs(daily_month_path)










# Get today's date as a string in the format DD-MM-YYYY
today_date = d1_2

# Define the path to today's folder inside the "daily data" folder
today_folder_path = os.path.join(daily_month_path, today_date)

# Check if today's folder exists and create it if not
if not os.path.exists(today_folder_path):
    os.makedirs(today_folder_path)






#Set display options to show full DataFrame
#pd.set_option('display.max_rows', 1000000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)


print('Creating AWS/ARG station list for Maharashtra')

                     #generate list of aws and STATIONS
aws_mh=["MUMBAI_COLABA","MUMBAI_SANTA_CRUZ", "PALGHAR_AWS400","MATHERAN",
'PALGHAR_KVK','IIG_MO_ALIBAG','KARJAT','MURUD',
'DAPOLI','RATNAGIRI','DEVGAD',
'MULDE_AMFU','AHMEDNAGAR','KOPERGAON','RAHURI',
'DHULE','CHOPDA','JALGAON','NANDURBAR',
'NANDURBAR_KVK','NAVAPUR','KALWAN',
'MALEGAON','VILHOLI','NIMGIRI_JUNNAR','CAGMO_SHIVAJINAGAR',
'CHRIST_UNIVERSITY_LAVASA','CME_DAPODI','DPS_HADAPSAR_PUNE',
'INS_SHIVAJI_LONAVALA','KHUTBAV_DAUND','LONIKALBHOR_HAVELI',
'NARAYANGOAN_KRISHI_KENDRA','NIASM_BARAMATI','PASHAN_AWS_LAB',
'RAJGURUNAGAR','TALEGAON','KOLHAPUR_AMFU','MAHABALESHWAR',
'BGRL_KARAD','SATARA','MOHOL_KVK','SOLAPUR','AURANGABAD','AURANGABAD_KVK','RATNAGIRI_AWS400','SANGOLA_MAHAVIDYALAYA',
'AMBEJOGAI','HINGOLI','JALNA','LATUR','NANDED','OSMANABAD',
'TULGA_KVK','PARBHANI_AMFU','RADHANAGRI_ARS','SANGLI_KVK','SHAHADA_AWS400','BEED_PTO','UDGIR_AWS400','TONDAPUR_AWS400','SAGROLI_KVK']


# Entries to be removed
aws_mh_to_remove = {'MURUD','NANDURBAR'}

aws_mh = list(filter(lambda x: x not in aws_mh_to_remove, aws_mh))

#print(len(aws_mh))


arg_mh=['BANDRA','DAHISAR','JUHU_AIRPORT','MUMBAI AIRPORT',
'RAM_MANDIR','TATA POWER CHEMBUR','VIDYAVIHAR',
'VIKHROLI','BYCULLA_MUMBAI',
'MAHALAXMI','MATUNGA_MUMBAI','SION_MUMBAI',
'BHAYANDER','KOPARKHAIRANE','MIRA_ROAD',
'BHIRA','POLADPUR','IIGHQ_NEWPANVEL',
'SAVARDE(GOLWANE)','CHIPLUN',
'POWARWADI(BHAMBHED)','AWALEGAON',
'VAIBHAVWADI','VENGURLA','AKKALKUWA',
'TALODA','SHIRPUR','SHIRUR',
'CHALISGAON','JAMNER','NIPHAD','TRIMBAKESHWAR',
'VANI','BHANDARDARA','PARNER','SHEVGAON',
'SHRIGONDA','BALLALWADI_JUNNAR','BLINDSCHOOL_KP_PUNE',
'CHINCHWAD_PUNE','GIRIVAN','GUDHE_BHOR',
'KHADAKWADI_AMBEGAON','LAVALE','MAGARPATTA_PUNE',
'MALIN_AMBEGAON','MTI_PASHAN_PUNE','NDA_PUNE','NES_LAKADI_INDAPUR',
'PABAL_SHIRUR','RJSPMCOP_DUDULGAON',
'SHIVAJINAGAR_PUNE','TALEGAON_DHAMDHERE',
'VETALE_KHED','WADGAONSHERI_PUNE','WALHE_PURANDAR',
'PANCHGANI','PHALTAN','SHIRALA','TASGAON',
'UMADI','GARGOTI(BHUDARGAD)','PANHALA',
'SHAHUWADI','AKKALKOT','KARMALA',
'GANGAPUR','KANNAD','PAITHAN','BHOKARDAN',
'GHANSANGAVI','PARTUR',
'PARALIVAIJANATH','KALAMB',
'CHAKUR','NILANGA',
'PURNA','SONPETH','AUNDHA_NAGNATH',
'KALAMNURI','BHOKAR']


# Entries to be removed
arg_mh_to_remove = {'BHANDARDARA','PAITHAN',
'PARALIVAIJANATH','SHIRUR','SHIRPUR','AUNDHA_NAGNATH',
'KALAMNURI','GARGOTI(BHUDARGAD)','SHAHUWADI','CHAKUR','NILANGA','BHOKAR','TALODA','KALAMB','TULZAPUR','PURNA','SONPETH','UMADI','PANCHGANI','PHALTAN','AKKALKOT','KARMALA'}

arg_mh = list(filter(lambda x: x not in arg_mh_to_remove, arg_mh))

#print(len(arg_mh))


all_mh=['MUMBAI_COLABA','BYCULLA_MUMBAI','MAHALAXMI','MATUNGA_MUMBAI','SION_MUMBAI','MUMBAI_SANTA_CRUZ','TATA POWER CHEMBUR','BANDRA','MUMBAI AIRPORT','VIDYAVIHAR','JUHU_AIRPORT','VIKHROLI','RAM_MANDIR','DAHISAR','KOPARKHAIRANE',
'BHAYANDER','MIRA_ROAD','IIGHQ_NEWPANVEL','KARJAT','IIG_MO_ALIBAG','MATHERAN','BHIRA',
'MURUD','POLADPUR','INS_SHIVAJI_LONAVALA','TALEGAON','GIRIVAN','CHINCHWAD_PUNE','MTI_PASHAN_PUNE','CME_DAPODI','RJSPMCOP_DUDULGAON','LAVALE','SHIVAJINAGAR_PUNE','PASHAN_AWS_LAB','RAJGURUNAGAR','BLINDSCHOOL_KP_PUNE','NDA_PUNE','MAGARPATTA_PUNE','WADGAONSHERI_PUNE','VETALE_KHED','DPS_HADAPSAR_PUNE','LONIKALBHOR_HAVELI','PABAL_SHIRUR','BALLALWADI_JUNNAR','KHADAKWADI_AMBEGAON','NIMGIRI_JUNNAR','TALEGAON_DHAMDHERE','NARAYANGOAN_KRISHI_KENDRA','CHRIST_UNIVERSITY_LAVASA','CAGMO_SHIVAJINAGAR','KHUTBAV_DAUND','WALHE_PURANDAR','MALIN_AMBEGAON','GUDHE_BHOR','NIASM_BARAMATI','NES_LAKADI_INDAPUR','BHANDARDARA','PARNER','KOPERGAON','SHRIGONDA',
'AHMEDNAGAR','RAHURI','SHEVGAON','PALGHAR_AWS400','PALGHAR_KVK','VILHOLI','TRIMBAKESHWAR','NIPHAD','VANI','KALWAN','MALEGAON','DAPOLI','SAVARDE(GOLWANE)',
'POWARWADI(BHAMBHED)','CHIPLUN','RATNAGIRI','RATNAGIRI_AWS400','MAHABALESHWAR','PANCHGANI','SATARA','PHALTAN','BGRL_KARAD','MOHOL_KVK','KARMALA','SOLAPUR','SANGOLA_MAHAVIDYALAYA',
'AKKALKOT','KOLHAPUR_AMFU','SHAHUWADI','PANHALA','RADHANAGRI_ARS','GARGOTI(BHUDARGAD)','GANGAPUR','PAITHAN','AURANGABAD_KVK','AURANGABAD','KANNAD','CHALISGAON','CHOPDA','JALGAON','JAMNER','DHULE','SHIRPUR','SHIRALA','UMADI','TASGAON','SANGLI_KVK','AKKALKUWA','NAVAPUR','TALODA','NANDURBAR','NANDURBAR_KVK','SHAHADA_AWS400','JALNA','BHOKARDAN','GHANSANGAVI','PARTUR','VAIBHAVWADI','AWALEGAON','MULDE_AMFU','DEVGAD',
'VENGURLA','OSMANABAD','KALAMB','TULGA_KVK','AMBEJOGAI','BEED_PTO','PARALIVAIJANATH',
'SHIRUR','CHAKUR','LATUR','NILANGA','UDGIR_AWS400','AUNDHA_NAGNATH','HINGOLI','KALAMNURI','TONDAPUR_AWS400','PARBHANI_AMFU','SONPETH','PURNA','NANDED','SAGROLI_KVK','BHOKAR']


# Entries to be removed
all_mh_to_remove = {'MURUD','NANDURBAR','BHANDARDARA','PAITHAN',
'PARALIVAIJANATH','SHIRUR','SHIRPUR','AUNDHA_NAGNATH',
'KALAMNURI','GARGOTI(BHUDARGAD)','SHAHUWADI','CHAKUR','NILANGA','BHOKAR','TALODA','KALAMB','TULZAPUR','PURNA','SONPETH','UMADI','PANCHGANI','PHALTAN','AKKALKOT','KARMALA'}

all_mh = list(filter(lambda x: x not in all_mh_to_remove, all_mh))


#print(len(all_mh))

print('Checking if the AWS/ARG website is working...')

try:
    #Collect today's data (adjust your URLs accordingly)
    today_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e={d0}&f={d1}&g=ALL_HOUR&h=ALL_MINUTE')[0]
    arg_today_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=ARG&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e={d0}&f={d1}&g=ALL_HOUR&h=ALL_MINUTE')[0]

    print('Website working.')

except Exception as e:
    print(f"Error fetching data from Website: {e}")
    time.sleep(5)
    exit()


print('Filtering Data...')

#Combine the dataframes
combine_tday_mh = pd.concat([today_mh, arg_today_mh], ignore_index=True)


                            #drop vidarbha stations
mah_drop_today = combine_tday_mh[(combine_tday_mh['DISTRICT'] == 'AKOLA') | (combine_tday_mh['DISTRICT'] == 'AMRAVATI')|
(combine_tday_mh['DISTRICT'] == 'BHANDARA') | (combine_tday_mh['DISTRICT'] == 'BULDHANA')|
(combine_tday_mh['DISTRICT'] == 'CHANDRAPUR') | (combine_tday_mh['DISTRICT'] == 'GADCHIROLI')|
(combine_tday_mh['DISTRICT'] == 'GONDIA') | (combine_tday_mh['DISTRICT'] == 'NAGPUR')|
(combine_tday_mh['DISTRICT'] == 'YAVATMAL') | (combine_tday_mh['DISTRICT'] == 'WARDHA')|
(combine_tday_mh['DISTRICT'] == 'WASHIM')].index
combine_tday_mh.drop(mah_drop_today, inplace=True)


                        #choose columns to include in combine_tday_mh
combine_tday_mh=combine_tday_mh[['STATION','DATE(YYYY-MM-DD)','TIME (UTC)','RAIN FALL CUM. SINCE 0300 UTC (mm)','BATTERY (Volts)']]


                       #replace names
combine_tday_mh.columns =combine_tday_mh.columns.str.replace('DATE(YYYY-MM-DD)', 'DATE',regex=False)
combine_tday_mh.columns =combine_tday_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
combine_tday_mh.columns=combine_tday_mh.columns.str.replace('BATTERY (Volts)', 'BAT',regex=False)


combine_tday_mh['DATETIME'] = pd.to_datetime(combine_tday_mh['DATE'] + ' ' + combine_tday_mh['TIME (UTC)'])
combine_tday_mh = combine_tday_mh.drop(columns=['DATE', 'TIME (UTC)'])

#print(combine_tday_mh)

#Define the start date, end date, and frequency
start_datetime = d0 + ' 03:00:00'
end_datetime = d1 + ' 03:00:00'
frequency = '15min'

#Create a datetime range
datetime_range = pd.date_range(start=start_datetime, end=end_datetime, freq=frequency)

#Filter data for the required time range
combine_tday_mh = combine_tday_mh[(combine_tday_mh['DATETIME'] >= start_datetime) &
(combine_tday_mh['DATETIME'] <= end_datetime) ]
#print(combine_tday_mh)

#Merge with all_mh to include all stations
all_stations_df = pd.DataFrame({'STATION': all_mh})
combined_all_stations = all_stations_df.merge(combine_tday_mh, on='STATION', how='left')

#Convert DATETIME column to datetime type if not already
combined_all_stations['DATETIME'] = pd.to_datetime(combined_all_stations['DATETIME'])

#Group by 'STATION' and get the index of latest DATETIME for each station
latest_idx = combined_all_stations.loc[~combined_all_stations['DATETIME'].isna()].groupby('STATION')['DATETIME'].idxmax()

#Create the new DataFrame with the latest data per station
latest_data_per_station = combined_all_stations.loc[latest_idx]

latest_empty = combined_all_stations.loc[combined_all_stations['DATETIME'].isna()]

#Concatenate both DataFrames
combined_latest_data = pd.concat([latest_data_per_station, latest_empty])

#Create a DataFrame with all stations from all_mh
all_mh_df = pd.DataFrame({'STATION': all_mh})

#Merge to ensure all stations from all_mh are included, with NaN for missing stations
latest_data_per_station = all_mh_df.merge(combined_latest_data, on='STATION', how='left')

#Reset index if needed
latest_data_per_station = latest_data_per_station.reset_index(drop=True)

#print(latest_data_per_station)
#print(latest_data_per_station.info())


# Create the specific datetimes to identify
#datetime_d0 = pd.to_datetime(d0 + ' 03:00:00')
datetime_d1 = pd.to_datetime(d1 + ' 03:00:00')

# Identify and clear the specific datetimes
latest_data_per_station.loc[latest_data_per_station['DATETIME'].isin([ datetime_d1]), 'DATETIME'] = pd.NaT


#latest_data_per_station['DATETIME'] = latest_data_per_station['DATETIME'].dt.strftime('%d-%m-%Y %H:%MUTC')
#print(latest_data_per_station)
#print(latest_data_per_station.info())

#latest_data_per_station.to_excel(os.path.join(os.path.join(os.environ['USERPROFILE']),'Downloads\\MAHARASHTRA ('+d0_2+' to '+d1_2+')''.xlsx'))





















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
combine_tday_03_mh=combine_tday_03_mh[['STATION','TEMP DAY MIN. (\'C)','TEMP. (\'C)','WIND DIR 10 m (Deg)','WIND SPEED 10 m (Kt)','RH (%)','MSLP (hPa / gpm)','SLP (hPa)','GPS']]


                       #replace names
combine_tday_03_mh.columns =combine_tday_03_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)
combine_tday_03_mh.columns=combine_tday_03_mh.columns.str.replace('TEMP. (\'C)', 'TEMP',regex=False)
combine_tday_03_mh.columns=combine_tday_03_mh.columns.str.replace('WIND DIR 10 m (Deg)', 'WD',regex=False)
combine_tday_03_mh.columns=combine_tday_03_mh.columns.str.replace('WIND SPEED 10 m (Kt)', 'WS',regex=False)
combine_tday_03_mh.columns=combine_tday_03_mh.columns.str.replace('SLP (hPa)', 'SLP',regex=False)
combine_tday_03_mh.columns=combine_tday_03_mh.columns.str.replace('MSLP (hPa / gpm)', 'MSLP',regex=False)
combine_tday_03_mh.columns=combine_tday_03_mh.columns.str.replace('MSLP (hPa / gpm)', 'MSLP',regex=False)



combined_all_03_stations = all_stations_df.merge(combine_tday_03_mh, on='STATION', how='left')

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
combine_yday_mh.columns =combine_yday_mh.columns.str.replace('TEMP DAY MAX. (\'C)', 'MAX T',regex=False)




combined_all_12_stations = all_stations_df.merge(combine_yday_mh, on='STATION', how='left')

#print(combined_all_12_stations)


combine_rf_mint=latest_data_per_station.merge(combined_all_03_stations, on='STATION', how='left')

combine_rf_mint_maxt=combine_rf_mint.merge(combined_all_12_stations, on='STATION', how='left')



#df.to_excel(os.path.join(os.path.join(os.environ['USERPROFILE']),'Downloads\\MAHARASHTRA ('+d0_2+' to '+d1_2+')''.xlsx'))

                        #set index
dfy_index_mh=combine_rf_mint_maxt.set_index("STATION")

df=dfy_index_mh.copy()
del dfy_index_mh
#print(df)

df['STATIONS']=df.index

# Reset index to drop the current index
df.reset_index(inplace=True)


df.insert(0, 'S.No.', range(1, 1 + len(df)))


def map_dis_to_sta_mh(row):
    station_to_district = {
        'MUMBAI_COLABA': 'MUMBAI_CITY',
        'MUMBAI_SANTA_CRUZ': 'MUMBAI_CITY',
        'PALGHAR_KVK': 'PALGHAR',
        'PALGHAR': 'PALGHAR',
        'PALGHAR_AWS400': 'PALGHAR',
        'IIG_MO_ALIBAG': 'RAIGAD',
        'KARJAT': 'RAIGAD',
        'MURUD': 'RAIGAD',
        'MATHERAN': 'RAIGAD',
        'DAPOLI': 'RATNAGIRI',
        'RATNAGIRI': 'RATNAGIRI',
        'RATNAGIRI_AWS400': 'RATNAGIRI',
        'SANGLI_KVK': 'SANGLI',
        'DEVGAD': 'SINDHUDURG',
        'MULDE_AMFU': 'SINDHUDURG',
        'NANDURBAR': 'NANDURBAR',
        'NANDURBAR_KVK': 'NANDURBAR',
        'NAVAPUR': 'NANDURBAR',
        'SHAHADA_AWS400': 'NANDURBAR',
        'DHULE': 'DHULE',
        'CHOPDA': 'JALGAON',
        'JALGAON': 'JALGAON',
        'KALWAN': 'NASHIK',
        'MALEGAON': 'NASHIK',
        'VILHOLI': 'NASHIK',
        'AHMEDNAGAR': 'AHMEDNAGAR',
        'KOPERGAON': 'AHMEDNAGAR',
        'RAHURI': 'AHMEDNAGAR',
        'NIMGIRI_JUNNAR': 'PUNE',
        'CAGMO_SHIVAJINAGAR': 'PUNE',
        'CHRIST_UNIVERSITY_LAVASA': 'PUNE',
        'CME_DAPODI': 'PUNE',
        'DPS_HADAPSAR_PUNE': 'PUNE',
        'INS_SHIVAJI_LONAVALA': 'PUNE',
        'KHUTBAV_DAUND': 'PUNE',
        'LONIKALBHOR_HAVELI': 'PUNE',
        'NARAYANGOAN_KRISHI_KENDRA': 'PUNE',
        'NIASM_BARAMATI': 'PUNE',
        'PASHAN_AWS_LAB': 'PUNE',
        'RAJGURUNAGAR': 'PUNE',
        'TALEGAON': 'PUNE',
        'BGRL_KARAD': 'SATARA',
        'MAHABALESHWAR': 'SATARA',
        'SATARA': 'SATARA',
        'KOLHAPUR_AMFU': 'KOLHAPUR',
        'RADHANAGRI_ARS': 'KOLHAPUR',
        'MOHOL_KVK': 'SOLAPUR',
        'SOLAPUR': 'SOLAPUR',
        'SANGOLA_MAHAVIDYALAYA': 'SOLAPUR',
        'AURANGABAD_KVK': 'AURANGABAD',
        'AURANGABAD': 'AURANGABAD',
        'AMBEJOGAI': 'BEED',
        'BEED_PTO': 'BEED',
        'OSMANABAD': 'OSMANABAD',
        'TULGA_KVK': 'OSMANABAD',
        'LATUR': 'LATUR',
        'UDGIR_AWS400': 'LATUR',
        'PARBHANI_AMFU': 'PARBHANI',
        'HINGOLI': 'HINGOLI',
        'TONDAPUR_AWS400': 'HINGOLI',
        'JALNA': 'JALNA',
        'NANDED': 'NANDED',
        'SAGROLI_KVK': 'NANDED',
        'BYCULLA_MUMBAI': 'MUMBAI_CITY',
        'MAHALAXMI': 'MUMBAI_CITY',
        'MATUNGA_MUMBAI': 'MUMBAI_CITY',
        'SION_MUMBAI': 'MUMBAI_CITY',
        'BANDRA': 'MUMBAI_SUBURBAN',
        'DAHISAR': 'MUMBAI_SUBURBAN',
        'MUMBAI AIRPORT': 'MUMBAI_SUBURBAN',
        'JUHU_AIRPORT': 'MUMBAI_SUBURBAN',
        'RAM_MANDIR': 'MUMBAI_SUBURBAN',
        'TATA POWER CHEMBUR': 'MUMBAI_SUBURBAN',
        'VIDYAVIHAR': 'MUMBAI_SUBURBAN',
        'VIKHROLI': 'MUMBAI_SUBURBAN',
        'BHAYANDER': 'THANE',
        'KOPARKHAIRANE': 'THANE',
        'MIRA_ROAD': 'THANE',
        'IIGHQ_NEWPANVEL': 'RAIGAD',
        'BHIRA': 'RAIGAD',
        'POLADPUR': 'RAIGAD',
        'CHIPLUN': 'RATNAGIRI',
        'POWARWADI(BHAMBHED)': 'RATNAGIRI',
        'SAVARDE(GOLWANE)': 'RATNAGIRI',
        'AWALEGAON': 'SINDHUDURG',
        'VAIBHAVWADI': 'SINDHUDURG',
        'VENGURLA': 'SINDHUDURG',
        'AKKALKUWA': 'NANDURBAR',
        'TALODA': 'NANDURBAR',
        'SHIRPUR': 'DHULE',
        'CHALISGAON': 'JALGAON',
        'JAMNER': 'JALGAON',
        'NIPHAD': 'NASHIK',
        'TRIMBAKESHWAR': 'NASHIK',
        'VANI': 'NASHIK',
        'BHANDARDARA': 'AHMEDNAGAR',
        'PARNER': 'AHMEDNAGAR',
        'SHEVGAON': 'AHMEDNAGAR',
        'SHRIGONDA': 'AHMEDNAGAR',
        'BALLALWADI_JUNNAR': 'PUNE',
        'BLINDSCHOOL_KP_PUNE': 'PUNE',
        'CHINCHWAD_PUNE': 'PUNE',
        'GIRIVAN': 'PUNE',
        'GUDHE_BHOR': 'PUNE',
        'KHADAKWADI_AMBEGAON': 'PUNE',
        'MTI_PASHAN_PUNE': 'PUNE',
        'LAVALE': 'PUNE',
        'MAGARPATTA_PUNE': 'PUNE',
        'MALIN_AMBEGAON': 'PUNE',
        'NDA_PUNE': 'PUNE',
        'NES_LAKADI_INDAPUR': 'PUNE',
        'PABAL_SHIRUR': 'PUNE',
        'RJSPMCOP_DUDULGAON': 'PUNE',
        'SHIVAJINAGAR_PUNE': 'PUNE',
        'TALEGAON_DHAMDHERE': 'PUNE',
        'VETALE_KHED': 'PUNE',
        'WADGAONSHERI_PUNE': 'PUNE',
        'WALHE_PURANDAR': 'PUNE',
        'PANCHGANI': 'SATARA',
        'PHALTAN': 'SATARA',
        'SHIRALA': 'SANGLI',
        'TASGAON': 'SANGLI',
        'UMADI': 'SANGLI',
        'GARGOTI(BHUDARGAD)': 'KOLHAPUR',
        'PANHALA': 'KOLHAPUR',
        'SHAHUWADI': 'KOLHAPUR',
        'AKKALKOT': 'SOLAPUR',
        'KARMALA': 'SOLAPUR',
        'GANGAPUR': 'AURANGABAD',
        'KANNAD': 'AURANGABAD',
        'PAITHAN': 'AURANGABAD',
        'BHOKARDAN': 'JALNA',
        'GHANSANGAVI': 'JALNA',
        'PARTUR': 'JALNA',
        'PARALIVAIJANATH': 'BEED',
        'SHIRUR': 'BEED',
        'KALAMB': 'OSMANABAD',
        'CHAKUR': 'LATUR',
        'NILANGA': 'LATUR',
        'PURNA': 'PARBHANI',
        'SONPETH': 'PARBHANI',
        'AUNDHA_NAGNATH': 'HINGOLI',
        'KALAMNURI': 'HINGOLI',
        'BHOKAR': 'NANDED'
    }
    
    station = row['STATIONS']
    if station in station_to_district:
        return station_to_district[station]
    else:
        return ''



# Function to check if the station is in aws list
def check_aws(station):
    if station in aws_mh:
        return 'AWS'
    elif station in arg_mh:
        return 'ARG'

# Apply the function to create the new column
df['TYPE'] = df['STATIONS'].apply(check_aws)


   



df['DISTRICT']=df.apply(map_dis_to_sta_mh, axis=1)










df['RF'] = df['RF'].astype(np.float64)
df['MIN T'] = df['MIN T'].astype(np.float64)
df['MAX T'] = df['MAX T'].astype(np.float64)
df['BAT'] = df['BAT'].astype(np.float64)











#print(len(df[(df['AWS/ARG'] == 'ARG') & (df['null'] == 3)]))









df['DATETIME'] = df['DATETIME'].dt.strftime('(%H:%M)')








# Create a new column 'RF_with_datetime'
df['RF_with_datetime'] = df.apply(lambda row: f"{row['RF']}\n{row['DATETIME']}" if not pd.isna(row['DATETIME']) else row['RF'], axis=1)


#df=df.drop('null', axis=1)
df=df.drop('RF', axis=1)
#df=df.drop('DATETIME', axis=1)

df.columns =df.columns.str.replace('RF_with_datetime', 'RF',regex=False)


#print(df)
#exit()





# Create a new column 'RF_with_datetime'
df['bat_with_datetime'] = df.apply(lambda row: f"{row['BAT']}\n{row['DATETIME']}" if not pd.isna(row['DATETIME']) else row['BAT'], axis=1)


#df=df.drop('null', axis=1)
df=df.drop('BAT', axis=1)
#df=df.drop('DATETIME', axis=1)

df.columns =df.columns.str.replace('bat_with_datetime', 'BAT',regex=False)


#print(df['STATIONS'],df['RF'],df['BAT'])

#exit()







# Create a new column 'RF_with_datetime'
df['station_with_district'] = df.apply(
    lambda row: f"{row['STATIONS']} ({row['DISTRICT']})" if not pd.isna(row['DISTRICT']) else row['STATIONS'],
    axis=1
)


#df=df.drop('null', axis=1)
df=df.drop('STATIONS', axis=1)
df=df.drop('DISTRICT', axis=1)

df.columns =df.columns.str.replace('station_with_district', 'STATIONS',regex=False)







df['null']=df.isna().sum(axis=1)

df_tot=len(aws_mh)
df_rep=len(aws_mh)-len(df[(df['TYPE'] == 'AWS') & (df['null'] == 3)])
arg_df_tot=len(arg_mh)
arg_df_rep=len(arg_mh)-len(df[(df['TYPE'] == 'ARG') & (df['null'] == 3)])


df=df.drop('null', axis=1)

# Reorder columns as needed
df = df[['S.No.','STATIONS','TYPE','RF', 'MIN T', 'MAX T', 'TEMP', 'WD','WS','RH (%)','SLP','MSLP', 'BAT', 'GPS']]
# Convert rainfall column to numeric, forcing errors to NaN
#df['RF'] = pd.to_numeric(df['RF'], errors='coerce')

#print(df.info())
#exit()




df_pg_hd_mh=pd.DataFrame(['STATE: MAHARASHTRA ('+d0_2+' 3UTC to '+d1_2+' 3UTC)'])


df_rf_leg_mh=pd.DataFrame({'':['Not Reported','1mm <= RF <= 2.4mm/\nLowest Temp','2.5mm <= RF <= 15.5mm','15.6mm <= RF <= 64.4mm','64.5mm <= RF <= 115.5mm','115.6mm <= RF <= 204.4mm','RF > 204.4/\nHighest Temp','Error Values']})
df_rf_leg_col_mh=pd.DataFrame({'':['','Lowest Temp','','','','','Highest Temp','Error Value']})
awsarg_df_sum_data_mh= pd.DataFrame([["Total AWS/AGRO stations working"],['Total AWS/AGRO stations reporting'],['Total ARG stations working'],['Total ARG stations reporting']])
awsarg_df_sum_val_mh= pd.DataFrame([[df_tot],[df_rep],[arg_df_tot],[arg_df_rep]])


#print(df['STATIONS'],df['RF'],df['BAT'])

#exit()



# Define your styling functions
#def highlight_max(s):
    #is_max = s == s.max()
    #return ['background-color: red; font-weight: bold' if v else '' for v in is_max]

#def highlight_min(s):
    #is_min = s == s.min()
    #return ['background-color: #98FB98; font-weight: bold' if v else '' for v in is_min]

def neg_val(val):
    try:
        # Attempt to convert the value to a numeric type
        numeric_val = float(val)
    except ValueError:
        # If conversion fails, treat the value as non-numeric
        return ''
    
    # Apply the styling only if the value is numeric and less than 0
    if numeric_val < 0:
        return 'border: 2px solid red; border-radius: 50%; padding: 2px; display: inline-block;'
    else:
        return ''

def color_range(val):
    try:
        # Extract the numeric value from the string, or use the value directly if it's numeric
        if isinstance(val, str):
            # Attempt to split the string and convert the first part to a float
            rf_value = float(val.split('\n')[0])
        else:
            # Use the value directly if it's already a numeric type
            rf_value = float(val)
    except (ValueError, IndexError):
        # If conversion fails or splitting does not work, handle it gracefully
        return ''
    
    # Apply styling based on the value range
    if pd.isna(rf_value):  # Handle NaN values
        return ''
    elif rf_value % 0.5 != 0:  # if not a multiple of 0.5
        return 'border: 2px solid red; border-radius: 50%; padding: 2px; display: inline-block;'
    #elif 1 <= rf_value <= 2.4:  # lr
       # return 'background-color: #ADFF2F; font-weight: bold'
    #elif 2.5 <= rf_value <= 15.5:  # mr
       # return 'background-color: #00FF00; font-weight: bold'
   # elif 15.6 <= rf_value <= 64.4:  # hr
   #     return 'background-color: #00FFFF; font-weight: bold'
    #elif 64.5 <= rf_value <= 115.5:  # vhr
    #    return 'background-color: #FFFF00; font-weight: bold'
   # elif 115.6 <= rf_value <= 204.4:  # vhr
    #    return 'background-color: #FFA500; font-weight: bold'
   # elif rf_value > 204.4:  # ehr
    #    return 'background-color: #FF0000; font-weight: bold'
    else:
        return ''
    
def bat_val(val):
    try:
        # Extract the numeric value from the string, or use the value directly if it's numeric
        if isinstance(val, str):
            # Attempt to split the string and convert the first part to a float
            bat_value = float(val.split('\n')[0])
        else:
            # Use the value directly if it's already a numeric type
            bat_value = float(val)
    except (ValueError, IndexError):
        # If conversion fails or splitting does not work, handle it gracefully
        return ''
    
    # Apply styling based on the value range
    if pd.isna(bat_value):  # Handle NaN values
        return ''
    
    # Apply styling if the value is less than 11
    elif bat_value < 11:
        return 'border: 2px solid red; border-radius: 50%; padding: 2px; display: inline-block;'
    else:
        return ''
    
def gps_val(val):
    if val =="U":
        return 'border: 2px solid red; border-radius: 50%; padding: 2px; display: inline-block;'
    else:
        return ''



#df['RF'] = pd.to_numeric(df['RF'], errors='coerce')
df['TEMP'] = pd.to_numeric(df['TEMP'], errors='coerce')
df['MIN T'] = pd.to_numeric(df['MIN T'], errors='coerce')
df['MAX T'] = pd.to_numeric(df['MAX T'], errors='coerce')
df['WD'] = pd.to_numeric(df['WD'], errors='coerce')
df['WS'] = pd.to_numeric(df['WS'], errors='coerce')
df['RH (%)'] = pd.to_numeric(df['RH (%)'], errors='coerce')
df['SLP'] = pd.to_numeric(df['SLP'], errors='coerce')
df['MSLP'] = pd.to_numeric(df['MSLP'], errors='coerce')
#df['BAT'] = pd.to_numeric(df['BAT'], errors='coerce')

# Function to restructure DataFrame
#def restructure_stations(df):
    #restructured_data = []
    #for district, group in df.groupby('DISTRICT'):
    #    restructured_data.append([f"<b>{district}</b>"])  # Add district in bold
     #   restructured_data.extend(group[['STATIONS']].values.tolist())  # Add stations
   # 
   # return pd.DataFrame(restructured_data, columns=['STATIONS'])

#df_restructured = restructure_stations(df)

#def style_stations(df):
# Apply CSS to ensure word wrapping in the HTML output
# Define the styling function for DataFrame 1 (df)
styled_df = df.style\
    .set_properties(**{'font-family': "Calibri", 'font-size': '12pt', 'border': '1pt solid',
                       'text-align': "center", 'white-space': 'pre-wrap', 'word-wrap': 'break-word'})\
    .set_table_styles([{'selector': 'th', 'props': [('border', '1pt solid black')]}])\
    .map(neg_val, subset=['MIN T', 'MAX T'])\
    .map(color_range, subset=['RF'])\
    .map(bat_val, subset=['BAT'])\
    .map(gps_val, subset=['GPS'])\
    .map(lambda x: 'font-weight: bold;' if '<b>' in str(x) else '')\
    .hide(axis='index')  # Hide the index

# Save styled df to HTML
html_file = 'styled_table.html'
styled_df.format(precision=1, na_rep="").to_html(html_file, index=False, escape=False)





















# Define the styling function for DataFrame 2 (df_pg_hd_mh)
head_styled_df = df_pg_hd_mh.style\
    .set_properties(**{'font-family': "Calibri", 'font-weight': 'bold', 'font-size': '16pt',
                       'text-align': "center", 'white-space': 'pre-wrap', 'word-wrap': 'break-word'})\
    .hide(axis='index')  # Hide the index

# Save the second styled df to another HTML file
head_html_file = 'head_styled_table.html'
head_styled_df.to_html(head_html_file, index=False, escape=False)

# Read both HTML files
with open(html_file, 'r') as f1:
    styled_table_html = f1.read()

with open(head_html_file, 'r') as f2:
    head_styled_table_html = f2.read()

# Combine the HTML strings with custom formatting
combined_html = f'''
<html>
<body>
    {head_styled_table_html}
    {styled_table_html}
</body>
</html>
'''

# Save the combined HTML content to a file
combined_html_file = 'combined_table.html'
with open(combined_html_file, 'w') as f:
    f.write(combined_html)

# Convert the combined HTML file to a PDF
pdf_file = 'styled_rainfall_with_borders.pdf'
options = {
    'margin-top': '1mm',
    'margin-bottom': '1mm',
    'margin-left': '5mm',
    'margin-right': '5mm',
    'page-size': 'A4',
}

# Convert combined HTML to PDF
pdfkit.from_file(combined_html_file, pdf_file, options=options)

exit()























































































































# Style DataFrame
def style_dataframe(df):
    styled_df = df.style\
        .set_properties(**{'font-family': "Calibri", 'font-size': '12pt', 'border': '1pt solid', 'text-align': "center", 'white-space': 'pre-wrap', 'word-wrap': 'break-word'})\
        .set_table_styles([{'selector': 'th', 'props': [('border', '1pt solid black')]}])\
        .map(neg_val, subset=['MIN T', 'MAX T'])\
        .map(color_range, subset=['RF'])\
        .map(bat_val, subset=['BAT'])\
        .map(gps_val, subset=['GPS'])\
        .format(precision=1, na_rep="")  # Handle precision and NaN values
    return styled_df

# Convert DataFrame to HTML with precision and NaN handling for non-styled DataFrame
def df_to_html(df, text_align='center'):
    # Handle precision and NaN for non-styled DataFrames
    if isinstance(df, pd.DataFrame):
        df = df.fillna('')  # Replace NaN with empty string
        return df.to_html(header=False, index=False)\
                 .replace('<table', f'<table style="text-align: {text_align}"')
    else:
        return df.to_html()

# Example DataFrames
df_pg_hd_mh = pd.DataFrame(['STATE: MAHARASHTRA (DATE)'])  # Example header DataFrame

# Styled DataFrame
styled_df = style_dataframe(df)



{df_to_html(df_pg_hd_mh, text_align='center')} 

{styled_df.to_html()}   



# Save the combined HTML to a file
html_file = 'combined_tables_maharashtra.html'
# Manually add additional CSS for header styling
html_content = ''
with open(html_file, 'r') as file:
    html_content = file.read()

html_content = html_content.replace(
    "<style type=\"text/css\">",
    "<style type=\"text/css\"> th { font-size: 12pt; }"
)

# Save updated HTML
with open(html_file, 'w') as file:
    file.write(html_content)
# Convert HTML file to PDF
pdf_file = 'styled_rainfall_with_borders.pdf'

# Define options for the PDF including margin settings
options = {
    'margin-top': '1mm',
    'margin-bottom': '1mm',
    'margin-left': '5mm',
    'margin-right': '5mm',
    'page-size': 'A3',
}

# Convert HTML file to PDF using pdfkit
pdfkit.from_file(html_file, pdf_file, options=options)



exit()

