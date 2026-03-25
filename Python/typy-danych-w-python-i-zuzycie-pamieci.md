# Typy danych w Pythonie i ich zużycie pamięci

## Krótkie podsumowanie
W Pythonie (a dokładniej w dominującej implementacji CPython) absolutnie wszystko jest obiektem. Z tego powodu typy proste znane z innych języków (jak `int` czy `float` w Javie/C++) mają tutaj znacznie większy narzut pamięciowy. Nawet "pusta" zmienna niesie ze sobą dodatkowe informacje, takie jak typ obiektu czy licznik referencji, z których korzysta Garbage Collector.

## Dlaczego to ma znaczenie?
Zrozumienie, ile pamięci zużywają poszczególne struktury danych w Pythonie, jest kluczowe, gdy pracujemy z bardzo dużymi zbiorami danych (np. Data Science, Machine Learning, przetwarzanie wielkich plików). Wybór odpowiedniej struktury (np. `tuple` zamiast `list`, tablice z NumPy zamiast zwykłych list, czy generatory w miejsce trzymania całości w pamięci) może uchronić nas przed wyczerpaniem pamięci operacyjnej (OOM) oraz znacząco przyspieszyć działanie programu z uwagi na lepsze wykorzystanie pamięci podręcznej procesora (CPU cache).

## Zużycie pamięci przez wbudowane typy danych
Poniższe wartości pochodzą z architektury 64-bitowej w standardowej implementacji CPython (wersja >= 3.0), można je samodzielnie sprawdzić używając funkcji `sys.getsizeof()`.

Wartością powtarzającą się w Pythonie jest narzut wynoszący zazwyczaj minimum kilkadziesiąt bajtów u zarania każdego obiektu:

### 1. Liczby całkowite (`int`)
W Pythonie (w przeciwieństwie np. do Java/C++, gdzie `int` to niemal zawsze 4 lub 8 bajtów) typ `int` ma nieograniczoną precyzję, więc jego rozmiar rośnie wraz z wielkością liczby.
* **0** – `24 bajty` (lub 28 bajtów zależnie od dokładnej wersji Pythona 3).
* Zwykle zajęcie pamięci dla `int` startuje od **28 bajtów** (w nowszych wersjach) i rośnie o 4 bajty na każdą dodatkową "cyfrę" w 32-bitowym systemie liczbowym używanym wewnętrznie.

### 2. Typ zmiennoprzecinkowy (`float`)
W Pythonie liczby `float` są oparte na typie `double` z języka C (standard IEEE 754, 64-bit).
* **Float** zajmuje ustandaryzowane **24 bajty** niezależnie od wartości.

### 3. Typ logiczny (`bool`)
W Pythonie klasa `bool` dziedziczy wprost po dynamicznie rosnącym typie całkowitoliczbowym `int`. Istnieją tylko dwa wbudowane singletony: `True` (traktowane pod spodem jako `1`) i `False` (traktowane jako `0`).

Dlaczego `bool` zajmuje 24/28 bajtów, skoro logicznie wystarczyłby mu zaledwie 1 bit informacji?
Ten potężny rozmiar wynika z tego, jak zbudowany jest język u jego rdzenia (w CPythonie, napisanym w C). Każda wartość to tam pełnoprawna struktura C (konkretnie `PyLongObject` odziedziczona po typie `int`). Pod spodem każdy obiekt – by w ogóle móc uczestniczyć w ekosystemie Pythona – wymaga w nagłówku na start następujących pól ułożonych w pamięci:
1. **Licznik referencji (`ob_refcnt`)** – 8 bajtów (na 64-bitowych platformach). Służy do śledzenia ilości referencji odwołujących się do danego obiektu, co jest podstawą działania Garbage Collectora. Kiedy wartość licznika spada do zera, pamięć uwalniana jest zwrotnie do systemu.
2. **Wskaźnik na typ obiektu (`ob_type`)** – 8 bajtów. CPython używa go, by język wiedział w locie, w jaki sposób zinterpretować obiekt (w tym wypadku, że jest to klasa `bool`). Skoro w Pythonie wszystkie zmienne mogą zmieniać swój typ, typ trzymany jest na poziomie samych danych.
3. **Rozmiar tablicy elementów wartości (`ob_size`)** – 8 bajtów. Tę warstwę `bool` dziedziczy po zmiennym `int` posiadającym nieskończoną precyzję, ponieważ rozmiar wartości definiowany jest tu specjalną wielką tablicą skompresowanych cyfr rzutowanych w C.

Samo posiadanie tych 3 nagłówków wymusza z góry minimum **24 bajty stałego narzutu**.
Na samo trzymanie wartości w klasie `int` (po której dziedziczy `bool`) CPython alokuje specjalne bloki liczbowe ("digits").

Z historycznego punktu widzenia obiekt "0" nie miał alokowanych tych bloków, stąd we wczesnych wersjach Pythona zajmował tylko te 24 bajty. Jednak w każdym współczesnym wydaniu Pythona ujednolicono ten zarys o **4 bajty** wyrównania dla obu wartości logicznych traktując najmniejszą możliwą wartość równą jednej "cyfrze".

Z tego właśnie powodu zarówno układ dla `True` (oznaczający logiczne `1`), jak i układ dla `False` (oznaczający `0`) po wliczeniu bazowego narzutu z nagłówka i pamięci pod najmniejszą wartość dają ostatecznie mityczny, ujednolicony dla obu singletonów układ rozmiarowy sięgający **28 bajtów**.

### 4. Tekst (`str`)
Zajętość pamięci przez łańcuchy znaków bywa skomplikowana ("Flexible String Representation" zdefiniowana w PEP 393).
* **Pusty ciąg (Empty String)**: zazwyczaj **49 bajtów**.
* Jeśli ciąg składa się tylko ze znaków ASCII (1 bajt na znak), do 49 bazowych dochodzi 1 bajt za każdy wymiar wielkości znaków.
* Gdy łańcuch używa znaków nie-ASCII (np. Emoji, rzadsze alfabety), Python może rozszerzyć kodowanie na 2 lub 4 bajty na znak dla CAŁEGO ciągu, co potęguje zużycie pamięci. 

### 5. Lista (`list`)
Typowa lista to ulepszona tablica wskaźników (ang. *dynamic array*).
* **Pusta lista**: **56 bajtów** narzutu obiektu.
* Rozmiar rośnie o **8 bajtów** dla każdego referowanego elementu (ponieważ są to tylko wskaźniki na właściwe obiekty; każdy umieszczony w liście int, float itp. wciąż zużywa własną pamięć oddzielnie).

### 6. Krotka (`tuple`)
Odpowiednik nieedytowalnej listy. Niezmienna, nie powiększa swojej puli w locie.
* **Pusta krotka**: około **40 bajtów**.
* Narzut jest mniejszy, a dodatkowo 8 bajtów na każdy wskaźnik do elementu. Gdy wielkość jest z góry znana, tworzenie krotki jest dużo tańsze od listy. 

### 7. Słownik (`dict`) i Zbiór (`set`)
Oparte na tablicach z haszowaniem (hash table). Oferują czas wyszukiwania O(1), lecz kosztem wysokiego narzutu narzuconego na wewnętrzne alokowanie ułożenia z rezerwą.
* **Pusty `dict`**: minimalnie wynosi ok. **232 bajtów**, w miare dodawania nowych kluczy alokuje nowe wskaźniki podnosząc zajętość z wyprzedzeniem.
* **Pusty `set`**: analogicznie, ok. **216 bajtów**.
Pamiętajmy również że klucz i wartość dodawana to oddzielne byty – same słowniki jedynie je grupują.

### 8. Pusty obiekt (`NoneType`)
* Obiekt `None` istnieje jako pojedyncza instancja w cyklu życia programu – jego rozmiar to **16 bajtów**.

## Czy to znaczy, że Python jest bardzo pamięciożerny w porównaniu np. do Javy?
Tak, u swego rdzenia standardowy Python (CPython) zużywa wielokrotnie więcej pamięci operacyjnej na te same dane niż języki kompilowane statycznie takie jak Java, C\# czy C++. Ze względu na naturę języka "wszystko jest obiektem", elastyczność programowania odbija się na narzutach:

1. **Brak typów prostych (primitives):** W Javie zwykły `int` (wymodelowany bez klasy-wrappera `Integer`) czy `boolean` zajmują minimalną możliwą przestrzeń. `int` z definicji pochłonie w RAM równo ustandaryzowane 4 bajty, natomiast `boolean` zajmie najczęściej 1 bajt i dodatkowo potrafi być optymalizowany przez procesor w tabelach. W Pythonie za to każda, nawet najbardziej nieznacząca wartość jak `False` czy 0 wymusza na maszynie wirtualnej skonstruowanie kompletnej nowej instrukcji instancji obiektu klasy C (posiadającego chociażby opisany wyżej 24-bajtowy dzwon nagłówka obiektu).
2. **Kolekcje to same wskaźniki na masę innych obiektów:** Kiedy w Javie powołamy do życia tablicę domyślnych typów `int[1000]`, JVM wykroi ze sterty jednolity, nierozłączny blok wielkości lekko ponad zaledwie `4 kB` (1000 wymnożone na 4 bajty przestrzeni). Gdy zrobimy to w Pythonie: `lista = [0] * 1000`, nasza struktura zażąda w pierwszej kolejności pamięci na wskaźniki (8 bajtów do każdego elementu), po czym każdy jeden indeks w tablicy będzie powiązywał nowy ułożony wielki 28-bajtowy "intowy" obiekt `0` na stercie w C. Ten jeden mały zabieg podbija zużycie pamięci dla tysiąca małych zer w Pythonie do prawie `36 kB`!
3. **Elastyczność atrybutów kosztuje:** Większość klas opartych na instancjach, powoływana do działania w ogólnym kodzie przez programistę w Pythonie buduje się wokół ukrytego atrybutu o strukturze słownika. Słowniki (`__dict__`) same narzucają potężny haszujący podkład pamięci by czas dostępu stał w przedziale `O(1)`. Rozmywa to kontrolę nad zawirowaniami przestrzeni i pamięci operacyjnej dla silników.

**Jak radzi sobie z tym dzisiejszy Python?**
W miejscach ciężkich inżynieryjnie oraz systemach Data Science eksperci używają dedykowanych bibliotek z potężnym kompilowanym wsparciem u samych podstaw. Dominującym zbawicielem stał się ekosystem **NumPy** oraz *pandas*. Dzięki `numpy.ndarray` tworzone masowo typy zachowują się jak w niższym języku C – możemy wymusić kolekcję tysięcy trzymanych twardo cyfr `np.int8` lub statycznych `np.float32`, które będą ułożone w pamięci perfekcyjnie płasko w idealnych wymiarach (kolejno 1 oraz 4 bajty za element), kompletnie wymijając pamięciożerny problem bazowego elastycznego standardu CPythona. Oszczędność powraca tam do rozmiarów z systemów Javy czy C.

## Jak sprawdzić zużycie? (Przykład w kodzie)

Aby sprawdzić zużycie pamięci przez dany typ w swoim środowisku, wystarczy zaimportować moduł `sys` i wywołać `sys.getsizeof()`:

```python
import sys

# Typy proste
print(sys.getsizeof(0))         # int: ~24/28 bajtów
print(sys.getsizeof(0.0))       # float: 24 bajty
print(sys.getsizeof(True))      # bool: 28 bajtów
print(sys.getsizeof(""))        # str (pusty): ~49 bajtów

# Struktury danych (kolekcje)
krotka = ()
lista = []
zbior = set()
slownik = {}

print(sys.getsizeof(krotka))    # tuple: 40 bajtów
print(sys.getsizeof(lista))     # list: 56 bajtów
print(sys.getsizeof(zbior))     # set: 216 bajtów
print(sys.getsizeof(slownik))   # dict: 232 bajtów
```

## Podobne pliki
- [[zużycie-pamięci-w-pythonie]]
- [[python-jako-język-interpretowany]]
