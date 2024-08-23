import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import squarify

# Define tickers and shares outstanding
tickers = [
    'GGAL.BA', 'YPFD.BA', 'PAMP.BA', 'TXAR.BA', 'ALUA.BA', 'CRES.BA', 'SUPV.BA', 'CEPU.BA', 
    'BMA.BA', 'TGSU2.BA', 'TRAN.BA', 'EDN.BA', 'LOMA.BA', 'MIRG.BA', 'DGCU2.BA', 'BBAR.BA', 
    'MOLI.BA', 'TGNO4.BA', 'CGPA2.BA', 'COME.BA', 'IRSA.BA', 'BYMA.BA', 'TECO2.BA', 'METR.BA', 
    'CECO2.BA', 'BHIP.BA', 'AGRO.BA', 'LEDE.BA', 'CVH.BA', 'HAVA.BA', 'AUSO.BA', 'VALO.BA', 
    'SEMI.BA', 'INVJ.BA', 'CTIO.BA', 'MORI.BA', 'HARG.BA', 'GCLA.BA', 'SAMI.BA', 'BOLT.BA', 
    'MOLA.BA', 'CAPX.BA', 'OEST.BA', 'LONG.BA', 'GCDI.BA', 'GBAN.BA', 'CELU.BA', 'FERR.BA', 
    'CADO.BA', 'GAMI.BA', 'PATA.BA', 'CARC.BA', 'BPAT.BA', 'RICH.BA', 'INTR.BA', 'GARO.BA', 
    'FIPL.BA', 'GRIM.BA', 'DYCA.BA', 'POLL.BA', 'DOME.BA', 'ROSE.BA', 'RIGO.BA', 'DGCE.BA', 
    'MTR.BA'
]

shares_outstanding = {
    'GGAL.BA': 1193470439, 'YPFD.BA': 393312793.1, 'PAMP.BA': 1383644606, 'TXAR.BA': 4517094019, 
    'ALUA.BA': 2800000000, 'CRES.BA': 592172573.1, 'SUPV.BA': 394984130.2, 'CEPU.BA': 1514022252, 
    'BMA.BA': 639413408, 'TGSU2.BA': 794495282.5, 'TRAN.BA': 217890149.5, 'EDN.BA': 906455097.6, 
    'LOMA.BA': 596026490.7, 'MIRG.BA': 18000000, 'DGCU2.BA': 202351290.7, 'BBAR.BA': 612710077.6, 
    'MOLI.BA': 201415126.1, 'TGNO4.BA': 439373937.5, 'CGPA2.BA': 333281047.1, 'COME.BA': 3119012723, 
    'IRSA.BA': 810895392, 'BYMA.BA': 3812500000, 'TECO2.BA': 2153688010, 'METR.BA': 278893888.6, 
    'CECO2.BA': 701988378.1, 'BHIP.BA': 1500000000, 'AGRO.BA': 100000000, 'LEDE.BA': 439714250.9, 
    'CVH.BA': 132888959.1, 'HAVA.BA': 46976134.56, 'AUSO.BA': 30469033.9, 'VALO.BA': 840182386, 
    'SEMI.BA': 191400000, 'INVJ.BA': 613174622.7, 'CTIO.BA': 409906728.5, 'MORI.BA': 281902003.1, 
    'HARG.BA': 365742910.5, 'GCLA.BA': 78549323.03, 'SAMI.BA': 148512803.8, 'BOLT.BA': 3150754416, 
    'MOLA.BA': 49082023.89, 'CAPX.BA': 179802282.4, 'OEST.BA': 160000000, 'LONG.BA': 153641509.4, 
    'GCDI.BA': 924990596.3, 'GBAN.BA': 159514578.7, 'CELU.BA': 100938186.5, 'FERR.BA': 947000000, 
    'CADO.BA': 123200000, 'GAMI.BA': 340000000, 'PATA.BA': 500000000, 'CARC.BA': 1091624474, 
    'BPAT.BA': 719145236.4, 'RICH.BA': 14167161.62, 'INTR.BA': 121085814.7, 'GARO.BA': 44000000, 
    'FIPL.BA': 129430000, 'GRIM.BA': 44307510, 'DYCA.BA': 30000000, 'POLL.BA': 6420388.889, 
    'DGCE.BA': 160457190, 'DOME.BA': 100000000, 'ROSE.BA': 42589433.96, 'RIGO.BA': 145064319.9, 
    'MTR.BA': 122787764
}

# Fetch data
data = yf.download(tickers, period='2d', group_by='ticker')

# Prepare a DataFrame to hold the latest data
latest_data = []
for ticker in tickers:
    try:
        df = data[ticker].iloc[-2:]  # Last two days for each ticker
        latest = df.iloc[-1]
        previous = df.iloc[-2]

        latest_data.append({
            'Ticker': ticker,
            'Price': latest['Close'],
            'Volume': latest['Volume'],
            'Open': latest['Open'],
            'High': latest['High'],
            'Low': latest['Low'],
            'Previous Close': previous['Close'],
            'Price Change': (latest['Close'] - previous['Close']) / previous['Close'] * 100,
            'Volume*Price': latest['Volume'] * latest['Close'],
            'Shares Outstanding*Price': shares_outstanding[ticker] * latest['Close'] if ticker in shares_outstanding else None
        })
    except:
        print(f"No data available for {ticker}")

df = pd.DataFrame(latest_data)

# Bubble chart: Y axis = volume*price; X axis = price variation with regard to the previous trading day
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='Price Change', y='Volume*Price', size='Volume*Price', sizes=(20, 2000), hue='Ticker', alpha=0.6, palette='viridis')
plt.title('Bubble Chart: Volume*Price vs. Price Change')
plt.xlabel('Price Change (%)')
plt.ylabel('Volume * Price')
plt.grid(True)
plt.show()

# Bubble chart: Y axis = open price; X axis = latest price
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='Price', y='Open', size='Volume*Price', sizes=(20, 2000), hue='Ticker', alpha=0.6, palette='coolwarm')
plt.title('Bubble Chart: Open Price vs. Latest Price')
plt.xlabel('Latest Price')
plt.ylabel('Open Price')
plt.grid(True)
plt.show()

# Bubble chart: Y axis = minimum price; X axis = maximum price
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x='High', y='Low', size='Volume*Price', sizes=(20, 2000), hue='Ticker', alpha=0.6, palette='magma')
plt.title('Bubble Chart: Minimum Price vs. Maximum Price')
plt.xlabel('Maximum Price')
plt.ylabel('Minimum Price')
plt.grid(True)
plt.show()

# Treemap: shares outstanding * price
plt.figure(figsize=(12, 8))
sizes = df['Shares Outstanding*Price'].dropna()
labels = df['Ticker'] + "\n" + df['Shares Outstanding*Price'].round(2).astype(str)
squarify.plot(sizes=sizes, label=labels, alpha=0.8, color=sns.color_palette("Spectral", len(df)))
plt.title('Treemap: Shares Outstanding * Price')
plt.axis('off')
plt.show()
