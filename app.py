import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import io
import os
import csv

link = 'https://docs.google.com/spreadsheets/d/1EEhBGtNGGFO6okTwj7nzDokZxk-gnfOY/edit?usp=sharing&ouid=112094221269107775969&rtpof=true&sd=true'
classifer = pd.read_excel(link, sheet_name='Классификатор')
st.write(classifer)

uploaded_file_1 = st.file_uploader("Зафгрузка файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file_1 is not None:   
     df1 = pd.read_excel(uploaded_file_1)
     df11 = pd.DataFrame(df1, columns=['Note', 'KKS Code'])
     st.write(df11)

uploaded_file_2 = st.file_uploader("Зафгрузка 2 файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file_2 is not None:   
     df2 = pd.read_excel(uploaded_file_2)
#     df22 = pd.DataFrame(df2, columns=['KKS Code','Note'])
     st.write(df2)

df3 = pd.DataFrame({'first column': [1, 2, 3, 4], 
                   'second column': [10, 20, 30, 40], 
                   'third column': ['ебаный', 'рот', 'этого', 'казино'], 
                   'fourth column': ['Хова', 'ты', 'бредишь', 'чтоли']})
df3

x = st.slider('x')  # 👈 this is a widget
st.write('глупых задач на работе', x, 'насколько мне неинтересно - ', x**x)

title = st.text_input('Введите код AKKU')
st.write('Ну и нахера ты ввел', title)
