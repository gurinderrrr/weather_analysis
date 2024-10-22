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

fp = 'C:\\Users\\hp\\Desktop\\gurinder\\district shape\\DISTRICT_BOUNDARY.shp'


map_df = gpd.read_file(fp)


mah=map_df.loc[map_df['STATE'] == "MAH>R>SHTRA"].sort_values(['District'])

mah['District'] = mah['District'].str.upper()

# Rename column from 'District' to 'DISTRICT'
mah.rename(columns={'District': 'DISTRICT'}, inplace=True)


#print(mah)

# Correct district names
mah['DISTRICT'] = mah['DISTRICT'].replace({
    'AHAMADNAGAR': 'AHMEDNAGAR',
    'AMAR>VATI': 'AMRAVATI',
    'AURANG>B>D': 'AURANGABAD',
    'BHAND>RA': 'BHANDARA',
    'BULDH>NA': 'BULDHANA', 
    'B|D': 'BEED',
    'PARLI-VAI': 'PARALIVAIJANATH',
    'J>LNA': 'JALNA',
    'KOLH>PUR': 'KOLHAPUR',
    'L>T@R': 'LATUR',
    'MUMBAI CITY': 'MUMBAI_CITY',
    'SUB URBAN MUMBAI': 'MUMBAI_SUBURBUN',
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
    'YAVATM>L': 'YAVATMAL'
})

#mah.drop(mah_drop, inplace=True)



mah = mah[['DISTRICT','geometry']]

mah = mah.to_crs(epsg=4326)

print(mah.crs)
print(mah.geometry.type)
print(mah['geometry'].head(1))



#mah.to_excel('C:\\Users\\hp\\Desktop\\shape test.xlsx')


# Step 4: Save the subset as a new shapefile
mah.to_file('C:\\Users\\hp\\Desktop\\gurinder\\filtered shape files\\maharashtra all districts.shp')