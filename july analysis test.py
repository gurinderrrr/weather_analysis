import pandas as pd
import itertools

combined_all_stations=pd.read_excel('C:\\Users\\hp\\Desktop\\july test.xlsx')


#print(combined_all_stations)

#exit()



#Define the start date, end date, and frequency
start_datetime = '2024-07-01 00:00:00'
end_datetime = '2024-07-31 23:45:00'
frequency = '2H'

#Create a datetime range
datetime_range = pd.date_range(start=start_datetime, end=end_datetime, freq=frequency)


# Reverse the order
#datetime_range = datetime_range[::-1]

#print(datetime_range)


# Create a DataFrame with the datetime range
datetime_df = pd.DataFrame(datetime_range, columns=['DATETIME (UTC)'])

datetime_df['DATETIME (UTC)'] = pd.to_datetime(datetime_df['DATETIME (UTC)'], format='%Y-%m-%d %H:%M:%S')

#print(date_df.info())
#exit()


# Step 1: Create all combinations of 'stations' and 'datetime'
stations_unique = combined_all_stations[['STATION']].drop_duplicates()
datetime_unique = datetime_df[['DATETIME (UTC)']].drop_duplicates()

# Perform a cross join to get all combinations
combinations = stations_unique.merge(datetime_unique, how='cross')

# Step 2: Merge with the original DataFrame to bring in the rainfall data
result = combinations.merge(combined_all_stations, on=['STATION', 'DATETIME (UTC)'], how='left')

result.to_excel('C:\\Users\\hp\\Desktop\\july datetime 2H test.xlsx', index=False)


#print(datetime_df)
#print('rows in date_df: ',len(date_df))
exit()



#Define the start date, end date, and frequency
start_time = '00:00'
end_time = '23:45'
frequency = '15min'

#Create a datetime range
time_range = pd.date_range(start=start_time, end=end_time, freq=frequency).strftime('%H:%M:%S')

# Reverse the order
#datetime_range = datetime_range[::-1]

#print(datetime_range)


# Create a DataFrame with the datetime range
time_df = pd.DataFrame(time_range, columns=['TIME (UTC)'])
#time_df['TIME (UTC)'] = pd.to_datetime(time_df['TIME (UTC)'], format='%H:%M')

print(time_df.info())
#exit()
#print(datetime_df)
#print('rows in time_df: ',len(time_df))
#exit()





















# Extract unique values
dates = date_df['DATE'].unique()
times = time_df['TIME (UTC)'].unique()

# Create a DataFrame with all combinations of 'station' and 'datetime'
all_combinations = pd.DataFrame(list(itertools.product(dates, times)), columns=['DATE', 'TIME (UTC)'])


print(all_combinations)


#exit()





all_combinations['DATETIME'] = pd.to_datetime(date_df['DATE'] + ' ' +time_df['TIME (UTC)'])

print(all_combinations)
exit()

# Merge with the original df to include all stations and all datetimes
complete_combined = pd.merge(all_combinations, combined_all_stations, on=['STATION', 'DATE'], how='left')

df_sorted = complete_combined.sort_values(by=['DATE', 'STATION'])
df_sorted = df_sorted.reset_index(drop=True)



#print(complete_combined['STATION'].nunique())
#print(complete_combined['DATE'].nunique())
#print(len(complete_combined))


#print(len(df_sorted))