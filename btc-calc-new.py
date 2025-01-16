import streamlit as st
import requests
import plotly.graph_objects as go

# פונקציה לקבלת שער הביטקוין במטבעות שונים
def get_bitcoin_price(currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("bitcoin", {}).get(currency, None)
    return None

# פונקציה ליצירת גרף היסטוריית מחירים
def get_price_history(currency):
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency={currency}&days=30"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("prices", [])
        return [(point[0], point[1]) for point in data]
    return []

# פונקציה ליצירת גרף
def create_price_chart(prices):
    timestamps = [point[0] for point in prices]
    values = [point[1] for point in prices]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=values, mode="lines", name="Bitcoin Price"))
    fig.update_layout(
        title="גרף היסטוריית מחירים של ביטקוין",
        xaxis_title="תאריך",
        yaxis_title="מחיר",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
    )
    return fig

# הגדרות עיצוב לעברית
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    body {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# כותרת ראשית
st.title("מחשבון השקעה בביטקוין")

# בחירת מטבע
currency = st.selectbox("בחר מטבע", ["usd", "eur", "ils"], format_func=lambda x: {"usd": "דולר", "eur": "יורו", "ils": "שקל"}[x])

# קבלת שער הביטקוין
current_price = get_bitcoin_price(currency)
if current_price is None:
    st.error("לא ניתן לקבל את שער הביטקוין כעת.")
else:
    st.success(f"שער הביטקוין הנוכחי ({currency.upper()}): {current_price:,.2f}")

# מחשבון השקעה
st.header("חישוב השקעה")
initial_investment = st.number_input("סכום ההשקעה הראשונית (במטבע שנבחר)", min_value=0.0, step=1.0)
bitcoin_price_then = st.number_input("שער הביטקוין בעת ההשקעה", min_value=0.0, step=1.0)

if st.button("חשב"):
    if bitcoin_price_then > 0:
        bitcoins_owned = initial_investment / bitcoin_price_then
        investment_value = bitcoins_owned * current_price
        st.write(f"מספר הביטקוינים שרכשת: {bitcoins_owned:.6f}")
        st.write(f"שווי ההשקעה כיום: {investment_value:,.2f} {currency.upper()}")
    else:
        st.error("אנא הזן שער ביטקוין תקין בעת ההשקעה.")

# גרף היסטוריית מחירים
st.header("גרף היסטוריית מחירים (30 ימים אחרונים)")
price_history = get_price_history(currency)
if price_history:
    chart = create_price_chart(price_history)
    st.plotly_chart(chart)
else:
    st.error("לא ניתן לטעון את נתוני היסטוריית המחירים.")