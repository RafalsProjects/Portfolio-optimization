import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize

# Funkcja do pobierania danych historycznych o cenach
def get_price_data(tickers, start_date, end_date):
    price_data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return price_data

# Funkcja do obliczania średnich zwrotów
def calculate_returns(price_data):
    returns = price_data.pct_change().dropna()
    mean_returns = returns.mean()
    return mean_returns

# Funkcja celu do maksymalizacji zwrotu
def negative_portfolio_return(weights, mean_returns):
    return -np.dot(weights, mean_returns)

# Funkcja do optymalizacji portfela
def optimize_portfolio(tickers, mean_returns):
    num_assets = len(tickers)
    args = (mean_returns,)
    
    # Ograniczenia: suma wag = 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    # Ograniczenia: wagi >= 0
    bounds = tuple((0, 1) for asset in range(num_assets))
    
    # Inicjalizacja wag równych dla wszystkich aktywów
    initial_weights = num_assets * [1. / num_assets,]
    
    # Optymalizacja
    optimal = minimize(negative_portfolio_return, initial_weights, args=args,
                       method='SLSQP', bounds=bounds, constraints=constraints)
    return optimal

# Główna funkcja
def main():
    tickers = ['BTC-USD', 'ETH-USD', 'TON11419-USD', 'SOL-USD', 'SUI20947-USD', 'TAO22974-USD', 'NEAR-USD'] # Wprowadź swoje tickery
    start_date = '2024-06-01'
    end_date = '2024-10-01'
    
    # Pobieranie danych
    price_data = get_price_data(tickers, start_date, end_date)
    
    # Obliczanie średnich zwrotów
    mean_returns = calculate_returns(price_data)
    
    # Optymalizacja portfela
    optimal = optimize_portfolio(tickers, mean_returns)

    # Wyświetlenie wyników
    print("Optymalne wagi portfela:")
    for i, ticker in enumerate(tickers):
        print(f"{ticker}: {optimal.x[i]:.4f}")
    
    # Obliczanie oczekiwanego zwrotu
    optimal_return = np.dot(optimal.x, mean_returns)

    print(f"\nOczekiwany zwrot: {optimal_return:.4f}")

if __name__ == "__main__":
    main()
