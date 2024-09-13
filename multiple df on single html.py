import pandas as pd
import numpy as np

# Sample DataFrames (Replace with your actual DataFrames)
df_pg_hd_mh = pd.DataFrame(['STATE: MAHARASHTRA (09-09-2024 3UTC to 10-09-2024 3UTC)'])


df_rf_leg_head_mh = pd.DataFrame({'':['LEGENDS']})


df_rf_leg_mh = pd.DataFrame({'RANGE':['Not Reported', '1mm <= RF <= 2.4mm/\nLowest Temp', '2.5mm <= RF <= 15.5mm',
                                 '15.6mm <= RF <= 64.4mm', '64.5mm <= RF <= 115.5mm', '115.6mm <= RF <= 204.4mm',
                                 'RF > 204.4/\nHighest Temp', 'Error Values']})
df_rf_leg_col_mh = pd.DataFrame({'COLORS':[np.nan, 'Lowest Temp', np.nan, np.nan, np.nan, np.nan, 'Highest Temp', 'Error Value']})


# Function to color cells with np.nan
def highlight_leg(val):
    if val == 'Not Reported':
        return 'background-color: white'
    elif val == '1mm <= RF <= 2.4mm/\nLowest Temp':
        return 'background-color: #ADFF2F; font-weight: bold'
    elif val == '2.5mm <= RF <= 15.5mm':
        return 'background-color: #00FF00; font-weight: bold'
    elif val == '15.6 <= rf_value <= 64.4':
        return 'background-color: #00FFFF; font-weight: bold'
    elif val == '64.5 <= rf_value <= 115.5':
        return 'background-color: #FFFF00; font-weight: bold'
    elif val == '115.6 <= rf_value <= 204.4':
        return 'background-color: #FFA500; font-weight: bold'
    elif val > 204.4:  # ehr
        return 'background-color: #FF0000; font-weight: bold'
    else:
        return ''
    

# Apply styling: highlight np.nan cells with red
leg_styled_df = df_rf_leg_mh.style.applymap(highlight_leg)



# Function to convert DataFrame to HTML with custom styles, excluding header and index
def df_to_html(df, border=True):
    return df.to_html(header=False, index=False, border=1)

# Combine the HTML for all DataFrames
html_string = f'''
<html>
<head>
<style>
    body {{
        font-family: Arial, sans-serif;
        margin: 20px;
    }}
    table {{
        margin-bottom: 30px;
        border-collapse: collapse;
        width: 50%;
    }}
    th, td {{
        border: 1px solid black;
        text-align: center;
        padding: 5px;
    }}
    h2 {{
        margin-top: 50px;
    }}
</style>
</head>
<body>

{df_to_html(df_pg_hd_mh)}

{df_to_html(leg_styled_df)}

</body>
</html>
'''

# Save the combined HTML to a file
with open('combined_tables_maharashtra.html', 'w') as f:
    f.write(html_string)