# Best Time to Buy and Sell Stock

Problem **Best Time to Buy and Sell Stock** to klasyczne zadanie algorytmiczne, w którym szukamy największego zysku z jednokrotnego kupna i sprzedaży akcji.

Masz daną tablicę `prices`, gdzie `prices[i]` oznacza cenę akcji danego dnia. Celem jest znalezienie takiej pary dni (dzień kupna, dzień sprzedaży), aby zysk był jak największy. Pamiętaj, że musisz kupić akcje **przed** ich sprzedażą. Jeśli nie można osiągnąć żadnego zysku (np. ceny cały czas spadają), funkcja powinna zwrócić `0`.

**Kiedy stosować?**
- Zadanie jest świetnym sprawdzeniem umiejętności śledzenia stanu pętli (tzw. _state tracking_) podczas jednego przejścia przez dane.
- Opiera się na koncepcie zbliżonym do uproszczonej wersji [Sliding Window](sliding-window.md) lub *Two Pointers*.

---

## Naiwne rozwiązanie (Brute Force) - $O(n^2)$

Najprostszym sposobem byłoby sprawdzenie każdej możliwej pary dni (kupno i sprzedaż w dniach następujących po nim) i zapisanie największego zysku. 

Jednak z uwagi na to, że tablica może mieć długość do $10^5$, rozwiązanie $O(n^2)$ przekroczy dopuszczalny limit czasu (Time Limit Exceeded).

---

## Optymalne rozwiązanie - $O(n)$

Aby zoptymalizować rozwiązanie, możemy przejść przez tablicę tylko raz (złożoność $O(n)$). 

### 💡 Intuicja

Wyobraź sobie, że masz **wehikuł czasu** i patrzysz na wykres cen akcji z perspektywy przyszłości. Chcesz wrócić w czasie, kupić akcje jednego dnia i sprzedać je innego, późniejszego dnia – tak, żeby zarobić jak najwięcej.

Kluczowe spostrzeżenie: **nie musisz znać przyszłości, wystarczy że pamiętasz przeszłość.**

Kiedy idziesz dzień po dniu i w dniu `i` zastanawiasz się „czy powinienem dzisiaj sprzedać?", to najlepszą strategią jest sprzedać po **najniższej cenie kupna, jaką widziałeś wcześniej**. Nie musisz cofać się i sprawdzać wszystkich poprzednich dni – wystarczy, że na bieżąco śledzisz jedno minimum.

Dlatego algorytm trzyma tylko **dwie zmienne**:
1. `min_price` – najniższa cena, jaką widzieliśmy do tej pory (najlepsza okazja zakupu).
2. `max_profit` – najlepszy zysk, jaki udało się osiągnąć do tej chwili.

W każdym dniu pytamy:
- **Czy dzisiaj jest taniej niż kiedykolwiek wcześniej?** → Aktualizuj `min_price`.
- **Ile zarobię, jeśli sprzedam dzisiaj?** → Oblicz `price - min_price`. Jeśli to więcej niż dotychczasowy rekord, zaktualizuj `max_profit`.

### 🔍 Wizualizacja (krok po kroku)

```
prices = [7, 1, 5, 3, 6, 4]

Dzień 0:  cena = 7   min_price = 7   zysk = 0   max_profit = 0
          Pierwsza cena → ustawiamy min_price.

Dzień 1:  cena = 1   min_price = 1   zysk = 0   max_profit = 0
          1 < 7 → nowe minimum! Ale jeszcze nic nie sprzedajemy.

Dzień 2:  cena = 5   min_price = 1   zysk = 4   max_profit = 4
          5 - 1 = 4 → nowy rekord zysku!

Dzień 3:  cena = 3   min_price = 1   zysk = 2   max_profit = 4
          3 - 1 = 2 → gorzej niż 4, zostawiamy.

Dzień 4:  cena = 6   min_price = 1   zysk = 5   max_profit = 5  ★
          6 - 1 = 5 → nowy rekord! To będzie odpowiedź.

Dzień 5:  cena = 4   min_price = 1   zysk = 3   max_profit = 5
          4 - 1 = 3 → gorzej niż 5, zostawiamy.

Wynik: 5  (kupno w dniu 1 za 1, sprzedaż w dniu 4 za 6)
```

> [!TIP]
> Zauważ, że `elif` w kodzie to optymalizacja – jeśli właśnie znaleźliśmy nowe minimum, to zysk ze sprzedaży w tym samym dniu wynosi 0 (kupujesz i sprzedajesz po tej samej cenie), więc nie ma sensu liczyć zysku. Ale kod zadziałałby poprawnie również z dwoma niezależnymi `if`-ami zamiast `if/elif`.

### ⚠️ Podchwytliwy przypadek: nowe minimum ≠ lepszy zysk

Co jeśli lepszy zysk daje **wyższa** cena kupna? Np. `prices = [4, 9, 2, 6, 5]`:
- Kupno za **4**, sprzedaż za **9** → zysk **5** ✅
- Kupno za **2**, sprzedaż za **6** → zysk **4** ❌

```
prices = [4, 9, 2, 6, 5]

Dzień 0:  cena = 4   min_price = 4   zysk = 0   max_profit = 0
Dzień 1:  cena = 9   min_price = 4   zysk = 5   max_profit = 5  ★
Dzień 2:  cena = 2   min_price = 2   zysk = 0   max_profit = 5
          ↑ Nowe minimum! Ale max_profit NIE jest resetowany.
Dzień 3:  cena = 6   min_price = 2   zysk = 4   max_profit = 5
          4 < 5 → stary rekord wygrywa.
Dzień 4:  cena = 5   min_price = 2   zysk = 3   max_profit = 5

Wynik: 5  (kupno w dniu 0 za 4, sprzedaż w dniu 1 za 9)
```

Algorytm działa poprawnie, bo **`min_price` i `max_profit` to dwie niezależne zmienne**. Aktualizacja `min_price` to nie jest „decyzja o kupnie" — to tylko zapamiętanie „gdybym chciał kupić w przyszłości, to najlepszą ceną jest teraz 2". Natomiast `max_profit` pamięta najlepszy wynik **ze wszystkich dotychczasowych par**, niezależnie od aktualnego `min_price`.

### Implementacja w Pythonie

```python
def maxProfit(prices: list[int]) -> int:
    # Inicjalizujemy min_price bardzo dużą wartością
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        # Aktualizacja minimalnej ceny zakupu
        if price < min_price:
            min_price = price
        # Obliczenie ewentualnego zysku, jeśli sprzedalibyśmy po obecnej cenie
        elif price - min_price > max_profit:
            max_profit = price - min_price
            
    return max_profit

# Przykłady użycia:
print(maxProfit([7, 1, 5, 3, 6, 4])) # Wyjście: 5 (Kupujesz za 1, sprzedajesz za 6)
print(maxProfit([7, 6, 4, 3, 1]))    # Wyjście: 0 (Ceny tylko spadają, nie kupujemy wcale)
```

**Złożoność:**
- **Czasowa:** $O(n)$ – iterujemy przez tablicę cen tylko raz.
- **Pamięciowa:** $O(1)$ – trzymamy tylko dwie zmienne.

---

## Podsumowanie

| Metoda | Złożoność Czasowa | Złożoność Pamięciowa |
| - | - | - |
| Brute Force | $O(n^2)$ | $O(1)$ |
| Śledzenie Minimum (Optymalna) | $O(n)$ | $O(1)$ |

**Powiązane tematy:**

- [Sliding Window](sliding-window.md)
