import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

st.title("\ud83d\udcca AI Stock Analysis Dashboard")
st.markdown("Enter a stock ticker (e.g., SHRIPISTON, INDNIPPON, PIDILITIND, SHANKARA, SUDARSCHEM, GABRIEL, KIRLOSBROS, CAMPUS, PDSL, DREDGECORP, HARSHA, EMUDHRA, FILATEX, GLENMARK, FMGOETZE, IXIGO, CLSEL, SYNCOMF, POLYPLEX, GANDHAR, REFEX, LTFOODS, INTERARCH, XPROINDIA, STYRENIX, TIIL, SKFINDIA, RRKABEL, DYCL, NUVOCO, BEPL, GOPAL, KALAMANDIR, JYOTICNC, AGIIL, VSSL, SANSTAR, NAVA, ELGIEQUIP, CONCORDBIO, SOBHA, SUZLON, OLECTRA, MOTHERSON, ANANTRAJ, RALLIS, HAPPYFORGE, CENTURYPLY, JINDALSTEL, VINATIORGA, ARE&M, MOLDTKPAC, HONASA, TATVA, JSL, DODLA, TDPOWERSYS, BAJAJHIND, LXCHEM, ICEMAKE, STEELCAS, GRWRHITECH, JASH, AARTIPHARM, TARIL, MARKSANS, SUPRIYA, VISHNU, MANINDS, OPTIEMUS, BIKAJI, NAVKARCORP, CELLO, LIKHITHA, JKIL, SUNFLAG, POWERINDIA, ASKAUTOLTD, LLOYDSENGG, MASTEK, GVT&D, LLOYDSME, DEEPAKNTR, NETWEB, HINDCOPPER)")

symbol = st.text_input("Enter Stock Ticker Symbol", value="SHRIPISTON").upper()

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

        st.subheader("\ud83d\udcc8 Price Chart")
        df = stock.history(period="6mo")
        st.line_chart(df["Close"])

        st.subheader("\ud83e\uddd0 AI Insight")
        detailed_info = {}
        try:
            detailed_info = stock.info
        except Exception as e:
            st.warning("Detailed info not available from Yahoo Finance.")

        roe = detailed_info.get("returnOnEquity")
        eps = detailed_info.get("trailingEps")
        debt_equity = detailed_info.get("debtToEquity")

        suggestion = ""
        ai_rating = ""
        if roe and roe > 0.20 and eps and eps > 30 and (not debt_equity or debt_equity < 0.5):
            suggestion = "\u2705 Excellent Fundamentals - Strong Buy"
            ai_rating = "\u2b50\u2b50\u2b50\u2b50\u2b50"
        elif roe and roe > 0.15 and eps and eps > 15:
            suggestion = "\u2705 Good Fundamentals - Consider for Investment"
            ai_rating = "\u2b50\u2b50\u2b50\u2b50"
        elif roe and roe > 0.10:
            suggestion = "\udfe1 Average Fundamentals - Hold or Watch Closely"
            ai_rating = "\u2b50\u2b50\u2b50"
        elif roe and roe < 0.05:
            suggestion = "\u26a0\ufe0f Weak ROE - Use Caution"
            ai_rating = "\u2b50"
        else:
            suggestion = "\ud83d\udd0e Neutral - Do further analysis"
            ai_rating = "\u2b50\u2b50"

        st.info(suggestion)
        st.success(f"AI Rating: {ai_rating}")

        st.subheader("\ud83d\udcca Screener Data")
        soup = get_screener_data(symbol.replace(".NS", ""))
        st.markdown("**Quarterly Sales Data**")
        sales_df = extract_quarterly_sales(soup)
        st.dataframe(sales_df)

        st.markdown("**Shareholding Pattern**")
        pattern_df = extract_shareholding_pattern(soup)
        st.dataframe(pattern_df)

    except Exception as e:
        st.error(f"Failed to fetch stock data: {e}")
