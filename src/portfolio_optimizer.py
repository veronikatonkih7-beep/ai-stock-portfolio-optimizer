import numpy as np

def optimize_portfolio(returns):
    """Простая оптимизация портфеля (равные веса)"""
    pivot = returns.pivot(index='Date', columns='Ticker', values='Return').dropna()
    n_assets = len(pivot.columns)
    weights = np.ones(n_assets) / n_assets
    metrics = {
        'return': float(np.mean(pivot.mean()) * 252),
        'volatility': float(np.std(pivot.mean()) * np.sqrt(252))
    }
    return weights, metrics