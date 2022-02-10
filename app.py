import streamlit as st
from gsheetsdb import connect
import pandas as pd
import numpy as np
import openpyxl
import io
import os
import csv

# Create a connection object.
conn = connect()
# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')
tab = pd.DataFrame(rows)
#st.write(tab)

uploaded_file = st.file_uploader("Зафгрузка файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file is not None:   
     excel = pd.read_excel(uploaded_file)
#     excel_1 = pd.DataFrame(excel, columns=['Note', 'KKS Code'])
final = pd.merge(excel, tab, how = 'inner', on = ['Note']) 
st.write(final)

@st.cache
output = final.to_excel('output.xlsx')
st.download_button(label="Download data as CSV", data=xlsx, file_name='output.xlsx', mime='text/xlsx',)
