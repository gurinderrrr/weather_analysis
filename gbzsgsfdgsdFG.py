import requests
import pdfplumber
import pandas as pd

# URL of the PDF
pdf_url = 'https://mausam.imd.gov.in/mumbai/mcdata/state_rain.pdf'

# Download the PDF file
response = requests.get(pdf_url)
pdf_path = 'state_rain.pdf'
with open(pdf_path, 'wb') as file:
    file.write(response.content)

# Function to ensure unique column names
def make_unique_columns(columns):
    seen = {}
    result = []
    for col in columns:
        if col in seen:
            seen[col] += 1
            result.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            result.append(col)
    return result

# Use pdfplumber to read the PDF
with pdfplumber.open(pdf_path) as pdf:
    all_tables = []
    for page_num, page in enumerate(pdf.pages, start=1):
        table = page.extract_table()
        if table:
            # Ensure unique column names
            unique_columns = make_unique_columns(table[0])
            df = pd.DataFrame(table[1:], columns=unique_columns)
            all_tables.append(df)

# Concatenate all dataframes along rows
df = pd.concat(all_tables, ignore_index=True, axis=0)

print(df)
df.to_excel('C:\\Users\\hp\\Desktop\\gurinder\\python test\\drms test.xlsx')