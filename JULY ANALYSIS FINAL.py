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

df=pd.read_excel('C:\\Users\\hp\\Desktop\\july datetime 1H test.xlsx')

print(len(df))
#exit()

df.dropna(subset=['RF'], inplace=True)

print(len(df))

#df.to_excel('C:\\Users\\hp\\Desktop\\gurinder\\python test\\rainfall_1Htest_animation.xlsx')
#exit()

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




df['LAT']=df.apply(map_lat, axis=1)
df['LONG']=df.apply(map_long, axis=1)



# Reorder columns as needed
df = df[['STATION','DATETIME (UTC)','RF','LAT','LONG']]

df['RF'] = pd.to_numeric(df['RF'], errors='coerce')
df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
df['LONG'] = pd.to_numeric(df['LONG'], errors='coerce')





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
    if 1 < rf <= 64.4:
        return '#98FB98'
    elif 64.5 <= rf <= 115.5:
        return '#FFFF00'
    elif 115.6 <= rf <= 204.4:
        return '#FFA500'
    elif rf > 204.4:
        return '#FF0000'
    else:
        return 'white'

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(22, 15))  # Keep your desired figure size
# Remove the axes
ax.axis('off')

# Plot the shapefile boundaries
gdf.plot(ax=ax, color='none', edgecolor='black')

# Filter out data points with missing or zero rainfall
#date_data = df[(df['DATETIME (UTC)'] == date) & (df['RF'] > 0)]

#colors = [get_custom_color(rf) for rf in date_data['RF']]
#print(colors)

#exit()
# Function to update the plot for each frame
def update(date):
    ax.clear()
    ax.axis('off')  # Ensure the axes remain off after clearing
    gdf.plot(ax=ax, color='none', edgecolor='black')

    # Filter out data points with missing or zero rainfall
    date_data = df[(df['DATETIME (UTC)'] == date) & (df['RF'] > 1)]

    
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
dates = df['DATETIME (UTC)'].unique()
ani = animation.FuncAnimation(
    fig, update, frames=dates, repeat=False, interval=2000
)

# Save the animation as a GIF file
output_path = 'C:\\Users\\hp\\Desktop\\gurinder\\python test\\rainfall_1H_animation.gif'
ani.save(output_path, writer=PillowWriter(fps=2))  # Use PillowWriter to save as GIF

plt.show()