import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Загрузка Excel")
if uploaded_file is not None:
     string_data = stringio.read()
     st.write(string_data)

df = pd.DataFrame({'first column': [1, 2, 3, 4], 
                   'second column': [10, 20, 30, 40], 
                   'third column': ['ебаный', 'рот', 'этого', 'казино'], 
                   'fourth column': ['Хова', 'ты', 'бредишь', 'чтоли']})
df

x = st.slider('x')  # 👈 this is a widget
st.write('задач на работе', x, 'насколько мне похуй - ', x * x)
