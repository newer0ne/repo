import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import io
import os
import csv

#link = 'https://github.com/newer0ne/repo/blob/main/book.xlsx'
#classifer = pd.read_excel(link)
#st.write(classifer)

uploaded_file_1 = st.file_uploader("Зафгрузка файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file_1 is not None:   
     df1 = pd.read_excel(uploaded_file_1)
     df11 = pd.DataFrame(df1, columns=['Note', 'KKS Code'])
     st.write(df11)

uploaded_file_2 = st.file_uploader("Зафгрузка 2 файла в формате .xlsx)
if uploaded_file_2 is not None:   
     df2 = pd.read_excel(uploaded_file_2)
#     df22 = pd.DataFrame(df2, columns=['KKS Code','Note'])
     st.write(df2)
