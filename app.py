import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Crypto Trend Realtime", layout="wide")

st.title("📈 Real-Time Crypto Price Trend")
st.write("Data diambil dari CoinGecko API (Polling 1 detik, bebas API Key).")

# pilih crypto
crypto = st.selectbox(
    "Pilih Cryptocurrency:",
    ["bitcoin", "ethereum", "binancecoin", "dogecoin", "solana", "cardano", "ripple"]
)

placeholder_chart.line_chart(
    st.session_state.df,
    x="time",
    y="price"
)

st.write(f"Menampilkan trend harga **{crypto.capitalize()}** terhadap USD.")

# session data
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["time", "price"])

placeholder_price = st.empty()
placeholder_chart = st.empty()

def get_price(coin):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        r = requests.get(url, timeout=5)
        data = r.json()
        return float(data[coin]["usd"])
    except:
        return None

# fetch harga
price = get_price(crypto)

if price is not None:
    now = pd.Timestamp.now()
    st.session_state.df.loc[len(st.session_state.df)] = [now, price]

    if len(st.session_state.df) > 300:
        st.session_state.df = st.session_state.df.iloc[-300:]

    # FIXED → pakai triple quotes
    placeholder_price.markdown(
        f"""
        ### 💰 Harga Terbaru: **{price:.5f} USD**  
        ⏳ Auto refresh setiap 1 detik
        """
    )

    placeholder_chart.line_chart(
        st.session_state.df,
        x="time",
        y="price"
    )
else:
    placeholder_price.error("Tidak bisa mengambil harga. Coba lagi.")


import plotly.graph_objects as go

df = st.session_state.df

# 1️⃣ Plotly Line Chart
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=df["time"], 
    y=df["price"],
    mode="lines",
    line=dict(color="#00ccff", width=3)
))
fig_line.update_layout(
    title="🌐 Trend Harga (Plotly Line Chart)",
    height=350,
    template="plotly_dark"
)
st.plotly_chart(fig_line, use_container_width=True)

# 2️⃣ Plotly Area Chart
fig_area = go.Figure()
fig_area.add_trace(go.Scatter(
    x=df["time"], 
    y=df["price"],
    fill="tozeroy",
    mode="lines",
    line=dict(color="#00ff88", width=2)
))
fig_area.update_layout(
    title="🌄 Grafik Area (Gradient)",
    height=300,
    template="plotly_dark"
)
st.plotly_chart(fig_area, use_container_width=True)


# auto refresh
time.sleep(1)
st.experimental_set_query_params(refresh=str(time.time()))

