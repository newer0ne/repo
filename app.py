import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import io
import os
import csv

# .streamlit/secrets.toml

public_gsheets_url = "https://docs.google.com/spreadsheets/d/1peUU7SHhShwFGF2cdpclgr3xJOJii2OQ/edit#gid=2119343756"

uploaded_file_1 = st.file_uploader("Зафгрузка файла в формате .xlsx .xls .odf, .ods, .odt")
if uploaded_file_1 is not None:   
     df1 = pd.read_excel(uploaded_file_1)
#     df11 = pd.DataFrame(df1, columns=['Note', 'KKS Code'])
     st.write(df1)
