import streamlit as st
import io
import os
import xlrd
import pandas as pd
import numpy as np

X = st.file_uploader("Загрузка Excel")
if X is not None:
     excel_workbook = xlrd.open_workbook(X)
     excel_worksheet = excel_workbook.sheet_by_index(1) # Открывает первый лист, 1 - второй и т.д.
     df = pd.DataFrame(excel_worksheet)
     df1 = df.drop([0, 1], axis=0)
     df1.columns = df1.iloc[0]
     df2 = df1.drop([2])
     st.write(df2)

df3 = pd.DataFrame({'first column': [1, 2, 3, 4], 
                   'second column': [10, 20, 30, 40], 
                   'third column': ['ебаный', 'рот', 'этого', 'казино'], 
                   'fourth column': ['Хова', 'ты', 'бредишь', 'чтоли']})
df3

x = st.slider('x')  # 👈 this is a widget
st.write('задач на работе', x, 'насколько мне похуй - ', x * x)
