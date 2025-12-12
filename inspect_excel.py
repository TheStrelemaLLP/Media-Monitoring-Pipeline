import pandas as pd
import os

input_file = r"c:\Users\HP\Desktop\Media-Monitoring\Input\input_leaders.xlsx"
try:
    df = pd.read_excel(input_file)
    print(df.head())
    print(df.columns)
except Exception as e:
    print(f"Error reading excel: {e}")
