# Zmienne nonlocal, global i zasięg (scope) w Pythonie

## Czym to jest?
W Pythonie słowa kluczowe `global` oraz `nonlocal` służą do określania zakresu (z ang. *scope*), z jakiego pochodzi modyfikowana zmienna. Pozwalają one interpreterowi zrozumieć, że nie chcemy tworzyć nowej zmiennej lokalnej, lecz zmodyfikować już istniejącą w zewnętrznym zakresie.

## Dlaczego to jest ważne i kiedy się przydaje?
Domyślnie, jeśli w Pythonie spróbujesz wewnątrz funkcji przypisać wartość do zmiennej (np. `x = 5`), Python uzna to za utworzenie **nowej zmiennej lokalnej**. Bez użycia `global` lub `nonlocal` nie możemy nadpisywać wartości zmiennych zdefiniowanych wyżej (chociaż możemy modyfikować ich stan, np. dodając element do listy). Zrozumienie tych słów kluczowych jest niezbędne do poprawnej kontroli nad cyklem życia zmiennych, zwłaszcza przy funkcjach zagnieżdżonych (np. przy tworzeniu domknięć - closures) czy skryptach korzystających ze stanu współdzielonego.

Aby to zrozumieć, należy pamiętać o regule **LEGB** – kolejności w jakiej Python szuka zmiennych:
1. **L**ocal – w bieżącej funkcji
2. **E**nclosing – w funkcji otaczającej (zewnętrznej)
3. **G**lobal – w module (pliku)
4. **B**uilt-in – we wbudowanych funkcjach (np. `print()`)

### Dlaczego nie ma słowa `local`?
W Pythonie nie ma słowa kluczowego `local`, ponieważ **każda zmienna, do której przypisujesz wartość wewnątrz funkcji, automatycznie staje się zmienną lokalną** (chyba że użyjesz `global` lub `nonlocal`). Python z założenia przyjmuje, że domyślnie chcemy działać na lokalnym zakresie, co chroni nas przed przypadkowym nadpisaniem zmiennych z zewnątrz.

## Jak to działa? (Przykłady)

### `global`
Używamy `global`, gdy chcemy zmodyfikować zmienną zdefiniowaną na poziomie modułu (poza wszystkimi funkcjami).

```python
licznik = 0  # Zmienna w zakresie Global

def zwieksz_licznik():
    # Bez poniższej linijki otrzymalibyśmy błąd: UnboundLocalError
    global licznik 
    licznik += 1

zwieksz_licznik()
print(licznik)  # Wypisze: 1
```
*Dobra praktyka:* Staraj się unikać zmiennych globalnych, ponieważ utrudniają testowanie i śledzenie zmian stanu w aplikacji. Zazwyczaj lepiej przekazywać stan jako argument lub wykorzystać programowanie obiektowe.

### `nonlocal`
Używamy `nonlocal`, gdy chcemy zmodyfikować zmienną w najbliższym zewnętrznym zakresie (Enclosing), który **nie jest** zakresem globalnym. Przydaje się to najczęściej wewnątrz funkcji zagnieżdżonych.

```python
def zewnetrzna_funkcja():
    stan = "początkowy"  # Zmienna w zakresie Enclosing

    def wewnetrzna_funkcja():
        # Wskazujemy, że chcemy zmodyfikować zmienną "stan" z funkcji zewnętrznej
        nonlocal stan
        stan = "zmieniony przez wewnątrz"

    wewnetrzna_funkcja()
    print(stan)

zewnetrzna_funkcja()  # Wypisze: zmieniony przez wewnątrz
```

### Alternatywy dla modyfikowania stanu
Zamiast korzystać z `nonlocal`, często wygodniejsze (i bezpieczniejsze) jest zastosowanie zmiennych mutowalnych (jak słowniki czy listy), ponieważ modyfikowanie ich zawartości nie wymaga zmiany przypisania samej zmiennej:

```python
def zewnetrzna():
    dane = {"licznik": 0}

    def wewnetrzna():
        # Działa poprawnie bez `nonlocal`, 
        # bo modyfikujemy zawartość istniejącego słownika.
        dane["licznik"] += 1

    wewnetrzna()
    print(dane["licznik"])

zewnetrzna() # Wypisze: 1
```

## Powiązane pliki
- [Wewnętrzne obiekty Pythona](opisz-wyczerpująco-następujące-zagadnienia-python-wewnętrzne-obiekty-pythona-fun.md)
- [Python Globalne Zmienne](python-globalne-zmienne.md)
