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
#st.write(tab)

uploaded_file = st.file_uploader("Зафгрузка ведомости опор в формате .xls (Удалить первые два скрытых столбца, таблица должна начинаться с Код KKS)")
if uploaded_file is not None:
    A = pd.read_excel(uploaded_file, sheet_name="Sheet1")
    final = pd.merge(A, tab, how = 'inner', on = ['Note'])
    show_final = final.drop(columns=['Name','Designation of the document', 'Pipeline system code', 'Pipe Run', 'Pipeline elevation', 'Room'])
    st.write(show_final)
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
    st.download_button(label='📥 Скачать обработанную ведомость', data=df_xlsx, file_name= 'Ведомость опор.xlsx')
    
sheet_url_t21 = st.secrets["public_gsheets_url_21"]
rows21 = run_query(f'SELECT Dn, Fz_21, mark_21 FROM "{sheet_url_t21}"')
tab21 = pd.DataFrame(rows21)
st.write(tab21)
sheet_url_t31 = st.secrets["public_gsheets_url_t31"]
rows31 = run_query(f'SELECT Dn, Fz_31, mark_31 FROM "{sheet_url_t31}"')
tab31 = pd.DataFrame(rows31)
st.write(tab31)

uploaded_file2 = st.file_uploader("Зафгрузка тестовая")
if uploaded_file2 is not None:
    B = pd.read_excel(uploaded_file2, sheet_name=0, dtype={'Lisega': str})
    B = B
    st.write(B)
#    B = pd.merge(B, tab21, on = ['Dn'])
#    B = pd.merge(B, tab31, on = ['Dn'])
#    B.insert(1, "mark", 'none')
#    final22 = B[(B['Fz'] <= B['Fz_21']) | (B['Fz'] <= B['Fz_31'])]
#    show_final2 = final2.drop(columns=['A','B', 'H', 'Fx_kN', 'Fy_kN', 'mass', 'mass_list'])
