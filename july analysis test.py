import pandas as pd
import itertools
#Define the start date, end date, and frequency
start_date = '2024-07-01'
end_date = '2024-07-31'
frequency = '1D'

#Create a datetime range
date_range = pd.date_range(start=start_date, end=end_date, freq=frequency).strftime('%d-%m-%Y')

# Reverse the order
#datetime_range = datetime_range[::-1]

#print(datetime_range)


# Create a DataFrame with the datetime range
date_df = pd.DataFrame(date_range, columns=['DATE'])

#print(date_df)
print('rows in date_df: ',len(date_df))




#Define the start date, end date, and frequency
start_time = '00:00:00'
end_time = '23:45:00'
frequency = '15min'

#Create a datetime range
time_range = pd.date_range(start=start_time, end=end_time, freq=frequency).strftime('%H:%M')

# Reverse the order
#datetime_range = datetime_range[::-1]

#print(datetime_range)


# Create a DataFrame with the datetime range
time_df = pd.DataFrame(time_range, columns=['TIME (UTC)'])

#print(datetime_df)
print('rows in time_df: ',len(time_df))




#exit()









# Extract unique values
dates = date_df['DATE'].unique()
times = time_df['TIME (UTC)'].unique()

# Create a DataFrame with all combinations of 'station' and 'datetime'
all_combinations = pd.DataFrame(list(itertools.product(dates, times)), columns=['DATE', 'TIME (UTC)'])


print(len(all_combinations))


exit()





all_combinations['DATETIME'] = pd.to_datetime(date_df['DATE'] + ' ' +time_df['TIME (UTC)'])



# Merge with the original df to include all stations and all datetimes
complete_combined = pd.merge(all_combinations, combined_all_stations, on=['STATION', 'DATE'], how='left')

df_sorted = complete_combined.sort_values(by=['DATE', 'STATION'])
df_sorted = df_sorted.reset_index(drop=True)



#print(complete_combined['STATION'].nunique())
#print(complete_combined['DATE'].nunique())
#print(len(complete_combined))


#print(len(df_sorted))