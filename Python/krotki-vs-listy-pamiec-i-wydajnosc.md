# Krotki vs Listy: Pamięć, Wydajność i Haszowalność

## Podsumowanie
Ten dokument szeroko wyjaśnia różnice między krotkami (`tuple`), a listami (`list`) w języku Python w oparciu o ich architekturę wewnętrzną. Opisuje, jak różnice te wpływają na zużycie pamięci, wydajność operacji oraz wyjaśnia koncept haszowalności struktury danych w kontekście użycia ich jako klucze w słownikach czy elementy w zbiorach.

## Dlaczego jest to ważne?
Wybór odpowiedniej struktury danych ma kluczowe znaczenie przy projektowaniu wydajnych aplikacji:
- **Oszczędność zasobów:** minimalizacja zużycia pamięci jest krytyczna przy przetwarzaniu obszernych zbiorów danych (np. Data Science).
- **Czas wykonania:** znajomość drobnych różnic szybkościowych (jak szybsze iterowanie lub czas dostępu) pozwala optymalizować wąskie gardła.
- **Odporność na błędy:** zrozumienie haszowalności zapobiega niespodziewanym błędom typu `TypeError` i determinuje typy użyte w tworzeniu zaawansowanych słowników i mapowań.

## Jak to działa?

### Pamięć i Wydajność (Memory & Performance)

**Krotki (Tuples) mają mniejszy ślad pamięciowy:**
Krotki w Pythonie są niemutowalne (immutable), co oznacza, że po utworzeniu nie da się dołączyć do nich nowych elementów, ani usunąć istniejących. Z tego powodu silnik języka alokuje dla krotki w pamięci blok idealnie odpowiadający wymaganiom na przechowanie przypisanych jej elementów. Ze względu na z góry ustalony rozmiar, interpreter tworzy i porusza się (iteruje) po krotkach zauważalnie szybciej.

**Listy używają nadmiarowej alokacji pamięci (over-allocation):**
W odróżnieniu od krotek, listy są mutowalne i oparte na koncepcie tablic dynamicznych. Mechanizm dodawania elementu np. poprzez `.append()` w idealnym wariancie posiada złożoność obliczeniową wynoszącą _zamortyzowane O(1)_. Aby umożliwić ten błyskawiczny czas dodawania kolejnego elementu, Python domyślnie **alokuje przestrzeni pamięciowej znacznie na wyrost** (over-allocation). Kiedy tworzysz listę lub do niej dopisujesz obiekty, system zakłada, że w przyszłości pojawią się kolejne, rezerwując przy tym ukryte puste miejsca.
Dzięki nadmiarowej pamięci lista nie musi kopiować całej swojej zawartości za każdym razem pod nowy, dłuższy obszar w pamięci, kiedy pojawia się kolejny element.

**Przykład:** Porównanie rozmiarów
```python
import sys

my_list = [1, 2, 3]
my_tuple = (1, 2, 3)

# Lista rezerwuje dodatkową pamięć!
print(f"Lista: {sys.getsizeof(my_list)} bajtów")  # np. 88 bajtów
print(f"Krotka: {sys.getsizeof(my_tuple)} bajtów") # np. 64 bajtów
```

### Haszowalność (Hashability)

Haszowalność oznacza, że Python potrafi przypisać niezmienną unikalną wartość całkowitą (reprezentację, tzw. hasz) do wartości lub obiektu w trakcie działania całego programu. By móc wyliczyć w ten sposób hasz, zawartość tego obiektu **nigdy nie może ulec zmianie**.

Dlatego krotki, będąc *niemutowalnymi* (o ile przechowują w sobie jedynie inne niemutowalne i haszowalne obiekty, takie jak liczby całkowite, ciągi znaków itp.), mogą być pomyślnie haszowane i wyciągane bezpośrednio (O(1)) z układy tablic z haszami.
Z kolei listy są *mutowalne* i nie mają absolutnie żadnej gwarancji, co do swojej niezmiennej zawartości. To fizycznie uniemożliwia wyznaczenia dla nich trwałego hasha, i powoduje błąd `TypeError`.

**Kiedy ma to znaczenie?**
Gdy próbujemy stworzyć zbiór (set) lub definiujemy klucze dla słownika (`dict`), ponieważ te obiekty pod spodem wykorzystują właśnie funkcje i struktury haszujące:

```python
# Użyto krotki jako klucza - To zadziała!
locations = {
    (52.2297, 21.0122): "Warszawa",
    (50.0647, 19.9450): "Kraków"
}
print(locations[(52.2297, 21.0122)])  # Wynik: Warszawa

# Próba użycia mutowalnej listy jako klucza rzuci wyjątek
try:
    bad_locations = {
        [52.2297, 21.0122]: "Warszawa"
    }
except TypeError as e:
    print(f"Błąd! Wyjątek: {e}")  
    # Zwraca: unhashable type: 'list'
```

## Powiązane materiały
- [Zużycie pamięci w Pythonie](zużycie-pamięci-w-pythonie.md)
- [Typy danych w Python i zużycie pamięci](typy-danych-w-python-i-zuzycie-pamieci.md)
- [Kiedy używać dict() / list(), a kiedy {} / []](kiedy-uzywac-dict-list-a-kiedy-dict-list.md)
