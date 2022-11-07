import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit  
from scipy.special import gamma
from scipy import optimize

def func_NBD(r,M,K):
    p = ( ( (1+M/K)**(-K) ) * gamma(K+r) ) / ( gamma(r+1) * gamma(K) ) * ( M / (M+K) )**r
    return p

def uploader():
    
    uploaded_file = st.file_uploader("ファイルのアップロード", type = 'csv')
    dataframe = None
    df_param = None
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file,encoding="shift-jis",index_col="index",parse_dates=True)
        st.table(dataframe)
        P0_list = np.array(dataframe['P0'])
        M_list = np.array(dataframe['M'])
        num = len(M_list)
        K_list = []

        for i in range(num):
            P0 = P0_list[i] 
            M = M_list[i]
            def func_NBD0(K):
                return (1+M/K)**(-K)

            def func_dif(K):
                return func_NBD0(K)-P0
            param = optimize.fsolve(func_dif,0)
            K_list.append(param[0])
        
        dataframe['K'] = K_list
        df_param = dataframe
        st.table(df_param)
        download(df_param)
    return df_param

def convert_df(df):
    return df.to_csv().encode('utf-8')

def download(df):
    df = convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=df,
        file_name='fitting.csv',
        mime='text/csv',
    )

def main():
    st.title("NBD")
    dataframe = uploader()
    print(dataframe)
    


if __name__ == '__main__':
    main()