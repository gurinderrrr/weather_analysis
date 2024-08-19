# import libraries
import pandas as pd
import csv
from datetime import datetime
from datetime import date
from datetime import timedelta
import os



            #create todays and yesterdays date
start_date =input('Enter the start date as ddmmyyyy: ')
sd=datetime.strptime(start_date, "%d%m%Y").strftime("%Y-%m-%d")
end_date =input('Enter the end date as ddmmyyyy: ')
ed=datetime.strptime(end_date, "%d%m%Y").strftime("%Y-%m-%d")


df=pd.DataFrame({'t_day':pd.date_range(sd,ed)})
print(df)
print(len(df))
with pd.ExcelWriter(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads\\MAHARASHTRA.xlsx')) as writer:
#for i in df['t_day'].astype(str), int(n) in range(1,len(df)+1):
        for i, n in zip(df['t_day'].astype(str), range(1,len(df)+1)):  
                today=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+i+'&f='+i+'&g=03&h=00')
                dft=today[0]
                #print(dft)
                #select colums to include in dft
                dftc=dft[['STATION','RAIN FALL CUM. SINCE 0300 UTC (mm)','TEMP DAY MIN. (\'C)','RH (%)','MSLP (hPa / gpm)','BATTERY (Volts)','GPS']]


                                        #replace names
                dftc.columns =dftc.columns.str.replace('RAIN FALL CUM. SINCE 0300 UTC (mm)', 'RF',regex=False)
                dftc.columns =dftc.columns.str.replace('TEMP DAY MIN. (\'C)', 'MIN T',regex=False)
                dftc.columns =dftc.columns.str.replace('RH (%)', 'RH_03UTC',regex=False)
                dftc.columns =dftc.columns.str.replace('MSLP (hPa / gpm)', 'MSLP_03UTC',regex=False)





                                        #set index
                dft_index=dftc.set_index("STATION")






                                        #reindex
                new_dft=dft_index.reindex(["MUMBAI_COLABA", "MUMBAI_SANTA_CRUZ", "PALGHAR",
                                        'PALGHAR_KVK','IIG_MO_ALIBAG','KARJAT','MURUD',
                                        'THANE','DAPOLI','RATNAGIRI','DEVGAD',
                                        'MULDE_AMFU','AHMEDNAGAR','KOPERGAON','RAHURI',
                                        'SHIRDI','DHULE','CHOPDA','JALGAON',
                                        'NANDURBAR_KVK','NAVAPUR','NANDURBAR','KALWAN',
                                        'MALEGAON','NIMGIRI_JUNNAR','CAGMO_SHIVAJINAGAR',
                                        'CHRIST_UNIVERSITY_LAVASA','CME_DAPODI','DPS_HADAPSAR_PUNE',
                                        'INS SHIVAJI_LONAVALA','KHUTBAV_DAUND','LONIKALBHOR_HAVELI',
                                        'NARAYANGOAN_KRISHI_KENDRA','NIASM_BARAMATI','PASHAN',
                                        'RAJGURUNAGAR','TALEGAON','KOLHAPUR_AMFU','MAHABALESHWAR',
                                        'BGRL_KARAD','SATARA','MOHOL_KVK','SOLAPUR','AURANGABAD','AURANGABAD_KVK',
                                        'AMBEJOGAI','HINGOLI','JALNA','LATUR','NANDED','OSMANABAD',
                                        'TULGA_KVK','PARBHANI_AMFU'])
                
                
                j=(datetime.strptime(i, "%Y-%m-%d")-timedelta(days=1)).strftime("%Y-%m-%d")
                
                        #collect yesterdays aws tabular data
                yesterday=pd.read_html('http://aws.imd.gov.in:8091/AWS/dataview.php?a=AWSAGRO&b=MAHARASHTRA&c=ALL_DISTRICT&d=ALL_STATION&e='+j+'&f='+j+'&g=12&h=00')
                dfy=yesterday[0]

                        
                                #select columns to include in dfy
                dfyc=dfy[['STATION','TEMP DAY MAX. (\'C)','RH (%)','MSLP (hPa / gpm)']]
                                #print(dfyc)




                                #replace names
                dfyc.columns =dfyc.columns.str.replace('TEMP DAY MAX. (\'C)', 'MAX T',regex=False)
                dfyc.columns =dfyc.columns.str.replace('RH (%)', 'RH_12UTC',regex=False)
                dfyc.columns =dfyc.columns.str.replace('MSLP (hPa / gpm)', 'MSLP_12UTC',regex=False)





                                #set index
                dfy_index=dfyc.set_index("STATION")





                                #reindex
                new_dfy=dfy_index.reindex(["MUMBAI_COLABA", "MUMBAI_SANTA_CRUZ", "PALGHAR",
                                                        'PALGHAR_KVK','IIG_MO_ALIBAG','KARJAT','MURUD',
                                                        'THANE','DAPOLI','RATNAGIRI','DEVGAD',
                                                        'MULDE_AMFU','AHMEDNAGAR','KOPERGAON','RAHURI',
                                                        'SHIRDI','DHULE','CHOPDA','JALGAON',
                                                        'NANDURBAR_KVK','NAVAPUR','NANDURBAR','KALWAN',
                                                        'MALEGAON','NIMGIRI_JUNNAR','CAGMO_SHIVAJINAGAR',
                                                        'CHRIST_UNIVERSITY_LAVASA','CME_DAPODI','DPS_HADAPSAR_PUNE',
                                                        'INS SHIVAJI_LONAVALA','KHUTBAV_DAUND','LONIKALBHOR_HAVELI',
                                                        'NARAYANGOAN_KRISHI_KENDRA','NIASM_BARAMATI','PASHAN',
                                                        'RAJGURUNAGAR','TALEGAON','KOLHAPUR_AMFU','MAHABALESHWAR',
                                                        'BGRL_KARAD','SATARA','MOHOL_KVK','SOLAPUR','AURANGABAD','AURANGABAD_KVK',
                                                        'AMBEJOGAI','HINGOLI','JALNA','LATUR','NANDED','OSMANABAD',
                                                        'TULGA_KVK','PARBHANI_AMFU'])
                
                new_dft.insert(loc=0, column='MAX T', value=new_dfy['MAX T'])
                new_dft.insert(loc=1, column='RH_12UTC', value=new_dfy['RH_12UTC'])
                new_dft.insert(loc=2, column='MSLP_12UTC', value=new_dfy['MSLP_12UTC'])

                print(new_dft)

                

                new_dft.style.set_properties(**{'font-family':"Calibri",'font-size':'12pt','border':'1pt solid', 'text-align':"center"})\
                                .to_excel(writer,sheet_name="MAHARASHTRA",index=False,startrow=0, startcol=(n-1)*10, engine='xlsxwriter') 
                workbook=writer.book

                worksheet = writer.sheets["MAHARASHTRA"]

                worksheet.autofit()

                

                #print(new_dfy)
                #print(i,j)