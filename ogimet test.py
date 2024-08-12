import pandas as pd
import os

# Reading the HTML table into a DataFrame
df = pd.read_html('https://www.ogimet.com/cgi-bin/gsynres?lang=en&ord=REV&ndays=31&ano=2024&mes=05&day=31&hora=03&ind=43057')[2]

print(df)
print(df.info())

# Correct column selection based on the actual structure of the DataFrame
# Inspecting the columns first
print(df.columns)

# Selecting the specific columns
selected_columns = df.loc[:, [('Date', 'Date'), 
                              ('Temperature (C)', 'Max'), 
                              ('Temperature (C)', 'Min'), 
                              ('Prec. (mm)', 'Prec. (mm)'),
                              ('Pres. s.lev (Hp)', 'Pres. s.lev (Hp)')]]

# Flattening the MultiIndex columns
selected_columns.columns = ['Date', 'Max', 'Min', 'RF', 'pressure']

print(selected_columns)
print(selected_columns.info())

selected_columns.to_excel(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads\\ogimet may test.xlsx'),index=False)