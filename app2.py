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
    A = pd.read_excel(uploaded_file, sheet_name=4,5)
    st.write(A)

    
