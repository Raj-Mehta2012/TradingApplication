# app.py
import streamlit as st
from stock_api import get_stock_data

# Define the app title
st.title('Stock Data Fetcher')

# Create input box for ticker name
ticker = st.text_input('Enter Ticker Name', '')

# Create a dropdown for duration selection
duration = st.selectbox(
    'Select Duration',
    ('1 week', '1 month', '6 months', '1 year')
)

# Create a submit button
if st.button('Fetch Stock Data'):
    if ticker:
        # Fetch stock data from backend
        stock_data = get_stock_data(ticker, duration)
        if stock_data is not None:
            st.write(stock_data)
        else:
            st.error('Failed to fetch stock data.')
    else:
        st.error('Please enter a ticker name.')
