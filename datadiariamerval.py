import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import squarify

# Shares outstanding data (provided by the user)
shares_outstanding = {
    "GGAL.BA": 1193470439, "YPFD.BA": 393312793.1, "PAMP.BA": 1383644606,
    "TXAR.BA": 4517094019, "ALUA.BA": 2800000000, "CRES.BA": 592172573.1,
    "SUPV.BA": 394984130.2, "CEPU.BA": 1514022252, "BMA.BA": 639413408,
    "TGSU2.BA": 794495282.5, "TRAN.BA": 217890149.5, "EDN.BA": 906455097.6,
    "LOMA.BA": 596026490.7, "MIRG.BA": 18000000, "DGCU2.BA": 202351290.7,
    "BBAR.BA": 612710077.6, "MOLI.BA": 201415126.1, "TGNO4.BA": 439373937.5,
    "CGPA2.BA": 333281047.1, "COME.BA": 3119012723, "IRSA.BA": 810895392,
    "BYMA.BA": 3812500000, "TECO2.BA": 2153688010, "METR.BA": 278893888.6,
    "CECO2.BA": 701988378.1, "BHIP.BA": 1500000000, "AGRO.BA": 100000000,
    "LEDE.BA": 439714250.9, "CVH.BA": 132888959.1, "HAVA.BA": 46976134.56,
    "AUSO.BA": 30469033.9, "VALO.BA": 840182386, "SEMI.BA": 191400000,
    "INVJ.BA": 613174622.7, "CTIO.BA": 409906728.5, "MORI.BA": 281902003.1,
    "HARG.BA": 365742910.5, "GCLA.BA": 78549323.03, "SAMI.BA": 148512803.8,
    "BOLT.BA": 3150754416, "MOLA.BA": 49082023.89, "CAPX.BA": 179802282.4,
    "OEST.BA": 160000000, "LONG.BA": 153641509.4, "GCDI.BA": 924990596.3,
    "GBAN.BA": 159514578.7, "CELU.BA": 100938186.5, "FERR.BA": 947000000,
    "CADO.BA": 123200000, "GAMI.BA": 340000000, "PATA.BA": 500000000,
    "CARC.BA": 1091624474, "BPAT.BA": 719145236.4, "RICH.BA": 14167161.62,
    "INTR.BA": 121085814.7, "GARO.BA": 44000000, "FIPL.BA": 129430000,
    "GRIM.BA": 44307510, "DYCA.BA": 30000000, "POLL.BA": 6420388.889,
    "DGCE.BA": 160457190, "DOME.BA": 100000000, "ROSE.BA": 42589433.96,
    "RIGO.BA": 145064319.9, "MTR.BA": 122787764
}

# Tickers list
tickers = list(shares_outstanding.keys())

# Fetch the latest data for each ticker
data = {}
for ticker in tickers:
    stock_data = yf.Ticker(ticker)
    hist = stock_data.history(period="2d")
    if len(hist) == 2:  # Ensure we have two days' worth of data
        prev_close = hist['Close'].iloc[-2]
        latest_close = hist['Close'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        open_price = hist['Open'].iloc[-1]
        high = hist['High'].iloc[-1]
        low = hist['Low'].iloc[-1]
        price_change = latest_close - prev_close
        
        data[ticker] = {
            "Volume*Price": volume * latest_close,
            "Price Change": price_change,
            "Open Price": open_price,
            "Latest Price": latest_close,
            "Minimum Price": low,
            "Maximum Price": high,
            "Shares Outstanding": shares_outstanding[ticker]
        }

# Convert to DataFrame
df = pd.DataFrame.from_dict(data, orient='index').reset_index()
df.rename(columns={"index": "Ticker"}, inplace=True)

# Debugging: Check for missing data
print("Missing Data:\n", df.isnull().sum())

# Debugging: Print the DataFrame structure
print(df.head())

# Check data types
print(df.dtypes)

# Plotting
sns.set(style="whitegrid")

# Bubble chart 1: Y axis = volume*price; X axis = price variation with regard to the previous trading day
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Price Change', y='Volume*Price', size='Volume*Price', sizes=(20, 2000), hue='Ticker', alpha=0.6, palette='viridis')
plt.title("Bubble Chart: Volume*Price vs. Price Change")
plt.show()

# Bubble chart 2: Y axis = open price; X axis = latest price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Latest Price', y='Open Price', size='Volume*Price', sizes=(20, 2000), hue='Ticker', alpha=0.6, palette='plasma')
plt.title("Bubble Chart: Open Price vs. Latest Price")
plt.show()

# Bubble chart 3: Y axis = minimum price; X axis = maximum price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Maximum Price', y='Minimum Price', size='Volume*Price', sizes=(20, 2000), hue='Ticker', alpha=0.6, palette='coolwarm')
plt.title("Bubble Chart: Minimum Price vs. Maximum Price")
plt.show()

# Treemap: shares outstanding * price
df['Market Cap'] = df['Latest Price'] * df['Shares Outstanding']
df = df[df['Market Cap'] > 0]  # Filter out any tickers with non-positive market cap

plt.figure(figsize=(12, 8))
squarify.plot(sizes=df['Market Cap'], label=df['Ticker'], alpha=.8)
plt.title("Treemap: Market Cap (Shares Outstanding * Price)")
plt.axis('off')
plt.show()
