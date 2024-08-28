print('Importing required libraries.')
# import libraries
import pandas as pd
import numpy as np
import geopandas as gpd
import pandas.io.formats.style
import csv
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
import itertools
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation, FFMpegWriter
import shapely


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
    today_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e=2024-07-01&f=2024-07-31&g=03&h=00')[0]
    arg_today_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=ARG&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e=2024-07-01&f=2024-07-31&g=03&h=00')[0]

    print('Website working.')

except Exception as e:
    print(f"Error fetching data from Website: {e}")
    time.sleep(5)
    exit()


print('Filtering Data...')

#Combine the dataframes
combine_tday_mh = pd.concat([today_mh, arg_today_mh], ignore_index=True)

#print(combine_tday_mh['STATION'].nunique())


                            #drop vidarbha stations
mah_drop_today = combine_tday_mh[(combine_tday_mh['DISTRICT'] == 'AKOLA') | (combine_tday_mh['DISTRICT'] == 'AMRAVATI')|
(combine_tday_mh['DISTRICT'] == 'BHANDARA') | (combine_tday_mh['DISTRICT'] == 'BULDHANA')|
(combine_tday_mh['DISTRICT'] == 'CHANDRAPUR') | (combine_tday_mh['DISTRICT'] == 'GADCHIROLI')|
(combine_tday_mh['DISTRICT'] == 'GONDIA') | (combine_tday_mh['DISTRICT'] == 'NAGPUR')|
(combine_tday_mh['DISTRICT'] == 'YAVATMAL') | (combine_tday_mh['DISTRICT'] == 'WARDHA')|
(combine_tday_mh['DISTRICT'] == 'WASHIM')].index
combine_tday_mh.drop(mah_drop_today, inplace=True)

#print(combine_tday_mh['STATION'].nunique())


                        #choose columns to include in combine_tday_mh
combine_tday_mh=combine_tday_mh[['STATION','DATE(YYYY-MM-DD)','RAIN FALL CUM. SINCE 0300 UTC (mm)']]


                       #replace names
combine_tday_mh.columns =combine_tday_mh.columns.str.replace('DATE(YYYY-MM-DD)', 'DATE',regex=False)
combine_tday_mh.columns =combine_tday_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)


#Merge with all_mh to include all stations
all_stations_df = pd.DataFrame({'STATION': all_mh})
combined_all_stations = all_stations_df.merge(combine_tday_mh, on='STATION', how='left')

#print(combined_all_stations['STATION'].nunique())





#Define the start date, end date, and frequency
start_date = '2024-07-01'
end_date = '2024-07-31'
frequency = '1D'

#Create a datetime range
datetime_range = pd.date_range(start=start_date, end=end_date, freq=frequency).strftime('%Y-%m-%d')

# Reverse the order
#datetime_range = datetime_range[::-1]

#print(datetime_range)







# Create a DataFrame with the datetime range
datetime_df = pd.DataFrame(datetime_range, columns=['DATE'])

#print(datetime_df)
#print('rows in datetime_df: ',len(datetime_df))


# Extract unique values
stations = all_stations_df['STATION'].unique()
datetimes = datetime_df['DATE'].unique()

# Create a DataFrame with all combinations of 'station' and 'datetime'
all_combinations = pd.DataFrame(list(itertools.product(stations, datetimes)), columns=['STATION', 'DATE'])

# Merge with the original df to include all stations and all datetimes
complete_combined = pd.merge(all_combinations, combined_all_stations, on=['STATION', 'DATE'], how='left')

df_sorted = complete_combined.sort_values(by=['DATE', 'STATION'])
df_sorted = df_sorted.reset_index(drop=True)



#print(complete_combined['STATION'].nunique())
#print(complete_combined['DATE'].nunique())
#print(len(complete_combined))


#print(len(df_sorted))


#df_sorted.to_excel('C:\\Users\\hp\\Desktop\\july test.xlsx', index=False)





























def map_lat(row):
    station_to_lat = {
'MUMBAI_COLABA':'18.897928',
'BYCULLA_MUMBAI':'18.983444',
'MAHALAXMI':'18.9799',
'MATUNGA_MUMBAI':'19.03203',
'SION_MUMBAI':'19.051943',
'MUMBAI_SANTA_CRUZ':'19.10064',
'TATA POWER CHEMBUR':'19.004494',
'BANDRA':'19.067',
'MUMBAI AIRPORT':'19.0931',
'VIDYAVIHAR':'19.07832',
'JUHU_AIRPORT':'19.098',
'VIKHROLI':'19.1096',
'RAM_MANDIR':'19.153217',
'DAHISAR':'19.249428',
'KOPARKHAIRANE':'19.009178',
'BHAYANDER':'19.314659',
'MIRA_ROAD':'19.279903',
'IIGHQ_NEWPANVEL':'19.014029',
'KARJAT':'18.91583',
'IIG_MO_ALIBAG':'18.64453',
'MATHERAN':'18.990254',
'BHIRA':'18.27',
'MURUD':'18.3311',
'POLADPUR':'17.981371',
'INS_SHIVAJI_LONAVALA':'18.724',
'TALEGAON':'18.722',
'GIRIVAN':'18.5607',
'CHINCHWAD_PUNE':'18.6595',
'MTI_PASHAN_PUNE':'18.5383',
'CME_DAPODI':'18.6032',
'RJSPMCOP_DUDULGAON':'18.6769',
'LAVALE':'18.5363',
'SHIVAJINAGAR_PUNE':'18.5286',
'PASHAN_AWS_LAB':'18.5167',
'RAJGURUNAGAR':'18.841',
'BLINDSCHOOL_KP_PUNE':'18.54',
'NDA_PUNE':'18.47',
'MAGARPATTA_PUNE':'18.5115',
'WADGAONSHERI_PUNE':'18.5482',
'VETALE_KHED':'18.939',
'DPS_HADAPSAR_PUNE':'18.4659',
'LONIKALBHOR_HAVELI':'18.4697',
'PABAL_SHIRUR':'18.8344',
'BALLALWADI_JUNNAR':'19.2396',
'KHADAKWADI_AMBEGAON':'18.9052',
'NIMGIRI_JUNNAR':'19.28087',
'TALEGAON_DHAMDHERE':'18.671',
'NARAYANGOAN_KRISHI_KENDRA':'19.1003',
'CHRIST_UNIVERSITY_LAVASA':'18.4144',
'CAGMO_SHIVAJINAGAR':'19.2092',
'KHUTBAV_DAUND':'18.5056',
'WALHE_PURANDAR':'18.1748',
'MALIN_AMBEGAON':'19.1574',
'GUDHE_BHOR':'18.0728',
'NIASM_BARAMATI':'18.153',
'NES_LAKADI_INDAPUR':'18.1748',
'BHANDARDARA':'19.33',
'PARNER':'19',
'KOPERGAON':'19.87598',
'SHRIGONDA':'18.620098',
'AHMEDNAGAR':'19.08825',
'RAHURI':'19.36654',
'SHEVGAON':'19.347307',
'PALGHAR_AWS400':'19.73184',
'PALGHAR_KVK':'20.05608',
'VILHOLI':'19.933',
'TRIMBAKESHWAR':'19.938992',
'NIPHAD':'20.071949',
'VANI':'20.330519',
'KALWAN':'20.47339',
'MALEGAON':'20.5692',
'DAPOLI':'17.75419',
'SAVARDE(GOLWANE)':'17.394104',
'POWARWADI(BHAMBHED)':'16.817108',
'CHIPLUN':'17.31',
'RATNAGIRI':'16.98617',
'RATNAGIRI_AWS400':'16.985963',
'MAHABALESHWAR':'17.92472',
'PANCHGANI':'17.56',
'SATARA':'17.68806',
'PHALTAN':'17.98',
'BGRL_KARAD':'17.2977',
'MOHOL_KVK':'17.4833',
'KARMALA':'18.9',
'SOLAPUR':'17.67017',
'SANGOLA_MAHAVIDYALAYA':'17.420765',
'AKKALKOT':'17.51',
'KOLHAPUR_AMFU':'16.6733',
'SHAHUWADI':'16.9',
'PANHALA':'16.81279',
'RADHANAGRI_ARS':'16.41029',
'GARGOTI(BHUDARGAD)':'16.18',
'GANGAPUR':'19.705767',
'PAITHAN':'19.48',
'AURANGABAD_KVK':'19.8512',
'AURANGABAD':'19.8561',
'KANNAD':'20.256844',
'CHALISGAON':'20.462271',
'CHOPDA':'21.23',
'JALGAON':'21.23691',
'JAMNER':'20.809813',
'DHULE':'20.90381',
'SHIRPUR':'21.35',
'SHIRALA':'16.98',
'UMADI':'17.2',
'TASGAON':'17.027506',
'SANGLI_KVK':'16.896059',
'AKKALKUWA':'21.2167',
'NAVAPUR':'21.16456',
'TALODA':'21.5667',
'NANDURBAR':'21.37',
'NANDURBAR_KVK':'21.43578',
'SHAHADA_AWS400':'21.5347',
'JALNA':'19.82642',
'BHOKARDAN':'20.239645',
'GHANSANGAVI':'19.522394',
'PARTUR':'19.589642',
'VAIBHAVWADI':'16.49',
'AWALEGAON':'16.11779',
'MULDE_AMFU':'16.01278',
'DEVGAD':'16.379',
'VENGURLA':'15.861483',
'OSMANABAD':'18.18536',
'KALAMB':'18.57',
'TULZAPUR':'18.012310',
'TULGA_KVK':'18.01231',
'AMBEJOGAI':'18.72419',
'BEED_PTO':'18.990814',
'PARALIVAIJANATH':'18.84',
'SHIRUR':'19.12',
'CHAKUR':'18.2833',
'LATUR':'18.40044',
'NILANGA':'18.12',
'UDGIR_AWS400':'18.387928',
'AUNDHA_NAGNATH':'19.52',
'HINGOLI':'19.73',
'KALAMNURI':'19.68',
'TONDAPUR_AWS400':'19.422893',
'PARBHANI_AMFU':'19.23781',
'SONPETH':'19.03',
'PURNA':'19.17',
'NANDED':'19.15044',
'SAGROLI_KVK':'18.69124',
'BHOKAR':'19.21'


    }


    # Entries to be removed
    station_to_lat_to_remove = {'MURUD', 'NANDURBAR', 'BHANDARDARA', 'PAITHAN',
                                     'PARALIVAIJANATH', 'SHIRUR', 'SHIRPUR', 'AUNDHA_NAGNATH',
                                     'KALAMNURI', 'GARGOTI(BHUDARGAD)', 'SHAHUWADI', 'CHAKUR',
                                     'NILANGA', 'BHOKAR', 'TALODA', 'KALAMB','TULZAPUR', 'PURNA', 'SONPETH',
                                     'UMADI', 'PANCHGANI', 'PHALTAN', 'AKKALKOT', 'KARMALA'}

    # Create a new dictionary excluding the unwanted entries
    filtered_station_to_lat = {k: v for k, v in station_to_lat.items() if k not in station_to_lat_to_remove}

    # Check if the station is in the filtered dictionary
    station = row['STATION']
    if station in filtered_station_to_lat:
        return filtered_station_to_lat[station]
    else:
        return ''  # Or some other default value if needed


def map_long(row):
    station_to_long = {
'MUMBAI_COLABA':'72.812897',
'BYCULLA_MUMBAI':'72.834549',
'MAHALAXMI':'72.8231',
'MATUNGA_MUMBAI':'72.853127',
'SION_MUMBAI':'72.866837',
'MUMBAI_SANTA_CRUZ':'72.85822',
'TATA POWER CHEMBUR':'72.904526',
'BANDRA':'72.8409',
'MUMBAI AIRPORT':'72.8568',
'VIDYAVIHAR':'72.896767',
'JUHU_AIRPORT':'72.8341',
'VIKHROLI':'72.9282',
'RAM_MANDIR':'72.84967',
'DAHISAR':'72.859573',
'KOPARKHAIRANE':'73.020246',
'BHAYANDER':'72.852028',
'MIRA_ROAD':'72.855766',
'IIGHQ_NEWPANVEL':'73.106094',
'KARJAT':'73.31722',
'IIG_MO_ALIBAG':'72.86903',
'MATHERAN':'73.26658',
'BHIRA':'73.23',
'MURUD':'72.9544',
'POLADPUR':'73.466118',
'INS_SHIVAJI_LONAVALA':'73.3697',
'TALEGAON':'73.6632',
'GIRIVAN':'73.5211',
'CHINCHWAD_PUNE':'73.7987',
'MTI_PASHAN_PUNE':'73.8045',
'CME_DAPODI':'73.8541',
'RJSPMCOP_DUDULGAON':'73.87664',
'LAVALE':'73.7325',
'SHIVAJINAGAR_PUNE':'73.8493',
'PASHAN_AWS_LAB':'73.85',
'RAJGURUNAGAR':'73.884',
'BLINDSCHOOL_KP_PUNE':'73.8886',
'NDA_PUNE':'73.78',
'MAGARPATTA_PUNE':'73.9285',
'WADGAONSHERI_PUNE':'73.9278',
'VETALE_KHED':'73.7744',
'DPS_HADAPSAR_PUNE':'73.9244',
'LONIKALBHOR_HAVELI':'74.0013',
'PABAL_SHIRUR':'74.0536',
'BALLALWADI_JUNNAR':'73.9155',
'KHADAKWADI_AMBEGAON':'74.0938',
'NIMGIRI_JUNNAR':'73.77124',
'TALEGAON_DHAMDHERE':'74.148',
'NARAYANGOAN_KRISHI_KENDRA':'73.9655',
'CHRIST_UNIVERSITY_LAVASA':'73.5069',
'CAGMO_SHIVAJINAGAR':'73.8725',
'KHUTBAV_DAUND':'74.3304',
'WALHE_PURANDAR':'74.1498',
'MALIN_AMBEGAON':'73.6811',
'GUDHE_BHOR':'73.6706',
'NIASM_BARAMATI':'74.5003',
'NES_LAKADI_INDAPUR':'74.689',
'BHANDARDARA':'73.45',
'PARNER':'74.26',
'KOPERGAON':'74.4829',
'SHRIGONDA':'74.698341',
'AHMEDNAGAR':'74.74679',
'RAHURI':'74.64379',
'SHEVGAON':'75.218307',
'PALGHAR_AWS400':'72.760869',
'PALGHAR_KVK':'72.75239',
'VILHOLI':'73.7213',
'TRIMBAKESHWAR':'73.533356',
'NIPHAD':'74.103271',
'VANI':'73.891579',
'KALWAN':'74.00817',
'MALEGAON':'73.6889',
'DAPOLI':'73.17675',
'SAVARDE(GOLWANE)':'73.489136',
'POWARWADI(BHAMBHED)':'73.632874',
'CHIPLUN':'73.32',
'RATNAGIRI':'73.32833',
'RATNAGIRI_AWS400':'73.328275',
'MAHABALESHWAR':'73.66028',
'PANCHGANI':'73.5',
'SATARA':'74.02639',
'PHALTAN':'74.43',
'BGRL_KARAD':'74.1238',
'MOHOL_KVK':'75.3815',
'KARMALA':'75.19',
'SOLAPUR':'75.6375',
'SANGOLA_MAHAVIDYALAYA':'75.194714',
'AKKALKOT':'76.19',
'KOLHAPUR_AMFU':'74.23778',
'SHAHUWADI':'73.94',
'PANHALA':'74.11145',
'RADHANAGRI_ARS':'73.994119',
'GARGOTI(BHUDARGAD)':'74.08',
'GANGAPUR':'75.001839',
'PAITHAN':'75.2833',
'AURANGABAD_KVK':'75.2968',
'AURANGABAD':'75.2853',
'KANNAD':'75.137871',
'CHALISGAON':'75.003738',
'CHOPDA':'75.29',
'JALGAON':'75.53856',
'JAMNER':'75.772324',
'DHULE':'74.80428',
'SHIRPUR':'74.88',
'SHIRALA':'74.13',
'UMADI':'75.5',
'TASGAON':'74.607323',
'SANGLI_KVK':'74.520167',
'AKKALKUWA':'74.02',
'NAVAPUR':'73.80383',
'TALODA':'74.2167',
'NANDURBAR':'74.23',
'NANDURBAR_KVK':'74.28058',
'SHAHADA_AWS400':'74.4859',
'JALNA':'75.87206',
'BHOKARDAN':'75.766083',
'GHANSANGAVI':'75.999146',
'PARTUR':'76.211868',
'VAIBHAVWADI':'73.74',
'AWALEGAON':'73.758484',
'MULDE_AMFU':'73.71667',
'DEVGAD':'73.38228',
'VENGURLA':'73.651428',
'OSMANABAD':'76.03561',
'KALAMB':'76.01',
'TULZAPUR':'76.080580',
'TULGA_KVK':'76.08058',
'AMBEJOGAI':'76.36489',
'BEED_PTO':'75.748339',
'PARALIVAIJANATH':'76.51',
'SHIRUR':'76.14',
'CHAKUR':'76.5',
'LATUR':'76.56222',
'NILANGA':'76.74',
'UDGIR_AWS400':'77.118043',
'AUNDHA_NAGNATH':'77.03',
'HINGOLI':'77.1333',
'KALAMNURI':'77.3',
'TONDAPUR_AWS400':'77.401878',
'PARBHANI_AMFU':'76.79325',
'SONPETH':'76.47',
'PURNA':'77.03',
'NANDED':'77.31181',
'SAGROLI_KVK':'77.732679',
'BHOKAR':'77.66'


    }


    # Entries to be removed
    station_to_long_to_remove = {'MURUD', 'NANDURBAR', 'BHANDARDARA', 'PAITHAN',
                                     'PARALIVAIJANATH', 'SHIRUR', 'SHIRPUR', 'AUNDHA_NAGNATH',
                                     'KALAMNURI', 'GARGOTI(BHUDARGAD)', 'SHAHUWADI', 'CHAKUR',
                                     'NILANGA', 'BHOKAR', 'TALODA', 'KALAMB','TULZAPUR', 'PURNA', 'SONPETH',
                                     'UMADI', 'PANCHGANI', 'PHALTAN', 'AKKALKOT', 'KARMALA'}

    # Create a new dictionary excluding the unwanted entries
    filtered_station_to_long = {k: v for k, v in station_to_long.items() if k not in station_to_long_to_remove}

    # Check if the station is in the filtered dictionary
    station = row['STATION']
    if station in filtered_station_to_long:
        return filtered_station_to_long[station]
    else:
        return ''  # Or some other default value if needed




df_sorted['LAT']=df_sorted.apply(map_lat, axis=1)
df_sorted['LONG']=df_sorted.apply(map_long, axis=1)



# Reorder columns as needed
df_sorted = df_sorted[['DATE','STATION','RF','LAT','LONG']]

df_sorted['RF'] = pd.to_numeric(df_sorted['RF'], errors='coerce')
df_sorted['LAT'] = pd.to_numeric(df_sorted['LAT'], errors='coerce')
df_sorted['LONG'] = pd.to_numeric(df_sorted['LONG'], errors='coerce')





# Load the shapefile
shapefile_path = 'C:\\Users\\hp\\Desktop\\gurinder\\python test\\maharashtra district excluding vidarbha.shp'
gdf = gpd.read_file(shapefile_path)

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter  # Import PillowWriter
import geopandas as gpd

# Assuming you have already set up your data and GeoDataFrame `gdf`

# Function to get custom color based on rainfall value
def get_custom_color(rf):
    if pd.isna(rf):
        return 'black'
    elif rf == 0:
        return 'silver'
    elif 0 < rf <= 2.5:
        return '#98FB98'
    elif 2.6 <= rf <= 15.5:
        return '#7FFF00'
    elif 15.6 <= rf <= 64.5:
        return '#228B22'
    elif 64.6 <= rf <= 115.5:
        return '#FFFF00'
    elif 115.6 <= rf <= 204.5:
        return '#FF8C00'
    elif rf > 204.5:
        return '#FF0000'
    else:
        return '#00008B'

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(22, 15))  # Keep your desired figure size
# Remove the axes
ax.axis('off')

# Plot the shapefile boundaries
gdf.plot(ax=ax, color='none', edgecolor='black')

# Function to update the plot for each frame
def update(date):
    ax.clear()
    ax.axis('off')  # Ensure the axes remain off after clearing
    gdf.plot(ax=ax, color='none', edgecolor='black')

    date_data = df_sorted[df_sorted['DATE'] == date]
    
    # Scatter plot with filled circles
    ax.scatter(
        date_data['LONG'],
        date_data['LAT'],
        s=50,  # Adjust size as needed
        c=[get_custom_color(rf) for rf in date_data['RF']],
        edgecolors='black',  # Border color
        facecolors=[get_custom_color(rf) for rf in date_data['RF']],  # Fill color
        linewidth=1.5,  # Adjust border thickness if needed
        alpha=1
    )

    ax.set_title(f"Rainfall on {date}")

# Create the animation
dates = df_sorted['DATE'].unique()
ani = animation.FuncAnimation(
    fig, update, frames=dates, repeat=False, interval=2000
)

# Save the animation as a GIF file
output_path = 'C:\\Users\\hp\\Desktop\\gurinder\\python test\\rainfall_animation.gif'
ani.save(output_path, writer=PillowWriter(fps=2))  # Use PillowWriter to save as GIF

plt.show()