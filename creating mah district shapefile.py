import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import shapefile as shp
from shapely.geometry import Point
sns.set_style('whitegrid')
import os
import matplotlib.colors as colors

fp = 'C:\\Users\\hp\\Desktop\\gurinder\\dist level shp file\\DISTRICT_BOUNDARY.shp'


map_df = gpd.read_file(fp)
map_df = map_df.to_crs(epsg=4326)

mah=map_df.loc[map_df['STATE'] == "MAH>R>SHTRA"].sort_values(['District'])

mah['District'] = mah['District'].str.upper()

                       #replace names
mah.columns =mah.columns.str.replace('District', 'DISTRICT',regex=False)


#print(mah)

mah['DISTRICT'].replace({'AHAMADNAGAR': 'AHMEDNAGAR',
                             'AMAR>VATI': 'AMRAVATI',
                               'AURANG>B>D': 'AURANGABAD',
                                 'BHAND>RA': 'BHANDARA',
                              'BULDH>NA': 'BULDHANA', 
                               'B|D': 'BEED',
                               'PARLI-VAI':'PARALIVAIJANATH',
                              'J>LNA': 'JALNA',
                               'KOLH>PUR': 'KOLHAPUR',
                               'L>T@R': 'LATUR',
                               'MUMBAI CITY':'MUMBAI_CITY',
                               'SUB URBAN MUMBAI':'MUMBAI_SUBURBUN',
                                'N>GPUR': 'NAGPUR',
                               'N>NDED': 'NANDED',
                                'N>SHIK': 'NASHIK',
                               'NANDURB>R': 'NANDURBAR',
                               'P>LGHAR': 'PALGHAR',
                               'R>YGAD': 'RAIGAD',
                               'RATN>GIRI': 'RATNAGIRI',
                               'S>NGLI': 'SANGLI',
                               'S>T>RA': 'SATARA',
                               'SOL>PUR': 'SOLAPUR',
                               'TH>NE': 'THANE',
                               'USM>N>B>D': 'OSMANABAD',
                               'W>SH|M': 'WASHIM',
                               'YAVATM>L': 'YAVATMAL'},inplace=True)

#mah.drop(mah_drop, inplace=True)


                            #drop vidarbha stations
mah_drop = mah[(mah['DISTRICT'] == 'AKOLA') | (mah['DISTRICT'] == 'AMRAVATI')|
(mah['DISTRICT'] == 'BHANDARA') | (mah['DISTRICT'] == 'BULDHANA')|
(mah['DISTRICT'] == 'CHANDRAPUR') | (mah['DISTRICT'] == 'GADCHIROLI')|
(mah['DISTRICT'] == 'GONDIA') | (mah['DISTRICT'] == 'NAGPUR')|
(mah['DISTRICT'] == 'YAVATMAL') | (mah['DISTRICT'] == 'WARDHA')|
(mah['DISTRICT'] == 'WASHIM')].index
mah.drop(mah_drop, inplace=True)






mah = mah[['DISTRICT','geometry']]



mah.to_excel('C:\\Users\\hp\\Desktop\\shape test.xlsx')


# Step 4: Save the subset as a new shapefile
mah.to_file('C:\\Users\\hp\\Desktop\\gurinder\\district level shape file\\maharashtra district excluding vidarbha.shp')