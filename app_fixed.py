
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

st.title("📊 AI Stock Analysis Dashboard")

st.markdown("Enter a stock ticker (e.g., TCS.NS, INFY.NS, RELIANCE.NS)")

ticker = st.text_input("Enter Stock Ticker:", "TCS.NS").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")

        st.subheader(f"📈 Price Chart for {ticker}")
        st.line_chart(hist['Close'])

        st.subheader("📄 Company Info")
        info = stock.info
        st.write({
            "Name": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "Website": info.get("website", "N/A"),
        })

        st.subheader("📊 Historical Data (Last 6 months)")
        st.dataframe(hist)

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
