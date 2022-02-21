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
st.write('Краткое описание интерфейса: слева - панель рабочих функций, ниже - рабочее поле. ',
         'После применения необходимой функции, например, проверки базы данных по АЭС - на рабочем поле отображаются результаты.') 




st.sidebar.header('Модуль классификации ведомостей ОПС на АЭС АККУЮ')

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')
tab = pd.DataFrame(rows)

uploaded_file = st.sidebar.file_uploader("Загрузка ведомости опор в формате .xls (Нужно удалить первые два скрытых столбца. Таблица должна начинаться со столбца **Код KKS**)")
if uploaded_file is not None:
    A = pd.read_excel(uploaded_file, sheet_name="Sheet1")
    final = pd.merge(A, tab, how = 'outer', on = ['Note'])
    show_final = final.drop(columns=['Name','Designation of the document', 'Pipeline system code', 'Pipe Run', 'Pipeline elevation', 'Room'])
    st.write('Соответствие опор запрашиваемых в ведомости ОПС на АЭС АККУЮ. ',
             '**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
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
        
        
        
        


st.sidebar.header('Модуль классификации ведомостей ОПС на Курскую АЭС')
    # Загружаем таблицу опор Lisega
Li = st.secrets["public_gsheets_url_Lisega"]
rows_Li = run_query(f'SELECT * FROM "{Li}"')
tab_Li = pd.DataFrame(rows_Li)
tab_Li['Li type'] = tab_Li['Lisega'].str[:2]
tab_Li['Li diam class'] = tab_Li['Lisega'].str[2:4]
tab_Li['Li temp class'] = tab_Li['Lisega'].str[4:6]

Link_ClassRuEn = st.secrets["ClassRuEn"]
Link_CatLi = st.secrets["CatLi"]
Link_CatKT2 = st.secrets["CatKT2"]

rows_ClassRuEn = run_query(f'SELECT * FROM "{Link_ClassRuEn}"')
rows_CatLi = run_query(f'SELECT * FROM "{Link_CatLi}"')
rows_CatKT2 = run_query(f'SELECT * FROM "{Link_CatKT2}"')

ClassRuEn = pd.DataFrame(rows_ClassRuEn, dtype=str)
CatLi = pd.DataFrame(rows_CatLi, dtype=str)
CatKT2 = pd.DataFrame(rows_CatKT2, dtype=str)

#st.write(ClassRuEn)
st.header('Оцифрованный каталог Lisega')
st.write(CatLi)
st.header('Оцифрованный каталог KT2')
st.write(CatKT2)


st.header('Таблица соответствия')
tabLiKT2 = pd.merge(CatLi, CatKT2, on = ['Li_type', 'Li_diam_class'])
tabLiKT2_show = pd.DataFrame(tabLiKT2.drop['Fz_250','Fz_350','Fz_450','Fz_500','Fz_510','Fz_530','Fz_560','Fz_580','Fz_600'], axis = 1)
st.write(tabLiKT2)



uploaded_file2 = st.sidebar.file_uploader("Загрузка тестовой ведомости опор для Курской АЭС (Столбец с кодировкой назвать Lisega, кодировка без пробелов)")
if uploaded_file2 is not None:
#    st.write(uploaded_file2)
    B = pd.read_excel(uploaded_file2, sheet_name=0, dtype={'Lisega': str})
    B['Li_type'] = B['Lisega'].str[:2]
    B['Li_diam_class'] = B['Lisega'].str[2:4]
    B['Li_temp_class'] = B['Lisega'].str[4:6]
    B_60 = B.loc[B['Li_type'] == '60']
    B_61 = B.loc[B['Li_type'] == '61']
    
#    B = pd.merge(B, tab_Li, how = 'left', on = ['Lisega'])
    st.write('Соответствие опор запрашиваемых в ведомости ОПС на Курскую АЭС. ',
             '**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
#    B = B.drop(['Li_prod_group', '№ чертежа'], 1)
    st.write(B)
    st.write(B.count())
#    st.write(B_61)
    B = pd.merge(B, ClassRuEn, how = 'inner', on = ['Li_type', 'Li_diam_class']) # 'Li_diam_class''Li_type'
    st.write(B)
    st.write(B.count())
    
#tab_Li['Li type'] = tab_Li['Lisega'].str[:2]
#tab_Li['Li diam class'] = tab_Li['Lisega'].str[2:4]
#tab_Li['Li temp class'] = tab_Li['Lisega'].str[4:6]
#st.write(tab_Li)
#tab_Li_61 = tab_Li.loc[tab_Li['Li type'] == '61']
#st.write(tab_Li_61)
    
    
    
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
    st.sidebar.download_button(label='📥 Скачать обработанную ведомость опор', data=df_xlsx, file_name= 'Ведомость опор на Курскую АЭС.xlsx')
    if st.sidebar.button('📥 Скачать ведомость отправочных марок'):
        st.sidebar.write('Мы тоже хотим чтобы это работало')
        st.balloons()

        

        
        
        
        
st.sidebar.header('Модуль проверки баз данных по АЭС')
stations = ["ЛАЭС-2 - АККУЮ","Курская АЭС", "АЭС АККУЮ", "АЭС Ханхикиви"]
add_selectbox = st.sidebar.selectbox("Выберите базу данных для обзора:", stations)
if st.sidebar.button('Просмотреть'):
    if add_selectbox == "ЛАЭС-2 - АККУЮ":
        st.header('Таблица соответствия ЛАЭС-2 - АККУЮ')
        st.write('**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
        Li2 = st.secrets["public_gsheets_url_Lisega2"]
        rows_Li2 = run_query(f'SELECT * FROM "{Li2}"')
        tab_Li2 = pd.DataFrame(rows_Li2)
        st.write(tab_Li2)
    if add_selectbox == "АЭС АККУЮ":
        st.header('База данных по АЭС АККУЮ')
        st.write('**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
        st.write(tab)
    if add_selectbox == "Курская АЭС":
        st.header('База данных по Курской АЭС')
        st.write('**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
        st.write(tab_Li)
    if add_selectbox == "АЭС Ханхикиви":
        st.header('Оптимистичный выбор :)')
        st.image('https://s.wine.style/images_gen/423/4239/0_0_prod_desktop.jpg')
