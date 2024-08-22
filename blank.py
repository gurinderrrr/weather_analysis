# import libraries
import pandas as pd
import numpy as np
import pandas.io.formats.style
import csv
from datetime import date,datetime
from datetime import timedelta
import os
import time


t_day = date.today()
d1 = t_day.strftime("%Y-%m-%d")
d1_2 = t_day.strftime("%d-%m-%Y")
y_day=t_day-timedelta(days=1)
d0=y_day.strftime("%Y-%m-%d")
d0_2 = y_day.strftime("%d-%m-%Y")








                     #generate list of aws and STATIONS
aws_mh=["MUMBAI_COLABA","MUMBAI_SANTA_CRUZ",'RATNAGIRI','MAHABALESHWAR','SATARA','SOLAPUR']
#Merge with all_mh to include all stations
aws_mh_df = pd.DataFrame({'STATION': aws_mh})



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
combine_tday_03_mh=combine_tday_03_mh[['STATION','RAIN FALL CUM. SINCE 0300 UTC (mm)','TEMP DAY MIN. (\'C)']]


                       #replace names
combine_tday_03_mh.columns =combine_tday_03_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
combine_tday_03_mh.columns =combine_tday_03_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)



combined_all_03_stations = aws_mh_df.merge(combine_tday_03_mh, on='STATION', how='left')

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




combined_all_12_stations = aws_mh_df.merge(combine_yday_mh, on='STATION', how='left')

#print(combined_all_12_stations)


combine_final=combined_all_03_stations.merge(combined_all_12_stations, on='STATION', how='left')


combine_final.to_excel('C:\\Users\\hp\\Desktop\\combined final.xlsx', index=False)