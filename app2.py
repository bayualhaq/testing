#import
import streamlit as st
import yfinance as yf
import cufflinks as cf
import datetime

#Consumer Good
#Food

# Menampilkan teks header pada slidebar
st.sidebar.header("Peramalan Saham \n Masukkan Data Saham")

# Membuat fungsi untuk mengambil informasi dari symbol saham
def get_ticker(ticker):
    company = yf.Ticker(ticker)
    return company

# Membuat fungsi untuk mengambil informasi period dan interval
def get_history(start, end):
    df = ticker_data.history(start=start, end=end)
    if len(df) == 0:
        st.write('Data saham tidak ditemukan, silahkan atur kembali sampai data tersedia')
    else:
        df.index = df.index.strftime("%d-%m-%Y")
        return df

# Input Data
ticker_symbol   = st.sidebar.text_input("Symbol Saham", "KLBF.JK") # Input Symbol Saham, default ANTM.JK
ticker_data     = get_ticker(ticker_symbol) # Untuk mengambil informasi dari symbol saham
start           = st.sidebar.date_input("Tanggal Mulai", datetime.date(2021, 1, 1)) #Input Tanggal Awal
end             = st.sidebar.date_input("Tanggal Akhir", datetime.date(2021, 12, 30)) #Input Tanggal Akhir



# Informasi saham
# Menampilkan nama lengkap saham
string_name = ticker_data.info['longName']
st.markdown("<h1 style='text-align: center; color: white;'>%s</h1>" % string_name, unsafe_allow_html=True)

# # Menampilkan logo saham
# string_logo = '<center><img src=%s ></center></br>' % ticker_data.info['logo_url']
# st.markdown(string_logo, unsafe_allow_html=True)

# Menampilkan informasi ringkas dari saham
string_summary = ticker_data.info['longBusinessSummary']
st.info(string_summary)

# Data saham
# Menampikan teks Header
st.header('**Data Saham**')

# Memasukkan input data ke Fungsi get_history
ticker_df = get_history(start, end)

#Save to CSV
csv = ticker_df.to_csv(ticker_symbol+'.csv')

st.write(ticker_df)

# Menampilkan Candlestick
st.header('**Smooth Moving Average**')
qf = cf.QuantFig(ticker_df, title='Smooth Moving Average', legend='top', name='Candlestick')
qf.add_sma(5,color='red',legendgroup=True)
qf.add_sma(10,color='green',legendgroup=True)
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

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