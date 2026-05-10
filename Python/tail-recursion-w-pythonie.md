# Czy w Pythonie istnieje Tail Recursion?

## Czym jest Tail Recursion (Rekurencja Ogonowa)?

Rekurencja ogonowa (ang. *tail recursion*) to szczególny rodzaj rekurencji, w którym **wywołanie rekurencyjne jest absolutnie ostatnią operacją** wykonywaną przez funkcję przed zwróceniem wyniku. 

W językach takich jak C++, Scala czy Haskell, kompilatory potrafią wykonać optymalizację takich wywołań. Jest to tzw. **Tail Call Optimization (TCO)**. Dzięki niej nie tworzy się nowej ramki na stosie wywołań (stack frame) dla każdego zagłębienia rekurencji. Zamiast tego aktualna ramka jest nadpisywana. Pozwala to na wykonywanie teoretycznie nieskończonej rekurencji bez ryzyka przepełnienia stosu pamięci (*Stack Overflow*) oraz przyspiesza działanie kodu.

## Tail Call Optimization w Pythonie

Odpowiedź brzmi: **Nie, Python domyślnie nie wspiera optymalizacji rekurencji ogonowej**.

Guido van Rossum (twórca Pythona) otwarcie odrzucił propozycje dodania TCO do standardowego interpretera (CPython). Główne powody tej decyzji to:

1. **Utrata precyzyjnych śladów wywołań (Tracebacks)**: TCO niszczy informacje o stosie wywołań, co znacznie utrudniłoby debugowanie błędów w Pythonie (który opiera się na bardzo czytelnych stack trace'ach).
2. **Czytelność i filozofia języka**: Python preferuje jawne pętle iteracyjne (`for`, `while`) zamiast skomplikowanych konstrukcji rekurencyjnych, które są bardziej charakterystyczne dla języków funkcyjnych.

Jeżeli napiszesz funkcję rekurencyjną w Pythonie, po osiągnięciu domyślnego limitu wywołań (zwykle ok. 1000) program po prostu zgłosi błąd i przestanie działać:

```python
RecursionError: maximum recursion depth exceeded
```

Limit ten można sztucznie zwiększyć modułem systemowym, ale nigdy nie rozwiąże to problemu wydajności i zużycia pamięci, a przy bardzo dużej wartości może zcrashować cały proces Pythona:
```python
import sys
sys.setrecursionlimit(5000)
```

## Jak sobie radzić zamiast rekurencji ogonowej?

Ponieważ Python nie ma TCO, zalecanym sposobem rozwiązania problemu jest **iteracja**. Jeśli algorytm potrafi być rozwiązany przez rekurencję ogonową, bardzo łatwo jest go zamienić na pętlę.

### Przykład: Silnia

Rozwiązanie za pomocą **rekurencji ogonowej** (narażone na `RecursionError` dla dużych liczb w Pythonie):
```python
def factorial_tail(n: int, accumulator: int = 1) -> int:
    if n == 0:
        return accumulator
    # Zwracany jest tylko wynik samej siebie. Nie ma mnożenia po wywołaniu!
    return factorial_tail(n - 1, n * accumulator)
```

**Rozwiązanie w Pythonie (Iteracja)** - to jest idiomatyczne podejście, które nie limituje nas głębokością stosu, a samo wykonanie będzie działać znacznie szybciej:
```python
def factorial_iter(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
```

### Alternatywa: Trampolina

Dla celów akademickich można zaimplementować TCO w języku Python za pomocą wzorca "Trampoliny" (zazwyczaj jako dekorator), który pod spodem opakowuje rekurencyjne wywołania w zwykłą pętlę `while`. W ekosystemie funkcjonują również zewnętrzne biblioteki (np. `tail-recursive`), które robią to za programistę. Odbiega to jednak od pythonowych standardów i na ogół nie powinno się tego używać w kodzie produkcyjnym.

## Powiązane tematy
- [Zaawansowane zagadnienia w Pythonie](zaawansowane-zagadnienia-w-pythonie.md)
- [Funkcje jako obiekty](funkcje-jako-obiekty.md)
- [Zużycie pamięci w Pythonie](zuzycie-pamieci-w-pythonie.md)
