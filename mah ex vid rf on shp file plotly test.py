print('importing required libraries')
import pandas as pd
from datetime import date, time, datetime, timedelta
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import json







print('Creating required date and time')

#Create today's and yesterday's date
t_day = date.today()
d1 = t_day.strftime("%Y-%m-%d")
d1_2 = t_day.strftime("%d-%m-%Y")
y_day=t_day-timedelta(days=1)
d0=y_day.strftime("%Y-%m-%d")
d0_2 = y_day.strftime("%d-%m-%Y")

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

print(len(aws_mh))


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
'PARALIVAIJANATH','KALAMB','TULZAPUR',
'CHAKUR','NILANGA',
'PURNA','SONPETH','AUNDHA_NAGNATH',
'KALAMNURI','BHOKAR']

# Entries to be removed
arg_mh_to_remove = {'BHANDARDARA','PAITHAN',
'PARALIVAIJANATH','SHIRUR','SHIRPUR','AUNDHA_NAGNATH',
'KALAMNURI','GARGOTI(BHUDARGAD)','SHAHUWADI','CHAKUR','NILANGA','BHOKAR','TALODA','KALAMB','TULZAPUR','PURNA','SONPETH','UMADI','PANCHGANI','PHALTAN','AKKALKOT','KARMALA'}

arg_mh = list(filter(lambda x: x not in arg_mh_to_remove, arg_mh))

print(len(arg_mh))


all_mh=['MUMBAI_COLABA','BYCULLA_MUMBAI','MAHALAXMI','MATUNGA_MUMBAI','SION_MUMBAI','MUMBAI_SANTA_CRUZ','TATA POWER CHEMBUR','BANDRA','MUMBAI AIRPORT','VIDYAVIHAR','JUHU_AIRPORT','VIKHROLI','RAM_MANDIR','DAHISAR','KOPARKHAIRANE',
'BHAYANDER','MIRA_ROAD','IIGHQ_NEWPANVEL','KARJAT','IIG_MO_ALIBAG','MATHERAN','BHIRA',
'MURUD','POLADPUR','INS_SHIVAJI_LONAVALA','TALEGAON','GIRIVAN','CHINCHWAD_PUNE','MTI_PASHAN_PUNE','CME_DAPODI','RJSPMCOP_DUDULGAON','LAVALE','SHIVAJINAGAR_PUNE','PASHAN_AWS_LAB','RAJGURUNAGAR','BLINDSCHOOL_KP_PUNE','NDA_PUNE','MAGARPATTA_PUNE','WADGAONSHERI_PUNE','VETALE_KHED','DPS_HADAPSAR_PUNE','LONIKALBHOR_HAVELI','PABAL_SHIRUR','BALLALWADI_JUNNAR','KHADAKWADI_AMBEGAON','NIMGIRI_JUNNAR','TALEGAON_DHAMDHERE','NARAYANGOAN_KRISHI_KENDRA','CHRIST_UNIVERSITY_LAVASA','CAGMO_SHIVAJINAGAR','KHUTBAV_DAUND','WALHE_PURANDAR','MALIN_AMBEGAON','GUDHE_BHOR','NIASM_BARAMATI','NES_LAKADI_INDAPUR','BHANDARDARA','PARNER','KOPERGAON','SHRIGONDA',
'AHMEDNAGAR','RAHURI','SHEVGAON','PALGHAR_AWS400','PALGHAR_KVK','VILHOLI','TRIMBAKESHWAR','NIPHAD','VANI','KALWAN','MALEGAON','DAPOLI','SAVARDE(GOLWANE)',
'POWARWADI(BHAMBHED)','CHIPLUN','RATNAGIRI','RATNAGIRI_AWS400','MAHABALESHWAR','PANCHGANI','SATARA','PHALTAN','BGRL_KARAD','MOHOL_KVK','KARMALA','SOLAPUR','SANGOLA_MAHAVIDYALAYA',
'AKKALKOT','KOLHAPUR_AMFU','SHAHUWADI','PANHALA','RADHANAGRI_ARS','GARGOTI(BHUDARGAD)','GANGAPUR','PAITHAN','AURANGABAD_KVK','AURANGABAD','KANNAD','CHALISGAON','CHOPDA','JALGAON','JAMNER','DHULE','SHIRPUR','SHIRALA','UMADI','TASGAON','SANGLI_KVK','AKKALKUWA','NAVAPUR','TALODA','NANDURBAR','NANDURBAR_KVK','SHAHADA_AWS400','JALNA','BHOKARDAN','GHANSANGAVI','PARTUR','VAIBHAVWADI','AWALEGAON','MULDE_AMFU','DEVGAD',
'VENGURLA','OSMANABAD','KALAMB','TULZAPUR','TULGA_KVK','AMBEJOGAI','BEED_PTO','PARALIVAIJANATH',
'SHIRUR','CHAKUR','LATUR','NILANGA','UDGIR_AWS400','AUNDHA_NAGNATH','HINGOLI','KALAMNURI','TONDAPUR_AWS400','PARBHANI_AMFU','SONPETH','PURNA','NANDED','SAGROLI_KVK','BHOKAR'
]


# Entries to be removed
all_mh_to_remove = {'MURUD','NANDURBAR','BHANDARDARA','PAITHAN',
'PARALIVAIJANATH','SHIRUR','SHIRPUR','AUNDHA_NAGNATH',
'KALAMNURI','GARGOTI(BHUDARGAD)','SHAHUWADI','CHAKUR','NILANGA','BHOKAR','TALODA','KALAMB','TULZAPUR','PURNA','SONPETH','UMADI','PANCHGANI','PHALTAN','AKKALKOT','KARMALA'}

all_mh = list(filter(lambda x: x not in all_mh_to_remove, all_mh))


print(len(all_mh))



print('Checking if the AWS/ARG website is working...')

try:
    #Collect today's data (adjust your URLs accordingly)
    today_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e={d1}&f={d1}&g=03&h=00')[0]
    arg_today_mh = pd.read_html(f'http://aws.imd.gov.in:8091/AWS/dataview.php?a=ARG&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e={d1}&f={d1}&g=03&h=00')[0]

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
combine_tday_mh=combine_tday_mh[['STATION','RAIN FALL CUM. SINCE 0300 UTC (mm)','TEMP DAY MIN. (\'C)']]


                       #replace names
combine_tday_mh.columns =combine_tday_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
combine_tday_mh.columns =combine_tday_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)



#Merge with all_mh to include all stations
all_stations_df = pd.DataFrame({'STATION': all_mh})
combined_all_stations = all_stations_df.merge(combine_tday_mh, on='STATION', how='left')














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



#Merge with all_mh to include all stations
combined_all_stations_all = combined_all_stations.merge(combine_yday_mh, on='STATION', how='left')

















                        #set index
index_mh=combined_all_stations_all.set_index("STATION")

df=index_mh.copy()
del index_mh
#print(df)

df['STATIONS']=df.index

# Reset index to drop the current index
df.reset_index(inplace=True)




#print(df)



def map_dist(row):
    station_to_district = {
        'MUMBAI_COLABA':'MUMBAI_CITY',
        'BYCULLA_MUMBAI':'MUMBAI_CITY',
        'MAHALAXMI':'MUMBAI_CITY',
        'MATUNGA_MUMBAI':'MUMBAI_CITY',
        'SION_MUMBAI':'MUMBAI_CITY',
        'MUMBAI_SANTA_CRUZ':'MUMBAI_CITY',
        'TATA POWER CHEMBUR':'MUMBAI_SUBURBAN',
        'BANDRA':'MUMBAI_SUBURBAN',
        'MUMBAI AIRPORT':'MUMBAI_SUBURBAN',
        'VIDYAVIHAR':'MUMBAI_SUBURBAN',
        'JUHU_AIRPORT':'MUMBAI_SUBURBAN',
        'VIKHROLI':'MUMBAI_SUBURBAN',
        'RAM_MANDIR':'MUMBAI_SUBURBAN',
        'DAHISAR':'MUMBAI_SUBURBAN',
        'KOPARKHAIRANE':'THANE',
        'BHAYANDER':'THANE',
        'MIRA_ROAD':'THANE',
        'IIGHQ_NEWPANVEL':'RAIGAD',
        'KARJAT':'RAIGAD',
        'IIG_MO_ALIBAG':'RAIGAD',
        'MATHERAN':'RAIGAD',
        'BHIRA':'RAIGAD',
        'POLADPUR':'RAIGAD',
        'INS_SHIVAJI_LONAVALA':'PUNE',
        'TALEGAON':'PUNE',
        'GIRIVAN':'PUNE',
        'CHINCHWAD_PUNE':'PUNE',
        'MTI_PASHAN_PUNE':'PUNE',
        'CME_DAPODI':'PUNE',
        'RJSPMCOP_DUDULGAON':'PUNE',
        'LAVALE':'PUNE',
        'SHIVAJINAGAR_PUNE':'PUNE',
        'PASHAN_AWS_LAB':'PUNE',
        'RAJGURUNAGAR':'PUNE',
        'BLINDSCHOOL_KP_PUNE':'PUNE',
        'NDA_PUNE':'PUNE',
        'MAGARPATTA_PUNE':'PUNE',
        'WADGAONSHERI_PUNE':'PUNE',
        'VETALE_KHED':'PUNE',
        'DPS_HADAPSAR_PUNE':'PUNE',
        'LONIKALBHOR_HAVELI':'PUNE',
        'PABAL_SHIRUR':'PUNE',
        'BALLALWADI_JUNNAR':'PUNE',
        'KHADAKWADI_AMBEGAON':'PUNE',
        'NIMGIRI_JUNNAR':'PUNE',
        'TALEGAON_DHAMDHERE':'PUNE',
        'NARAYANGOAN_KRISHI_KENDRA':'PUNE',
        'CHRIST_UNIVERSITY_LAVASA':'PUNE',
        'CAGMO_SHIVAJINAGAR':'PUNE',
        'KHUTBAV_DAUND':'PUNE',
        'WALHE_PURANDAR':'PUNE',
        'MALIN_AMBEGAON':'PUNE',
        'GUDHE_BHOR':'PUNE',
        'NIASM_BARAMATI':'PUNE',
        'NES_LAKADI_INDAPUR':'PUNE',
        'BHANDARDARA':'AHMEDNAGAR',
        'PARNER':'AHMEDNAGAR',
        'KOPERGAON':'AHMEDNAGAR',
        'SHRIGONDA':'AHMEDNAGAR',
        'AHMEDNAGAR':'AHMEDNAGAR',
        'RAHURI':'AHMEDNAGAR',
        'SHEVGAON':'AHMEDNAGAR',
        'PALGHAR_AWS400':'PALGHAR',
        'PALGHAR_KVK':'PALGHAR',
        'VILHOLI':'NASHIK',
        'TRIMBAKESHWAR':'NASHIK',
        'NIPHAD':'NASHIK',
        'VANI':'NASHIK',
        'KALWAN':'NASHIK',
        'MALEGAON':'NASHIK',
        'DAPOLI':'RATNAGIRI',
        'SAVARDE(GOLWANE)':'RATNAGIRI',
        'POWARWADI(BHAMBHED)':'RATNAGIRI',
        'CHIPLUN':'RATNAGIRI',
        'RATNAGIRI':'RATNAGIRI',
        'RATNAGIRI_AWS400':'RATNAGIRI',
        'MAHABALESHWAR':'SATARA',
        'PANCHGANI':'SATARA',
        'SATARA':'SATARA',
        'PHALTAN':'SATARA',
        'BGRL_KARAD':'SATARA',
        'MOHOL_KVK':'SOLAPUR',
        'KARMALA':'SOLAPUR',
        'SOLAPUR':'SOLAPUR',
        'SANGOLA_MAHAVIDYALAYA':'SOLAPUR',
        'AKKALKOT':'SOLAPUR',
        'KOLHAPUR_AMFU':'KOLHAPUR',
        'SHAHUWADI':'KOLHAPUR',
        'PANHALA':'KOLHAPUR',
        'RADHANAGRI_ARS':'KOLHAPUR',
        'GARGOTI(BHUDARGAD)':'KOLHAPUR',
        'GANGAPUR':'AURANGABAD',
        'PAITHAN':'AURANGABAD',
        'AURANGABAD_KVK':'AURANGABAD',
        'AURANGABAD':'AURANGABAD',
        'KANNAD':'AURANGABAD',
        'CHALISGAON':'JALGAON',
        'CHOPDA':'JALGAON',
        'JALGAON':'JALGAON',
        'JAMNER':'JALGAON',
        'DHULE':'DHULE',
        'SHIRPUR':'DHULE',
        'SHIRALA':'SANGLI',
        'UMADI':'SANGLI',
        'TASGAON':'SANGLI',
        'SANGLI_KVK':'SANGLI',
        'AKKALKUWA':'NANDURBAR',
        'NAVAPUR':'NANDURBAR',
        'TALODA':'NANDURBAR',
        'NANDURBAR':'NANDURBAR',
        'NANDURBAR_KVK':'NANDURBAR',
        'SHAHADA_AWS400':'NANDURBAR',
        'JALNA':'JALNA',
        'BHOKARDAN':'JALNA',
        'GHANSANGAVI':'JALNA',
        'PARTUR':'JALNA',
        'VAIBHAVWADI':'SIDHUDURG',
        'AWALEGAON':'SIDHUDURG',
        'MULDE_AMFU':'SINDHUDURG',
        'DEVGAD':'SINDHUDURG',
        'VENGURLA':'SIDHUDURG',
        'OSMANABAD':'OSMANABAD',
        'KALAMB':'OSMANABAD',
        'TULZAPUR':'OSMANABAD',
        'TULGA_KVK':'OSMANABAD',
        'AMBEJOGAI':'BEED',
        'BEED_PTO':'BEED',
        'PARALIVAIJANATH':'BEED',
        'SHIRUR':'BEED',
        'CHAKUR':'LATUR',
        'LATUR':'LATUR',
        'NILANGA':'LATUR',
        'UDGIR_AWS400':'LATUR',
        'AUNDHA_NAGNATH':'HINGOLI',
        'HINGOLI':'HINGOLI',
        'KALAMNURI':'HINGOLI',
        'TONDAPUR_AWS400':'HINGOLI',
        'PARBHANI_AMFU':'PARBHANI',
        'SONPETH':'PARBHANI',
        'PURNA':'PARBHANI',
        'NANDED':'NANDED',
        'SAGROLI_KVK':'NANDED',
        'BHOKAR':'NANDED',
    }
    # Entries to be removed
    station_to_district_to_remove = {'MURUD', 'NANDURBAR', 'BHANDARDARA', 'PAITHAN',
                                     'PARALIVAIJANATH', 'SHIRUR', 'SHIRPUR', 'AUNDHA_NAGNATH',
                                     'KALAMNURI', 'GARGOTI(BHUDARGAD)', 'SHAHUWADI', 'CHAKUR',
                                     'NILANGA', 'BHOKAR', 'TALODA', 'KALAMB','TULZAPUR', 'PURNA', 'SONPETH',
                                     'UMADI', 'PANCHGANI', 'PHALTAN', 'AKKALKOT', 'KARMALA'}

    # Create a new dictionary excluding the unwanted entries
    filtered_station_to_district = {k: v for k, v in station_to_district.items() if k not in station_to_district_to_remove}

    # Check if the station is in the filtered dictionary
    station = row['STATIONS']
    if station in filtered_station_to_district:
        return filtered_station_to_district[station]
    else:
        return ''  # Or some other default value if needed
    
      




def map_type(row):
    station_to_type = {
        'MUMBAI_COLABA':'AWS',
'BYCULLA_MUMBAI':'ARG',
'MAHALAXMI':'ARG',
'MATUNGA_MUMBAI':'ARG',
'SION_MUMBAI':'ARG',
'MUMBAI_SANTA_CRUZ':'AWS',
'TATA POWER CHEMBUR':'ARG',
'BANDRA':'ARG',
'MUMBAI AIRPORT':'ARG',
'VIDYAVIHAR':'ARG',
'JUHU_AIRPORT':'ARG',
'VIKHROLI':'ARG',
'RAM_MANDIR':'ARG',
'DAHISAR':'ARG',
'KOPARKHAIRANE':'ARG',
'BHAYANDER':'ARG',
'MIRA_ROAD':'ARG',
'IIGHQ_NEWPANVEL':'ARG',
'KARJAT':'AWS',
'IIG_MO_ALIBAG':'AWS',
'MATHERAN':'AWS',
'BHIRA':'ARG',
'MURUD':'UR',
'POLADPUR':'ARG',
'INS_SHIVAJI_LONAVALA':'AWS',
'TALEGAON':'ARG',
'GIRIVAN':'ARG',
'CHINCHWAD_PUNE':'ARG',
'MTI_PASHAN_PUNE':'ARG',
'CME_DAPODI':'AWS',
'RJSPMCOP_DUDULGAON':'ARG',
'LAVALE':'ARG',
'SHIVAJINAGAR_PUNE':'ARG',
'PASHAN_AWS_LAB':'AWS',
'RAJGURUNAGAR':'AWS',
'BLINDSCHOOL_KP_PUNE':'ARG',
'NDA_PUNE':'ARG',
'MAGARPATTA_PUNE':'ARG',
'WADGAONSHERI_PUNE':'ARG',
'VETALE_KHED':'ARG',
'DPS_HADAPSAR_PUNE':'AWS',
'LONIKALBHOR_HAVELI':'AWS',
'PABAL_SHIRUR':'ARG',
'BALLALWADI_JUNNAR':'ARG',
'KHADAKWADI_AMBEGAON':'ARG',
'NIMGIRI_JUNNAR':'AWS',
'TALEGAON_DHAMDHERE':'AWS',
'NARAYANGOAN_KRISHI_KENDRA':'AWS',
'CHRIST_UNIVERSITY_LAVASA':'AWS',
'CAGMO_SHIVAJINAGAR':'AWS',
'KHUTBAV_DAUND':'AWS',
'WALHE_PURANDAR':'ARG',
'MALIN_AMBEGAON':'ARG',
'GUDHE_BHOR':'ARG',
'NIASM_BARAMATI':'AWS',
'NES_LAKADI_INDAPUR':'ARG',
'BHANDARDARA':'UR',
'PARNER':'ARG',
'KOPERGAON':'AWS',
'SHRIGONDA':'ARG',
'AHMEDNAGAR':'AWS',
'RAHURI':'AWS',
'SHEVGAON':'ARG',
'PALGHAR_AWS400':'AWS',
'PALGHAR_KVK':'AWS',
'VILHOLI':'AWS',
'TRIMBAKESHWAR':'ARG',
'NIPHAD':'ARG',
'VANI':'ARG',
'KALWAN':'AWS',
'MALEGAON':'AWS',
'DAPOLI':'AWS',
'SAVARDE(GOLWANE)':'ARG',
'POWARWADI(BHAMBHED)':'ARG',
'CHIPLUN':'ARG',
'RATNAGIRI':'AWS',
'RATNAGIRI_AWS400':'AWS',
'MAHABALESHWAR':'AWS',
'PANCHGANI':'UR',
'SATARA':'AWS',
'PHALTAN':'UR',
'BGRL_KARAD':'AWS',
'MOHOL_KVK':'AWS',
'KARMALA':'UR',
'SOLAPUR':'AWS',
'SANGOLA_MAHAVIDYALAYA':'AWS',
'AKKALKOT':'UR',
'KOLHAPUR_AMFU':'AWS',
'SHAHUWADI':'UR',
'PANHALA':'ARG',
'RADHANAGRI_ARS':'AWS',
'GARGOTI(BHUDARGAD)':'UR',
'GANGAPUR':'ARG',
'PAITHAN':'UR',
'AURANGABAD_KVK':'AWS',
'AURANGABAD':'AWS',
'KANNAD':'ARG',
'CHALISGAON':'ARG',
'CHOPDA':'AWS',
'JALGAON':'AWS',
'JAMNER':'ARG',
'DHULE':'AWS',
'SHIRPUR':'UR',
'SHIRALA':'ARG',
'UMADI':'UR',
'TASGAON':'ARG',
'SANGLI_KVK':'AWS',
'AKKALKUWA':'ARG',
'NAVAPUR':'AWS',
'TALODA':'UR',
'NANDURBAR':'UR',
'NANDURBAR_KVK':'AWS',
'SHAHADA_AWS400':'AWS',
'JALNA':'ARG',
'BHOKARDAN':'ARG',
'GHANSANGAVI':'ARG',
'PARTUR':'ARG',
'VAIBHAVWADI':'ARG',
'AWALEGAON':'ARG',
'MULDE_AMFU':'AWS',
'DEVGAD':'AWS',
'VENGURLA':'ARG',
'OSMANABAD':'AWS',
'KALAMB':'UR',
'TULZAPUR':'UR',
'TULGA_KVK':'AWS',
'AMBEJOGAI':'AWS',
'BEED_PTO':'AWS',
'PARALIVAIJANATH':'UR',
'SHIRUR':'UR',
'CHAKUR':'UR',
'LATUR':'AWS',
'NILANGA':'UR',
'UDGIR_AWS400':'AWS',
'AUNDHA_NAGNATH':'UR',
'HINGOLI':'AWS',
'KALAMNURI':'UR',
'TONDAPUR_AWS400':'AWS',
'PARBHANI_AMFU':'AWS',
'SONPETH':'UR',
'PURNA':'UR',
'NANDED':'AWS',
'SAGROLI_KVK':'AWS',
'BHOKAR':'UR'

    }


    # Entries to be removed
    station_to_type_to_remove = {'MURUD', 'NANDURBAR', 'BHANDARDARA', 'PAITHAN',
                                     'PARALIVAIJANATH', 'SHIRUR', 'SHIRPUR', 'AUNDHA_NAGNATH',
                                     'KALAMNURI', 'GARGOTI(BHUDARGAD)', 'SHAHUWADI', 'CHAKUR',
                                     'NILANGA', 'BHOKAR', 'TALODA', 'KALAMB','TULZAPUR', 'PURNA', 'SONPETH',
                                     'UMADI', 'PANCHGANI', 'PHALTAN', 'AKKALKOT', 'KARMALA'}

    # Create a new dictionary excluding the unwanted entries
    filtered_station_to_type = {k: v for k, v in station_to_type.items() if k not in station_to_type_to_remove}

    # Check if the station is in the filtered dictionary
    station = row['STATIONS']
    if station in filtered_station_to_type:
        return filtered_station_to_type[station]
    else:
        return ''  # Or some other default value if needed



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
    station = row['STATIONS']
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
    station = row['STATIONS']
    if station in filtered_station_to_long:
        return filtered_station_to_long[station]
    else:
        return ''  # Or some other default value if needed



df['DISTRICT']=df.apply(map_dist, axis=1)
df['TYPE']=df.apply(map_type, axis=1)
df['LAT']=df.apply(map_lat, axis=1)
df['LONG']=df.apply(map_long, axis=1)
df.insert(0, 'S.No.', range(1, 1 + len(df)))



# Reorder columns as needed
df = df[['S.No.','DISTRICT','STATIONS','TYPE','RF','MIN T','MAX T','LAT','LONG']]

df['RF'] = pd.to_numeric(df['RF'], errors='coerce')
df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
df['LONG'] = pd.to_numeric(df['LONG'], errors='coerce')

#print(df)
#print(df.info())
#df.to_excel('C:\\Users\\hp\\Desktop\\gurinder\\python test\\removed.xlsx')


# Define the custom color function
def rf_color_range(rf_value):
    if rf_value == 0:
        return 'silver'
    elif 0 < rf_value < 1:
        return '#71797E'
    elif 1 <= rf_value <= 2.4:
        return '#ADFF2F'
    elif 2.5 <= rf_value <= 15.5:
        return '#00FF00'
    elif 15.6 <= rf_value <= 64.4:
        return '#00FFFF'
    elif 64.5 <= rf_value <= 115.5:
        return '#FFFF00'
    elif 115.6 <= rf_value <= 204.4:
        return '#FFA500'
    elif rf_value > 204.4:
        return '#FF0000'
    else:
        return '#00008B'

# Define the custom opacity function
def rf_opacity_range(rf_value):
    if pd.isna(rf_value):
        return 1
    else:
        return 1

# Load shapefile
shapefile_path = 'C:\\Users\\hp\\Desktop\\gurinder\\python test\\maharashtra district excluding vidarbha.shp'
gdf = gpd.read_file(shapefile_path)

# Convert the GeoDataFrame to GeoJSON format
geojson = json.loads(gdf.to_json())

# Calculate the centroid of each district polygon
gdf['centroid'] = gdf.geometry.centroid
gdf['centroid_lon'] = gdf.centroid.x
gdf['centroid_lat'] = gdf.centroid.y

# Create the figure
fig = go.Figure()

# Add shapefile boundaries
for feature in geojson['features']:
    coords = feature['geometry']['coordinates']
    if feature['geometry']['type'] == 'Polygon':
        lon, lat = zip(*coords[0])
        fig.add_trace(go.Scattermapbox(
            lon=lon,
            lat=lat,
            mode='lines',
            line=dict(width=1, color='black'),
            fill='toself',
            fillcolor='rgba(255, 255, 255, 0.3)',
            showlegend=False
        ))
    elif feature['geometry']['type'] == 'MultiPolygon':
        for polygon in coords:
            lon, lat = zip(*polygon[0])
            fig.add_trace(go.Scattermapbox(
                lon=lon,
                lat=lat,
                mode='lines',
                line=dict(width=1, color='black'),
                fill='toself',
                fillcolor='rgba(255, 255, 255, 0.3)',
                showlegend=False
            ))

# Add district names as text annotations with better visibility
for _, row in gdf.iterrows():
    fig.add_trace(go.Scattermapbox(
        lon=[row['centroid_lon']],
        lat=[row['centroid_lat']],
        mode='text',
        text=row['DISTRICT'],
        showlegend=False,
        textfont=dict(size=12, color='black'),  # Adjust text size and color as needed
    ))

# Apply custom color and opacity functions to the dataframe
df['color'] = df['RF'].apply(rf_color_range)
df['opacity'] = df['RF'].apply(rf_opacity_range)

def generate_rf_hover_text(row):
    station_type = row['TYPE']
    station_name = row['STATIONS']
    rainfall = "DATA NOT AVAILABLE" if pd.isna(row['RF']) else f"{row['RF']} mm"
    return f"<b>{station_type}</b><br>Station: {station_name}<br>Rainfall: {rainfall}"

df['rf_hover_text'] = df.apply(generate_rf_hover_text, axis=1)

# Mask for values that are NaN
nan_mask = pd.isna(df['RF'])

# Mask for values that are not multiples of 0.5
faulty_data_mask = (df['RF'] % 0.5 != 0) & ~nan_mask

# Add markers for valid rainfall values (neither NaN nor faulty)
valid_mask = ~nan_mask & ~faulty_data_mask
fig.add_trace(go.Scattermapbox(
    lon=df['LONG'][valid_mask],
    lat=df['LAT'][valid_mask],
    mode='markers',
    marker=dict(
        size=10,
        color=df['color'][valid_mask],
        opacity=df['opacity'][valid_mask]
    ),
    hoverinfo='text',
    hovertext=df['rf_hover_text'][valid_mask],
    showlegend=False
))

# Add text 'x' for faulty data (not multiples of 0.5)
fig.add_trace(go.Scattermapbox(
    lon=df['LONG'][faulty_data_mask],
    lat=df['LAT'][faulty_data_mask],
    mode='text',
    text='X',
    textposition='middle center',
    textfont=dict(size=15, color='red'),
    hoverinfo='text',
    hovertext=df['rf_hover_text'][faulty_data_mask],
    showlegend=False
))

# Add text 'O' for NaN values with black color
fig.add_trace(go.Scattermapbox(
    lon=df['LONG'][nan_mask],
    lat=df['LAT'][nan_mask],
    mode='text',
    text='O',
    textposition='middle center',
    textfont=dict(size=15, color='red'),
    hoverinfo='text',
    hovertext=df['rf_hover_text'][nan_mask],
    showlegend=False
))

# Add dummy traces for the legend
legend_colors = {
    '<b>1 <= RF <= 2.4</b>': '#ADFF2F',
    '<b>2.5 <= RF <= 15.5</b>': '#00FF00',
    '<b>15.6 <= RF <= 64.4</b>': '#00FFFF',
    '<b>64.5 <= RF <= 115.5</b>': '#FFFF00',
    '<b>115.6 <= RF <= 204.4</b>': '#FFA500',
    '<b>RF > 204.5 mm</b>': '#FF0000',
    '<b>Data Not Available</b>': '#FFFFFF',
    '<b>Faulty data</b>': '#FFFFFF',
    '<b>0 mm</b>': 'silver',
    '<b>0 < RF < 1</b>': '#71797E',
}

for label, color in legend_colors.items():
    fig.add_trace(go.Scattermapbox(
        lon=[None],
        lat=[None],
        mode='markers',
        marker=dict(size=30, color=color),
        showlegend=True,
        name=label
    ))

# Center of the bounding box
bounds = gdf.total_bounds
center_lon = (bounds[0] + bounds[2]) / 2
center_lat = (bounds[1] + bounds[3]) / 2

# Update layout for the map
fig.update_layout(
    mapbox=dict(
        style='white-bg',
        center=dict(lat=center_lat, lon=center_lon),
        zoom=6  # Adjust the zoom level to an optimal value
    ),
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    title={
        'text': "<b>Rainfall Data for Maharashtra (excluding Vidarbha): "f"{d0_2} 3UTC to {d1_2} 3UTC</b>",
        'y': 0.98,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)


# Add the text "x" as an annotation
fig.add_annotation(
    x=1.035,  # x-coordinate in paper coordinates (0 to 1 range for the figure)
    y=0.815,  # y-coordinate in paper coordinates (0 to 1 range for the figure)
    text="O",  # Text to display
    showarrow=False,  # Hide the arrow
    font=dict(size=15, color="red"),  # Customize the text font and color
    xref="paper",  # x reference to the figure, can also be 'x' for data coordinates
    yref="paper",  # y reference to the figure, can also be 'y' for data coordinates
    xanchor="center",  # Horizontal alignment of the text
    yanchor="middle"   # Vertical alignment of the text
)


# Add the text "x" as an annotation
fig.add_annotation(
    x=1.035,  # x-coordinate in paper coordinates (0 to 1 range for the figure)
    y=0.788,  # y-coordinate in paper coordinates (0 to 1 range for the figure)
    text="X",  # Text to display
    showarrow=False,  # Hide the arrow
    font=dict(size=15, color="red"),  # Customize the text font and color
    xref="paper",  # x reference to the figure, can also be 'x' for data coordinates
    yref="paper",  # y reference to the figure, can also be 'y' for data coordinates
    xanchor="center",  # Horizontal alignment of the text
    yanchor="middle"   # Vertical alignment of the text
)

# Save the figure to an HTML file
fig.write_html('C:\\Users\\hp\\Desktop\\gurinder\\python test\\RF PLOT.html')


































# Define the custom color function
def temp_range(temp_value):
    if 0.1 <= temp_value <= 10.0:
        return '#00FF00'
    elif 10.1 <= temp_value <= 20.0:
        return '#00FFFF'
    elif 20.1 <= temp_value <= 30.0:
        return '#FFFF00'
    elif 30.1 <= temp_value <= 40.0:
        return '#FFA500'
    elif temp_value >= 40.1:
        return '#FF0000'
    else:
        return '#00008B'

# Define the custom opacity function
def temp_opacity_range(temp_value):
    if pd.isna(temp_value):
        return 1
    else:
        return 1

# Load shapefile
#shapefile_path = 'C:\\Users\\hp\\Desktop\\gurinder\\python test\\maharashtra district excluding vidarbha.shp'
#gdf = gpd.read_file(shapefile_path)

# Convert the GeoDataFrame to GeoJSON format
#geojson = json.loads(gdf.to_json())

# Calculate the centroid of each district polygon
#gdf['centroid'] = gdf.geometry.centroid
#gdf['centroid_lon'] = gdf.centroid.x
#gdf['centroid_lat'] = gdf.centroid.y

# Create the figure
fig = go.Figure()

# Add shapefile boundaries
for feature in geojson['features']:
    coords = feature['geometry']['coordinates']
    if feature['geometry']['type'] == 'Polygon':
        lon, lat = zip(*coords[0])
        fig.add_trace(go.Scattermapbox(
            lon=lon,
            lat=lat,
            mode='lines',
            line=dict(width=1, color='black'),
            fill='toself',
            fillcolor='rgba(255, 255, 255, 0.3)',
            showlegend=False
        ))
    elif feature['geometry']['type'] == 'MultiPolygon':
        for polygon in coords:
            lon, lat = zip(*polygon[0])
            fig.add_trace(go.Scattermapbox(
                lon=lon,
                lat=lat,
                mode='lines',
                line=dict(width=1, color='black'),
                fill='toself',
                fillcolor='rgba(255, 255, 255, 0.3)',
                showlegend=False
            ))

# Add district names as text annotations with better visibility
for _, row in gdf.iterrows():
    fig.add_trace(go.Scattermapbox(
        lon=[row['centroid_lon']],
        lat=[row['centroid_lat']],
        mode='text',
        text=row['DISTRICT'],
        showlegend=False,
        textfont=dict(size=12, color='black'),  # Adjust text size and color as needed
    ))

# Apply custom color and opacity functions to the dataframe
df['color'] = df['MIN T'].apply(temp_range)
df['opacity'] = df['MIN T'].apply(temp_opacity_range)

def generate_temp_hover_text(row):
    station_type = row['TYPE']
    station_name = row['STATIONS']
    mint = "DATA NOT AVAILABLE" if pd.isna(row['MIN T']) else f"{row['MIN T']} mm"
    return f"<b>{station_type}</b><br>Station: {station_name}<br>MIN T: {mint}"

df['temp_hover_text'] = df.apply(generate_temp_hover_text, axis=1)

# Mask for values that are NaN
nan_mask = pd.isna(df['MIN T'])

# Mask for values that are not multiples of 0.5
faulty_data_mask = (df['MIN T'] <0) & ~nan_mask

# Add markers for valid rainfall values (neither NaN nor faulty)
valid_mask = ~nan_mask & ~faulty_data_mask
fig.add_trace(go.Scattermapbox(
    lon=df['LONG'][valid_mask],
    lat=df['LAT'][valid_mask],
    mode='markers',
    marker=dict(
        size=10,
        color=df['color'][valid_mask],
        opacity=df['opacity'][valid_mask]
    ),
    hoverinfo='text',
    hovertext=df['temp_hover_text'][valid_mask],
    showlegend=False
))

# Add text 'x' for faulty data (not multiples of 0.5)
fig.add_trace(go.Scattermapbox(
    lon=df['LONG'][faulty_data_mask],
    lat=df['LAT'][faulty_data_mask],
    mode='text',
    text='X',
    textposition='middle center',
    textfont=dict(size=15, color='red'),
    hoverinfo='text',
    hovertext=df['temp_hover_text'][faulty_data_mask],
    showlegend=False
))

# Add text 'x' for NaN values with black color
fig.add_trace(go.Scattermapbox(
    lon=df['LONG'][nan_mask],
    lat=df['LAT'][nan_mask],
    mode='text',
    text='O',
    textposition='middle center',
    textfont=dict(size=15, color='red'),
    hoverinfo='text',
    hovertext=df['temp_hover_text'][nan_mask],
    showlegend=False
))

# Add dummy traces for the legend
legend_colors = {
    '<b>0.1 <= temp_value <= 10.0</b>': '#00FF00',
    '<b>10.1 <= temp_value <= 20.0</b>': '#00FFFF',
    '<b>20.1 <= temp_value <= 30.0</b>': '#FFFF00',
    '<b>30.1 <= temp_value <= 40.0</b>': '#FFA500',
    '<b>temp_value >= 40.1</b>': '#FF0000',
    '<b>Data Not Available</b>': '#FFFFFF',
    '<b>Faulty data</b>': '#FFFFFF',
}



for label, color in legend_colors.items():
    fig.add_trace(go.Scattermapbox(
        lon=[None],
        lat=[None],
        mode='markers',
        marker=dict(size=30, color=color),
        showlegend=True,
        name=label
    ))

# Center of the bounding box
bounds = gdf.total_bounds
center_lon = (bounds[0] + bounds[2]) / 2
center_lat = (bounds[1] + bounds[3]) / 2

# Update layout for the map
fig.update_layout(
    mapbox=dict(
        style='white-bg',
        center=dict(lat=center_lat, lon=center_lon),
        zoom=6  # Adjust the zoom level to an optimal value
    ),
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    title={
        'text': "<b>MIN T Data for Maharashtra (excluding Vidarbha): "f"{d0_2} 3UTC to {d1_2} 3UTC</b>",
        'y': 0.98,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)


# Add the text "x" as an annotation
fig.add_annotation(
    x=1.035,  # x-coordinate in paper coordinates (0 to 1 range for the figure)
    y=0.815,  # y-coordinate in paper coordinates (0 to 1 range for the figure)
    text="x",  # Text to display
    showarrow=False,  # Hide the arrow
    font=dict(size=15, color="red"),  # Customize the text font and color
    xref="paper",  # x reference to the figure, can also be 'x' for data coordinates
    yref="paper",  # y reference to the figure, can also be 'y' for data coordinates
    xanchor="center",  # Horizontal alignment of the text
    yanchor="middle"   # Vertical alignment of the text
)


# Add the text "x" as an annotation
fig.add_annotation(
    x=1.035,  # x-coordinate in paper coordinates (0 to 1 range for the figure)
    y=0.788,  # y-coordinate in paper coordinates (0 to 1 range for the figure)
    text="x",  # Text to display
    showarrow=False,  # Hide the arrow
    font=dict(size=15, color="red"),  # Customize the text font and color
    xref="paper",  # x reference to the figure, can also be 'x' for data coordinates
    yref="paper",  # y reference to the figure, can also be 'y' for data coordinates
    xanchor="center",  # Horizontal alignment of the text
    yanchor="middle"   # Vertical alignment of the text
)

# Save the figure to an HTML file
fig.write_html('C:\\Users\\hp\\Desktop\\gurinder\\python test\\MIN T PLOT.html')