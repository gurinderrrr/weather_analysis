# import libraries
import pandas as pd
import csv
from datetime import datetime
from datetime import date
from datetime import timedelta
import os




                          #generate list of aws and STATIONS
aws_mh=["MUMBAI_COLABA","MUMBAI_SANTA_CRUZ", "PALGHAR_AWS400","MATHERAN",
                          'PALGHAR_KVK','IIG_MO_ALIBAG','KARJAT','MURUD',
                          'DAPOLI','RATNAGIRI','DEVGAD',
                          'MULDE_AMFU','AHMEDNAGAR','KOPERGAON','RAHURI',
                          'DHULE','CHOPDA','JALGAON','NANDURBAR',
                          'NANDURBAR_KVK','NAVAPUR','KALWAN',
                          'MALEGAON','VILHOLI','NIMGIRI_JUNNAR','CAGMO_SHIVAJINAGAR',
                          'CHRIST_UNIVERSITY_LAVASA','CME_DAPODI','DPS_HADAPSAR_PUNE',
                          'INS SHIVAJI_LONAVALA','KHUTBAV_DAUND','LONIKALBHOR_HAVELI',
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



            #create todays and yesterdays date
start_date =input('Enter the start date as ddmmyyyy: ')
sd=datetime.strptime(start_date, "%d%m%Y").strftime("%Y-%m-%d")
end_date =input('Enter the end date as ddmmyyyy: ')
ed=datetime.strptime(end_date, "%d%m%Y").strftime("%Y-%m-%d")


df=pd.DataFrame({'t_day':pd.date_range(sd,ed)})
print(df)
print(len(df))
with pd.ExcelWriter(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads\MAHARASHTRA.xlsx')) as writer:

        for i, n in zip(df['t_day'].astype(str), range(1,len(df)+1)):  
                today=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+i+'&f='+i+'&g=03&h=00')
                dft=today[0]
                arg_today=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=ARG&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+i+'&f='+i+'&g=03&h=00')
                arg_dft=arg_today[0]






                                                #combine the two dataframes
                combine_tday_mh=pd.concat([dft,arg_dft], ignore_index=True)





                                                #drop vidarbha stations
                mah_drop_today = combine_tday_mh[(combine_tday_mh['DISTRICT'] == 'AKOLA') | (combine_tday_mh['DISTRICT'] == 'AMRAVATI')|
               (combine_tday_mh['DISTRICT'] == 'BHANDARA') | (combine_tday_mh['DISTRICT'] == 'BULDHANA')|
               (combine_tday_mh['DISTRICT'] == 'CHANDRAPUR') | (combine_tday_mh['DISTRICT'] == 'GADCHIROLI')|
               (combine_tday_mh['DISTRICT'] == 'GONDIA') | (combine_tday_mh['DISTRICT'] == 'NAGPUR')|
               (combine_tday_mh['DISTRICT'] == 'YAVATMAL') | (combine_tday_mh['DISTRICT'] == 'WARDHA')|
               (combine_tday_mh['DISTRICT'] == 'WASHIM')].index
                combine_tday_mh.drop(mah_drop_today, inplace=True)
                #print(dft)
                






                                        #select colums to include in combine_tday_mh
                combine_tday_mh=combine_tday_mh[['STATION','RAIN FALL CUM. SINCE 0300 UTC (mm)','TEMP DAY MIN. (\'C)','RH (%)','MSLP (hPa / gpm)','BATTERY (Volts)','GPS']]


                                        #replace names
                combine_tday_mh.columns =combine_tday_mh.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
                combine_tday_mh.columns =combine_tday_mh.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)
                combine_tday_mh.columns =combine_tday_mh.columns.str.replace('RH (%)', 'RH_03UTC',regex=False)
                combine_tday_mh.columns =combine_tday_mh.columns.str.replace('MSLP (hPa / gpm)', 'MSLP_03UTC',regex=False)





                                        #set index
                dft_index=combine_tday_mh.set_index("STATION")






                                        #reindex
                new_dft=dft_index.reindex(['MUMBAI_COLABA','BYCULLA_MUMBAI','MAHALAXMI','MATUNGA_MUMBAI','SION_MUMBAI','MUMBAI_SANTA_CRUZ','TATA POWER CHEMBUR','BANDRA','MUMBAI AIRPORT','VIDYAVIHAR','JUHU_AIRPORT','VIKHROLI','RAM_MANDIR','DAHISAR','KOPARKHAIRANE',
'BHAYANDER','MIRA_ROAD','IIGHQ_NEWPANVEL','KARJAT','IIG_MO_ALIBAG','MATHERAN','BHIRA',
'MURUD','POLADPUR','INS SHIVAJI_LONAVALA','TALEGAON','GIRIVAN','CHINCHWAD_PUNE','MTI_PASHAN_PUNE','CME_DAPODI','RJSPMCOP_DUDULGAON','LAVALE','SHIVAJINAGAR_PUNE','PASHAN_AWS_LAB','RAJGURUNAGAR','BLINDSCHOOL_KP_PUNE','NDA_PUNE','MAGARPATTA_PUNE','WADGAONSHERI_PUNE','VETALE_KHED','DPS_HADAPSAR_PUNE','LONIKALBHOR_HAVELI','PABAL_SHIRUR','BALLALWADI_JUNNAR','KHADAKWADI_AMBEGAON','NIMGIRI_JUNNAR','TALEGAON_DHAMDHERE','NARAYANGOAN_KRISHI_KENDRA','CHRIST_UNIVERSITY_LAVASA','CAGMO_SHIVAJINAGAR','KHUTBAV_DAUND','WALHE_PURANDAR','MALIN_AMBEGAON','GUDHE_BHOR','NIASM_BARAMATI','NES_LAKADI_INDAPUR','BHANDARDARA','PARNER','KOPERGAON','SHRIGONDA',
'AHMEDNAGAR','RAHURI','SHEVGAON','PALGHAR_AWS400','PALGHAR_KVK','VILHOLI','TRIMBAKESHWAR','NIPHAD','VANI','KALWAN','MALEGAON','DAPOLI','SAVARDE(GOLWANE)',
'POWARWADI(BHAMBHED)','CHIPLUN','RATNAGIRI','RATNAGIRI_AWS400','MAHABALESHWAR','PANCHGANI','SATARA','PHALTAN','BGRL_KARAD','MOHOL_KVK','KARMALA','SOLAPUR','SANGOLA_MAHAVIDYALAYA',
'AKKALKOT','KOLHAPUR_AMFU','SHAHUWADI','PANHALA','RADHANAGRI_ARS','GARGOTI(BHUDARGAD)','GANGAPUR','PAITHAN','AURANGABAD_KVK','AURANGABAD','KANNAD','CHALISGAON','CHOPDA','JALGAON','JAMNER','DHULE','SHIRPUR','SHIRALA','UMADI','TASGAON','SANGLI_KVK','AKKALKUWA','NAVAPUR','TALODA','NANDURBAR','NANDURBAR_KVK','SHAHADA_AWS400','JALNA','BHOKARDAN','GHANSANGAVI','PARTUR','VAIBHAVWADI','AWALEGAON','MULDE_AMFU','DEVGAD',
'VENGURLA','OSMANABAD','KALAMB','TULGA_KVK','AMBEJOGAI','BEED_PTO','PARALIVAIJANATH',
'SHIRUR','CHAKUR','LATUR','NILANGA','UDGIR_AWS400','AUNDHA_NAGNATH','HINGOLI','KALAMNURI','TONDAPUR_AWS400','PARBHANI_AMFU','SONPETH','PURNA','NANDED','SAGROLI_KVK','BHOKAR'])
                
                
                j=(datetime.strptime(i, "%Y-%m-%d")-timedelta(days=1)).strftime("%Y-%m-%d")
                
                        #collect yesterdays aws tabular data
                yesterday=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+j+'&f='+j+'&g=12&h=00')
                dfy=yesterday[0]
                       #collect arg_yesterdays aws tabular data
                arg_yesterday=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=ARG&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+j+'&f='+j+'&g=12&h=00')
                arg_dfy=arg_yesterday[0]






                                                #combine the two dataframes
                combine_yday_mh=pd.concat([dfy,arg_dfy], ignore_index=True)






                                                #drop vidarbha stations
                mah_drop_yesterday = combine_yday_mh[(combine_yday_mh['DISTRICT'] == 'AKOLA') | (combine_yday_mh['DISTRICT'] == 'AMRAVATI')|
               (combine_yday_mh['DISTRICT'] == 'BHANDARA') | (combine_yday_mh['DISTRICT'] == 'BULDHANA')|
               (combine_yday_mh['DISTRICT'] == 'CHANDRAPUR') | (combine_yday_mh['DISTRICT'] == 'GADCHIROLI')|
               (combine_yday_mh['DISTRICT'] == 'GONDIA') | (combine_yday_mh['DISTRICT'] == 'NAGPUR')|
               (combine_yday_mh['DISTRICT'] == 'YAVATMAL') | (combine_yday_mh['DISTRICT'] == 'WARDHA')|
               (combine_yday_mh['DISTRICT'] == 'WASHIM')].index
                combine_yday_mh.drop(mah_drop_yesterday, inplace=True)










                        
                                #select columns to include in dfy
                combine_yday_mh=combine_yday_mh[['STATION','TEMP DAY MAX. (\'C)','RH (%)','MSLP (hPa / gpm)']]
                                #print(dfyc)




                                #replace names
                combine_yday_mh.columns =combine_yday_mh.columns.str.replace('TEMP DAY MAX. (\'C)', 'MAX T',regex=False)
                combine_yday_mh.columns =combine_yday_mh.columns.str.replace('RH (%)', 'RH_12UTC',regex=False)
                combine_yday_mh.columns =combine_yday_mh.columns.str.replace('MSLP (hPa / gpm)', 'MSLP_12UTC',regex=False)





                                #set index
                dfy_index=combine_yday_mh.set_index("STATION")





                                #reindex
                new_dfy=dfy_index.reindex(['MUMBAI_COLABA','BYCULLA_MUMBAI','MAHALAXMI','MATUNGA_MUMBAI','SION_MUMBAI','MUMBAI_SANTA_CRUZ','TATA POWER CHEMBUR','BANDRA','MUMBAI AIRPORT','VIDYAVIHAR','JUHU_AIRPORT','VIKHROLI','RAM_MANDIR','DAHISAR','KOPARKHAIRANE',
'BHAYANDER','MIRA_ROAD','IIGHQ_NEWPANVEL','KARJAT','IIG_MO_ALIBAG','MATHERAN','BHIRA',
'MURUD','POLADPUR','INS SHIVAJI_LONAVALA','TALEGAON','GIRIVAN','CHINCHWAD_PUNE','MTI_PASHAN_PUNE','CME_DAPODI','RJSPMCOP_DUDULGAON','LAVALE','SHIVAJINAGAR_PUNE','PASHAN_AWS_LAB','RAJGURUNAGAR','BLINDSCHOOL_KP_PUNE','NDA_PUNE','MAGARPATTA_PUNE','WADGAONSHERI_PUNE','VETALE_KHED','DPS_HADAPSAR_PUNE','LONIKALBHOR_HAVELI','PABAL_SHIRUR','BALLALWADI_JUNNAR','KHADAKWADI_AMBEGAON','NIMGIRI_JUNNAR','TALEGAON_DHAMDHERE','NARAYANGOAN_KRISHI_KENDRA','CHRIST_UNIVERSITY_LAVASA','CAGMO_SHIVAJINAGAR','KHUTBAV_DAUND','WALHE_PURANDAR','MALIN_AMBEGAON','GUDHE_BHOR','NIASM_BARAMATI','NES_LAKADI_INDAPUR','BHANDARDARA','PARNER','KOPERGAON','SHRIGONDA',
'AHMEDNAGAR','RAHURI','SHEVGAON','PALGHAR_AWS400','PALGHAR_KVK','VILHOLI','TRIMBAKESHWAR','NIPHAD','VANI','KALWAN','MALEGAON','DAPOLI','SAVARDE(GOLWANE)',
'POWARWADI(BHAMBHED)','CHIPLUN','RATNAGIRI','RATNAGIRI_AWS400','MAHABALESHWAR','PANCHGANI','SATARA','PHALTAN','BGRL_KARAD','MOHOL_KVK','KARMALA','SOLAPUR','SANGOLA_MAHAVIDYALAYA',
'AKKALKOT','KOLHAPUR_AMFU','SHAHUWADI','PANHALA','RADHANAGRI_ARS','GARGOTI(BHUDARGAD)','GANGAPUR','PAITHAN','AURANGABAD_KVK','AURANGABAD','KANNAD','CHALISGAON','CHOPDA','JALGAON','JAMNER','DHULE','SHIRPUR','SHIRALA','UMADI','TASGAON','SANGLI_KVK','AKKALKUWA','NAVAPUR','TALODA','NANDURBAR','NANDURBAR_KVK','SHAHADA_AWS400','JALNA','BHOKARDAN','GHANSANGAVI','PARTUR','VAIBHAVWADI','AWALEGAON','MULDE_AMFU','DEVGAD',
'VENGURLA','OSMANABAD','KALAMB','TULGA_KVK','AMBEJOGAI','BEED_PTO','PARALIVAIJANATH',
'SHIRUR','CHAKUR','LATUR','NILANGA','UDGIR_AWS400','AUNDHA_NAGNATH','HINGOLI','KALAMNURI','TONDAPUR_AWS400','PARBHANI_AMFU','SONPETH','PURNA','NANDED','SAGROLI_KVK','BHOKAR'])
                





                
                new_dft.insert(loc=0, column='MAX T', value=new_dfy['MAX T'])
                new_dft.insert(loc=1, column='RH_12UTC', value=new_dfy['RH_12UTC'])
                new_dft.insert(loc=2, column='MSLP_12UTC', value=new_dfy['MSLP_12UTC'])

                #print(new_dft)

                






                new_dft.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt','border':'1pt solid', 'text-align':"center"})\
                                .to_excel(writer,sheet_name="AWSARG",index=False,startrow=0, startcol=(n-1)*10, engine='xlsxwriter') 
                workbook=writer.book

                worksheet = writer.sheets["AWSARG"]

                worksheet.autofit()

                #print(new_dfy)
                #print(i,j)
