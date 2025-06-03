import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")
st.title("📊 AI Stock Analysis Dashboard")

st.markdown("Enter a stock ticker (e.g., SHRIPISTON, INDNIPPON, PIDILITIND, SHANKARA, SUDARSCHEM...)")
symbol = st.text_input("Enter Stock Ticker Symbol", value="SHRIPISTON").upper()

# ========== Scraping Functions ==========

def get_screener_data(symbol):
    url = f"https://www.screener.in/company/{symbol}/consolidated/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_quarterly_sales(soup):
    try:
        table = soup.find('section', {'id': 'quarters'}).find('table')
        df = pd.read_html(str(table))[0]
        return df
    except Exception as e:
        return f"Error: {e}"

def extract_shareholding_pattern(soup):
    try:
        tables = pd.read_html(str(soup))
        for table in tables:
            if 'Shareholding Pattern' in table.columns[0]:
                return table
        return "Not Found"
    except Exception as e:
        return f"Error: {e}"

# ========== Main Logic ==========

if symbol:
    try:
        if not symbol.endswith(".NS"):
            symbol += ".NS"
        stock = yf.Ticker(symbol)
        info = stock.fast_info

        st.subheader(f"Company Overview: {symbol}")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Previous Close:**", info.get("previous_close", "N/A"))
            st.write("**Market Cap:**", info.get("market_cap", "N/A"))
            st.write("**Year High:**", info.get("year_high", "N/A"))
            st.write("**Year Low:**", info.get("year_low", "N/A"))
        with col2:
            st.write("**Open:**", info.get("open", "N/A"))
            st.write("**Day High:**", info.get("day_high", "N/A"))
            st.write("**Day Low:**", info.get("day_low", "N/A"))
            st.write("**Volume:**", info.get("volume", "N/A"))

        st.subheader("📈 Price Chart")
        df = stock.history(period="6mo")
        st.line_chart(df["Close"])

        st.subheader("🧠 AI Insight")
        detailed_info = {}
        try:
            detailed_info = stock.info
        except Exception:
            st.warning("Detailed info not available from Yahoo Finance.")

        roe = detailed_info.get("returnOnEquity")
        eps = detailed_info.get("trailingEps")
        debt_equity = detailed_info.get("debtToEquity")

        suggestion = ""
        ai_rating = ""
        if roe and roe > 0.20 and eps and eps > 30 and (not debt_equity or debt_equity < 0.5):
            suggestion = "✅ Excellent Fundamentals - Strong Buy"
            ai_rating = "⭐⭐⭐⭐⭐"
        elif roe and roe > 0.15 and eps and eps > 15:
            suggestion = "✅ Good Fundamentals - Consider for Investment"
            ai_rating = "⭐⭐⭐⭐"
        elif roe and roe > 0.10:
            suggestion = "🟡 Average Fundamentals - Hold or Watch Closely"
            ai_rating = "⭐⭐⭐"
        elif roe and roe < 0.05:
            suggestion = "⚠️ Weak ROE - Use Caution"
            ai_rating = "⭐"
        else:
            suggestion = "🔎 Neutral - Do further analysis"
            ai_rating = "⭐⭐"

        st.info(suggestion)
        st.success(f"AI Rating: {ai_rating}")

        # ========== Screener Data Section ==========
        st.subheader("📊 Screener Data")
        soup = get_screener_data(symbol.replace(".NS", ""))

        st.markdown("**Quarterly Sales Data**")
        sales_df = extract_quarterly_sales(soup)
        if isinstance(sales_df, pd.DataFrame):
            st.dataframe(sales_df)
        else:
            st.warning(f"Quarterly Sales Not Available: {sales_df}")

        st.markdown("**Shareholding Pattern**")
        pattern_df = extract_shareholding_pattern(soup)
        if isinstance(pattern_df, pd.DataFrame):
            st.dataframe(pattern_df)
        else:
            st.warning(f"Shareholding Pattern Not Found: {pattern_df}")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
