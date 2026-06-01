# Struktury danych korzystające z hashowania w Pythonie i rozwiązywanie kolizji

Oprócz słownika (`dict`), który jest najbardziej znanym przykładem struktury opartej na tablicy z haszowaniem (hash table), w Pythonie istnieje kilka innych ważnych struktur, które używają tego mechanizmu. Dodatkowo, podejście Pythona do rozwiązywania kolizji jest **zupełnie inne** niż to, które znasz z języka Java.

## Jakie struktury danych korzystają z funkcji hashujących?

W Pythonie mechanizm hashowania znajdziesz w:

1. **`set` (zbiory)** – Zbiór to tak naprawdę "słownik, który ma tylko klucze (bez wartości)". Dzięki temu sprawdzenie przynależności do zbioru (`x in my_set`) ma złożoność O(1).
2. **`frozenset`** – Niezmienna (immutable) wersja zbioru. Ponieważ `frozenset` jest niezmienny, sam w sobie jest hashowalny (w przeciwieństwie do `set`), co oznacza, że może stanowić np. klucz w słowniku.
3. **Pochodne klasy `dict` z modułu `collections`**:
   - `defaultdict` – słownik, który automatycznie tworzy wartości dla nieistniejących kluczy.
   - `Counter` – zoptymalizowany słownik do zliczania elementów.
   - `OrderedDict` – słownik zachowujący kolejność (choć od Pythona 3.7 zwykły `dict` również ją gwarantuje).
4. **Przestrzeń nazw (Namespaces)** – Wewnątrz Pythona atrybuty klas, modułów czy instancji obiektów często trzymane są w specjalnych atrybutach `__dict__`, co oznacza, że cały mechanizm szukania zmiennych i metod w Pythonie opiera się pod spodem na strukturach hashujących!

---

## Jak w Pythonie rozwiązywane są konflikty hashów?

Zauważyłeś słusznie: w **Javie** (w strukturze `HashMap`) kolizje są rozwiązywane metodą **łańcuchową (Separate Chaining)**. Jeśli elementy trafiają do tego samego "kubełka", dodaje się je do listy jednokierunkowej, a od Javy 8 – gdy lista przekroczy 8 elementów – jest optymalizowana do zrównoważonego drzewa (Red-Black Tree), żeby uniknąć pesymistycznego scenariusza O(N).

**Python stosuje zupełnie inną strategię!**
Nie używa list ani drzew. Rozwiązuje konflikty za pomocą techniki **adresowania otwartego (Open Addressing)** połączonego ze zoptymalizowanym próbkowaniem. 

### Dlaczego Python nie używa list z elementami (Chaining)?

W Pythonie wszystko jest obiektem ulokowanym gdzieś w stercie (Heap), a wskaźniki do obiektów są drogie pamięciowo. Przechodzenie po liście połączonej (linked list) wymagałoby częstych skoków po różnych miejscach pamięci RAM, co bardzo niszczy **Cache L1 procesora** (tzw. cache miss). Dlatego twórcy Pythona wybrali ciągłą strukturę w pamięci.

### Adresowanie otwarte w Pythonie (Open Addressing with Pseudo-random Probing)

Jeżeli w Pythonie dochodzi do kolizji (dwa klucze mają ten sam hash wskazujący na ten sam indeks tablicy), mechanizm słownika wpisuje ten element po prostu w **następne wolne miejsce** – jednak nie w zwykłe "następne" (linear probing), bo to prowadzi do grupowania kluczy w jednym miejscu tablicy.

Python stosuje specjalny matematyczny wzór do **pseudo-losowego próbkowania**. Korzysta z pozostałych (wyższych) bitów pierwotnej wartości hasha (technika tzw. *perturbacji*).

Schemat wygląda mniej więcej tak:
1. Skomplikuj hash, żeby wyznaczyć początkowy "kubełek" (np. indeks `i`).
2. Jeśli `i` jest zajęte, a klucz jest inny (mamy kolizję!), Python generuje **kolejny indeks** `j` za pomocą wzoru korzystającego ze zmiennej zaburzającej `perturb` (przesuwanej bitowo).
3. Sprawdza indeks `j`. Jeśli wolny, wstawia tam element. Jeśli nie – liczy kolejny indeks `k`, i tak dalej.

Dzięki temu nowe elementy szybko znajdują losowe miejsce w tablicy w przypadku kolizji, a obciążenie (Load Factor) tablicy jest utrzymywane na poziomie poniżej 2/3. Kiedy zapełnienie osiągnie 66%, Python całkowicie realokuje pamięć na nową, większą tablicę, przeliczając hashe na nowo.

### Skąd Python wie, gdzie szukać klucza przy odczycie?

Algorytm wyszukiwania klucza przechodzi **dokładnie tą samą ścieżką matematyczną**, co proces wstawiania. Ponieważ generowanie pseudolosowych indeksów (`j`, `k` itd.) za pomocą wzoru perturbacji jest w pełni deterministyczne (zawsze dla tego samego hasha da ten sam ciąg kolejnych indeksów), Python postępuje następująco:
1. Oblicza z hasha początkowy indeks `i`.
2. Sprawdza "kubełek" `i`:
   - Jeśli jest **pusty**, to od razu wie, że klucza w ogóle **nie ma w słowniku** (`KeyError` lub rzucenie domyślnej wartości).
   - Jeśli jest **zajęty**, Python sprawdza dwie rzeczy: czy zgadza się hash ORAZ czy zgadza się wartość samego klucza (czyli wykonuje zwykłe porównanie `==`).
   - Jeśli tak, odnalazł właściwy element - zwraca go.
   - Jeśli to inny klucz (czyli w tym miejscu w przeszłości wydarzyła się kolizja dla tego indeksu), to przechodzi do punktu 3.
3. Python wrzuca pierwotny hash do **tego samego wzoru matematycznego**, którego używa przy wstawianiu, i wylicza kolejny indeks `j`.
4. Sprawdza indeks `j` – i znów powtarza proces: pusty? (nie ma elementu), ten sam klucz? (mamy go!), inny klucz? (policz indeks `k` i szukaj dalej).

Dzięki temu Python nie musi nigdzie specjalnie "zapamiętywać" drogi od `i` do `j`. Oblicza ją po prostu na nowo "w locie" w trakcie odczytywania.

---

## Podsumowanie - słowniki w Pythonie od wersji 3.6+

Dodatkowym interesującym aspektem jest rewolucja pamięciowa wprowadzona w Pythonie 3.6 (skopiowana z PyPy).
Struktura słownika została podzielona na dwie tablice, by zaoszczędzić miejsce:
1. **Rzadką tablicę z indeksami** (Sparse Array) - bardzo mała tablica, przechowująca tylko typ zmiennych całkowitych. Tu szukany jest hash i znajduje się tylko liczba kierująca do właściwej tablicy. Zastosowane jest tutaj adresowanie otwarte opisane wyżej.
2. **Gęstą tablicę klucz-wartość** (Dense Array) - tu dane układane są po kolei jedno za drugim bez wolnych przestrzeni między nimi. Zapewnia to dodatkowo właściwość "zapamiętywania kolejności wstawiania elementów".

W efekcie zapytanie O(1) w Pythonie jest niesamowicie szybkie z perspektywy cache'owania procesora, a użycie pamięci jest mniejsze o około 20-25% w stosunku do Pythona starszego niż 3.6. Nigdy nie dojdzie tu do transformacji w drzewo jak ma to miejsce w Javie.
