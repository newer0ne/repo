import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import xlrd
from openpyxl import load_workbook
import csv

uploaded_file = st.file_uploader("Зафгрузка файла в формате xlsx", type='xlsx')
if uploaded_file is not None:   
     book = load_workbook(uploaded_file)
     sheet = book.active
     df = pd.read_excel(uploaded_file)
#     df1 = df.drop([0, 1], axis=0)
#     df1.columns = df1.iloc[0]
#     df2 = df1.drop([2])
#     st.write(df2)
     st.write(df)


df3 = pd.DataFrame({'first column': [1, 2, 3, 4], 
                   'second column': [10, 20, 30, 40], 
                   'third column': ['ебаный', 'рот', 'этого', 'казино'], 
                   'fourth column': ['Хова', 'ты', 'бредишь', 'чтоли']})
df3

x = st.slider('x')  # 👈 this is a widget
st.write('глупых задач на работе', x, 'насколько мне неинтересно - ', x**x)
