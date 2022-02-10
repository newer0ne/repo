import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import io
import os
import csv

classifer = pd.read_excel(github.com/newer0ne/repo/blob/main/SL1.xlsx)
st.write(classifer)

uploaded_file_1 = st.file_uploader("Зафгрузка файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file_1 is not None:   
     df1 = pd.read_excel(uploaded_file_1)
#     df11 = pd.DataFrame(df1, columns=['Note', 'KKS Code'])
     st.write(df1)
