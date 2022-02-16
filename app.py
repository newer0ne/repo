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

st.title('Отдел инновационных технологий')
st.header('Инженерно-программная группа')
st.sidebar.subheader('Модуль классификации ведомостей ОПС на АЭС АККУЮ')

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')
tab = pd.DataFrame(rows)

uploaded_file = st.sidebar.file_uploader("Загрузка ведомости опор в формате .xls (Удалить первые два скрытых столбца, таблица должна начинаться с Код KKS)")
if uploaded_file is not None:
    A = pd.read_excel(uploaded_file, sheet_name="Sheet1")
    final = pd.merge(A, tab, how = 'outer', on = ['Note'])
    show_final = final.drop(columns=['Name','Designation of the document', 'Pipeline system code', 'Pipe Run', 'Pipeline elevation', 'Room'])
    st.write('Соответствие опор запрашиваемых в ведомости ОПС:)
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
    st.sidebar.download_button(label='📥 Скачать обработанную ведомость', data=df_xlsx, file_name= 'Ведомость опор.xlsx')
    if st.sidebar.button('📥 Скачать ведомость отправочных марок'):
        st.sidebar.write('Мы тоже хотим чтобы это работало')
        st.balloons()
        


st.subheader('Модуль классификации ведомостей ОПС на Курскую АЭС')
    # Загружаем таблицу опор Lisega
Li = st.secrets["public_gsheets_url_Lisega"]
rows_Li = run_query(f'SELECT * FROM "{Li}"')
tab_Li = pd.DataFrame(rows_Li)

uploaded_file2 = st.file_uploader("Загрузка тестовой ведомости опор для Курской АЭС (Столбец с кодировкой назвать Lisega, кодировка без пробелов)")
if uploaded_file2 is not None:
#    st.write(uploaded_file2)
    B = pd.read_excel(uploaded_file2, sheet_name=0, dtype={'Lisega': str})
    B = pd.merge(B, tab_Li, how = 'left', on = ['Lisega'])
    st.write(B)

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
    st.download_button(label='📥 Скачать обработанную ведомость опор', data=df_xlsx, file_name= 'Ведомость опор на Курскую АЭС.xlsx')
    if st.button('📥 Скачать ведомость отправочных марок'):
        st.write('Мы тоже хотим чтобы это работало')
        st.balloons()

st.sidebar.title('Модуль проверки базы данных по атомной станции')
stations = ["Курская АЭС", "АЭС АККУЮ", "АЭС Хинхакиви"]
add_selectbox = st.sidebar.selectbox("Выберите базу данных для обзора:", stations)
if st.sidebar.button('Просмотреть'):
    if add_selectbox == "АЭС АККУЮ":
        st.sidebar.write(tab)
    if add_selectbox == "Курская АЭС":
        st.sidebar.write(tab_Li)
    if add_selectbox == "АЭС Хинхакиви":
        st.sidebar.write('Оптимистичный выбор :)')
        st.sidebar.image('https://s.wine.style/images_gen/423/4239/0_0_prod_desktop.jpg')

st.subheader('Таблица соответствия ЛАЭС-2 - АККУЮ')
    # Загружаем таблицу опор Lisega
Li2 = st.secrets["public_gsheets_url_Lisega2"]
rows_Li2 = run_query(f'SELECT * FROM "{Li2}"')
tab_Li2 = pd.DataFrame(rows_Li2)
st.write(tab_Li2)
