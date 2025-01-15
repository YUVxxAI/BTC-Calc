import streamlit as st
import requests
import pandas as pd
import datetime

# פונקציה לקבלת מחיר הביטקוין הנוכחי
def get_bitcoin_price():
    try:
        response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
        data = response.json()
        return float(data['bpi']['USD']['rate'].replace(',', ''))
    except Exception as e:
        st.error(f"שגיאה בקבלת המחיר: {e}")
        return None

# פונקציה לקבלת היסטוריית מחירים
def get_bitcoin_history():
    try:
        response = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?for=yesterday')
        data = response.json()
        return pd.DataFrame(list(data['bpi'].items()), columns=['Date', 'Price'])
    except Exception as e:
        st.error(f"שגיאה בקבלת היסטוריית המחירים: {e}")
        return None

# פונקציה לחישוב ערך ההשקעה
def calculate_investment_value(initial_investment, bitcoin_price_then, bitcoin_price_now):
    bitcoin_owned = initial_investment / bitcoin_price_then
    return bitcoin_owned * bitcoin_price_now

# כותרת
st.title("מחשבון השקעה בביטקוין")

# קלט מהמשתמש
st.header("הזן את נתוני ההשקעה:")
initial_investment = st.number_input("כמה השקעת בביטקוין (בדולר)?", min_value=0.0, format="%.2f")
bitcoin_price_then = st.number_input("מה היה ערך הביטקוין כשקנית (בדולר)?", min_value=0.0, format="%.2f")

# קבלת נתוני היסטוריית מחירים
st.sidebar.title("נתוני היסטוריית מחירים")
history_data = get_bitcoin_history()
if history_data is not None:
    st.sidebar.line_chart(history_data.set_index('Date'))

# חישוב והצגת הערך
if st.button("חשב את הערך הנוכחי"):
    bitcoin_price_now = get_bitcoin_price()
    if bitcoin_price_now:
        current_value = calculate_investment_value(initial_investment, bitcoin_price_then, bitcoin_price_now)
        st.success(f"ההשקעה שלך שווה היום: ${current_value:,.2f}")
        st.info(f"ערך הביטקוין הנוכחי: ${bitcoin_price_now:,.2f}")
    else:
        st.error("לא ניתן לשלוף את המחיר הנוכחי של ביטקוין.")