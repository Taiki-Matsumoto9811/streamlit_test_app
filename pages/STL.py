from sqlite3 import Date
import streamlit as st
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def uploader():
    uploaded_file = st.file_uploader("ファイルのアップロード", type = 'csv')
    dataframe = None
    df_param = None
    date = None
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file,encoding="shift-jis",index_col="date",parse_dates=True)

        stl = sm.tsa.seasonal_decompose(dataframe['trend'])
        stl_o = stl.observed #観測データ（STL分解前の元のデータ）＝トレンド＋季節性＋残差
        stl_t = stl.trend    #トレンド（trend）
        stl_s = stl.seasonal #季節性（seasonal）
        stl_r = stl.resid    #残差（resid）
        st.subheader("Observed")
        st.line_chart(data=stl_o,width=0,height=0,use_container_width=True)
        st.subheader("Trend")
        st.line_chart(data=stl_t,width=0,height=0,use_container_width=True)
        st.subheader("Seasonal")
        st.line_chart(data=stl_s,width=0,height=0,use_container_width=True)
        st.subheader("resid")
        st.line_chart(data=stl_r,width=0,height=0,use_container_width=True)

        dataframe.reset_index(inplace=True)
        date = dataframe.rename(columns={'index': 'Items'})['date']

        df_param = pd.DataFrame({"observed":stl_o,"trend":stl_t,"seasonal":stl_s,"resid":stl_r})
        download(df_param)
    return df_param

def convert_df(df):
    return df.to_csv().encode('utf-8')

def download(df):
    df = convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=df,
        file_name='STL.csv',
        mime='text/csv',
    )

def main():
    st.title("STL")
    dataframe = uploader()



if __name__ == '__main__':
    main()


#=====================

#file_path = r"C:\Users\hdypc\python\test.xlsx"
#df = pd.read_excel(file_path)

#x = np.array(df['date'])
#y = np.array(df['trend'])

#df.date = pd.to_datetime(df.date)
#df = df.set_index("date")

#res = sm.tsa.seasonal_decompose(df['trend'])

#print(info(res))

#res.plot()
#plt.show()

#参考URL　https://qiita.com/DS27/items/1e998a58488e76bfcbdc