import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import io
import os
import csv

uploaded_file = st.file_uploader("Зафгрузка файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file is not None:   
     df1 = pd.read_excel(uploaded_file)
     df1 = pd.DataFrame(df, columns=['KKS Code','Note'])
     st.write(df1)

uploaded_file_2 = st.file_uploader("Зафгрузка 2 файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file_2 is not None:   
     df2 = pd.read_excel(uploaded_file_2)
     df2 = pd.DataFrame(df, columns=['KKS Code','Note'])
     st.write(df2)

df3 = pd.DataFrame({'first column': [1, 2, 3, 4], 
                   'second column': [10, 20, 30, 40], 
                   'third column': ['ебаный', 'рот', 'этого', 'казино'], 
                   'fourth column': ['Хова', 'ты', 'бредишь', 'чтоли']})
df3

x = st.slider('x')  # 👈 this is a widget
st.write('глупых задач на работе', x, 'насколько мне неинтересно - ', x**x)

title = st.text_input('Введите код AKKU', 'Код')
st.write('The current movie title is', title)
