"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import openpyxl

uploaded_file = st.file_uploader("Загрузка Excel")
if uploaded_file is not None:
     book = pd.read_excel(uploaded_file, read_only = true, engine='openpyxl')
     sheet = book.active
     st.write(sheet)
    
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40],
  'third column': ['ебаный', 'рот', 'этого', 'казино'],
  'fourth column': ['Хова', 'ты', 'бредишь', 'чтоли']
})

df

x = st.slider('x')  # 👈 this is a widget
st.write('задач на работе', x, 'насколько мне похуй - ', x * x)
