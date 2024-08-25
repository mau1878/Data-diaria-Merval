import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime as dt
import streamlit as st

# Lista de tickers y datos de acciones en circulación
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

# Datos de acciones en circulación
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

# Función para obtener datos
def fetch_data(tickers, start_date):
    data = {}
    for ticker in tickers:
        # Obtener datos
        stock_data = yf.Ticker(ticker)
        df = stock_data.history(start=start_date - dt.timedelta(days=30), end=start_date + dt.timedelta(days=1))
        df = df.dropna()

        # Asegurarse de tener al menos 2 días de datos
        if len(df) < 2:
            print(f"No hay suficientes datos para {ticker}")
            continue
        
        # Seleccionar los dos últimos días (el día seleccionado y el día de negociación anterior)
        latest_data = df.iloc[-1]
        previous_data = df.iloc[-2]
        
        # Calcular variación porcentual del precio
        price_variation = (latest_data['Close'] - previous_data['Close']) / previous_data['Close'] * 100
        
        data[ticker] = {
            'price_variation': price_variation,
            'max_min_diff': (latest_data['High'] - latest_data['Low']) / latest_data['Low'] * 100,
            'close_open_diff': (latest_data['Close'] - latest_data['Open']) / latest_data['Open'] * 100
        }
    return data

# Establecer las fechas mínimas y máximas para el widget del calendario
min_date = dt.datetime(2000, 1, 1)
max_date = dt.datetime.now()

# Streamlit: El usuario selecciona una fecha con un rango más amplio
st.title("Análisis de Datos de Acciones")
selected_date = st.date_input(
    "Selecciona una fecha",
    value=max_date,  # Valor predeterminado a la fecha actual
    min_value=min_date,  # Permitir fechas desde el año 2000
    max_value=max_date  # Hasta la fecha actual
)

# Obtener los datos
try:
    data = fetch_data(tickers, selected_date)
except Exception as e:
    st.error(f"Error al obtener datos: {e}")
    st.stop()

# Limpiar datos
def clean_data(data):
    clean_data = {}
    for ticker, d in data.items():
        if not np.isnan(d['price_variation']):
            clean_data[ticker] = d
    return clean_data

data = clean_data(data)

# Función para crear gráficos de barras
def create_bar_plot(data, metric, title):
    # Filtrar tickers sin datos
    data = {ticker: info for ticker, info in data.items() if not np.isnan(info[metric])}
    
    # Convertir datos a DataFrame para facilitar el gráfico
    df = pd.DataFrame(data).T
    df = df.sort_values(by=metric, ascending=False)
    
    plt.figure(figsize=(14, 18))  # Altura aumentada para mejor visibilidad de etiquetas
    sns.barplot(x=df[metric], y=df.index, palette="viridis")
    plt.title(title, fontsize=18)
    plt.xlabel(f'{metric} (%)', fontsize=16)
    plt.ylabel('Ticker', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.7)
    st.pyplot(plt)

# Crear gráficos de barras
try:
    create_bar_plot(data, 'price_variation', 'Tickers con el Mayor Aumento Porcentual')
    create_bar_plot(data, 'max_min_diff', 'Tickers con la Mayor Diferencia Porcentual Entre Precios Máximos y Mínimos')
    create_bar_plot(data, 'close_open_diff', 'Tickers con la Mayor Diferencia Porcentual Entre Precios de Cierre y Apertura')
except Exception as e:
    st.error(f"Error al crear gráficos: {e}")
