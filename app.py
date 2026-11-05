
import streamlit as st
from datetime import datetime
import websocket
import json
from supabase import create_client, Client
def get_deriv_price():
    try:
        ws = websocket.create_connection(
            "wss://api.derivws.com/trading/v1/options/ws/public",
            timeout=8
        )

        ws.send(json.dumps({
            "ticks": "1HZ100V",
            "req_id": 1
        }))

        response = json.loads(ws.recv())
        ws.close()

        if "tick" in response:
            return response["tick"]["quote"]

        return None

    except Exception:
        return None
        
st.set_page_config(
    page_title="ZILLABOT",
    page_icon="🤖",
    layout="wide"
)

if "balance" not in st.session_state:
    st.session_state.balance = 1000.0

if "trades" not in st.session_state:
    st.session_state.trades = []

st.title("🤖 ZILLABOT")
st.caption("SMART AUTOMATED TRADING - DEMO MODE")

st.subheader("Live Deriv Market")

live_price = get_deriv_price()

if live_price is not None:
    st.metric("Volatility 100 Index", live_price)
else:
    st.warning("Live price unavailable. Please try again.")
    
st.success("Demo account active. No real money is being traded.")

st.metric("Demo Balance", f"${st.session_state.balance:,.2f}")

st.divider()

st.subheader("Trading Dashboard")

pair = st.selectbox(
    "Select currency pair",
    ["USD/KES", "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
)

price = st.number_input(
    "Enter a test market price",
    min_value=0.0001,
    value=129.50,
    step=0.01
)

amount = st.number_input(
    "Demo trade amount ($)",
    min_value=1.0,
    max_value=1000.0,
    value=10.0
)

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 BUY", use_container_width=True):
        if amount <= st.session_state.balance:
            st.session_state.balance -= amount
            st.session_state.trades.append({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Pair": pair,
                "Action": "BUY",
                "Price": price,
                "Amount": amount
            })
            st.success("Demo BUY recorded!")
        else:
            st.error("Insufficient demo balance.")

with col2:
    if st.button("🔴 SELL", use_container_width=True):
        if amount <= st.session_state.balance:
            st.session_state.balance -= amount
            st.session_state.trades.append({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Pair": pair,
                "Action": "SELL",
                "Price": price,
                "Amount": amount
            })
            st.success("Demo SELL recorded!")
        else:
            st.error("Insufficient demo balance.")

st.divider()

st.subheader("Trading History")

if st.session_state.trades:
    st.dataframe(
        st.session_state.trades,
        use_container_width=True
    )
else:
    st.info("No demo trades yet.")

st.caption("ZILLABOT v1.0 | Educational demo trading only")
          
