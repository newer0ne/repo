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

Li = st.secrets["public_gsheets_url_Lisega"]
rows_Li = run_query(f'SELECT Dn, Lisega, Fz FROM "{Li}"')
tab_Li = pd.DataFrame(rows_Li, dtype={'Dn': float,'Lisega': str, 'Fz': float})
#st.write(tab_Li)
sheet_url_t21 = st.secrets["public_gsheets_url_t21"]
rows_21 = run_query(f'SELECT Dn, Fz_21, mark_21 FROM "{sheet_url_t21}"')
tab_21 = pd.DataFrame(rows_21)
#st.write(tab_21)
sheet_url_t31 = st.secrets["public_gsheets_url_t31"]
rows_31 = run_query(f'SELECT Dn, Fz_31, mark_31 FROM "{sheet_url_t31}"')
tab_31 = pd.DataFrame(rows_31)
#st.write(tab_31)

tab_Li_kt2 = pd.merge(tab_Li, tab_21, how = 'inner', on = ['Dn'])
tab_Li_kt2 = pd.merge(tab_Li_kt2, tab_31, how = 'inner', on = ['Dn'])
tab_Li_kt2.dropna(subset=['Fz'], inplace=True)
st.write(tab_Li_kt2)
for Fz_31 in tab_Li_kt2:
    if Fz_31 <= 100:
        tab_Li_kt2['mark'] == 'yepp'
    else:
        tab_Li_kt2['mark'] == 'fuck'
st.write(tab_Li_kt2)
#X = tab_Li_kt2[tab_Li_kt2['Fz'] <= tab_Li_kt2['Fz_31']]
#st.write(X)

#for Fz in tab_Li_kt2:
#    if Fz <= Fz_21:
#        tab_Li_kt2['mark'] = tab_Li_kt2['mark_21']
#tab_Li_kt2['mark'] = tab_Li_kt2['Fz'] <= tab_Li_kt2['Fz_21']


uploaded_file2 = st.file_uploader("Зафгрузка тестовая")
if uploaded_file2 is not None:
    B = pd.read_excel(uploaded_file2, sheet_name=0, dtype={'Lisega': str})
    st.write(B)
#    B = pd.merge(B, tab21, on = ['Dn'])
#    B = pd.merge(B, tab31, on = ['Dn'])
#    B.insert(1, "mark", 'none')
#    final22 = B[(B['Fz'] <= B['Fz_21']) | (B['Fz'] <= B['Fz_31'])]
#    show_final2 = final2.drop(columns=['A','B', 'H', 'Fx_kN', 'Fy_kN', 'mass', 'mass_list'])
