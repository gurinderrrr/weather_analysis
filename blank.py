import geopandas as gpd
import matplotlib.pyplot as plt

shape_path='C:\\Users\\HP\\Desktop\\guri\\district shape\\DISTRICT_BOUNDARY.shp'

gdf=gpd.read_file(shape_path)

#gdf=gdf.to_crs(epsg=4326)


mah=gdf.loc[gdf['STATE'] == "MAH>R>SHTRA"].sort_values(['District'])

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

# Plot the shapefile
fig, ax = plt.subplots(figsize=(15, 10))
mah.plot(ax=ax, color='lightgrey', edgecolor='black', linewidth=1)


# Add taluka names
for x, y, dist in zip(mah.centroid.geometry.x, mah.centroid.geometry.y, mah['DISTRICT']):
    ax.text(x, y, dist, ha='center', va='center', fontsize=4, color='black')


# Set x and y limits to "zoom" the area
xmin, xmax = mah.total_bounds[0], mah.total_bounds[2]  # Get min and max x values
ymin, ymax = mah.total_bounds[1], mah.total_bounds[3]  # Get min and max y values

# Adjust these values to zoom in or out
padding = 0.1  # Add some padding to make sure the labels fit
ax.set_xlim(xmin - padding, xmax + padding)
ax.set_ylim(ymin - padding, ymax + padding)

#gdf.plot()
plt.show()