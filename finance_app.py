import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import datetime
import requests

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
	page_title="COMO: Finanční vizualizace",  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
)

ticker_list = ['Crypto', 'Akcie']
ticker_stock_list = ['AAPL', 'MSFT']
ticker_crypto_list = ['BTC', 'ETH']
asset_type = st.radio("Vyberte si zda chcete vidět Crypto nebo Akcie", ticker_list)
if asset_type == 'Crypto':
    ticker_name = st.selectbox("Vyberte si název daného Crypta či Akcie",ticker_crypto_list, index = 0)
elif asset_type == 'Akcie':
    ticker_name = st.selectbox("Vyberte si název daného Crypta či Akcie",ticker_stock_list, index = 0)
ticker_start_date = st.date_input("Zadejte začátek dne", value = datetime.date(2022, 1,1))

if (ticker_start_date > datetime.date.today()):
    st.write("Den začátku je v budoucnosti, to nedokážu ukázat")
    st.stop()
elif (ticker_start_date == datetime.date.today()):
    st.write("Dnešní data ještě nebudu mít :(")
    st.stop()

btn_dostat_data = st.button("Dostat data")

@st.cache
def get_stock_data(ticker_name, ticker_start_date):
    alpha_vantage_api_key = 'IR88KE96511BM5SQ'
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol={ticker_name}&apikey={alpha_vantage_api_key}"
    response = requests.get(url)
    df = pd.DataFrame.from_dict(response.json()['Time Series (Daily)'], orient = "index")
    df = df.reset_index()
    df.columns = ['date','open', 'high', 'low', 'close', 'adj_close', 'vol', 'div', 'split']
    for i in df.columns[1:]:
        df[i] = df[i].astype(float)
    df = df[df["date"] >= ticker_start_date.strftime("%Y-%m-%d")]
    return df

@st.cache
def get_crypto_data(ticker_name, ticker_start_date): 
    alpha_vantage_api_key = 'IR88KE96511BM5SQ'
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={ticker_name}&market=CZK&apikey={alpha_vantage_api_key}"
    response = requests.get(url)
    df = pd.DataFrame.from_dict(response.json()['Time Series (Digital Currency Daily)'], orient = "index")
    df = df.reset_index()
    df.columns = ["date","open_czk", "open_usd", "high_czk", "high_usd",  "low_czk", "low_usd", "close_czk", "close_use", "vol", "market_cap"]
    df = df.loc[:,["date", "open_czk", "high_czk", "low_czk", "close_czk", "vol"]]
    df.columns = ["date", "open", "high", "low", "close", "vol"]
    df["adj_close"] = df["close"]
    for i in df.columns[1:]:
        df[i] = df[i].astype(float)
    df = df[df["date"] >= ticker_start_date.strftime("%Y-%m-%d")]
    return df

@st.cache
def simple_visualization(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df["date"], y = df["adj_close"]))
    return fig

@st.cache
def candlestick_visualization(df):
    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
    return fig

if btn_dostat_data:
    if asset_type == 'Akcie':
        data  = get_stock_data(ticker_name, ticker_start_date)
    elif asset_type == 'Crypto':
        data = get_crypto_data(ticker_name, ticker_start_date)
    st.header("Základní graf")
    st.plotly_chart(simple_visualization(data))
    st.header("Svíčkový graf")
    st.plotly_chart(candlestick_visualization(data))

