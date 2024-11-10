import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from datetime import datetime


# Funkcja do pobierania danych historycznych o cenach
def get_price_data(tickers, start_date, end_date):
    price_data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return price_data

# Funkcja do obliczania średnich zwrotów i macierzy kowariancji
def calculate_returns(price_data):
    returns = price_data.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    return mean_returns, cov_matrix

# Funkcja celu do minimalizacji (ryzyko)
def portfolio_volatility(weights, mean_returns, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

# Funkcja do optymalizacji portfela
def optimize_portfolio(tickers, mean_returns, cov_matrix):
    num_assets = len(tickers)
    args = (mean_returns, cov_matrix)
    
    # Ograniczenia: suma wag = 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    # Ograniczenia: wagi >= 0
    bounds = tuple((0, 1) for asset in range(num_assets))
    
    # Inicjalizacja wag równych dla wszystkich aktywów
    initial_weights = num_assets * [1. / num_assets,]
    
    # Optymalizacja
    optimal = minimize(portfolio_volatility, initial_weights, args=args,
                       method='SLSQP', bounds=bounds, constraints=constraints)
    return optimal

# Główna funkcja
def main():
    tickers = ['SOL-USD', 'SUI20947-USD', 'TAO22974-USD', 'RUNE-USD', 'AAVE-USD', 'PEPE24478-USD', 'FET-USD', 'WIF-USD', 'BONK-USD', 'PENDLE-USD', 'KAS-USD']  # Wprowadź swoje tickery
    start_date = '2024-08-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Pobieranie danych
    price_data = get_price_data(tickers, start_date, end_date)
    
    # Obliczanie średnich zwrotów i macierzy kowariancji
    mean_returns, cov_matrix = calculate_returns(price_data)
    
    # Optymalizacja portfela
    optimal = optimize_portfolio(tickers, mean_returns, cov_matrix)

    # Wyświetlenie wyników
    print("Optymalne wagi portfela:")
    for i, ticker in enumerate(tickers):
        print(f"{ticker}: {optimal.x[i]:.4f}")
    
    # Obliczanie ryzyka i zwrotu
    optimal_return = np.dot(optimal.x, mean_returns)
    optimal_volatility = portfolio_volatility(optimal.x, mean_returns, cov_matrix)
    
    print(f"\nOczekiwany zwrot: {optimal_return:.4f}")
    print(f"Ryzyko (zmienność): {optimal_volatility:.4f}")

    # Wykres ryzyko-zwrot
    plt.scatter(optimal_volatility, optimal_return, color='red', marker='o', s=200)
    plt.title('Optymalizacja portfela')
    plt.xlabel('Ryzyko (zmienność)')
    plt.ylabel('Oczekiwany zwrot')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
