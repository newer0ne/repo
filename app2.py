"""
# My first app
Here's our first attempt at using data to create a table:
"""

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     st.write(bytes_data)

     # To convert to a string based IO:
     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
     st.write(stringio)

     # To read file as string:
     string_data = stringio.read()
     st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
     dataframe = pd.read_csv(uploaded_file)
     st.write(dataframe)


import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40],
  'third column': ['ебаный', 'рот', 'этого', 'казино'],
  'fourth column': ['Хова', 'ты', 'бредишь', 'чтоли']
})

df

x = st.slider('x')  # 👈 this is a widget
st.write('задач на работе', x, 'насколько мне похуй - ', x * x)
