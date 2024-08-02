print('Importing required libraries.')
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
#pd.set_option('future.no_silent_downcasting', True)
import shutil


print('Creating required date and time')


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

#print(len(arg_mh))


all_mh=['MUMBAI_COLABA','BYCULLA_MUMBAI','MAHALAXMI','MATUNGA_MUMBAI','SION_MUMBAI','MUMBAI_SANTA_CRUZ','TATA POWER CHEMBUR','BANDRA','MUMBAI AIRPORT','VIDYAVIHAR','JUHU_AIRPORT','VIKHROLI','RAM_MANDIR','DAHISAR','KOPARKHAIRANE',
'BHAYANDER','MIRA_ROAD','IIGHQ_NEWPANVEL','KARJAT','IIG_MO_ALIBAG','MATHERAN','BHIRA',
'MURUD','POLADPUR','INS_SHIVAJI_LONAVALA','TALEGAON','GIRIVAN','CHINCHWAD_PUNE','MTI_PASHAN_PUNE','CME_DAPODI','RJSPMCOP_DUDULGAON','LAVALE','SHIVAJINAGAR_PUNE','PASHAN_AWS_LAB','RAJGURUNAGAR','BLINDSCHOOL_KP_PUNE','NDA_PUNE','MAGARPATTA_PUNE','WADGAONSHERI_PUNE','VETALE_KHED','DPS_HADAPSAR_PUNE','LONIKALBHOR_HAVELI','PABAL_SHIRUR','BALLALWADI_JUNNAR','KHADAKWADI_AMBEGAON','NIMGIRI_JUNNAR','TALEGAON_DHAMDHERE','NARAYANGOAN_KRISHI_KENDRA','CHRIST_UNIVERSITY_LAVASA','CAGMO_SHIVAJINAGAR','KHUTBAV_DAUND','WALHE_PURANDAR','MALIN_AMBEGAON','GUDHE_BHOR','NIASM_BARAMATI','NES_LAKADI_INDAPUR','BHANDARDARA','PARNER','KOPERGAON','SHRIGONDA',
'AHMEDNAGAR','RAHURI','SHEVGAON','PALGHAR_AWS400','PALGHAR_KVK','VILHOLI','TRIMBAKESHWAR','NIPHAD','VANI','KALWAN','MALEGAON','DAPOLI','SAVARDE(GOLWANE)',
'POWARWADI(BHAMBHED)','CHIPLUN','RATNAGIRI','RATNAGIRI_AWS400','MAHABALESHWAR','PANCHGANI','SATARA','PHALTAN','BGRL_KARAD','MOHOL_KVK','KARMALA','SOLAPUR','SANGOLA_MAHAVIDYALAYA',
'AKKALKOT','KOLHAPUR_AMFU','SHAHUWADI','PANHALA','RADHANAGRI_ARS','GARGOTI(BHUDARGAD)','GANGAPUR','PAITHAN','AURANGABAD_KVK','AURANGABAD','KANNAD','CHALISGAON','CHOPDA','JALGAON','JAMNER','DHULE','SHIRPUR','SHIRALA','UMADI','TASGAON','SANGLI_KVK','AKKALKUWA','NAVAPUR','TALODA','NANDURBAR','NANDURBAR_KVK','SHAHADA_AWS400','JALNA','BHOKARDAN','GHANSANGAVI','PARTUR','VAIBHAVWADI','AWALEGAON','MULDE_AMFU','DEVGAD',
'VENGURLA','OSMANABAD','KALAMB','TULGA_KVK','AMBEJOGAI','BEED_PTO','PARALIVAIJANATH',
'SHIRUR','CHAKUR','LATUR','NILANGA','UDGIR_AWS400','AUNDHA_NAGNATH','HINGOLI','KALAMNURI','TONDAPUR_AWS400','PARBHANI_AMFU','SONPETH','PURNA','NANDED','SAGROLI_KVK','BHOKAR']



# Create a DataFrame with canary_mh
all_stations = pd.DataFrame(all_mh, columns=['STATION'])

#print(len(all_stations ))


print('Checking if the AWS/ARG website is working...')

try:

    #Collect today's data (adjust your URLs accordingly)
    today_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e={d0}&f={d1}&g=ALL_HOUR&h=ALL_MINUTE')[0]

    print('Website working.')

except Exception as e:
    print(f"Error fetching data from Website: {e}")
    time.sleep(5)
    exit()

#print(today_mh.info())

print('Filtering Data...')

                           #drop vidarbha stations
mah_drop_today = today_mh[(today_mh['DISTRICT'] == 'AKOLA') | (today_mh['DISTRICT'] == 'AMRAVATI')|
(today_mh['DISTRICT'] == 'BHANDARA') | (today_mh['DISTRICT'] == 'BULDHANA')|
(today_mh['DISTRICT'] == 'CHANDRAPUR') | (today_mh['DISTRICT'] == 'GADCHIROLI')|
(today_mh['DISTRICT'] == 'GONDIA') | (today_mh['DISTRICT'] == 'NAGPUR')|
(today_mh['DISTRICT'] == 'YAVATMAL') | (today_mh['DISTRICT'] == 'WARDHA')|
(today_mh['DISTRICT'] == 'WASHIM')].index

today_mh.drop(mah_drop_today, inplace=True)







   #choose columns to include in today_mh
today_mh=today_mh[['STATION','DATE(YYYY-MM-DD)','TIME (UTC)','RAIN FALL CUM. SINCE 0300 UTC (mm)','TEMP DAY MIN. (\'C)','TEMP DAY MAX. (\'C)','TEMP. (\'C)','RH (%)','SLP (hPa)','MSLP (hPa / gpm)','BATTERY (Volts)','GPS']]

#print(today_mh)




                       #replace names
today_mh.columns=today_mh.columns.str.replace('DATE(YYYY-MM-DD)', 'DATE',regex=False)
today_mh.columns=today_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
today_mh.columns=today_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)
today_mh.columns=today_mh.columns.str.replace('TEMP DAY MAX. (\'C)', 'MAX T',regex=False)
today_mh.columns=today_mh.columns.str.replace('TEMP. (\'C)', 'TEMP',regex=False)
today_mh.columns=today_mh.columns.str.replace('SLP (hPa)', 'SLP',regex=False)
today_mh.columns=today_mh.columns.str.replace('MSLP (hPa / gpm)', 'MSLP',regex=False)

#print(today_mh)

# Perform a left merge to include all stations from canary_mh in today_mh
merged = pd.merge(all_stations, today_mh, on='STATION', how='left')

#print(merged)
#print(merged.nunique())


 
  
   





                
df=merged.copy()
del merged


#print(df)
#print(df.info())
#print(df['STATION'].nunique())






df['DATE'] = pd.to_datetime(df['DATE'],format='%Y-%m-%d')
df['DATE'] = df['DATE'].dt.strftime('%d-%m-%Y')

df['TIME (UTC)'] = pd.to_datetime(df['TIME (UTC)'],format='%H:%M:%S')
df['TIME (UTC)'] = df['TIME (UTC)'].dt.strftime('%H:%M')

#print(df)




# Combine DATE and TIME (UTC) columns into DATETIME (UTC) 
df['DATE , TIME(UTC)'] = df['DATE']+","+ df['TIME (UTC)']



df = df.drop(columns=['DATE','TIME (UTC)'])


#print(df)


#print('unique stations in df: ',df['STATION'].nunique())
#print('unique datetime in df: ',df['DATETIME (UTC)'].nunique())






#Define the start date, end date, and frequency
start_datetime = d0 + ' 03:00'
end_datetime = d1 + ' 03:00'
frequency = '15min'

#Create a datetime range
datetime_range = pd.date_range(start=start_datetime, end=end_datetime, freq=frequency).strftime('%d-%m-%Y'+' , '+'%H:%M')

#print(datetime_range)







# Create a DataFrame with the datetime range
datetime_df = pd.DataFrame(datetime_range, columns=['DATE , TIME(UTC)'])

#print(datetime_df)
#print('rows in datetime_df: ',len(datetime_df))


# Extract unique values
stations = df['STATION'].unique()
datetimes = datetime_df['DATE , TIME(UTC)'].unique()

# Create a DataFrame with all combinations of 'station' and 'datetime'
all_combinations = pd.DataFrame(list(itertools.product(stations, datetimes)), columns=['STATION', 'DATE , TIME(UTC)'])

# Merge with the original df to include all stations and all datetimes
complete_combined = pd.merge(all_combinations, df, on=['STATION', 'DATE , TIME(UTC)'], how='left')


#print(complete_combined)
#print('unique stations in complete_combined: ',complete_combined['STATION'].nunique())
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
        'INS SHIVAJI_LONAVALA': 'PUNE',
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
    
    station = row['STATION']
    if station in station_to_district:
        return station_to_district[station]
    else:
        return ''
    

complete_combined['DISTRICT']=complete_combined.apply(map_dis_to_sta_mh, axis=1)

# Function to check if the station is in aws list
def check_aws(station):
    if station in aws_mh:
        return 'AWS'
    elif station in arg_mh:
        return 'ARG'

# Apply the function to create the new column
complete_combined['AWS/ARG'] = complete_combined['STATION'].apply(check_aws)





#complete_combined['DATETIME (UTC)'] = pd.to_datetime(complete_combined['DATETIME (UTC)'])

complete_combined = complete_combined[['DISTRICT', 'STATION','AWS/ARG', 'DATE , TIME(UTC)', 'RF', 'MIN T', 'MAX T', 'TEMP', 'RH (%)','SLP', 'MSLP', 'BATTERY (Volts)', 'GPS']]

print('Filtering data done.')

print('Applying colors...')

#print(complete_combined)

#print(complete_combined.info())
#print(complete_combined.info())


def rf(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s % 0.5 != 0) & (s.notna()), s.values, np.nan)), props, '')

def temp(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s < 0) & (s.notna()), s.values, np.nan)), props, '')

def rh(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s > 100) & (s.notna()), s.values, np.nan)), props, '')

def slp(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s.diff().abs() > 2) & (s.notna()), s.values, np.nan)), props, '')

def mslp(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s.diff().abs() > 2) & (s.notna()), s.values, np.nan)), props, '')

def battery(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s < 11) & (s.notna()), s.values, np.nan)), props, '')

def gps(s, props='background-color:red;color:yellow;font-weight:bold'):
    return np.where((s == np.where((s == "U") & (s.notna()), s.values, np.nan)), props, '')


        


print('Creating Excel File...')
# File path for the Excel file
# Define the file path
file_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\WEEKLY ANALYSIS('+d0_2+' to'+d1_2+').xlsx')


# Create a Pandas Excel writer using XlsxWriter as the engine
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:

    # Iterate over unique districts and create a sheet for each district
    for district in complete_combined['DISTRICT'].unique():

    # Filter the DataFrame for the current district and drop the 'DISTRICT' column
        district_df = complete_combined[complete_combined['DISTRICT'] == district]
        
        # Apply highlighting and styling to the district_data
        district_df.style.set_table_styles([
            {'selector': 'th.col_heading', 'props': [('font-weight', 'bold'), ('font-size', '14px')]}
        ])
        district_df.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt','border':'1pt solid', 'text-align':"center"})\
        .apply(rf, subset=['RF'])\
        .apply(temp, subset=['MIN T', 'MAX T','TEMP'])\
        .apply(rh, subset=['RH (%)'])\
        .apply(slp, subset=['SLP'])\
        .apply(mslp, subset=['MSLP'])\
        .apply(battery, subset=['BATTERY (Volts)'])\
        .apply(gps, subset=['GPS'])\
        .to_excel(writer, sheet_name=district, index=False, engine='xlsxwriter')

        
        # Access the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets[district]

print('Excel file created for Maharashtra')
exit()
        
        # Set column widths (example widths, adjust as needed)
        #worksheet.set_column('A:A', 30)
        #worksheet.set_column('B:B', 20)
        #worksheet.set_column('C:C', 9)
        #worksheet.set_column('D:D', 7)
        #worksheet.set_column('E:E', 7)
        #worksheet.set_column('F:F', 7)
        #worksheet.set_column('G:G', 9)
        #worksheet.set_column('H:H', 15)
        #worksheet.set_column('I:I', 15)
        #worksheet.set_column('J:J', 20)
        #worksheet.set_column('K:K', 5)

#print('Excel file created for Maharashtra')
