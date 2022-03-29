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


conn = connect()                                                        # Create a connection object.

# Perform SQL query on the Google Sheet.
@st.cache(ttl=300)                                                       # Uses st.cache to only rerun when the query changes or after 5 min.

def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0,00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


# Модуль загрузок ##########################################################################################################################################################

# Загружаем таблицы
Link_CatLi = st.secrets["CatLi"]
Link_CatKT2 = st.secrets["CatKT2"]
Link_CatAKU = st.secrets["CatAKU"]
Link_Cat = st.secrets["Cat2"]

# Извлекаем строки SQL запросом по линку
rows_CatLi = run_query(f'SELECT * FROM "{Link_CatLi}"')
rows_CatKT2 = run_query(f'SELECT * FROM "{Link_CatKT2}"')
rows_CatAKU = run_query(f'SELECT Note, kt2cat, kt2, name, mass, load FROM "{Link_CatAKU}"')
rows_Cat = run_query(f'SELECT * FROM "{Link_Cat}"')

# Собираем датафреймы
CatLi = pd.DataFrame(rows_CatLi, dtype=str)
CatKT2 = pd.DataFrame(rows_CatKT2, dtype=str)
CatAKU = pd.DataFrame(rows_CatAKU, dtype=str)
Cat = pd.DataFrame(rows_Cat, dtype=str)


# Отображаемый заголовок страницы ##########################################################################################################################################################



st.title('Отдел инновационных технологий')
st.header('Проект Группы Автоматизации')
st.write('Краткое описание интерфейса: слева - панель рабочих функций, ниже - рабочее поле. ',
         'После применения необходимой функции, например, проверки базы данных по АЭС - на рабочем поле отображаются результаты.') 



# Смотрим на наши каталоги ##########################################################################################################################################################



with st.expander("Каталог AKU"):
    #st.header('Каталог Lisega')
    show_CatAKU = CatAKU[['Note', 'kt2cat', 'kt2', 'name', 'mass', 'load']]
    st.write(show_CatAKU)
    title_AKU = st.text_input('Поле ввода кода AKU для проверки')
    st.write(show_CatAKU.loc[show_CatAKU['Note'] == title_AKU])

with st.expander("Каталог Lisega"):
    #st.header('Каталог Lisega')
    show_CatLi = CatLi[['Note', 'Li_name', 'Li_diam', 'Li_Fz_100']]
    st.write(show_CatLi)
    title_Li = st.text_input('Поле ввода кода Lisega для проверки')
    st.write(show_CatLi.loc[show_CatLi['Note'] == title_Li])
    
with st.expander("Каталог KT2"):
    #st.header('Каталог KT2')
    show_CatKT2 = CatKT2[['Note', 'AKU', 'Маркировка_KT2', 'Обозначение_KT2', 'Наименование_KT2', 'KT2_diam', 'Масса_KT2', 'Нагрузка_KT2']]
    st.write(show_CatKT2.sort_values(by=['Маркировка_KT2', 'KT2_diam']))
    title_KT2_1 = st.text_input('Поле ввода Маркировки KT2 для проверки')
    st.write(show_CatKT2.loc[show_CatKT2['Маркировка_KT2'] == title_KT2_1])
    title_KT2_2 = st.text_input('Поле ввода Обозначения KT2 для проверки')
    st.write(show_CatKT2.loc[show_CatKT2['Обозначение_KT2'] == title_KT2_2])
    

    
    
    
    
st.sidebar.header('Модуль классификации ведомостей ОПС') ##################################################################################################
st.sidebar.write("1. Загрузка ведомости опор осуществляется в формате таблиц excel с листа Sheet1")
st.sidebar.write("2. Нужно удалить две верхних строки и первые два скрытых столбца - таблица должна начинаться со столбца KKS Code (в ячейке A1)")
st.sidebar.write("3. Определяемый столбец дожен иметь название Note")

uploaded_file3 = st.sidebar.file_uploader("Область загрузки")
if uploaded_file3 is not None:
    st.write("Filename: ", uploaded_file3.name)
    С = pd.read_excel(uploaded_file3, sheet_name = "Sheet1", dtype = {'Note': str})
    final = pd.merge(С, Cat, how = 'left', on = ['Note'])
    st.write('Соответствие опор запрашиваемых в ведомости.',
             '**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
    st.write(final)
    
    # Скачиваем обработанную ведомость
    df_xlsx = to_excel(final)
    st.sidebar.download_button(label='📥 Скачать обработанную ведомость', data=df_xlsx, file_name=uploaded_file3.name)
    if st.sidebar.button('📥 Скачать ведомость отправочных марок'):
        st.sidebar.write('Мы тоже хотим чтобы это работало')
        st.balloons()


        
        
        
        
        
        
# Выбрасываем лишние стлобцы из каталогов и склеиваем их по средствам pd.merge
#st.header('Таблица соответствия')
#CatLi_Fz100 = CatLi.drop(columns=['Fz_250','Fz_350','Fz_450','Fz_500','Fz_510','Fz_530','Fz_560','Fz_580','Fz_600'])
#CatKT2_Fz100 = CatKT2.drop(columns=['Fz_250','Fz_350'])
#tabLiKT2 = pd.merge(CatLi_Fz100, CatKT2_Fz100, how = 'outer', on = ['Note'])


#with st.expander("Таблица соответствия ОПС Lisega - KT2"):
#    st.write("""В таблице отражено соответствие компонентов ОПС Lisega (2010-2020) и KT2 (EN и RU)
#            с условием, что **нагрузки при 100°С** у элементов KT2 **больше или равны** элементам Lisega
#            """)
#    tabLiKT2[(tabLiKT2.Li_Fz_100 <= tabLiKT2.Нагрузка_KT2)]        
        
        


#st.sidebar.header('Модуль классификации ведомостей ОПС по коду TTT') ##################################################################################################
#uploaded_file = st.sidebar.file_uploader("Загрузка ведомости опор в формате .xls (Нужно удалить первые два скрытых столбца. Таблица должна начинаться со столбца **Код KKS**)")
#if uploaded_file is not None:
#    st.write("Filename: ", uploaded_file.name)
#    A = pd.read_excel(uploaded_file, sheet_name="Sheet1")
#    final = pd.merge(A, CatAKU, how = 'left', on = ['Note'])
#    st.write('Соответствие опор запрашиваемых в ведомости ОПС на АЭС АККУЮ. ',
#             '**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
#    st.write(final)
    
    # Скачиваем обработанную ведомость
#    df_xlsx = to_excel(final)
#    st.sidebar.download_button(label='📥 Скачать обработанную ведомость', data=df_xlsx, file_name=uploaded_file.name)
#    if st.sidebar.button('📥 Скачать ведомость отправочных марок'):
#        st.sidebar.write('Мы тоже хотим чтобы это работало')
#        st.balloons()



#st.sidebar.header('Модуль классификации ведомостей ОПС по коду Lisega') ##################################################################################################

# Создаём кнопку загрузки в сайдбаре для Курской АЭС
#uploaded_file2 = st.sidebar.file_uploader("Загрузка тестовой ведомости опор для Курской АЭС (Столбец с кодировкой назвать Lisega, кодировка без пробелов)")
#if uploaded_file2 is not None:
#    st.write("Filename: ", uploaded_file2.name)
#    B = pd.read_excel(uploaded_file2, sheet_name=0, dtype={'Note': str})
#    show_CatKT2['Note'].astype('str')
#    show_CatKT2['Масса_KT2'].astype('float64')
#    show_CatKT2 = show_CatKT2['Масса_KT2'].round(1)
#    B = pd.merge(B, show_CatKT2, how = 'left', on = ['Note'])
#    st.write('Соответствие опор запрашиваемых в ведомости ОПС на Курскую АЭС. ',
#             '**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
#    B = B.drop(['Li_prod_group', '№ чертежа'], 1)
#    st.write(B)

#    # Скачиваем файл талицы
#    df_xlsx = to_excel(B)
#    st.sidebar.download_button(label='📥 Скачать обработанную ведомость опор', data=df_xlsx, file_name=uploaded_file2.name)
#    if st.sidebar.button('📥 Скачать ведомость отправочных марок'):
#        st.sidebar.write('Мы тоже хотим чтобы это работало')
#        st.balloons()

     
#st.sidebar.header('Модуль проверки баз данных по АЭС') ##################################################################################################
#stations = ["ЛАЭС-2 - АККУЮ","Курская АЭС", "АЭС АККУЮ", "АЭС Ханхикиви"]
#add_selectbox = st.sidebar.selectbox("Выберите базу данных для обзора:", stations)
#if st.sidebar.button('Просмотреть'):
#    if add_selectbox == "ЛАЭС-2 - АККУЮ":
#        st.header('Таблица соответствия ЛАЭС-2 - АККУЮ')
#        st.write('**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
#        Li2 = st.secrets["public_gsheets_url_Lisega2"]
#        rows_Li2 = run_query(f'SELECT * FROM "{Li2}"')
#        tab_Li2 = pd.DataFrame(rows_Li2)
#        st.write(tab_Li2)
#    if add_selectbox == "АЭС АККУЮ":
#        st.header('База данных по АЭС АККУЮ')
#       st.write('**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
#        st.write(tab)
#    if add_selectbox == "Курская АЭС":
#        st.header('База данных по Курской АЭС')
#        st.write('**Развернуть** таблицу на весь экран можно кнопкой, находящейся **в правом верхнем углу** таблицы.')
#        st.write(tab_Li)
#    if add_selectbox == "АЭС Ханхикиви":
#        st.header('Оптимистичный выбор :)')
#        st.image('https://s.wine.style/images_gen/423/4239/0_0_prod_desktop.jpg')
