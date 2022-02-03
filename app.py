import streamlit as st
import io
import os
import xlrd
import pandas as pd
import numpy as np
import csv

uploaded_file = st.file_uploader("Зафгрузка файла в формате CSV", type='csv')
if uploaded_file is not None:
     with open(uploaded_file, 'r', encoding='utf-8', errors='ignore') as infile, open(uploaded_file + 'final.csv', 'w') as outfile:
          inputs = csv.reader(infile)
          output = csv.writer(outfile)

          for index, row in enumerate(inputs):
           # Create file with no header
               if index == 0:
                    continue
               output.writerow(row)
     
     df = pd.read_csv(outfile)
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
st.write('глупых задач на работе', x, 'насколько мне неинтересно - ', x**x)
