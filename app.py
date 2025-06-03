import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="📈 AI Stock Screener", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2e86de;'>📊 AI Stock Screener (NSE)</h1>", unsafe_allow_html=True)

@st.cache_data
def load_nse_symbols():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(url)
    return df["SYMBOL"].dropna().unique().tolist()

symbols_list = load_nse_symbols()

st.markdown("### 🔍 Select Stocks to Analyze (Max 50)")
selected_symbols = st.multiselect("Choose Stocks", symbols_list, default=symbols_list[:5], max_selections=50)

@st.cache_data(show_spinner=False)
def get_screener_data(symbol):
    try:
        url = f'https://www.screener.in/company/{symbol}/'
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.select('section#top-ratios div.flex.flex-wrap span')
        data = [row.get_text(strip=True) for row in rows]
        return dict(zip(data[::2], data[1::2]))
    except:
        return {}

def get_rating(roe, eps, debt_eq):
    try:
        roe = float(roe.strip('%')) / 100 if '%' in roe else float(roe)
        eps = float(eps)
        debt_eq = float(debt_eq)
        if roe > 0.2 and eps > 30 and debt_eq < 0.5:
            return "🌟🌟🌟🌟🌟 Strong Buy"
        elif roe > 0.15 and eps > 15:
            return "🌟🌟🌟🌟 Buy"
        elif roe > 0.1:
            return "🌟🌟🌟 Hold"
        elif roe < 0.05:
            return "⚠️ Weak ROE"
        else:
            return "🔍 Neutral"
    except:
        return "❓ Unknown"

headers = ["EPS", "Sales growth", "Profit growth", "ROE", "ROCE", "Debt to equity", "OPM", "PEG Ratio", "P/E", "P/B"]
all_data = []

progress = st.progress(0, text="⏳ Fetching data...")
for i, symbol in enumerate(selected_symbols):
    ratios = get_screener_data(symbol)
    row = [symbol] + [ratios.get(h, "N/A") for h in headers[::-1]]

    # AI suggestion
    rating = get_rating(ratios.get("ROE", "N/A"), ratios.get("EPS", "N/A"), ratios.get("Debt to equity", "N/A"))
    row.append(rating)
    all_data.append(row)
    progress.progress((i+1)/len(selected_symbols), text=f"✅ Processed {symbol}")

progress.empty()

final_df = pd.DataFrame(all_data, columns=["Symbol"] + headers[::-1] + ["AI Suggestion"])

st.markdown("### 🧠 AI Ratings & Key Ratios")
st.dataframe(final_df, use_container_width=True
