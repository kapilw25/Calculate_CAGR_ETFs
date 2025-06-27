import streamlit as st
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="ETF CAGR Dashboard", layout="wide")

st.title("📈 ETF CAGR Dashboard (Custom Range)")
st.markdown("Analyze CAGR, total returns, and dividend-adjusted returns for popular ETFs.")

# ETF List
etfs = {
    "S&P 500 (SPY)": "SPY",
    "NASDAQ-100 (QQQ)": "QQQ",
    "Russell 2000 (IWM)": "IWM",
    "Total Market (VTI)": "VTI",
    "Tech Sector (XLK)": "XLK",
    "Nifty 50": "^NSEI",
    "Bank Nifty": "^NSEBANK"
}

col1, col2 = st.columns(2)
with col1:
    start_year = st.selectbox("📅 Start Year", range(1950, 2026), index=0)
    start_date = datetime(start_year, 1, 1)
with col2:
    end_year = st.selectbox("📅 End Year", range(1950, 2026), index=75)  # Default to 2025
    end_date = datetime(end_year, 12, 31)

st.markdown("---")

def calculate_cagr(start_price, end_price, num_years):
    return ((end_price / start_price) ** (1 / num_years)) - 1

# Create empty list to store results
results = []

for name, symbol in etfs.items():
    try:
        data = yf.download(symbol, start=start_date, end=end_date, progress=False, auto_adjust=False)
        if data.empty:
            st.warning(f"No data for {name}")
            continue

        # Use Adj Close for accurate calculations (includes dividends)
        start_price = float(data["Adj Close"].iloc[0])
        end_price = float(data["Adj Close"].iloc[-1])
        total_return = (end_price - start_price) / start_price
        years = (end_date - start_date).days / 365.25
        cagr = calculate_cagr(start_price, end_price, years)

        # Add results to list
        results.append({
            "ETF": name,
            "Total Return": f"{float(total_return)*100:.2f}%",
            "CAGR": f"{float(cagr)*100:.2f}%",
            "Period": f"{float(years):.2f} years"
        })
        
    except Exception as e:
        st.error(f"Error loading {name}: {e}")

# Display results in a table
if results:
    import pandas as pd
    df = pd.DataFrame(results)
    st.table(df)
