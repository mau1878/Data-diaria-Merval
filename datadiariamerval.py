import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime as dt
import squarify
import streamlit as st
from matplotlib.ticker import FuncFormatter

# List of tickers
tickers = [
    "GGAL.BA", "YPFD.BA", "PAMP.BA", "TXAR.BA", "ALUA.BA", "CRES.BA", "SUPV.BA", "CEPU.BA", "BMA.BA",
    "TGSU2.BA", "TRAN.BA", "EDN.BA", "LOMA.BA", "MIRG.BA", "DGCU2.BA", "BBAR.BA", "MOLI.BA", "TGNO4.BA",
    "CGPA2.BA", "COME.BA", "IRSA.BA", "BYMA.BA", "TECO2.BA", "METR.BA", "CECO2.BA", "BHIP.BA", "AGRO.BA",
    "LEDE.BA", "CVH.BA", "HAVA.BA", "AUSO.BA", "VALO.BA", "SEMI.BA", "INVJ.BA", "CTIO.BA", "MORI.BA",
    "HARG.BA", "GCLA.BA", "SAMI.BA", "BOLT.BA", "MOLA.BA", "CAPX.BA", "OEST.BA", "LONG.BA", "GCDI.BA",
    "GBAN.BA", "CELU.BA", "FERR.BA", "CADO.BA", "GAMI.BA", "PATA.BA", "CARC.BA", "BPAT.BA", "RICH.BA",
    "INTR.BA", "GARO.BA", "FIPL.BA", "GRIM.BA", "DYCA.BA", "POLL.BA", "DGCE.BA", "DOME.BA", "ROSE.BA",
    "RIGO.BA", "MTR.BA", "^MERV"
]

# Shares outstanding data
shares_outstanding = {
    "GGAL.BA": 1193470439, "YPFD.BA": 393312793.1, "PAMP.BA": 1383644606, "TXAR.BA": 4517094019,
    "ALUA.BA": 2800000000, "CRES.BA": 592172573.1, "SUPV.BA": 394984130.2, "CEPU.BA": 1514022252,
    "BMA.BA": 639413408, "TGSU2.BA": 794495282.5, "TRAN.BA": 217890149.5, "EDN.BA": 906455097.6,
    "LOMA.BA": 596026490.7, "MIRG.BA": 18000000, "DGCU2.BA": 202351290.7, "BBAR.BA": 612710077.6,
    "MOLI.BA": 201415126.1, "TGNO4.BA": 439373937.5, "CGPA2.BA": 333281047.1, "COME.BA": 3119012723,
    "IRSA.BA": 810895392, "BYMA.BA": 3812500000, "TECO2.BA": 2153688010, "METR.BA": 278893888.6,
    "CECO2.BA": 701988378.1, "BHIP.BA": 1500000000, "AGRO.BA": 100000000, "LEDE.BA": 439714250.9,
    "CVH.BA": 132888959.1, "HAVA.BA": 46976134.56, "AUSO.BA": 30469033.9, "VALO.BA": 840182386,
    "SEMI.BA": 191400000, "INVJ.BA": 613174622.7, "CTIO.BA": 409906728.5, "MORI.BA": 281902003.1,
    "HARG.BA": 365742910.5, "GCLA.BA": 78549323.03, "SAMI.BA": 148512803.8, "BOLT.BA": 3150754416,
    "MOLA.BA": 49082023.89, "CAPX.BA": 179802282.4, "OEST.BA": 160000000, "LONG.BA": 153641509.4,
    "GCDI.BA": 924990596.3, "GBAN.BA": 159514578.7, "CELU.BA": 100938186.5, "FERR.BA": 947000000,
    "CADO.BA": 123200000, "GAMI.BA": 340000000, "PATA.BA": 500000000, "CARC.BA": 1091624474,
    "BPAT.BA": 719145236.4, "RICH.BA": 14167161.62, "INTR.BA": 121085814.7, "GARO.BA": 44000000,
    "FIPL.BA": 129430000, "GRIM.BA": 44307510, "DYCA.BA": 30000000, "POLL.BA": 6420388.889,
    "DGCE.BA": 160457190, "DOME.BA": 100000000, "ROSE.BA": 42589433.96, "RIGO.BA": 145064319.9,
    "MTR.BA": 122787764
}

# Function to fetch data for a given date and the previous trading day
def fetch_data(tickers, start_date):
    data = {}
    for ticker in tickers:
        # Fetch data
        stock_data = yf.Ticker(ticker)
        df = stock_data.history(start=start_date - dt.timedelta(days=30), end=start_date + dt.timedelta(days=1))
        df = df.dropna()

        # Ensure we have at least 2 days of data
        if len(df) < 2:
            print(f"Not enough data for {ticker}")
            continue
        
        # Select the latest two days (the selected day and the previous trading day)
        latest_data = df.iloc[-1]
        previous_data = df.iloc[-2]
        
        # Calculate percentage price variation
        price_variation = (latest_data['Close'] - previous_data['Close']) / previous_data['Close'] * 100
        
        data[ticker] = {
            'latest': latest_data,
            'previous': previous_data,
            'price_variation': price_variation,
            'outstanding_shares': shares_outstanding.get(ticker, np.nan)
        }
    return data

# Streamlit: User selects a date
st.title("Stock Data Analysis")
selected_date = st.date_input("Choose a date", dt.datetime(2024, 8, 22))

# Fetch the data
try:
    data = fetch_data(tickers, selected_date)
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# Check for missing or non-numeric data
def clean_data(data):
    clean_data = {}
    for ticker, d in data.items():
        if not np.isnan(d['price_variation']) and not np.isnan(d['latest']['Volume']) and not np.isnan(d['latest']['Close']):
            clean_data[ticker] = d
    return clean_data

data = clean_data(data)

# Function to format large numbers (e.g., 1,000 as 1K, 1,000,000 as 1M)
def format_large_number(num):
    if num >= 1_000_000_000:
        return f'{num / 1_000_000_000:.1f}B'
    elif num >= 1_000_000:
        return f'{num / 1_000_000:.1f}M'
    elif num >= 1_000:
        return f'{num / 1_000:.1f}K'
    else:
        return str(num)

# Function to create a bubble chart with different colors and labels
def create_bubble_chart(x, y, size, labels, xlabel, ylabel, title):
    plt.figure(figsize=(14, 10))
    
    # Generate a scatter plot with varying bubble colors
    cmap = plt.get_cmap("viridis")
    norm = plt.Normalize(min(size), max(size))
    colors = cmap(norm(size))
    
    # Plot bubbles
    scatter = plt.scatter(x=x, y=y, s=size, c=colors, alpha=0.6, edgecolors="w", linewidth=2)
    
    # Add labels with arrows/lines
    for i, label in enumerate(labels):
        plt.annotate(label,
                     (x[i], y[i]),
                     textcoords="offset points",
                     xytext=(10, 10),  # Distance from the point
                     ha='center',
                     arrowprops=dict(arrowstyle="->", lw=1.5, color='black'))
    
    # Customize and format the plot
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(True)
    
    # Formatter for large numbers
    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: format_large_number(x)))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: format_large_number(y)))
    
    st.pyplot(plt)  # Display the plot in Streamlit

# Prepare data for the bubble chart
price_variation = [d['price_variation'] for d in data.values()]
volume_price = [d['latest']['Volume'] * d['latest']['Close'] for d in data.values()]
labels = list(data.keys())

# Ensure that data is consistent
if len(price_variation) == len(volume_price) == len(labels):
    create_bubble_chart(price_variation, volume_price, volume_price, labels, 'Price Variation (%)', 'Volume * Price', 'Volume * Price vs. Price Variation')
else:
    st.error("Data lengths do not match. Please check the data fetching process.")

# Prepare data for the bubble chart
open_price = [d['latest']['Open'] for d in data.values()]
latest_price = [d['latest']['Close'] for d in data.values()]

if len(open_price) == len(latest_price) == len(labels):
    try:
        create_bubble_chart(latest_price, open_price, open_price, labels, 'Latest Price', 'Open Price', 'Open Price vs. Latest Price')
    except Exception as e:
        st.error(f"Error creating Open Price vs. Latest Price chart: {e}")
else:
    st.error("Data lengths for Open Price and Latest Price do not match. Please check the data.")


# Plot: Bubble chart with minimum price vs. maximum price
# Prepare data for the bubble chart
min_price = [d['latest']['Low'] for d in data.values()]
max_price = [d['latest']['High'] for d in data.values()]

if len(min_price) == len(max_price) == len(labels):
    try:
        create_bubble_chart(max_price, min_price, max_price, labels, 'Max Price', 'Min Price', 'Min Price vs. Max Price')
    except Exception as e:
        st.error(f"Error creating Min Price vs. Max Price chart: {e}")
else:
    st.error("Data lengths for Min Price and Max Price do not match. Please check the data.")


# Plot: Treemap with shares outstanding * price
# Prepare data for the treemap
sizes = [d['latest']['Close'] * d['outstanding_shares'] for d in data.values()]
labels = [f"{ticker}\n{format_large_number(d['latest']['Close'] * d['outstanding_shares'])}" for ticker, d in data.items()]

try:
    plt.figure(figsize=(12, 8))
    squarify.plot(sizes=sizes, label=labels, alpha=.8)
    plt.title('Treemap of Market Value (Shares Outstanding * Price)')
    plt.axis('off')
    st.pyplot(plt)  # Display the plot in Streamlit
except Exception as e:
    st.error(f"Error creating Treemap chart: {e}")
