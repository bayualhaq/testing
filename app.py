# Author
__judul__       = "Peramalan Harga Saham Menggunakan Pengembangan Moving Average di PT. Unilever Indonesia Tbk"
__author__      = "Ahmad Try Bayu Al Haq"
__nim__         = "170441100024"
__copyright__   = "Copyright 2022, Tugas Akhir Skripsi Universitas Trunojoyo Madura"
__version__     = "1.0.1"
__email__       = "bayualhaq@gmail.com"

# Import
import streamlit as st
import yfinance as yf
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Menampilkan Sidebar parameter
st.sidebar.subheader('Masukkan Parameter berikut:')

# memasukkan kode saham, default UNVR.JK, ADHI.JK, ^JKSE
ticker = st.sidebar.text_input("Kode Saham", "ADHI.JK")

metode = st.sidebar.selectbox(
        'Metode Peramalan Saham',
        ('SMA', 'WMA', 'WEMA', 'BWEMA'))
        
# Unilever
# start_date   = st.sidebar.date_input("Tanggal Mulai", datetime.date(2021, 12, 1)) #Input Tanggal Awal
# end_date     = st.sidebar.date_input("Tanggal Akhir", datetime.date(2021, 12, 31)) #Input Tanggal Akhir

# ^JKSE
# start_date   = st.sidebar.date_input("Tanggal Mulai", datetime.date(2013, 9, 2)) #Input Tanggal Awal
# end_date     = st.sidebar.date_input("Tanggal Akhir", datetime.date(2013, 11, 13)) #Input Tanggal Akhir

# ^JKSE 2017 - 2018
# start_date   = st.sidebar.date_input("Tanggal Mulai", datetime.date(2017, 5, 2)) #Input Tanggal Awal
# end_date     = st.sidebar.date_input("Tanggal Akhir", datetime.date(2018, 5, 3)) #Input Tanggal Akhir

# ADHI
start_date   = st.sidebar.date_input("Tanggal Mulai", datetime.date(2017, 3, 1)) #Input Tanggal Awal
end_date     = st.sidebar.date_input("Tanggal Akhir", datetime.date(2018, 3, 2)) #Input Tanggal Akhir

# penggambilan tanggal untuk save file CSV
start_date_str  = start_date.strftime("%Y-%m-%d")
end_date_str    = end_date.strftime("%Y-%m-%d")

# mendapatkan data dari yahoo finance dari inputan kode saham
ticker_data = yf.Ticker(ticker)

# mendapatkan data harga saham dengan periode 1 hari
ticker_df = ticker_data.history(period='1d', start=start_date, end=end_date, auto_adjust = False)

# Kondisi pengecekan apakah saham itu ada atau tidak
if ticker_df.empty:
    st.error('Kode Saham **'+ticker+'** tidak ditemukan atau **Koneksi Internet** Anda bermasalah, silahkan cek ulang kembali')
else:   
    st.warning('Kode Saham **'+ticker+'** ditemukan')
        
    # Mengubah tanggal dan menghilangkan index pada kolom Date
    ticker_df.index = ticker_df.index.strftime("%Y-%m-%d")
    ticker_df=ticker_df.reset_index(drop=False)
    ticker_df.index += 1

    # Menghapus kolom Dividends dan Stock Splits
    ticker_df = ticker_df.drop(columns=['Dividends', 'Stock Splits'])

    # Judul
    string_name = ticker_data.info['longName'] 
    st.markdown("<h2 style='text-align: center'>Peramalan Harga Saham</h2>".format(string_name), unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center'>%s</h2>" % string_name, unsafe_allow_html=True)

    # # mengambil logo Saham
    # string_logo = '<center><img src=%s></center></br>' % ticker_data.info['logo_url'] 
    # st.markdown(string_logo, unsafe_allow_html=True)

    # mengambil deskripsi saham
    # script ignore jika kode error dan tetap menjalankan script lain 
    try:
        string_summary = ticker_data.info['longBusinessSummary']
        st.warning(string_summary)
    except:
        st.error("Deskripsi Tidak Ada")
    
    # Data Saham ditampilkan dalam bentuk tabel
    st.markdown("<h2 style='text-align: center'>Data Histori Harga Saham</h2>", unsafe_allow_html=True)
    st.write(ticker_df)

    # Menampilkan Candlestick
    st.markdown("<h2 style='text-align: center'>Grafik Candlestick</h2>", unsafe_allow_html=True)
    fig_candle = go.Figure(data=[go.Candlestick(
        x=ticker_df.index,
        open=ticker_df.Open, 
        high=ticker_df.High,
        low=ticker_df.Low, 
        close=ticker_df.Close,
        increasing_line_color= '#E19318', 
        decreasing_line_color= '#1866E1'
    )])
    fig_candle.update_layout(
                        xaxis_title='Hari',
                        yaxis_title='Harga Saham',
                        hovermode="x unified",
                        xaxis=dict(showgrid=False,showline=True,zeroline=False),
                        yaxis=dict(showgrid=False,showline=True,zeroline=False),
                        autosize=True,
                        margin=dict(
                            l=50,
                            r=0,
                            b=30,
                            t=30,
                            pad=1)
                        )
    st.plotly_chart(fig_candle)

    # Menghapus kolom 'Open','High','Low', 'Adj Close', 'Volume'
    df_close = ticker_df.drop(columns=['Open','High','Low', 'Adj Close', 'Volume'])

    # Total data peramalan
    totaldata=df_close["Close"].count()

    # Membuat baris baru untuk hasil peramalan
    forecast = [
        ['Peramalan'],
    ] 

    # Membuat dataframe untuk menampung inputan harga saham yang baru
    df_close1 = pd.DataFrame(forecast, columns =['Date'])

    #menggabungkan df_close dan df_close1 menjadi variabel df_close2
    # df_close2 = df_close.append(df_close1, ignore_index=True, sort=False)
    df_close2 = pd.concat([df_close, pd.DataFrame(df_close1)], ignore_index=True, sort=False)

    
    # If Elif Else pemilihan metode peramalan
    ################################## METODE SMA ##################################
    if metode == 'SMA':
        st.markdown("""---""")
        st.markdown("<h2 style='text-align: center'>Hasil Peramalan Metode SMA</h2>", unsafe_allow_html=True)

        # Copy dataframe df_close2 ke variabel baru df_close_sma
        df_close_sma = df_close2.copy()
    
        # Memasukkan input Nilai Moving Average    
        ma_sma    = st.number_input('Masukkan jumlah moving average `SMA`', 
                                    min_value   = 1, 
                                    max_value   = 100, 
                                    value       =5)          # nilai awal moving average adalah 5
        
        # Menampilkan Nilai Moving Average
        st.warning('Nilai moving average **'+str(ma_sma)+'**')
        
        # melakukan perhitungan peramalan metode SMA
        df_close_sma['SMA'] = np.round(df_close_sma['Close'].rolling(ma_sma).mean().shift(1),decimals=2)
        
        # Perintah untuk menghitung nilai error SMA dari MAD dan MAPE
        df_close_sma['MAD'] = np.round((df_close_sma['Close']-df_close_sma['SMA']).abs(),decimals=2)
        df_close_sma['MAPE'] = np.round((df_close_sma['MAD']/df_close_sma['Close'])*100,decimals=2)

        # Perintah untuk menghitang rata-rata MAD dan MAPE
        madsma = np.round(df_close_sma['MAD'].mean(), decimals=2)
        mapesma = np.round(df_close_sma['MAPE'].mean(), decimals=2)

        # Mengambil data aktual terakhir 
        data_akhir_aktual_sma = (df_close_sma['Close'].iloc[-2])

        # Mengambil data hasil peramalan periode selanjutnya 
        hasil_peramalan_sma = (df_close_sma['SMA'].iloc[-1])

        # menghitung akurasi dari data aktual dengan nilai prediksi
        hasil_akurasi_sma = np.round(100-(np.absolute(data_akhir_aktual_sma-hasil_peramalan_sma)/data_akhir_aktual_sma)*100,decimals=2)

        # Perintah untuk membuat dataframe baru
        data_sma = {
            'Date'  :['Rata-rata', 
                      'Moving Average', 
                      'Akurasi Peramalan',
                      'Total Data'],
            'MAD'   :[madsma, 
                      np.nan, 
                      np.nan,
                      np.nan],
            'MAPE'  :[mapesma,
                      np.nan, 
                      np.nan,
                      np.nan],
            'Close' :[np.nan, 
                      ma_sma, 
                      hasil_akurasi_sma,
                      totaldata]}

        df_sma = pd.DataFrame(data_sma)

        # Perintah untuk mengabungkan dataframe df_close_sma dan df_sma
        # hasilsma = df_close_sma.append(df_sma, ignore_index=True, sort=False)
        hasilsma = pd.concat([df_close_sma, pd.DataFrame(df_sma)], ignore_index=True, sort=False)


        #membuat index dimulai dari angka 1
        hasilsma.index += 1
        
        # menampilkan hasil dalam bentuk tabel
        st.dataframe(hasilsma)

        # menampilkan grafik garis hasil peramalan metode SMA
        df_close_sma.index +=1
        fig_sma = go.Figure()
        fig_sma.update_traces(hovertemplate=None)
        fig_sma.add_trace(go.Scatter(x=df_close_sma.index,y=df_close_sma.Close,
                                mode='lines',
                                name='Close',
                                marker=dict(
                                    color='#E19318',
                                    size=20))
                                )
        fig_sma.add_trace(go.Scatter(x=df_close_sma.index,
                                y=df_close_sma.SMA,
                                mode='lines',
                                name='SMA',
                                marker=dict(
                                    color='#1866E1',
                                    size=20),
                                    line=dict(dash='dash'))
                                )
        fig_sma.update_layout(title='Grafik Peramalan Harga Penutupan Saham ' +string_name+' dengan Metode '+metode,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1),
                        xaxis_title='Hari',
                        yaxis_title='Harga Penutupan Saham',
                        hovermode="x unified",
                        xaxis=dict(showgrid=False,showline=True,zeroline=False),
                        yaxis=dict(showgrid=False,showline=True,zeroline=False),
                        autosize=True,
                        margin=dict(
                            l=50,
                            r=0,
                            b=30,
                            t=100,
                            pad=1)
                        )
        st.plotly_chart(fig_sma)
        
        # menampilkan hasil kesimpulan dalam bentuk kolom
        col1, col2, col3 = st.columns(3)
        col1.subheader("Total Data")
        col1.markdown(totaldata)

        col2.subheader("Moving Average")
        col2.markdown(ma_sma)

        col3.subheader("Hasil Peramalan")
        col3.markdown(hasil_peramalan_sma)

        col4, col5, col6 = st.columns(3)
        col4.subheader("Akurasi Peramalan")
        col4.markdown("{}%".format(hasil_akurasi_sma))

        col5.subheader("MAD")
        col5.markdown(madsma)

        col6.subheader("MAPE")
        col6.markdown("{}%".format(mapesma))
      
        #Download data CSV SMA
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(hasilsma)

        st.download_button(
            label="Download Hasil Peramalan SMA ",
            data=csv,
            file_name='Hasil Peramalan Metode SMA dengan Kode Saham '+ticker+' ('+start_date_str+' - '+end_date_str+').csv',
            mime='text/csv',
        )
    
    ################################## METODE WMA ##################################
    elif metode == 'WMA':

        st.markdown("""---""")
        st.markdown("<h2 style='text-align: center'>Hasil Peramalan Metode WMA</h2>", unsafe_allow_html=True)

        # menyalin dataframe df_close2 ke df_close_wma
        df_close_wma = df_close2.copy()
    
        # Memasukkan input Nilai Moving Average dan Bobot           
        ma_wma    = st.number_input('Masukkan jumlah moving average `WMA` dan `Bobot`', 
                                    min_value   = 1, 
                                    max_value   = 100, 
                                    value       =5)         # nilai awal moving average adalah 5

        bobotwma          = np.arange(1, 1+ma_wma)      # nilai bobot mulai dari angka 1 sampai batas jumlah moving average
        reversed_arr = bobotwma[::-1]              # membalik nilai array untuk menampilkan pada halaman website
        totalbobotwam     = np.sum(bobotwma)            # menjumlah nilai bobot

        # Menampilkan Nilai Moving Average dan Bobot
        st.warning('Nilai moving average **'+str(ma_wma)+'** | Nilai bobot yang digunakan **'+str(reversed_arr)+'** | Total nilai bobot **'+str(totalbobotwam)+'**')
        
        # menghitung peramalan WMA
        df_close_wma['WMA'] = np.round(df_close_wma['Close'].rolling(ma_wma).apply(lambda x: np.sum(bobotwma*x)/totalbobotwam).shift(1),decimals=2)
        
        # Perintah untuk menghitung nilai error WMA dari MAD dan MAPE
        df_close_wma['MAD'] = np.round((df_close_wma['Close']-df_close_wma['WMA']).abs(),decimals=2)
        df_close_wma['MAPE'] = np.round((df_close_wma['MAD']/df_close_wma['Close'])*100,decimals=2)

        # Perintah untuk menghitang rata-rata MAD dan MAPE
        madwma = np.round(df_close_wma['MAD'].mean(), decimals=2)
        mapewma = np.round(df_close_wma['MAPE'].mean(), decimals=2)

        # Mengambil data aktual terakhir 
        data_akhir_aktual_wma = (df_close_wma['Close'].iloc[-2])

        # Mengambil data hasil peramalan periode selanjutnya 
        hasil_peramalan_wma = (df_close_wma['WMA'].iloc[-1])

        # menghitung akurasi dari data aktual dengan nilai prediksi
        hasil_akurasi_wma = np.round(100-(np.absolute(data_akhir_aktual_wma-hasil_peramalan_wma)/data_akhir_aktual_wma)*100,decimals=2)

        # Perintah untuk membuat dataframe baru
        data_wma = {
            'Date'  :['Rata-rata', 
                    'Moving Average', 
                    'Akurasi Peramalan',
                    'Total Data'],
            'MAD'   :[madwma, 
                    np.nan, 
                    np.nan,
                    np.nan],
            'MAPE'  :[mapewma,
                    np.nan, 
                    np.nan,
                    np.nan],
            'Close' :[np.nan, 
                    ma_wma, 
                    hasil_akurasi_wma,
                    totaldata]}

        df_wma = pd.DataFrame(data_wma)

        # Perintah untuk mengabungkan dataframe df_close_wma dan df_wma
        hasil_wma = df_close_wma.append(df_wma, ignore_index=True, sort=False)

        #membuat index dimulai dari angka 1
        hasil_wma.index += 1
        
        # menampilkan hasil dalam bentuk tabel
        st.dataframe(hasil_wma)

        # menampilkan grafik garis hasil peramalan metode WMA
        df_close_wma.index +=1
        fig_wma = go.Figure()
        fig_wma.update_traces(hovertemplate=None)
        fig_wma.add_trace(go.Scatter(x=df_close_wma.index,y=df_close_wma.Close,
                                mode='lines',
                                name='Close',
                                marker=dict(
                                    color='#E19318',
                                    size=20))
                                )
        fig_wma.add_trace(go.Scatter(x=df_close_wma.index,
                                y=df_close_wma.WMA,
                                mode='lines',
                                name='WMA',
                                marker=dict(
                                    color='#1866E1',
                                    size=20),
                                    line=dict(dash='dash'))
                                )
        fig_wma.update_layout(title='Grafik Peramalan Harga Penutupan Saham ' +string_name+' dengan Metode '+metode,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1),
                        xaxis_title='Hari',
                        yaxis_title='Harga Penutupan Saham',
                        hovermode="x unified",
                        xaxis=dict(showgrid=False,showline=True,zeroline=False),
                        yaxis=dict(showgrid=False,showline=True,zeroline=False),
                        autosize=True,
                        margin=dict(
                            l=50,
                            r=0,
                            b=30,
                            t=100,
                            pad=1)
                        )
        st.plotly_chart(fig_wma)

        # menampilkan hasil kesimpulan dalam bentuk kolom
        col1, col2, col3 = st.columns(3)
        col1.subheader("Total Data")
        col1.markdown(totaldata)

        col2.subheader("Moving Average")
        col2.markdown(ma_wma)

        col3.subheader("Hasil Peramalan")
        col3.markdown(hasil_peramalan_wma)

        col4, col5, col6 = st.columns(3)
        col4.subheader("Akurasi Peramalan")
        col4.markdown("{}%".format(hasil_akurasi_wma))

        col5.subheader("MAD")
        col5.markdown(madwma)

        col6.subheader("MAPE")
        col6.markdown("{}%".format(mapewma))

        #Download data CSV WMA
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(hasil_wma)

        st.download_button(
            label="Download Hasil Peramalan WMA ",
            data=csv,
            file_name='Hasil Peramalan Metode WMA dengan Kode Saham '+ticker+' ('+start_date_str+' - '+end_date_str+').csv',
            mime='text/csv',
        )
    
    ################################## METODE WEMA ##################################
    elif metode == 'WEMA':

        st.markdown("""---""")
        st.markdown("<h2 style='text-align: center'>Hasil Peramalan Metode WEMA</h2>", unsafe_allow_html=True)

        # menyalin dataframe df_close2 ke df_close_wema
        df_close_wema = df_close2.copy()
    
        # Memasukkan input Nilai Moving Average dan Bobot  
        ma_wema    = st.number_input('Masukkan jumlah moving average `WEMA` dan `Bobot`', 
                                    min_value   = 1, 
                                    max_value   = 100, 
                                    value       =5)          # nilai awal moving average adalah 5
        alpha_wema = st.number_input(
                                    "Masukkan Nilai Alpha",
                                    min_value   =0.1,
                                    max_value   =1.0,
                                    value       =2/(ma_wema+1),
                                    key=0            
                                    )                       # nilai alpha mulai dari 0.1 sampai 1.0
        bobotwema          = np.arange(1, 1+ma_wema)        # nilai bobot mulai dari angka 1 sampai batas jumlah moving average
        reversed_bobotwema = bobotwema[::-1]                # membalik nilai array untuk menampilkan pada halaman website
        totalbobotwema     = np.sum(bobotwema)              # menjumlah nilai 
        
        # Menampilkan Nilai Moving Average dan Bobot
        st.warning('Nilai moving average **'+str(ma_wema)+'** | Nilai bobot yang digunakan **'+str(reversed_bobotwema)+'** | Total nilai bobot **'+str(totalbobotwema)+'**')

        # inisialisasi metode WEMA dengan menggunakan nilai awal dari metode WMA
        df_close_wema['WEMA'] = np.round(df_close_wema['Close']
            .rolling(ma_wema)
            .apply(lambda x: np.sum(bobotwema*x)/totalbobotwema)
            .shift(1),
            decimals=2
        )

        # membuat perulangan untuk mencari nilai peramalan WEMA
        for i in range(0, df_close_wema.shape[0] - (ma_wema+1)):
            df_close_wema.loc[(i+ma_wema+1),'WEMA'] = np.round(
                alpha_wema*df_close_wema.loc[(i+ma_wema),'Close']
                +(1-alpha_wema)*df_close_wema.loc[(i+ma_wema),'WEMA'],
                decimals=2
            )

        # Perintah untuk menghitung nilai error WEMA dari MAD, MSE dan MAPE
        df_close_wema['MAD'] = np.round((df_close_wema['Close']-df_close_wema['WEMA']).abs(),decimals=2)
        df_close_wema['MSE'] = np.round(df_close_wema['MAD']**2,decimals=2)
        df_close_wema['MAPE'] = np.round((df_close_wema['MAD']/df_close_wema['Close'])*100,decimals=2)

        # Perintah untuk menghitang rata-rata MAD, MSE dan MAPE
        madwema = np.round(df_close_wema['MAD'].mean(), decimals=2)
        msewema = np.round(df_close_wema['MSE'].mean(), decimals=2)
        mapewema = np.round(df_close_wema['MAPE'].mean(), decimals=2)

        # Mengambil data aktual terakhir 
        data_akhir_aktual_wema = (df_close_wema['Close'].iloc[-2])

        # Mengambil data hasil peramalan periode selanjutnya 
        hasil_peramalan_wema = (df_close_wema['WEMA'].iloc[-1])

        # menghitung akurasi dari data aktual dengan nilai prediksi
        hasil_akurasi_wema = np.round(100-(np.absolute(data_akhir_aktual_wema-hasil_peramalan_wema)/data_akhir_aktual_wema)*100,decimals=2)

        # Perintah untuk membuat dataframe baru
        data_wema = {
            'Date'  :['Rata-rata', 
                    'Moving Average', 
                    'Akurasi Peramalan',
                    'Total Data'],
            'MAD'   :[madwema, 
                    np.nan, 
                    np.nan,
                    np.nan],
            'MSE'   :[msewema, 
                    np.nan, 
                    np.nan,
                    np.nan],
            'MAPE'  :[mapewema,
                    np.nan, 
                    np.nan,
                    np.nan],
            'Close' :[np.nan, 
                    ma_wema, 
                    hasil_akurasi_wema,
                    totaldata]}

        df_wema = pd.DataFrame(data_wema)

        # Perintah untuk mengabungkan dataframe df_close_wema dan df_wema
        hasil_wema = df_close_wema.append(df_wema, ignore_index=True, sort=False)

        #membuat index dimulai dari angka 1
        hasil_wema.index += 1
        
        # menampilkan hasil dalam bentuk tabel
        st.dataframe(hasil_wema)

        # menampilkan grafik garis hasil peramalan metode WEMA
        df_close_wema.index +=1
        fig_wema = go.Figure()
        fig_wema.update_traces(hovertemplate=None)
        fig_wema.add_trace(go.Scatter(x=df_close_wema.index,
                                y=df_close_wema.Close,
                                mode='lines',
                                name='Close',
                                marker=dict(
                                    color='#E19318',
                                    size=20))
                                )
        fig_wema.add_trace(go.Scatter(x=df_close_wema.index,
                                y=df_close_wema.WEMA,
                                mode='lines',
                                name='WEMA',
                                marker=dict(
                                    color='#1866E1',
                                    size=20),
                                    line=dict(dash='dash'))
                                )
        fig_wema.update_layout(title='Grafik Peramalan Harga Penutupan Saham ' +string_name+' dengan Metode '+metode,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1),
                        xaxis_title='Hari',
                        yaxis_title='Harga Penutupan Saham',
                        hovermode="x unified",
                        xaxis=dict(showgrid=False,showline=True,zeroline=False),
                        yaxis=dict(showgrid=False,showline=True,zeroline=False),
                        autosize=True,
                        margin=dict(
                            l=50,
                            r=0,
                            b=30,
                            t=100,
                            pad=1)
                        )
        st.plotly_chart(fig_wema)

        # menampilkan hasil kesimpulan dalam bentuk kolom
        col1, col2, col3 = st.columns(3)
        col1.subheader("Total Data")
        col1.markdown(totaldata)

        col2.subheader("Moving Average")
        col2.markdown(ma_wema)

        col3.subheader("Hasil Peramalan")
        col3.markdown(hasil_peramalan_wema)

        col4, col5, col6 = st.columns(3)
        col4.subheader("Akurasi Peramalan")
        col4.markdown("{}%".format(hasil_akurasi_wema))

        col5.subheader("MAD")
        col5.markdown(madwema)

        col6.subheader("MAPE")
        col6.markdown("{}%".format(mapewema))

        #Download data CSV WEMA
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(hasil_wema)

        st.download_button(
            label="Download Hasil Peramalan WEMA ",
            data=csv,
            file_name='Hasil Peramalan Metode WEMA dengan Kode Saham '+ticker+' ('+start_date_str+' - '+end_date_str+').csv',
            mime='text/csv',
        )

    ################################## METODE B-WEMA ##################################
    else:

        st.markdown("""---""")
        st.markdown("<h2 style='text-align: center'>Hasil Peramalan Metode B-WEMA</h2>", unsafe_allow_html=True)

        # menyalin dataframe df_close2 ke df_close_bwema
        df_close_bwema = df_close2.copy()
    
        # Memasukkan input Nilai Moving Average dan Bobot  
        ma_bwema    = st.number_input('Masukkan jumlah moving average `B-WEMA` dan `Bobot`', 
                                    min_value   = 1, 
                                    max_value   = 100, 
                                    value       =5)         # nilai awal moving average adalah 5
        alpha_bwema = st.number_input(
                                    "Masukkan Nilai Alpha",
                                    min_value   =0.1,
                                    max_value   =1.0,
                                    value       =0.44 ,
                                    key=1           
                                    )                       # nilai alpha mulai dari 0.1 sampai 1.0
        bobotbwema          = np.arange(1, 1+ma_bwema)      # nilai bobot mulai dari angka 1 sampai batas jumlah moving average
        reversed_bobotbwema = bobotbwema[::-1]              # membalik nilai array untuk menampilkan pada halaman website
        totalbobotbwema     = np.sum(bobotbwema)            # menjumlah nilai bobot

        # meramalkan periode selanjutnya dengan inputan awal 1
        periode_peramalan_bwema = st.number_input("Masukkan jumlah peramalan yang akan ditampilkan",min_value=1,max_value=100,value=1)
        
        # Menampilkan Nilai Moving Average dan Bobot
        st.warning('Nilai moving average **'+str(ma_bwema)+'** | Nilai bobot yang digunakan **'+str(reversed_bobotbwema)+'** | Total nilai bobot **'+str(totalbobotbwema)+'** | Peramalan yang ditampilkan **'+str(periode_peramalan_bwema)+'**')
        
        # inisialisasi metode B-WEMA dengan menggunakan nilai awal dari metode WMA
        df_close_bwema['S1'] = df_close_bwema['S2'] = df_close_bwema['a'] = np.round(df_close_bwema['Close']
            .rolling(ma_bwema)
            .apply(lambda x: np.sum(bobotbwema*x)/totalbobotbwema),
            decimals=2
        )
        df_close_bwema.loc[(ma_bwema-1),'b'] = 0
        
        # membuat perulangan untuk mencari nilai pemulusan S1 dan S2
        for i in range(0, df_close_bwema.shape[0] - ma_bwema):
            # mendapatkan nilai pemulusan ke S1
            df_close_bwema.loc[(i+ma_bwema),'S1'] = np.round(
                alpha_bwema*df_close_bwema.loc[(i+ma_bwema),'Close']
                +(1-alpha_bwema)*df_close_bwema.loc[(i+ma_bwema-1),'S1'],
                decimals=2
            )

            # mendapatkan nilai pemulusan ke S2
            df_close_bwema.loc[(i+ma_bwema),'S2'] = np.round(
                alpha_bwema*df_close_bwema.loc[(i+ma_bwema),'S1']
                +(1-alpha_bwema)*df_close_bwema.loc[(i+ma_bwema-1),'S2'],
                decimals=2
            )

            # mendapatkan nilai a
            df_close_bwema.loc[(i+ma_bwema),'a'] = np.round(
                2*df_close_bwema.loc[(i+ma_bwema),'S1']-df_close_bwema.loc[(i+ma_bwema),'S2'],
                decimals=2
            )

            # mendapatkan nilai b
            df_close_bwema.loc[(i+ma_bwema),'b'] = np.round(
                (alpha_bwema/(1-alpha_bwema))
                *(df_close_bwema.loc[(i+ma_bwema),'S1']-df_close_bwema.loc[(i+ma_bwema),'S2']),
                decimals=2
            )
        
        # mendapatkan nilai peramalan BWEMA
        df_close_bwema['BWEMA'] = (df_close_bwema['a']+df_close_bwema['b']).shift(1)

        # Perintah untuk menghitung nilai error WEMA dari MAD, MSE dan MAPE
        df_close_bwema['MAD'] = np.round((df_close_bwema['Close']-df_close_bwema['BWEMA']).abs(),decimals=2)
        df_close_bwema['MSE'] = np.round(df_close_bwema['MAD']**2,decimals=2)
        df_close_bwema['MAPE'] = np.round((df_close_bwema['MAD']/df_close_bwema['Close'])*100,decimals=2)

        # Perintah untuk menghitang rata-rata MAD, MSE dan MAPE
        madbwema = np.round(df_close_bwema['MAD'].mean(), decimals=2)
        msebwema = np.round(df_close_bwema['MSE'].mean(), decimals=2)
        mapebwema = np.round(df_close_bwema['MAPE'].mean(), decimals=2)

        # variabel penampungan hasil peramalan
        peramalan_bwema = []

        # perulangan untuk menghitung peramalan periode selanjutnya
        for i in range(2,periode_peramalan_bwema+1):
            ramal_periode = df_close_bwema['a'].iloc[-2]+(df_close_bwema['b'].iloc[-2]*i)
            peramalan_bwema.append(ramal_periode)

        # memasukkan data peramalan ke dataframe baru
        data_penampungan_bwema = {'Date':'Peramalan','BWEMA':peramalan_bwema}
        df_data_penampungan_bwema = pd.DataFrame(data_penampungan_bwema)

        # mengabungkan dataframe baru ke dataframe lama 
        df_close_bwema = df_close_bwema.append(df_data_penampungan_bwema, ignore_index=True, sort=False)

        # Mengambil data aktual terakhir 
        data_akhir_aktual_bwema = (df_close_bwema['Close'].iloc[-periode_peramalan_bwema-1])

        # Mengambil data hasil peramalan periode selanjutnya 
        hasil_peramalan_bwema = np.round((df_close_bwema['BWEMA'].iloc[-1]),decimals=2)

        # menghitung akurasi dari data aktual dengan nilai prediksi
        hasil_akurasi_bwema = np.round(100-(np.absolute(data_akhir_aktual_bwema-hasil_peramalan_bwema)/data_akhir_aktual_bwema)*100,decimals=2)

        # Perintah untuk membuat dataframe baru
        data_bwema = {
            'Date'  :['Rata-rata', 
                    'Moving Average', 
                    'Akurasi Peramalan',
                    'Total Data'],
            'MAD'   :[madbwema, 
                    np.nan, 
                    np.nan,
                    np.nan],
            'MSE'   :[msebwema, 
                    np.nan, 
                    np.nan,
                    np.nan],
            'MAPE'  :[mapebwema,
                    np.nan, 
                    np.nan,
                    np.nan],
            'Close' :[np.nan, 
                    ma_bwema, 
                    hasil_akurasi_bwema,
                    totaldata]}

        df_bwema = pd.DataFrame(data_bwema)

        # Perintah untuk mengabungkan dataframe df_close_wema dan df_wema
        hasil_bwema = df_close_bwema.append(df_bwema, ignore_index=True, sort=False)

        #membuat index dimulai dari angka 1
        hasil_bwema.index += 1
        
        # menampilkan hasil dalam bentuk tabel
        st.dataframe(hasil_bwema)

        # menampilkan grafik garis hasil peramalan metode BWEMA
        df_close_bwema.index +=1
        fig_bwema = go.Figure()
        fig_bwema.update_traces(hovertemplate=None)
        fig_bwema.add_trace(go.Scatter(x=df_close_bwema.index,
                                y=df_close_bwema.Close,
                                mode='lines',
                                name='Close',
                                marker=dict(
                                    color='#E19318',
                                    size=20))
                                )
        fig_bwema.add_trace(go.Scatter(x=df_close_bwema.index,
                                y=df_close_bwema.BWEMA,
                                mode='lines',
                                name='BWEMA',
                                marker=dict(
                                    color='#1866E1',
                                    size=20),
                                    line=dict(dash='dash'))
                                )
        fig_bwema.update_layout(title='Grafik Peramalan Harga Penutupan Saham ' +string_name+' dengan Metode '+metode,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1),
                        xaxis_title='Hari',
                        yaxis_title='Harga Penutupan Saham',
                        hovermode="x unified",
                        xaxis=dict(showgrid=False,showline=True,zeroline=False),
                        yaxis=dict(showgrid=False,showline=True,zeroline=False),
                        autosize=True,
                        margin=dict(
                            l=50,
                            r=0,
                            b=30,
                            t=100,
                            pad=1)
                        )
        st.plotly_chart(fig_bwema)

        # menampilkan hasil kesimpulan dalam bentuk kolom
        col1, col2, col3 = st.columns(3)
        col1.subheader("Total Data")
        col1.markdown(totaldata)

        col2.subheader("Moving Average")
        col2.markdown(ma_bwema)

        col3.subheader("Hasil Peramalan")
        col3.markdown(hasil_peramalan_bwema)

        col4, col5, col6 = st.columns(3)
        col4.subheader("Akurasi Peramalan")
        col4.markdown("{}%".format(hasil_akurasi_bwema))

        col5.subheader("MAD")
        col5.markdown(madbwema)

        col6.subheader("MAPE")
        col6.markdown("{}%".format(mapebwema))

        #Download data CSV BWEMA
        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(hasil_bwema)

        st.download_button(
            label="Download Hasil Peramalan BWEMA ",
            data=csv,
            file_name='Hasil Peramalan Metode BWEMA dengan Kode Saham '+ticker+' ('+start_date_str+' - '+end_date_str+').csv',
            mime='text/csv',
        )

st.markdown("<h2 style='text-align: center'>Tentang Aplikasi</h2>", unsafe_allow_html=True)
st.markdown('''
- Tugas Akhir Skripsi Universitas Trunojoyo Madura Prodi Sistem Informasi 2017
    - Aplikasi dibuat oleh `Ahmad Try Bayu Al Haq (170441100024)`
    - Email `bayualhaq@gmail.com`
- Versi Aplikasi `1.0.1`
- Referensi aplikasi dari [AlexTeboul](https://github.com/AlexTeboul/streamlit-stock-price-app).
- Aplikasi ini menggunakan bahasa pemrograman `Python` dan menggunakan `library` : `streamlit`, `yfinance`, `plotly`, `numpy` dan `pandas`
- Jika Anda menemukan `bug, salah perhitungan metode, dll.` pada aplikasi ini, bisa lapor ke [Link](https://instagram.com/bayualhaq) berikut
- Copyright 2022
''')

st.markdown("<h2 style='text-align: center'>Daftar Pembaruan Aplikasi</h2>", unsafe_allow_html=True)
st.markdown('''
- Versi `1.0.1`
    - Perbaikan metode `B-WEMA`
- Versi `1.0.0`
    - Menambahkan input pilihan metode `SMA`, `WMA`, `WEMA`, `BWEMA` pada `sidebar`
    - Menambahkan metode perhitungan peramalan `SMA`, `WMA`, `WEMA`, `BWEMA`
    - Menampilkan hasil permalan tiap metode dalam bentuk `dataframe`
    - Menambahkan grafik peramalan tiap metode menggunakan `plotly`
    - Menampilkan ringkasan hasil peramalan seperti `Total Data`, `Moving Average`, `Hasil Peramalan`, `Akurasi Peramalan`, `MAD`, `MAPE`
    - Menambahkan fitur `download` hasil peramalan pada tiap metode peramalan, hasil download dalam bentuk format `.csv`
    - Perubahan tata letak
''')















    # add_bollinger_bands() - It adds Bollinger Bands (BOLL) study to the figure.
    # add_volume() - It adds volume bar charts to the figure.
    # add_sma() - It adds Simple Moving Average (SMA) study to the figure.
    # add_rsi() - It adds Relative Strength Indicator (RSI) study to the figure.
    # add_adx() - It adds Average Directional Index (ADX) study to the figure.
    # add_cci() - It adds Commodity Channel Indicator study to the figure.
    # add_dmi() - It adds Directional Movement Index (DMI) study to the figure.
    # add_ema() - It adds Exponential Moving Average (EMA) to the figure.
    # add_atr() - It adds Average True Range (ATR) study to the figure.
    # add_macd() - It adds Moving Average Convergence Divergence (MACD) to the figure.
    # add_ptps() - It adds Parabolic SAR (PTPS) study to the figure.
    # add_resistance() - It adds resistance line to the figure.
    # add_trendline() - It adds trend line to the figure.
    # add_support() - It adds support line to the figure.


# # Pengambilan 1 tahun
# start = st.date_input("Tanggal Mulai", datetime.datetime.now() - datetime.timedelta(days=1*365)) #Input Tanggal Awal
# end = st.date_input("Tanggal Akhir", datetime.datetime.now()) #Input Tanggal Akhir

# # Pengambilan 1 tahun
# start = st.date_input("Tanggal Mulai", datetime.date(2021, 12, 31) - datetime.timedelta(days=1*30)) #Input Tanggal Awal
# end = st.date_input("Tanggal Akhir", datetime.date(2021, 12, 31)) #Input Tanggal Akhir