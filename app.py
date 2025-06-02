
import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

st.title("📊 AI Stock Analysis Dashboard")
st.markdown("Enter a stock ticker (e.g.,SHRIPISTON,INDNIPPON,PIDILITIND,SHANKARA,SUDARSCHEM,GABRIEL,KIRLOSBROS,CAMPUS,PDSL,DREDGECORP,HARSHA,EMUDHRA,FILATEX,GLENMARK,FMGOETZE,IXIGO,CLSEL,SYNCOMF,POLYPLEX,GANDHAR,REFEX,LTFOODS,INTERARCH,XPROINDIA,STYRENIX,TIIL,SKFINDIA,RRKABEL,DYCL,NUVOCO,BEPL,GOPAL,KALAMANDIR,JYOTICNC,AGIIL,VSSL,SANSTAR,NAVA,ELGIEQUIP,CONCORDBIO,SOBHA,SUZLON,OLECTRA,MOTHERSON,ANANTRAJ,RALLIS,HAPPYFORGE,CENTURYPLY,JINDALSTEL,VINATIORGA,ARE&M,MOLDTKPAC,HONASA,TATVA,JSL,DODLA,TDPOWERSYS,BAJAJHIND,LXCHEM,ICEMAKE,STEELCAS,GRWRHITECH,JASH,AARTIPHARM,TARIL,ANANTRAJ,GANDHAR,MARKSANS,SUPRIYA,VISHNU,MANINDS,AGIIL,OPTIEMUS,BIKAJI,NAVKARCORP,FILATEX,CELLO,LIKHITHA,JKIL,SUNFLAG,POWERINDIA,ASKAUTOLTD,LLOYDSENGG,MASTEK,GVT&D,LLOYDSME,DEEPAKNTR,NETWEB,HINDCOPPER,NAVA,VALIANTORG,ADSL,DREDGECORP,ARKADE,IPL,MIDHANI,APOLLO,PRECAM,INSECTICID,AVANTIFEED,FMGOETZE) to view financial analysis and AI insights.")

symbol = st.text_input("Enter Stock Ticker Symbol", value="INFY")

if symbol:
    stock = yf.Ticker(symbol)
    info = stock.info

    st.subheader(f"Company Overview: {info.get('longName', 'N/A')}")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Industry:**", info.get("industry", "N/A"))
        st.write("**Market Cap:**", info.get("marketCap", "N/A"))
        st.write("**Book Value:**", info.get("bookValue", "N/A"))
        st.write("**52W High:**", info.get("fiftyTwoWeekHigh", "N/A"))
    with col2:
        st.write("**ROE:**", info.get("returnOnEquity", "N/A"))
        st.write("**EPS:**", info.get("trailingEps", "N/A"))
        st.write("**Debt/Equity:**", info.get("debtToEquity", "N/A"))
        st.write("**Dividend Yield:**", info.get("dividendYield", "N/A"))

    st.subheader("📈 Price Chart")
    df = stock.history(period="6mo")
    st.line_chart(df["Close"])

    st.subheader("🤖 AI Insight")
    roe = info.get("returnOnEquity")
    pe = info.get("trailingPE")
    eps = info.get("trailingEps")
    debt_equity = info.get("debtToEquity")

    suggestion = ""
    if roe and roe > 0.15 and eps and eps > 20 and (not debt_equity or debt_equity < 1):
        suggestion = "✅ Strong Fundamentals - Consider for Investment"
    elif roe and roe < 0.05:
        suggestion = "⚠️ Weak ROE - Use Caution"
    else:
        suggestion = "🔎 Neutral - Do further analysis"

    st.info(suggestion)
