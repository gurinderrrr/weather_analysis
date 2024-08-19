import pandas as pd
import os
from datetime import date,datetime
from datetime import timedelta
import os
import time

# Get today's date
t_day = date.today()

# Separate year, month, and day as strings
year_str = t_day.strftime("%Y")  # Year as a string
month_str = t_day.strftime("%m")  # Month as a string
day_str = t_day.strftime("%d")    # Day as a string

# Reading the HTML table into a DataFrame
df = pd.read_html(f'https://www.ogimet.com/cgi-bin/gsynres?lang=en&ord=DIR&ndays=1&ano={year_str}&mes={month_str}&day={day_str}&hora=03&state=India')[2]

#print(df)
#print(df.info())




# Correct column selection based on the actual structure of the DataFrame
# Inspecting the columns first
#print(df.columns)



# Selecting the specific columns
selected_columns = df.loc[:, [('Station', 'Station'), 
                              ('Temperature (C)', 'Max'), 
                              ('Temperature (C)', 'Min'), 
                              ('Prec. (mm)', 'Prec. (mm)')
                              ]]

# Flattening the MultiIndex columns
selected_columns.columns = ['Station', 'Max', 'Min', 'RF']

                        #choose columns to include in combine_tday_mh
#selected_columns.columns =selected_columns.columns.str.replace('DATE(YYYY-MM-DD)', 'DATE',regex=False)

print(selected_columns)
print(selected_columns.info())

selected_columns.to_excel(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads\\ogimet may test.xlsx'),index=False)