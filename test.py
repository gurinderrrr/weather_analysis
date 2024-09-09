import pandas as pd

# Sample DataFrames (Replace with your actual DataFrames)
df_pg_hd_mh = pd.DataFrame(['STATE: MAHARASHTRA (09-09-2024 3UTC to 10-09-2024 3UTC)'])
df_rf_leg_head_mh = pd.DataFrame({'':['LEGENDS']})
df_rf_leg_mh = pd.DataFrame({'':['Not Reported', '1mm <= RF <= 2.4mm/\nLowest Temp', '2.5mm <= RF <= 15.5mm',
                                 '15.6mm <= RF <= 64.4mm', '64.5mm <= RF <= 115.5mm', '115.6mm <= RF <= 204.4mm',
                                 'RF > 204.4/\nHighest Temp', 'Error Values']})
df_rf_leg_col_mh = pd.DataFrame({'':['', 'Lowest Temp', '', '', '', '', 'Highest Temp', 'Error Value']})
awsarg_df_sum_data_mh = pd.DataFrame([["Total AWS/AGRO stations working"], ['Total AWS/AGRO stations reporting'],
                                      ['Total ARG stations working'], ['Total ARG stations reporting']])
awsarg_df_sum_val_mh = pd.DataFrame([[10], [8], [5], [3]])  # Sample values for total stations reporting

# Function to convert a DataFrame to HTML
def df_to_html(df,header=False, index=False, border=True):
    return df.style\
        .set_properties(**{'font-family': "Calibri", 'font-size': '12pt', 'border': '1pt solid',
                           'text-align': "center", 'white-space': 'pre-wrap', 'word-wrap': 'break-word'})\
        .set_table_styles([{
        'selector': 'th',
        'props': [('border', '1pt solid')]}])\
        .hide(axis='index').to_html()

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


{df_to_html(df_rf_leg_head_mh)}


{df_to_html(df_rf_leg_mh)}


{df_to_html(df_rf_leg_col_mh)}


{df_to_html(awsarg_df_sum_data_mh)}


{df_to_html(awsarg_df_sum_val_mh)}

</body>
</html>
'''

# Save the combined HTML to a file
with open('combined_tables_maharashtra.html', 'w') as f:
    f.write(html_string)