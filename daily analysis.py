                    # import libraries
import pandas as pd
import numpy as np
import pandas.io.formats.style
import csv
from datetime import date,datetime,timedelta,timezone
import os
import time
import xlsxwriter
from styleframe import StyleFrame
import openpyxl
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.formatting.rule import FormulaRule
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MinuteLocator
import itertools
import matplotlib.dates as mdates
import shutil
#warnings.filterwarnings("ignore")




#Create today's and yesterday's date
t_day = date.today()
d1 = t_day.strftime("%Y-%m-%d")
d1_2 = t_day.strftime("%d-%m-%Y")
d1_22 = t_day.strftime("%d-%m")
#print(d1_22)

y_day=t_day-timedelta(days=7)
d0=y_day.strftime("%Y-%m-%d")
d0_2 = y_day.strftime("%d-%m-%Y")
d0_22 = y_day.strftime("%d-%m")
#print(d0_22)


# Get the path to the OneDrive
analysis_path = os.path.join(os.path.expanduser("~"), "Desktop\\gurinder")

# Define the path to the "daily data" folder
daily_data_path = os.path.join(analysis_path, "daily analysis")

# Check if the "daily data" folder exists and create it if not
if not os.path.exists(daily_data_path):
    os.makedirs(daily_data_path)

# Get today's date as a string in the format DD-MM-YYYY
today_date = d1_2

# Define the path to today's folder inside the "daily data" folder
today_folder_path = os.path.join(daily_data_path, today_date)

# Check if today's folder exists and create it if not
if not os.path.exists(today_folder_path):
    os.makedirs(today_folder_path)



#Set display options to show full DataFrame
#pd.set_option('display.max_rows', 1000000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)





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



all_mh=['MUMBAI_COLABA','BYCULLA_MUMBAI','MAHALAXMI','MATUNGA_MUMBAI','SION_MUMBAI','MUMBAI_SANTA_CRUZ','TATA POWER CHEMBUR','BANDRA','MUMBAI AIRPORT','VIDYAVIHAR','JUHU_AIRPORT','VIKHROLI','RAM_MANDIR','DAHISAR','KOPARKHAIRANE',
'BHAYANDER','MIRA_ROAD','IIGHQ_NEWPANVEL','KARJAT','IIG_MO_ALIBAG','MATHERAN','BHIRA',
'MURUD','POLADPUR','INS_SHIVAJI_LONAVALA','TALEGAON','GIRIVAN','CHINCHWAD_PUNE','MTI_PASHAN_PUNE','CME_DAPODI','RJSPMCOP_DUDULGAON','LAVALE','SHIVAJINAGAR_PUNE','PASHAN_AWS_LAB','RAJGURUNAGAR','BLINDSCHOOL_KP_PUNE','NDA_PUNE','MAGARPATTA_PUNE','WADGAONSHERI_PUNE','VETALE_KHED','DPS_HADAPSAR_PUNE','LONIKALBHOR_HAVELI','PABAL_SHIRUR','BALLALWADI_JUNNAR','KHADAKWADI_AMBEGAON','NIMGIRI_JUNNAR','TALEGAON_DHAMDHERE','NARAYANGOAN_KRISHI_KENDRA','CHRIST_UNIVERSITY_LAVASA','CAGMO_SHIVAJINAGAR','KHUTBAV_DAUND','WALHE_PURANDAR','MALIN_AMBEGAON','GUDHE_BHOR','NIASM_BARAMATI','NES_LAKADI_INDAPUR','BHANDARDARA','PARNER','KOPERGAON','SHRIGONDA',
'AHMEDNAGAR','RAHURI','SHEVGAON','PALGHAR_AWS400','PALGHAR_KVK','VILHOLI','TRIMBAKESHWAR','NIPHAD','VANI','KALWAN','MALEGAON','DAPOLI','SAVARDE(GOLWANE)',
'POWARWADI(BHAMBHED)','CHIPLUN','RATNAGIRI','RATNAGIRI_AWS400','MAHABALESHWAR','PANCHGANI','SATARA','PHALTAN','BGRL_KARAD','MOHOL_KVK','KARMALA','SOLAPUR','SANGOLA_MAHAVIDYALAYA',
'AKKALKOT','KOLHAPUR_AMFU','SHAHUWADI','PANHALA','RADHANAGRI_ARS','GARGOTI(BHUDARGAD)','GANGAPUR','PAITHAN','AURANGABAD_KVK','AURANGABAD','KANNAD','CHALISGAON','CHOPDA','JALGAON','JAMNER','DHULE','SHIRPUR','SHIRALA','UMADI','TASGAON','SANGLI_KVK','AKKALKUWA','NAVAPUR','TALODA','NANDURBAR','NANDURBAR_KVK','SHAHADA_AWS400','JALNA','BHOKARDAN','GHANSANGAVI','PARTUR','VAIBHAVWADI','AWALEGAON','MULDE_AMFU','DEVGAD',
'VENGURLA','OSMANABAD','KALAMB','TULGA_KVK','AMBEJOGAI','BEED_PTO','PARALIVAIJANATH',
'SHIRUR','CHAKUR','LATUR','NILANGA','UDGIR_AWS400','AUNDHA_NAGNATH','HINGOLI','KALAMNURI','TONDAPUR_AWS400','PARBHANI_AMFU','SONPETH','PURNA','NANDED','SAGROLI_KVK','BHOKAR']

# Create a DataFrame with canary_mh
all_stations = pd.DataFrame(all_mh, columns=['STATIONS'])




                   #collect todays aws tabular data
today_mh=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+d0+'&f='+d1+'&g=ALL_HOUR&h=ALL_MINUTE')
dft_mh=today_mh[0]
                                #collect todays arg tabular data
arg_today_mh=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=ARG&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+d0+'&f='+d1+'&g=ALL_HOUR&h=ALL_MINUTE')
arg_dft_mh=arg_today_mh[0]






                                #combine the two dataframes
combine_tday_mh=pd.concat([dft_mh,arg_dft_mh], ignore_index=True)







                                #drop vidarbha stations
mah_drop_today = combine_tday_mh[(combine_tday_mh['DISTRICT'] == 'AKOLA') | (combine_tday_mh['DISTRICT'] == 'AMRAVATI')|
               (combine_tday_mh['DISTRICT'] == 'BHANDARA') | (combine_tday_mh['DISTRICT'] == 'BULDHANA')|
               (combine_tday_mh['DISTRICT'] == 'CHANDRAPUR') | (combine_tday_mh['DISTRICT'] == 'GADCHIROLI')|
               (combine_tday_mh['DISTRICT'] == 'GONDIA') | (combine_tday_mh['DISTRICT'] == 'NAGPUR')|
               (combine_tday_mh['DISTRICT'] == 'YAVATMAL') | (combine_tday_mh['DISTRICT'] == 'WARDHA')|
               (combine_tday_mh['DISTRICT'] == 'WASHIM')].index
combine_tday_mh.drop(mah_drop_today, inplace=True)









                            #choose columns to include in combine_tday_mh
combine_tday_mh=combine_tday_mh[['STATION','DATE(YYYY-MM-DD)','TIME (UTC)','RAIN FALL CUM. SINCE 0300 UTC (mm)','TEMP DAY MIN. (\'C)','TEMP DAY MAX. (\'C)','TEMP. (\'C)','RH (%)','MSLP (hPa / gpm)','SLP (hPa)','BATTERY (Volts)','GPS']]





                           #replace names
                       #replace names
combine_tday_mh.columns=combine_tday_mh.columns.str.replace('STATION', 'STATIONS',regex=False)
combine_tday_mh.columns=combine_tday_mh.columns.str.replace('DATE(YYYY-MM-DD)', 'DATE',regex=False)
combine_tday_mh.columns=combine_tday_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
combine_tday_mh.columns=combine_tday_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)
combine_tday_mh.columns=combine_tday_mh.columns.str.replace('TEMP DAY MAX. (\'C)', 'MAX T',regex=False)
combine_tday_mh.columns=combine_tday_mh.columns.str.replace('TEMP. (\'C)', 'TEMP',regex=False)
combine_tday_mh.columns=combine_tday_mh.columns.str.replace('SLP (hPa)', 'SLP',regex=False)
combine_tday_mh.columns=combine_tday_mh.columns.str.replace('MSLP (hPa / gpm)', 'MSLP',regex=False)


#print(combine_tday_mh['STATION'].nunique())



# Perform a left merge to include all stations from canary_mh in today_mh
merged = pd.merge(all_stations, combine_tday_mh, on='STATIONS', how='left')

#print(merged['STATION'].nunique())

df=merged.copy()
del merged


df['DATE'] = pd.to_datetime(df['DATE'],format='%Y-%m-%d')
df['DATE'] = df['DATE'].dt.strftime('%d-%m-%Y')

df['TIME (UTC)'] = pd.to_datetime(df['TIME (UTC)'],format='%H:%M:%S')
df['TIME (UTC)'] = df['TIME (UTC)'].dt.strftime('%H:%M')

#print(df)




# Combine DATE and TIME (UTC) columns into DATETIME (UTC) 
df['DATETIME (UTC)'] = df['DATE']+" "+ df['TIME (UTC)']



df = df.drop(columns=['DATE','TIME (UTC)'])

#print(df)
#print('unique stations in df: ',df['STATIONS'].nunique())
#print('unique datetime in df: ',df['DATETIME (UTC)'].nunique())





#print(df)


#print('unique stations in df: ',df['STATION'].nunique())
#print('unique datetime in df: ',df['DATETIME (UTC)'].nunique())






#Define the start date, end date, and frequency
start_datetime = d0 + ' 03:00'
end_datetime = d1 + ' 03:00'
frequency = '15min'

#Create a datetime range
datetime_range = pd.date_range(start=start_datetime, end=end_datetime, freq=frequency).strftime('%d-%m-%Y %H:%M')

# Reverse the order
datetime_range = datetime_range[::-1]

#print(datetime_range)







# Create a DataFrame with the datetime range
datetime_df = pd.DataFrame(datetime_range, columns=['DATETIME (UTC)'])

#print(datetime_df)
#print('rows in datetime_df: ',len(datetime_df))


# Extract unique values
stations = df['STATIONS'].unique()
datetimes = datetime_df['DATETIME (UTC)'].unique()

# Create a DataFrame with all combinations of 'station' and 'datetime'
all_combinations = pd.DataFrame(list(itertools.product(stations, datetimes)), columns=['STATIONS', 'DATETIME (UTC)'])

# Merge with the original df to include all stations and all datetimes
complete_combined = pd.merge(all_combinations, df, on=['STATIONS', 'DATETIME (UTC)'], how='left')


#print(complete_combined)
#print('unique stations in complete_combined: ',complete_combined['STATIONS'].nunique())
#print('unique datetime in complete_combined: ',complete_combined['DATETIME (UTC)'].nunique())


#complete_combined.to_excel(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\daily data\\400_test.xlsx'))




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
complete_combined['AWS/ARG'] = complete_combined['STATIONS'].apply(check_aws)
    

complete_combined['DISTRICT']=complete_combined.apply(map_dis_to_sta_mh, axis=1)





#complete_combined['DATETIME (UTC)'] = pd.to_datetime(complete_combined['DATETIME (UTC)'])

complete_combined = complete_combined[['DISTRICT', 'STATIONS','AWS/ARG', 'DATETIME (UTC)', 'RF', 'MIN T', 'MAX T', 'TEMP', 'RH (%)','SLP','MSLP', 'BATTERY (Volts)', 'GPS']]

#print(complete_combined)
#print('unique stations in complete_combined: ',complete_combined['STATIONS'].nunique())
#print('unique datetime in complete_combined: ',complete_combined['DATETIME (UTC)'].nunique())


complete_combined['RF'] = pd.to_numeric(complete_combined['RF'], errors='coerce')
complete_combined['MIN T'] = pd.to_numeric(complete_combined['MIN T'], errors='coerce')
complete_combined['MAX T'] = pd.to_numeric(complete_combined['MAX T'], errors='coerce')
complete_combined['TEMP'] = pd.to_numeric(complete_combined['TEMP'], errors='coerce')
complete_combined['SLP'] = pd.to_numeric(complete_combined['SLP'], errors='coerce')
complete_combined['MSLP'] = pd.to_numeric(complete_combined['MSLP'], errors='coerce')
complete_combined['BATTERY (Volts)'] = pd.to_numeric(complete_combined['BATTERY (Volts)'], errors='coerce')


def rf_color_range(rf_value):
    styles = []
    for v in rf_value:
        if pd.isna(v):  # Handle NaN values
            styles.append('')  # No style for NaN cells
        elif v % 0.5 != 0:  # if not multiple of 0.5
            styles.append('background-color: black; color: white; font-weight: bold')
        elif v == 0:
            styles.append('background-color: silver')
        elif 0 < v < 1:
            styles.append('background-color: #71797E')
        elif 1 <= v <= 2.4:
            styles.append('background-color: #ADFF2F')
        elif 2.5 <= v <= 15.5:
            styles.append('background-color: #00FF00')
        elif 15.6 <= v <= 64.4:
            styles.append('background-color: #00FFFF')
        elif 64.5 <= v <= 115.5:
            styles.append('background-color: #FFFF00')
        elif 115.6 <= v <= 204.4:
            styles.append('background-color: #FFA500')
        elif v > 204.4:
            styles.append('background-color: #FF0000')
        else:
            styles.append('background-color: #00008B')
    return styles
    

# Define the custom color function
def temp_range(temp_values):
    styles = []
    previous_value = None  # To keep track of the previous value for the .diff() logic
    for v in temp_values:
        if pd.isna(v):  # Handle NaN values
            styles.append('')  # No style for NaN cells
        elif previous_value is not None and abs(v - previous_value) > 2:  # Check difference from the previous value
            styles.append('background-color: black; color: white; font-weight: bold')
        elif v <0:
            styles.append('background-color: black; color: white; font-weight: bold')
        elif 0.1 <= v <= 10.0:
            styles.append('background-color: #00FF00')
        elif 10.1 <= v <= 20.0:
            styles.append('background-color: #00FFFF')
        elif 20.1 <= v <= 30.0:
            styles.append('background-color: #FFFF00')
        elif 30.1 <= v <= 40.0:
            styles.append('background-color: #FFA500')
        elif v >= 40.1:
            styles.append('background-color: #FF0000')
        else:
            styles.append('background-color: #00008B')
    return styles
    


def rh_range(rh_values):
    styles = []
    for v in rh_values:
        if pd.isna(v):  # Handle NaN values
            styles.append('')  # No style for NaN cells
        elif v > 100:  # if values are greater than 100
            styles.append('background-color: black; color: white; font-weight: bold')
        elif 1 <= v <= 20:
            styles.append('background-color: #ADFF2F')
        elif 21 <= v <= 40:
            styles.append('background-color: #00FF00')
        elif 41 <= v <= 60:
            styles.append('background-color: #00FFFF')
        elif 61 <= v <= 80:
            styles.append('background-color: #FFFF00')
        elif 81 <= v <= 90:
            styles.append('background-color: #FFA500')
        elif 91 <= v <= 100:
            styles.append('background-color: #FF0000')
        else:
            styles.append('background-color: #00008B')
    return styles
    

    

# Define the custom color function
def slp_range(slp_values):
    styles = []
    previous_value = None  # To keep track of the previous value for the .diff() logic

    for v in slp_values:
        if pd.isna(v):  # Handle NaN values
            styles.append('')  # No style for NaN cells
        elif previous_value is not None and abs(v - previous_value) > 2:  # Check difference from the previous value
            styles.append('background-color: black; color: white; font-weight: bold')
        elif 500.1 <= v <= 800.0:
            styles.append('background-color: #ADFF2F')
        elif 800.1 <= v <= 900.0:
            styles.append('background-color: #00FF00')
        elif 900.1 <= v <= 950.0:
            styles.append('background-color: #00FFFF')
        elif 950.1 <= v <= 1000.0:
            styles.append('background-color: #FFFF00')
        elif 1000.1 <= v <= 1025.0:
            styles.append('background-color: #FFA500')
        elif v >= 1025.1:
            styles.append('background-color: #FF0000')
        else:
            styles.append('background-color: #00008B')
        
        previous_value = v  # Update the previous value

    return styles
    

# Define the custom color function
def bat_range(bat_values):
    styles = []
    for v in bat_values:
        if pd.isna(v):  # Handle NaN values
            styles.append('')  # No style for NaN cells
        elif 14.1 <= v <= 15:
            styles.append('background-color: #ADFF2F')
        elif 13.1 <= v <= 14:
            styles.append('background-color: #00FF00')
        elif 12.1 <= v <= 13:
            styles.append('background-color: #00FFFF')
        elif 11.1 <= v <= 12:
            styles.append('background-color: #FFFF00')
        elif 10.1 <= v <= 11:
            styles.append('background-color: #FFA500')
        elif v <= 10:
            styles.append('background-color: #FF0000')
        else:
            styles.append('background-color: #00008B')
    return styles
    
def gps(s, props='background-color:black;color:white;font-weight:bold'):
    return np.where((s == np.where((s == "U") & (s.notna()), s.values, np.nan)), props, '')

  
    


    


#def rf(s, props='background-color:black;color:white;font-weight:bold'):
    return np.where((s == np.where((s % 0.5 != 0) & (s.notna()), s.values, np.nan)), props, '')

#def temp(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s < 0) & (s.notna()), s.values, np.nan)), props, '')

#def rh(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s > 100) & (s.notna()), s.values, np.nan)), props, '')

#def mslp(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s.diff().abs() > 2) & (s.notna()), s.values, np.nan)), props, '')

#def battery(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s < 11) & (s.notna()), s.values, np.nan)), props, '')

#def gps(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s == "U") & (s.notna()), s.values, np.nan)), props, '')


        



# File path for the Excel file
# Define the file path
# Define Excel export path
excel_path = os.path.join(today_folder_path,'('+d0_2+' to '+d1_2+').xlsx')

# Ensure the directory exists
#directory = os.path.dirname(file_path)
#if not os.path.exists(directory):
    #os.makedirs(directory)
#date_folder=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\daily data')
# Combine the parent folder path and the new folder name
#new_folder_path = os.path.join(date_folder, 'yheyeyweyweyey')



# Create a Pandas Excel writer using XlsxWriter as the engine
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:

    # Iterate over unique districts and create a sheet for each district
    for district in complete_combined['DISTRICT'].unique():

    # Filter the DataFrame for the current district and drop the 'DISTRICT' column
        district_df = complete_combined[complete_combined['DISTRICT'] == district].drop(columns=['DISTRICT'])
        
        # Apply highlighting and styling to the district_data
        district_df.style.set_table_styles([
            {'selector': 'th.col_heading', 'props': [('font-weight', 'bold'), ('font-size', '14px')]}
        ])
        district_df.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt','border':'1pt solid', 'text-align':"center"})\
        .apply(rf_color_range, subset=['RF'])\
        .apply(temp_range, subset=['MIN T', 'MAX T','TEMP'])\
        .apply(rh_range, subset=['RH (%)'])\
        .apply(slp_range, subset=['SLP','MSLP'])\
        .apply(bat_range, subset=['BATTERY (Volts)'])\
        .apply(gps, subset=['GPS'])\
        .to_excel(writer, sheet_name=district, index=False, engine='xlsxwriter')
        
        
        # Access the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets[district]
        
        # Set column widths (example widths, adjust as needed)
        worksheet.set_column('A:A', 40)
        worksheet.set_column('B:B', 9)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 6)
        worksheet.set_column('F:F', 6)
        worksheet.set_column('G:G', 6)
        worksheet.set_column('H:H', 9)
        worksheet.set_column('I:I', 9)
        worksheet.set_column('J:J', 9)
        worksheet.set_column('K:K', 20)
        worksheet.set_column('L:L', 5)

        # Freeze the top row (row 0)
        worksheet.freeze_panes(1, 0)
 

exit()
# Iterate through each district in the combined DataFrame
for district_name in complete_combined['DISTRICT'].unique():
    df_district = complete_combined[complete_combined['DISTRICT'] == district_name]
    
    # Create folder for the district inside today's date folder
    district_folder = os.path.join(today_folder_path, district_name)
    
    # Check if the district folder exists and remove it if it does
    if os.path.exists(district_folder):
        shutil.rmtree(district_folder)
    
    # Create a new, empty district folder
    os.makedirs(district_folder)
    
    # Iterate through each station in the district
    for station in df_district['STATIONS'].unique():
        df_station = df_district[df_district['STATIONS'] == station]
        
        # Convert 'DATETIME (UTC)' to datetime format
        df_station.loc[:, 'DATETIME (UTC)'] = pd.to_datetime(df_station['DATETIME (UTC)'], format='%d-%m %H:%M')

        # Create a figure with 6 subplots (6 rows, 1 column)
        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, figsize=(22, 10), sharex=True)

        # Plot 'DATETIME (UTC)' vs 'RF'
        ax1.plot(df_station['DATETIME (UTC)'], df_station['RF'], 'g-', label='RF', marker='o')
        ax1.tick_params(axis='y', labelcolor='g')
        ax1.set_title(f'RAINFALL(mm)', fontsize=14, fontweight='bold', color='g')

        # Plot 'DATETIME (UTC)' vs 'TEMP'
        ax2.plot(df_station['DATETIME (UTC)'], df_station['TEMP'], 'r-', label='Temperature', marker='o')
        ax2.tick_params(axis='y', labelcolor='r')
        ax2.set_title(f'TEMPERATURE(°C)', fontsize=14, fontweight='bold', color='r')

        # Plot 'DATETIME (UTC)' vs 'MSLP'
        ax3.plot(df_station['DATETIME (UTC)'], df_station['MSLP'], 'b-', label='MSLP', marker='o')
        ax3.tick_params(axis='y', labelcolor='b')
        ax3.set_title(f'MSLP(hPa)', fontsize=14, fontweight='bold', color='b')

        # Plot 'DATETIME (UTC)' vs 'RH (%)'
        ax4.plot(df_station['DATETIME (UTC)'], df_station['RH (%)'], '#4B0082', label='RH (%)', marker='o')
        ax4.tick_params(axis='y', labelcolor='#4B0082')
        ax4.set_title(f'RH(%)', fontsize=14, fontweight='bold', color='#4B0082')

        # Plot 'DATETIME (UTC)' vs 'BATTERY'
        ax5.plot(df_station['DATETIME (UTC)'], df_station['BATTERY (Volts)'], '#000000', label='BATTERY (Volts)', marker='o')
        ax5.tick_params(axis='y', labelcolor='#000000')
        ax5.set_title(f'BATTERY VOLTAGE (V)', fontsize=14, fontweight='bold', color='#000000')

        # Replace values in GPS column
        df_station.loc[:, 'GPS']=df_station.loc[:, 'GPS'].replace({'L': 1, 'U': 0})
        # Plot 'DATETIME (UTC)' vs 'GPS'
        ax6.plot(df_station['DATETIME (UTC)'], df_station['GPS'], '#000000', label='GPS', marker='o')
        ax6.tick_params(axis='y', labelcolor='#000000')
        ax6.set_title(f'GPS', fontsize=14, fontweight='bold', color='#000000')

        # Set common x-axis label
        ax6.set_xlabel('DATETIME (UTC)', fontsize=12, fontweight='bold')
        plt.xticks(rotation=90)
        ax6.set_xticks(df_station['DATETIME (UTC)'])

        # Apply date formatter to the x-axis of all subplots
        date_format = mdates.DateFormatter('%d-%m %H:%M')
        for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
            ax.xaxis.set_major_formatter(date_format)

        # Title and layout
        fig.tight_layout(rect=[0, 0, 1, 1])  # Adjust layout to make room for the main title
        plt.xlim(min(df_station['DATETIME (UTC)']), max(df_station['DATETIME (UTC)']))  # Set limits based on your data range

        # Save the plot to the district folder
        plot_filename = f'{station}.png'
        plot_path = os.path.join(district_folder, plot_filename)
        plt.savefig(plot_path)
        plt.close(fig)

print('Required pdf files have been generated in "daily data" folder on the desktop.')
time.sleep(15)
