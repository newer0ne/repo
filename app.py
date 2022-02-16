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
    final = pd.merge(A, tab, how = 'outer', on = ['Note'])
    show_final = final.drop(columns=['Name','Designation of the document', 'Pipeline system code', 'Pipe Run', 'Pipeline elevation', 'Room'])
    st.write(show_final)
    @st.cache
    
        # Скачиваем обработанную ведомость
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

    # Загружаем таблицу опор Lisega
Li = st.secrets["public_gsheets_url_Lisega"]
rows_Li = run_query(f'SELECT * FROM "{Li}"')
tab_Li = pd.DataFrame(rows_Li)

uploaded_file2 = st.file_uploader("Загрузка тестовой ведомости опор для Курской АЭС (Столбец с кодировкой назвать Lisega, кодировка без пробелов)")
if uploaded_file2 is not None:
    B = pd.read_excel(uploaded_file2, sheet_name=0, dtype={'Lisega': str})
    B = pd.merge(B, tab_Li, how = 'left', on = ['Lisega'])
    st.write(B)
    C = B['Lisega'], B['№ п/п']
    C = B.groupby(['Lisega']).count()
    st.write(C)

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
    df_xlsx = to_excel(B)
    st.download_button(label='📥 Скачать обработанную ведомость', data=df_xlsx, file_name= 'Ведомость опор на Курскую АЭС.xlsx')
