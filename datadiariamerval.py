import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime as dt
import squarify
import streamlit as st
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib import cm
import matplotlib.colors as mcolors

# Set Seaborn style
sns.set_style('whitegrid')

# Function to format large numbers
def format_large_numbers(num):
    if abs(num) >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif abs(num) >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif abs(num) >= 1_000:
        return f"{num/1_000:.2f}K"
    else:
        return f"{num:.2f}"

# List of tickers
tickers = [
    "GGAL.BA", "YPFD.BA", "PAMP.BA", "TXAR.BA", "ALUA.BA", "CRES.BA", "SUPV.BA", "CEPU.BA", "BMA.BA",
    "TGSU2.BA", "TRAN.BA", "EDN.BA", "LOMA.BA", "MIRG.BA", "DGCU2.BA", "BBAR.BA", "MOLI.BA", "TGNO4.BA",
    "CGPA2.BA", "COME.BA", "IRSA.BA", "BYMA.BA", "TECO2.BA", "METR.BA", "CECO2.BA", "BHIP.BA", "AGRO.BA",
    "LEDE.BA", "CVH.BA", "HAVA.BA", "AUSO.BA", "VALO.BA", "SEMI.BA", "INVJ.BA", "CTIO.BA", "MORI.BA",
    "HARG.BA", "GCLA.BA", "SAMI.BA", "BOLT.BA", "MOLA.BA", "CAPX.BA", "OEST.BA", "LONG.BA", "GCDI.BA",
    "GBAN.BA", "CELU.BA", "FERR.BA", "CADO.BA", "GAMI.BA", "PATA.BA", "CARC.BA", "BPAT.BA", "RICH.BA",
    "INTR.BA", "GARO.BA", "FIPL.BA", "GRIM.BA", "DYCA.BA", "POLL.BA", "DGCE.BA", "DOME.BA", "ROSE.BA",
    "RIGO.BA", "MTR.BA"
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
@st.cache_data(ttl=3600)
def fetch_data(tickers, start_date):
    data = {}
    for ticker in tickers:
        try:
            # Fetch data
            stock_data = yf.Ticker(ticker)
            df = stock_data.history(start=start_date - dt.timedelta(days=10), end=start_date + dt.timedelta(days=1))
            df = df.dropna()
    
            # Ensure we have at least 2 days of data
            if len(df) < 2:
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
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            continue
    return data

# Streamlit: User selects a date
st.title("📈 Stock Data Analysis Dashboard")

st.sidebar.header("User Inputs")

selected_date = st.sidebar.date_input(
    "Select Date",
    dt.datetime.now().date() - dt.timedelta(days=1),
    max_value=dt.datetime.now().date() - dt.timedelta(days=1)
)

# Fetch the data
with st.spinner('Fetching data...'):
    data = fetch_data(tickers, selected_date)

if not data:
    st.error("No data available for the selected date. Please choose a different date.")
    st.stop()

# Function to create a bubble chart with enhanced visuals
def create_bubble_chart(x, y, size, labels, xlabel, ylabel, title, color_var=None):
    plt.figure(figsize=(14, 10))
    norm = plt.Normalize(min(size), max(size))
    cmap = cm.get_cmap('viridis')

    scatter = plt.scatter(
        x, y,
        s=[(s / max(size)) * 2000 + 100 for s in size],  # Adjust size scaling
        c=color_var if color_var else size,
        cmap='viridis',
        alpha=0.7,
        edgecolors='black',
        linewidth=0.5
    )

    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Value')

    # Add annotations
    for i, label in enumerate(labels):
        plt.annotate(
            label,
            (x[i], y[i]),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center',
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7)
        )

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(plt)
    plt.close()

# Prepare data for plots
df = pd.DataFrame({
    'Ticker': list(data.keys()),
    'Price Variation (%)': [d['price_variation'] for d in data.values()],
    'Volume': [d['latest']['Volume'] for d in data.values()],
    'Latest Price': [d['latest']['Close'] for d in data.values()],
    'Open Price': [d['latest']['Open'] for d in data.values()],
    'Min Price': [d['latest']['Low'] for d in data.values()],
    'Max Price': [d['latest']['High'] for d in data.values()],
    'Market Value': [d['latest']['Close'] * d['outstanding_shares'] for d in data.values()]
})

# Format large numbers in dataframe
df['Volume (formatted)'] = df['Volume'].apply(format_large_numbers)
df['Market Value (formatted)'] = df['Market Value'].apply(format_large_numbers)

# Bubble Chart: Volume * Price vs. Price Variation
st.subheader("📊 Volume * Price vs. Price Variation")
df['Volume * Price'] = df['Volume'] * df['Latest Price']
df['Volume * Price (formatted)'] = df['Volume * Price'].apply(format_large_numbers)

create_bubble_chart(
    x=df['Price Variation (%)'],
    y=df['Volume * Price'],
    size=df['Volume * Price'],
    labels=df['Ticker'],
    xlabel='Price Variation (%)',
    ylabel='Volume * Price',
    title='Volume * Price vs. Price Variation',
    color_var=df['Price Variation (%)']
)

# Bubble Chart: Open Price vs. Latest Price
st.subheader("📊 Open Price vs. Latest Price")

create_bubble_chart(
    x=df['Latest Price'],
    y=df['Open Price'],
    size=df['Market Value'],
    labels=df['Ticker'],
    xlabel='Latest Price',
    ylabel='Open Price',
    title='Open Price vs. Latest Price',
    color_var=df['Market Value']
)

# Bubble Chart: Min Price vs. Max Price
st.subheader("📊 Min Price vs. Max Price")

create_bubble_chart(
    x=df['Max Price'],
    y=df['Min Price'],
    size=df['Volume'],
    labels=df['Ticker'],
    xlabel='Max Price',
    ylabel='Min Price',
    title='Min Price vs. Max Price',
    color_var=df['Volume']
)

# Treemap: Market Value
st.subheader("🗺️ Treemap of Market Value")

# Sort data for better visualization
df_treemap = df.sort_values('Market Value', ascending=False)

sizes = df_treemap['Market Value']
labels = df_treemap.apply(lambda x: f"{x['Ticker']}\n{format_large_numbers(x['Market Value'])}", axis=1)
colors = [cm.viridis(norm) for norm in np.linspace(0, 1, len(sizes))]

plt.figure(figsize=(18, 12))
squarify.plot(
    sizes=sizes,
    label=labels,
    color=colors,
    alpha=0.8,
    text_kwargs={'fontsize':12, 'weight':'bold', 'color':'white'}
)
plt.title('Treemap of Market Value (Shares Outstanding * Price)', fontsize=18)
plt.axis('off')
st.pyplot(plt)
plt.close()

# Display Data Table
st.subheader("📄 Detailed Data Table")
st.dataframe(df[['Ticker', 'Price Variation (%)', 'Volume (formatted)', 'Latest Price', 'Open Price',
                 'Min Price', 'Max Price', 'Market Value (formatted)']].set_index('Ticker'))
