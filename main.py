import streamlit as st
import numpy as np
import pandas as pd

def uploader():
    uploaded_file = st.file_uploader("ファイルのアップロード", type = 'csv')
    dataframe = None
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file,encoding="shift-jis")
    return dataframe

def main():
    st.title("トップページ")
    dataframe = uploader()
    st.table(dataframe)
    

if __name__ == '__main__':
    main()
