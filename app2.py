import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Загрузка Excel")
if uploaded_file is not None:
     dataframe = pd.read_csv(io=uploaded_file, 
                             engine='openpylx',
                             sheet_name='Sheet1',
                             skiprows=3,
                             usecols='A:D',
                             nrows=10)  
     st.write(dataframe)

df = pd.DataFrame({'first column': [1, 2, 3, 4], 
                   'second column': [10, 20, 30, 40], 
                   'third column': ['ебаный', 'рот', 'этого', 'казино'], 
                   'fourth column': ['Хова', 'ты', 'бредишь', 'чтоли']})
df

x = st.slider('x')  # 👈 this is a widget
st.write('задач на работе', x, 'насколько мне похуй - ', x * x)
