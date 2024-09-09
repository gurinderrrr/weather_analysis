import pandas as pd

# Sample DataFrames (Replace with your actual DataFrames)
df_pg_hd_mh = pd.DataFrame(['STATE: MAHARASHTRA (09-09-2024 3UTC to 10-09-2024 3UTC)'])

awsarg_df_sum_data_mh = pd.DataFrame([[f"Total AWS/AGRO stations working= {23}"], ['Total AWS/AGRO stations reporting'],['Total ARG stations working'], ['Total ARG stations reporting']])
awsarg_df_sum_val_mh = pd.DataFrame([[10], [8], [5], [3]])  # Sample values for total stations reporting


# Function to convert DataFrame to HTML with custom alignment, excluding header and index
def df_to_html(df, text_align='center'):
    return df.to_html(header=False, index=False, border=1)\
        .replace('<table', f'<table style="text-align: {text_align}"')  # Custom text alignment per table

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


{df_to_html(df_pg_hd_mh, text_align='center')}



{df_to_html(awsarg_df_sum_data_mh, text_align='center')}


{df_to_html(awsarg_df_sum_val_mh)}

</body>
</html>
'''

# Save the combined HTML to a file
with open('combined_tables_maharashtra.html', 'w') as f:
    f.write(html_string)