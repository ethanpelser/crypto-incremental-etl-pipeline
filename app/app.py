import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

DB_PATH = Path("crypto_prices.db")

st.set_page_config(
    page_title="Crypto ETL Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Crypto Incremental ETL Dashboard")
st.caption("Interactive dashboard displaying metrics from a normalized ETL database.")


@st.cache_data(ttl=60)
def load_data():
    if not DB_PATH.exists():
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        c.coin_id,
        c.coin_name,
        cur.currency_code,
        o.price_timestamp,
        o.price,
        o.market_cap,
        o.total_volume
    FROM crypto_price_observations o
    JOIN coins c
        ON o.coin_key = c.coin_key
    JOIN currencies cur
        ON o.currency_key = cur.currency_key
    ORDER BY o.price_timestamp;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    df["price_timestamp"] = pd.to_datetime(df["price_timestamp"])

    return df


df = load_data()

if df.empty:
    st.warning("No data found. Run your ETL pipeline first so crypto_prices.db exists.")
    st.stop()

latest_timestamp = df["price_timestamp"].max()
total_records = len(df)
total_coins = df["coin_name"].nunique()
avg_price = df["price"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{total_records:,}")
col2.metric("Coins Tracked", total_coins)
col3.metric("Average Price", f"${avg_price:,.2f}")
col4.metric("Latest Update", latest_timestamp.strftime("%Y-%m-%d %H:%M"))

st.divider()

selected_coin = st.selectbox(
    "Select a coin",
    sorted(df["coin_name"].unique())
)

coin_df = df[df["coin_name"] == selected_coin]

fig_price = px.line(
    coin_df,
    x="price_timestamp",
    y="price",
    title=f"{selected_coin} Price Over Time",
    markers=True
)

st.plotly_chart(fig_price, use_container_width=True)

fig_volume = px.bar(
    coin_df,
    x="price_timestamp",
    y="total_volume",
    title=f"{selected_coin} Trading Volume"
)

st.plotly_chart(fig_volume, use_container_width=True)

st.subheader("Latest Records")

latest_df = df.sort_values("price_timestamp", ascending=False).head(20)

st.dataframe(
    latest_df,
    use_container_width=True,
    hide_index=True
)