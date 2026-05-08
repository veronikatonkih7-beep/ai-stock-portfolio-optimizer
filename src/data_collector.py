import yfinance as yf
import pandas as pd
import numpy as np

def fetch_data(tickers):
    """Загружает исторические данные"""
    data = yf.download(tickers, period="1y")
    df = data['Close'].reset_index().melt(id_vars='Date', var_name='Ticker', value_name='Close')
    return df

def calculate_returns(data):
    """Рассчитывает доходности"""
    data = data.sort_values(['Ticker', 'Date'])
    data['Return'] = data.groupby('Ticker')['Close'].pct_change()
    return data.dropna()