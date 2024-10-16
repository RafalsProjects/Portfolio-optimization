import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Funkcja do obliczania wskaźnika Sharpe'a
def sharpe_ratio(returns, risk_free_rate=0):
    return (returns.mean() - risk_free_rate) / returns.std()

# Funkcja do pobierania danych historycznych i sprawdzania dostępności danych
def fetch_data(assets, start_date, end_date):
    data = yf.download(assets, start=start_date, end=end_date)['Adj Close']
    returns = data.pct_change().dropna()

    # Sprawdzanie, czy dane zwrotów są puste
    if returns.empty:
        print("Brak zwrotów po obliczeniu zmian procentowych. Sprawdzam dane dla okresu 3 dni...")
        # Zmiana okresu na 3 dni wstecz
        new_start_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
        data = yf.download(assets, start=new_start_date, end=end_date)['Adj Close']
        returns = data.pct_change().dropna()

        if returns.empty:
            print("Brak danych dla okresu 3 dni.")
        else:
            print(f"Dane dla aktywów (3 dni): \n{data}")

    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)

    # Zapisanie danych do pliku Excel
    filename = f"data_{start_date}_to_{end_date}.xlsx"
    data.to_excel(filename, sheet_name='Historical Data')
    print(f"Dane zostały zapisane do pliku: {filename}")

    return returns

# Funkcja do optymalizacji portfela
def optimize_portfolio(assets, start_date, end_date, num_portfolios=10000, risk_free_rate=0):
    returns = fetch_data(assets, start_date, end_date)

    if returns.empty:
        print("Brak wystarczających danych do optymalizacji portfela.")
        return None, None

    # Inicjalizacja list dla wyników
    results = np.zeros((num_portfolios, 4))  # Dodatkowa kolumna dla rocznego zwrotu
    weights_record = []

    for i in range(num_portfolios):
        weights = np.random.random(len(assets))
        weights /= np.sum(weights)  # Normalizacja wag
        weights_record.append(weights)

        # Obliczenie zwrotu i ryzyka portfela
        portfolio_return = np.dot(weights, returns.mean()) * 365  # Roczny zwrot
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 365, weights)))  # Roczna zmienność
        portfolio_sharpe = sharpe_ratio(returns.dot(weights), risk_free_rate)

        # Zapisanie wyników
        results[i, 0] = portfolio_return
        results[i, 1] = portfolio_std_dev
        results[i, 2] = portfolio_sharpe
        results[i, 3] = portfolio_return / portfolio_std_dev  # Stosunek zwrotu do zmienności

    return results, weights_record

# Parametry do optymalizacji
# assets = ['SOL-USD', 'SUI20947-USD', 'TAO22974-USD', 'RUNE-USD', 'AAVE-USD', 'PEPE24478-USD', 'FET-USD', 'WIF-USD', 'BONK-USD', 'PENDLE-USD']
# assets = ['OM-USD', 'CPOOL-USD', 'RIO-USD', 'ONDO-USD']
# assets = ['ACX22620-USD', 'BANANA28066-USD']
# assets = ['PAAL-USD', 'BTC-USD']
assets = ['BTC-USD', 'MUBI-USD', 'ORDI-USD', '1000SATS-USD', 'SOV-USD', 'SAVM-USD', 'TRAC25208-USD', 'DOG30933-USD', 'ORNJ-USD']
end_date = datetime.now().strftime('%Y-%m-%d')

# Okresy do analizy (w dniach)
# periods = [3, 7, 30, 90]  # 3 dni, 7 dni, 30 dni, 90 dni
periods = [7]
results_all_periods = {}

for period in periods:
    start_date = (datetime.now() - timedelta(days=period)).strftime('%Y-%m-%d')

    # Optymalizacja portfela
    results, weights_record = optimize_portfolio(assets, start_date, end_date)

    if results is not None:
        results_all_periods[period] = (results, weights_record)

# Wyświetlenie wyników dla każdego okresu
for period, (results, weights_record) in results_all_periods.items():
    sorted_indices = results[:, 3].argsort()[::-1]  # Indeksy portfeli posortowane malejąco
    top_n = 5  # Liczba najlepszych portfeli do wyświetlenia

    # Znajdowanie portfela o maksymalnym rocznym zwrocie i najlepszym wskaźniku Sharpe'a
    max_return_index = results[:, 0].argmax()
    max_return_portfolio = results[max_return_index]
    max_sharpe_index = results[:, 2].argmax()
    max_sharpe_portfolio = results[max_sharpe_index]

    # Ustalanie liczby dni dla poprawnego wyświetlenia
    days_label = 'dzień' if period == 1 else 'dni'
    print(f'\n=== Wyniki dla okresu {period} {days_label} ===')

    # Wyświetlenie portfela z najlepszym wskaźnikiem Sharpe'a
    #print(f'\nPortfel z najlepszym wskaźnikiem Sharpe\'a:')
    #print(f'Roczny zwrot: {max_sharpe_portfolio[0]:.4f}')
    #print(f'Zmienność: {max_sharpe_portfolio[1]:.4f}')
    #print('Wagi portfela:')
    #max_sharpe_weights = weights_record[max_sharpe_index]
    #for ticker, weight in zip(assets, max_sharpe_weights):
    #    print(f'{ticker}: {weight:.2%}')

    # Wyświetlenie najlepszych portfeli
    print(f'\nNajlepsze {top_n} portfeli według modelu Sharpe"a (zwrot/zmienność):')
    for i in range(top_n):
        idx = sorted_indices[i]
        weights = weights_record[idx]
        print(f'\nPortfel {i + 1}:')
        print(f'Roczny zwrot: {results[idx, 0]:.4f}')
        print(f'Zmienność: {results[idx, 1]:.4f}')
        print('Wagi portfela:')
        for ticker, weight in zip(assets, weights):
            print(f'{ticker}: {weight:.2%}')

    # Wyświetlenie portfela o maksymalnym zwrocie
    #print(f'\nPortfel o maksymalnym rocznym zwrocie:')
    #print(f'Roczny zwrot: {max_return_portfolio[0]:.4f}')
    #print(f'Zmienność: {max_return_portfolio[1]:.4f}')
    #print('Wagi portfela:')
    #max_return_weights = weights_record[max_return_index]
    #for ticker, weight in zip(assets, max_return_weights):
    #    print(f'{ticker}: {weight:.2%}')

# Inicjalizacja listy dla wybranych portfeli
selected_portfolios = []

# Wybór portfela przez użytkownika
print("\nWybierz portfel, który chcesz zaadoptować (1-5):")
for i in range(top_n):
    idx = sorted_indices[i]
    print(f'{i + 1}. Portfel {i + 1}: Roczny zwrot: {results[idx, 0]:.4f}, Zmienność: {results[idx, 1]:.4f}')

user_choice = int(input("Wprowadź numer portfela (1-5): ")) - 1
if user_choice < 0 or user_choice >= top_n:
    print("Nieprawidłowy wybór!")
else:
    # Dodaj wybrany portfel do listy
    weights = weights_record[sorted_indices[user_choice]]
    portfolio = [(ticker, weight) for ticker, weight in zip(assets, weights)]
    selected_portfolios.append(portfolio)
    print(f"Wybrany portfel {user_choice + 1} został dodany do listy: {portfolio}")

print(f'\n Lista krotek, (ticker, % of portfolio) dla każdego podanego coina we wcześniejszej części programu: {portfolio}')

    # Wykres wyników
    #plt.figure(figsize=(10, 6))
    #plt.scatter(results[:, 1], results[:, 0], c=results[:, 2], cmap='viridis', marker='o')
    #for i in range(top_n):
    #    idx = sorted_indices[i]
    #    plt.scatter(results[idx, 1], results[idx, 0], s=50, label=f'Portfel {i + 1}')

    # Dodanie portfela o maksymalnym zwrocie
    #plt.scatter(max_return_portfolio[1], max_return_portfolio[0], s=75, color='red', label='Max roczny zwrot', edgecolor='black')

    # Dodanie portfela z najlepszym wskaźnikiem Sharpe'a
    #plt.scatter(max_sharpe_portfolio[1], max_sharpe_portfolio[0], s=150, color='orange', label='Najlepszy #Sharpe', edgecolor='black', alpha=0.5)

    #plt.xlabel('Zmienność roczna')
    #plt.ylabel('Roczny zwrot')
    #plt.colorbar(label='Wskaźnik Sharpe\'a')
    #plt.title(f'Optymalizacja portfela kryptowalut (okres: {period} {days_label})')
    #plt.legend()
    #plt.show()
