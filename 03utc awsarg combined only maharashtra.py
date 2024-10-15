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
combine_tday_mh=combine_tday_mh[['STATION','DATE(YYYY-MM-DD)','TIME (UTC)','RAIN FALL CUM. SINCE 0300 UTC (mm)']]


                       #replace names
combine_tday_mh.columns =combine_tday_mh.columns.str.replace('DATE(YYYY-MM-DD)', 'DATE',regex=False)
combine_tday_mh.columns =combine_tday_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)


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
combine_tday_03_mh=combine_tday_03_mh[['STATION','TEMP DAY MIN. (\'C)']]


                       #replace names
combine_tday_03_mh.columns =combine_tday_03_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)



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
df['AWS/ARG'] = df['STATIONS'].apply(check_aws)


   



df['DISTRICT']=df.apply(map_dis_to_sta_mh, axis=1)










df['RF'] = df['RF'].astype(np.float64)
df['MIN T'] = df['MIN T'].astype(np.float64)
df['MAX T'] = df['MAX T'].astype(np.float64)











#print(len(df[(df['AWS/ARG'] == 'ARG') & (df['null'] == 3)]))









df['DATETIME'] = df['DATETIME'].dt.strftime('(Upto'+'\n'+'%d-%m-%Y'+'\n'+'%H:%M UTC)')

# Create a new column 'RF_with_datetime'
df['RF_with_datetime'] = df.apply(lambda row: f"{row['RF']}\n{row['DATETIME']}" if not pd.isna(row['DATETIME']) else row['RF'], axis=1)


#df=df.drop('null', axis=1)
df=df.drop('RF', axis=1)
df=df.drop('DATETIME', axis=1)

df.columns =df.columns.str.replace('RF_with_datetime', 'RF',regex=False)



df['null']=df.isna().sum(axis=1)

df_tot=len(aws_mh)
df_rep=len(aws_mh)-len(df[(df['AWS/ARG'] == 'AWS') & (df['null'] == 3)])
arg_df_tot=len(arg_mh)
arg_df_rep=len(arg_mh)-len(df[(df['AWS/ARG'] == 'ARG') & (df['null'] == 3)])



df_pg_hd_mh=pd.DataFrame(['STATE: MAHARASHTRA ('+d0_2+' 3UTC to '+d1_2+' 3UTC)'])
df_rf_leg_head_mh=pd.DataFrame({'':['LEGENDS']})
df_rf_leg_mh=pd.DataFrame({'':['Not Reported','1mm <= RF <= 2.4mm/\nLowest Temp','2.5mm <= RF <= 15.5mm','15.6mm <= RF <= 64.4mm','64.5mm <= RF <= 115.5mm','115.6mm <= RF <= 204.4mm','RF > 204.4/\nHighest Temp','Error Values']})
df_rf_leg_col_mh=pd.DataFrame({'':['','Lowest Temp','','','','','Highest Temp','Error Value']})
awsarg_df_sum_data_mh= pd.DataFrame([["Total AWS/AGRO stations working"],['Total AWS/AGRO stations reporting'],['Total ARG stations working'],['Total ARG stations reporting']])
awsarg_df_sum_val_mh= pd.DataFrame([[df_tot],[df_rep],[arg_df_tot],[arg_df_rep]])

df=df.drop('null', axis=1)


# Reorder columns as needed
df = df[['S.No.','DISTRICT','STATIONS','AWS/ARG','RF','MIN T','MAX T']]


print('Filtering data done.')

print('Applying colors...')

def highlight_single_cells(x):
    df_rf_leg_col = x.copy()
    df_rf_leg_col.loc[:,:] = ''
    #set particular cells colors
    df_rf_leg_col.iloc[0,0] = 'background-color: white'
    df_rf_leg_col.iloc[1,0] = 'background-color: #ADFF2F;color: black;font-weight:bold'
    df_rf_leg_col.iloc[2,0] = 'background-color: #00FF00'
    df_rf_leg_col.iloc[3,0] = 'background-color: #00FFFF'
    df_rf_leg_col.iloc[4,0] = 'background-color: #FFFF00'
    df_rf_leg_col.iloc[5,0] = 'background-color: #FFA500'
    df_rf_leg_col.iloc[6,0] = 'background-color: #FF0000;color: black;font-weight:bold'
    df_rf_leg_col.iloc[7,0] = 'background-color: black;color: white;font-weight:bold'
    return df_rf_leg_col

#print(len(new_dft_mh.index))

l=12+len(awsarg_df_sum_data_mh)+1

#print('l= :',l)

#exit()






# Define your styling functions
def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: red; font-weight: bold' if v else '' for v in is_max]

def highlight_min(s):
    is_min = s == s.min()
    return ['background-color: #98FB98; font-weight: bold' if v else '' for v in is_min]

def neg_val(val):
    if val < 0:
        return 'background-color: black; color: white; font-weight: bold'
    else:
        return ''

def color_range(val):
    if isinstance(val, str):
        rf_value = float(val.split('\n')[0])  # Extract RF value from RF_with_datetime
    else:
        rf_value = val  # Directly use the value if it's not a string (e.g., float or NaN)

    if pd.isna(rf_value):  # Handle NaN values
        return ''
    elif rf_value % 0.5 != 0:  # if not multiple of 0.5
        return 'background-color: black; color: white; font-weight: bold'
    elif 1 <= rf_value <= 2.4:  # lr
        return 'background-color: #ADFF2F; font-weight: bold'
    elif 2.5 <= rf_value <= 15.5:  # mr
        return 'background-color: #00FF00; font-weight: bold'
    elif 15.6 <= rf_value <= 64.4:  # hr
        return 'background-color: #00FFFF; font-weight: bold'
    elif 64.5 <= rf_value <= 115.5:  # vhr
        return 'background-color: #FFFF00; font-weight: bold'
    elif 115.6 <= rf_value <= 204.4:  # vhr
        return 'background-color: #FFA500; font-weight: bold'
    elif rf_value > 204.4:  # ehr
        return 'background-color: #FF0000; font-weight: bold'
    else:
        return ''
    



# Replace empty strings with NaN in the DataFrame
df.replace('', np.nan, inplace=True)


#print(df)
#print(df.info())



# Apply styles to the DataFrame
styled_df = df.style\
        .set_properties(**{'font-family': "Calibri", 'font-size': '12pt', 'border': '1pt solid',
                           'text-align': "center", 'white-space': 'pre-wrap', 'word-wrap': 'break-word'})\
        .set_table_styles([{
        'selector': 'th',
        'props': [('border', '1pt solid')]}])\
        .apply(highlight_max, subset=['MAX T'])\
        .apply(highlight_min, subset=['MIN T'])\
        .map(neg_val, subset=['MIN T', 'MAX T'])\
        .map(color_range, subset=['RF'])\
        .hide(axis='index')  # Hide the index


print('Creating Excel File...')

# Define Excel export path
excel_path = os.path.join(today_folder_path,'MAHARASHTRA ('+d0_2+' 3UTC to '+d1_2+' 3UTC).xlsx')

# Export to Excel with styling
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    
    styled_df.to_excel(writer, sheet_name="MAHARASHTRA",startrow=l, startcol=0, index=False)

    workbook = writer.book
    worksheet = writer.sheets["MAHARASHTRA"]


    merge_format = workbook.add_format({'bold':True,'font_name':'Calibri',"align": "center","valign": "vcenter"})
    worksheet.merge_range("B1:I1", "", merge_format)
    worksheet.merge_range("B3:C3", "", merge_format)
    border_format = workbook.add_format({'border':1,})
    worksheet.conditional_format('B3:C3', {'type': 'no_blanks','format': border_format})
    worksheet.conditional_format('B3:C3', {'type': 'blanks','format': border_format})
   

    df_pg_hd_mh.style.set_properties(**{'font-family':"Arial Rounded MT Bold",'font-size':'18pt','font-weight':'bold', 'text-align':"left"})\
                  .to_excel(writer,sheet_name="MAHARASHTRA",header=False,index=False,startrow=0, startcol=1, engine='xlsxwriter')
    df_rf_leg_head_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'14pt','font-weight':'bold', 'text-align':"center"})\
                   .to_excel(writer,sheet_name="MAHARASHTRA",index=False,header=False,startrow=2, startcol=1, engine='xlsxwriter')
    df_rf_leg_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt','font-weight':'bold', 'text-align':"center",'border':'1pt solid'})\
                   .to_excel(writer,sheet_name="MAHARASHTRA",index=False,header=False,startrow=3, startcol=1, engine='xlsxwriter')
    df_rf_leg_col_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt','font-weight':'bold', 'text-align':"center",'border':'1pt solid'})\
                    .apply(highlight_single_cells, axis=None)\
                   .to_excel(writer,sheet_name="MAHARASHTRA",index=False,header=False,startrow=3, startcol=2, engine='xlsxwriter')
   
    awsarg_df_sum_data_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt','font-weight':'bold', 'align':"center",'border':'1pt solid'})\
                     .to_excel(writer,sheet_name="MAHARASHTRA",header=False,index=False,startrow=12, startcol=1, engine='xlsxwriter')
    awsarg_df_sum_val_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt', 'text-align':"center",'font-weight':'bold', 'border':'1pt solid'})\
                    .to_excel(writer,sheet_name="MAHARASHTRA",header=False,index=False,startrow=12, startcol=2, engine='xlsxwriter')



    #worksheet.freeze_panes(1, 0)  # Freeze the header row

    # Set column widths
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 32)
    worksheet.set_column('D:D', 9)
    worksheet.set_column('E:E', 12)
    worksheet.set_column('F:F', 7)
    worksheet.set_column('G:G', 7)

    # Define a format with text wrapping
    wrap_format = workbook.add_format({'text_wrap': True})
    
    # Apply the wrap format to the entire column (assuming the last column RF_with_datetime)
    worksheet.set_column('E:E', 12, wrap_format)


print('Excel file created for Maharashtra')

print('Creating pdf file for office copy...')





# Import Module
from win32com import client
 
# Open Microsoft Excel
excel = client.Dispatch("Excel.Application")
 
# Read Excel File
sheets = excel.Workbooks.Open(os.path.join(today_folder_path,'MAHARASHTRA ('+d0_2+' 3UTC to '+d1_2+' 3UTC).xlsx'))
ws = sheets.Worksheets[0]

sheets.Worksheets[0].PageSetup.Zoom = 85
sheets.Worksheets[0].PageSetup.FitToPagesTall = False
sheets.Worksheets[0].PageSetup.FitToPagesWide = False
#sheets.Worksheets[0].PageSetup.PrintArea = 'A1:M60'
sheets.Worksheets[0].PageSetup.LeftMargin = 15
sheets.Worksheets[0].PageSetup.RightMargin = 5
sheets.Worksheets[0].PageSetup.TopMargin = 5
sheets.Worksheets[0].PageSetup.BottomMargin = 5

 
# Convert into PDF File
ws.ExportAsFixedFormat(0, (os.path.join(today_folder_path,'MAHARASHTRA ('+d0_2+' 3UTC to '+d1_2+' 3UTC).pdf')))

sheets.Close(True)
excel.Quit()
del excel


print('pdf file created for Maharashtra.')




print('Creating pdf file for office copy...')



# Define Excel export path
excel_path = os.path.join(today_folder_path,'MAHARASHTRA ('+d0_2+' 3UTC to '+d1_2+' 3UTC).xlsx')

# Export to Excel with styling
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    
    styled_df.to_excel(writer, sheet_name="MAHARASHTRA",startrow=l, startcol=0, index=False)

    workbook = writer.book
    worksheet = writer.sheets["MAHARASHTRA"]


    merge_format = workbook.add_format({'bold':True,'font_name':'Calibri',"align": "center","valign": "vcenter"})
    worksheet.merge_range("B1:I1", "", merge_format)
    worksheet.merge_range("B3:C3", "", merge_format)
    border_format = workbook.add_format({'border':1,})
    worksheet.conditional_format('B3:C3', {'type': 'no_blanks','format': border_format})
    worksheet.conditional_format('B3:C3', {'type': 'blanks','format': border_format})
   

    df_pg_hd_mh.style.set_properties(**{'font-family':"Arial Rounded MT Bold",'font-size':'18pt','font-weight':'bold', 'text-align':"left"})\
                  .to_excel(writer,sheet_name="MAHARASHTRA",header=False,index=False,startrow=0, startcol=1, engine='xlsxwriter')
    df_rf_leg_head_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'14pt','font-weight':'bold', 'text-align':"center"})\
                   .to_excel(writer,sheet_name="MAHARASHTRA",index=False,header=False,startrow=2, startcol=1, engine='xlsxwriter')
    df_rf_leg_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt','font-weight':'bold', 'text-align':"center",'border':'1pt solid'})\
                   .to_excel(writer,sheet_name="MAHARASHTRA",index=False,header=False,startrow=3, startcol=1, engine='xlsxwriter')
    df_rf_leg_col_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt','font-weight':'bold', 'text-align':"center",'border':'1pt solid'})\
                    .apply(highlight_single_cells, axis=None)\
                   .to_excel(writer,sheet_name="MAHARASHTRA",index=False,header=False,startrow=3, startcol=2, engine='xlsxwriter')
   
    awsarg_df_sum_data_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'9pt','font-weight':'bold', 'align':"center",'border':'1pt solid'})\
                     .to_excel(writer,sheet_name="MAHARASHTRA",header=False,index=False,startrow=12, startcol=1, engine='xlsxwriter')
    awsarg_df_sum_val_mh.style.set_properties(**{'font-family':"Calibri",'font-size':'9pt', 'text-align':"center",'font-weight':'bold', 'border':'1pt solid'})\
                    .to_excel(writer,sheet_name="MAHARASHTRA",header=False,index=False,startrow=12, startcol=2, engine='xlsxwriter')



    #worksheet.freeze_panes(1, 0)  # Freeze the header row

    # Set column widths
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 32)
    worksheet.set_column('D:D', 9)
    worksheet.set_column('E:E', 12)
    worksheet.set_column('F:F', 7)
    worksheet.set_column('G:G', 7)

    # Define a format with text wrapping
    wrap_format = workbook.add_format({'text_wrap': True})
    
    # Apply the wrap format to the entire column (assuming the last column RF_with_datetime)
    worksheet.set_column('E:E', 12, wrap_format)


# Import Module
from win32com import client

# Open Microsoft Excel
excel = client.Dispatch("Excel.Application")

# Read Excel File
sheets = excel.Workbooks.Open(os.path.join(today_folder_path,'MAHARASHTRA ('+d0_2+' 3UTC to '+d1_2+' 3UTC).xlsx'))
ws = sheets.Worksheets[0]

sheets.Worksheets[0].PageSetup.Zoom = 80
sheets.Worksheets[0].PageSetup.FitToPagesTall = False
sheets.Worksheets[0].PageSetup.FitToPagesWide = False
#sheets.Worksheets[0].PageSetup.PrintArea = 'A1:M60'
sheets.Worksheets[0].PageSetup.LeftMargin = 60
sheets.Worksheets[0].PageSetup.RightMargin = 5
sheets.Worksheets[0].PageSetup.TopMargin = 5
sheets.Worksheets[0].PageSetup.BottomMargin = 5

 
# Convert into PDF File
ws.ExportAsFixedFormat(0, (os.path.join(today_folder_path,'MAHARASHTRA ('+d0_2+' 3UTC to '+d1_2+' 3UTC) office copy.pdf')))

sheets.Close(True)
excel.Quit()
del excel

#os.remove(os.path.join(today_folder_path,'MAHARASHTRA ('+d0_2+' 3UTC to '+d1_2+' 3UTC).xlsx'))






print('Office copy of pdf file created for Maharashtra.')
print('\n')
print('Required files have been generated in the DAILY DATA folder under OneDrive folder of your PC.')
time.sleep(15)
exit()