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
#df = pd.read_html(f'https://www.ogimet.com/cgi-bin/gsynres?lang=en&ord=DIR&ndays=1&ano={year_str}&mes={month_str}&day={day_str}&hora=03&state=India')[2]

#df = pd.read_html(f'https://www.ogimet.com/display_synops2.php?lang=en&lugar=43057&tipo=ALL&ord=REV&ano=2024&mes=08&day=19&hora=03&anof=2024&mesf=08&dayf=19&horaf=03')[2]

df = pd.read_csv(f'http://www.ogimet.com/cgi-bin/getsynop?begin=202408190300&end=202408190300&state=Ind&lang=eng')

print(df)
print(df.info())
df.to_csv('C:\\Users\\hp\\Desktop\\test ogi.csv')
exit()
# Extracting the 4th group for pressure
pressure_group = df[3].str.split().str[5]

print(pressure_group)
#print(df.info())
exit()




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