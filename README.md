# Description
Here we may notice Python project for portoflio optimalization.

We may notice 2 projects:
- Markowitz theory
- Shapre theory

# Teoria Markowitza vs. Teoria Sharpe'a
Zarządzanie portfelem inwestycyjnym opiera się na dwóch kluczowych teoriach: teorii Markowitza i teorii Sharpe'a. Choć obie koncepcje są ze sobą powiązane, różnią się założeniami, celami oraz metodologią.

## Teoria Markowitza
Teoria Markowitza, opracowana przez Harry’ego Markowitza w 1952 roku, koncentruje się na optymalizacji portfela poprzez równoważenie ryzyka i zwrotu. Jej kluczowe elementy to:

**Cel**: Minimalizacja ryzyka przy założonym zwrocie lub maksymalizacja zwrotu przy danym poziomie ryzyka.
**Ryzyko**: Definiowane jako odchylenie standardowe zwrotów portfela.
**Dywersyfikacja**: Wykorzystanie korelacji między aktywami w celu zmniejszenia ryzyka.
**Efektywna granica**: Zbiór portfeli o najlepszym stosunku ryzyka do zwrotu.
Teoria Markowitza zakłada, że inwestorzy są racjonalni i awersyjni wobec ryzyka.

### Wzory w teorii Markowitza
1. Oczekiwana stopa zwrotu portfela

E(Rp) = Σ(wi * E(Ri))

Gdzie:
E(Rp): Oczekiwana stopa zwrotu portfela,
wi: Waga aktywa i w portfelu,
E(Ri): Oczekiwana stopa zwrotu aktywa i,
n: Liczba aktywów w portfelu.

2. Ryzyko (wariancja) portfela
σp² = ΣΣ(wi * wj * σij)

Gdzie:
σp²: Wariancja portfela,
wi, wj: Wagi aktywów i i j,
σij: Kowariancja między aktywami i i j.

3. Efektywna granica
Efektywna granica to zbiór portfeli maksymalizujących zwrot przy danym poziomie ryzyka lub minimalizujących ryzyko przy danym poziomie zwrotu. Wzór na optymalne wagi aktywów dla portfela:

W = (Σ⁻¹ * (R - Rf * 1)) / (1' * Σ⁻¹ * (R - Rf * 1))

Gdzie:
W: Wektor wag optymalnych aktywów,
Σ⁻¹: Odwrotna macierz kowariancji aktywów,
R: Wektor oczekiwanych zwrotów,
Rf: Stopa zwrotu aktywa wolnego od ryzyka,
1: Wektor jednostkowy,
1': Transpozycja wektora jednostkowego.

4. Odchylenie standardowe portfela
σp = √(σp²)

Gdzie:
σp: Odchylenie standardowe portfela,
σp²: Wariancja portfela.

## Teoria Sharpe'a
Teoria Sharpe'a, stworzona przez Williama Sharpe'a w 1964 roku, bazuje na modelu CAPM (Capital Asset Pricing Model). Główne założenia to:

**Cel**: Maksymalizacja efektywności portfela, czyli premii za ryzyko w stosunku do zmienności.
**Ryzyko systematyczne**: Skupienie na ryzyku rynkowym, które nie może zostać wyeliminowane przez dywersyfikację.
**Aktywo wolne od ryzyka**: Wprowadzenie portfela rynkowego oraz inwestycji wolnych od ryzyka jako punktu odniesienia.
**Współczynnik Sharpe’a**: Miara efektywności portfela:


Opis wzorów w teorii Sharpe’a
**Współczynnik Sharpe’a**:
Miara efektywności portfela:

S = (Rp - Rf) / σp

Gdzie:
- S – wskaźnik Sharpe’a,
- Rp – stopa zwrotu portfela,
- Rf – stopa zwrotu aktywa wolnego od ryzyka,
- σp – odchylenie standardowe zwrotu portfela (całkowite ryzyko).

**Model CAPM (Capital Asset Pricing Model)**:
Wyznacza oczekiwaną stopę zwrotu aktywa na podstawie ryzyka systematycznego:

E(Ri) = Rf + βi * (E(Rm) - Rf)

Gdzie:
- E(Ri) – oczekiwana stopa zwrotu aktywa,
- Rf – stopa zwrotu aktywa wolnego od ryzyka,
- βi – współczynnik beta aktywa (miara ryzyka systematycznego),
- E(Rm) – oczekiwana stopa zwrotu rynku,
- (E(Rm) - Rf) – premia za ryzyko rynkowe.

# Główne różnice między teorią Markowitza a teorią Sharpe'a
**Cel**:
*Markowitz:* Minimalizacja ryzyka lub maksymalizacja zwrotu.
*Sharpe:* Maksymalizacja stosunku premii za ryzyko do zmienności (wskaźnika Sharpe’a).

**Ryzyko**:
*Markowitz:* Uwzględnia całkowite ryzyko portfela, mierzone odchyleniem standardowym.
*Sharpe:* Koncentruje się na ryzyku systematycznym (ryzyko związane z rynkiem jako całością).

**Dywersyfikacja**:
*Markowitz:* Kluczowy element redukcji ryzyka przez analizę korelacji między aktywami.
*Sharpe:* Zakłada, że ryzyko niesystematyczne zostało już wyeliminowane dzięki dywersyfikacji.

**Punkt odniesienia**:
*Markowitz:* Efektywna granica portfeli, czyli zbiór portfeli o najlepszym stosunku ryzyka do zwrotu.
*Sharpe:* Portfel rynkowy (optymalny portfel) oraz aktywo wolne od ryzyka.

**Narzędzia**:
*Markowitz:* Analiza macierzy kowariancji stóp zwrotu aktywów.
*Sharpe:* Model CAPM (Capital Asset Pricing Model) i wskaźnik Sharpe’a.