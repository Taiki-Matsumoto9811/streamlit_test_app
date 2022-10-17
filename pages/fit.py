import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit  

#近似モデル式
def func_fit(x,a,b,K):
    y = (K * x ** b) / (x ** b + a)
    return y

def uploader():
    uploaded_file = st.file_uploader("ファイルのアップロード", type = 'csv')
    dataframe = None
    df_param = None
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file,encoding="shift-jis")
        st.table(dataframe)
        #print(dataframe[0:0])
        x_observed = np.array(dataframe['GRP'])   #横軸をGRPで固定
        num = dataframe.shape[1]-1 #データの数
        #初期値の設定
        ini_param = (0 ,[100000000. , 5. , 100.] )
        index_list = ["one","three","Aw"]
        a_list = []
        b_list = []
        K_list = []
        R_list = []
        for i in range(num):
            y = dataframe.iloc[:,i+1]
            print(y)
            param, pcov = curve_fit(func_fit,x_observed,y,bounds=ini_param,maxfev=10000000000)
            fit_y = func_fit(x_observed,param[0],param[1],param[2])
            y_ave = np.average(y)
            R = sum((fit_y-y_ave)**2) / sum((y-y_ave)**2)
            a_list.append(param[0])
            b_list.append(param[1])
            K_list.append(param[2])
            R_list.append(R)
        
        df_param = pd.DataFrame({"a":a_list,"b":b_list,"max_value":K_list,"Nunber of decisions":R_list})
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
    st.title("Reach fitting")
    dataframe = uploader()
    print(dataframe)
    


if __name__ == '__main__':
    main()





#with pd.ExcelWriter(filepath2) as writer:
#    df_param.to_excel(writer,sheet_name='Optimal parameters')
#    df_one.to_excel(writer,sheet_name='reach1+')
#    df_three.to_excel(writer,sheet_name='reach3+')
#    df_Aw.to_excel(writer,sheet_name='awereness')