import streamlit as st
from gsheetsdb import connect
import pandas as pd
import numpy as np
import openpyxl
import io
from io import BytesIO
import os
import csv
from pyxlsb import open_workbook as open_xlsb

uploaded_file = st.file_uploader("Зафгрузка файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file is not None:
    B = pd.read_excel(uploaded_file, sheet_name="Sheet1")
    C = pd.read_excel(uploaded_file, sheet_name=2)
    D = pd.read_excel(uploaded_file, sheet_name=3)
    E = pd.read_excel(uploaded_file, sheet_name=4)
    st.write(B)
    st.write(C)
    st.write(D)
    st.write(E)

    
