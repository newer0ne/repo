import streamlit as st
from gsheetsdb import connect
import pandas as pd
import numpy as np
import openpyxl
import io
from io import BytesIO
import os
import csv
from pyxlsb import open_workbook as open_xlsb

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
tab.round({'mass': 3})
#st.write(tab)

uploaded_file = st.file_uploader("Зафгрузка файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file is not None:
    A = pd.read_excel(uploaded_file, sheet_name="Sheet1")
#    excel_1 = pd.DataFrame(A, columns=['Note', 'KKS Code'])
    final = pd.merge(A, tab, how = 'inner', on = ['Note']) 
    st.write(final)
    @st.cache
    
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('A:A', None, format1)
        writer.save()
        processed_data = output.getvalue()
        return processed_data
    df_xlsx = to_excel(final)
    st.download_button(label='📥 Download Current Result', data=df_xlsx, file_name= 'df_test.xlsx')
    
    
    
    
#    def convert_df(df):
#        return df.to_excel()
#        return df.to_csv().encode('utf-8')      # IMPORTANT: Cache the conversion to prevent computation on every rerun
#    output = convert_df(final)
#    st.download_button(label="Скачать без регистрации и СМС", data=output, file_name='output.xlsx')#, mime='text/xlsx')
