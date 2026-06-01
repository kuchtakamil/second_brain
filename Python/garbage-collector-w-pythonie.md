# Garbage Collector w Pythonie

> **Kontekst:** Czytelnik zna już GC z perspektywy Javy (generacje young/old, rodzaje kolektorów G1/ZGC/Shenandoah, stop-the-world, reachability przez GC roots). Celem jest wyjaśnienie, jak zarządzanie pamięcią i odśmiecanie działa w Pythonie (CPython) — z porównaniem do znanych już koncepcji z JVM.

---

## 1. Architektura zarządzania pamięcią w CPython — przegląd

W Pythonie trzeba od razu rozdzielić dwie rzeczy:

1. **język Python** jako specyfikację,
2. **CPython** jako najpopularniejszą implementację interpretera.

Ten rozdział dotyczy głównie CPythona, bo to właśnie on ma klasyczny model: **reference counting + cykliczny garbage collector**. Inne implementacje, takie jak PyPy czy Jython, mogą zarządzać pamięcią inaczej.

W CPythonie obiekty żyją na prywatnej stercie zarządzanej przez interpreter. Programista nie wywołuje `malloc()` ani `free()` bezpośrednio, nawet jeśli wewnętrznie interpreter korzysta z alokatorów pamięci. Z perspektywy kodu Pythona wygląda to podobnie jak w Javie: tworzysz obiekt, używasz go, a runtime decyduje, kiedy odzyskać pamięć.

Różnica względem JVM jest jednak fundamentalna. W Javie głównym mechanizmem zwalniania pamięci jest **tracing garbage collector**, który okresowo analizuje graf obiektów zaczynając od GC roots. W CPythonie podstawowy mechanizm jest prostszy i bardziej lokalny: każdy obiekt ma licznik referencji. Jeśli licznik spadnie do zera, obiekt może zostać zwolniony natychmiast.

### Prywatna sterta CPythona

CPython ma własny system zarządzania pamięcią dla obiektów Pythona. Oznacza to, że pamięć może zostać zwolniona z punktu widzenia obiektu Pythona, ale niekoniecznie natychmiast wróci do systemu operacyjnego. Interpreter często trzyma już przydzielone fragmenty pamięci, żeby szybciej obsłużyć kolejne alokacje. Źródło: [Python/C API — Memory Management](https://docs.python.org/3/c-api/memory.html).

To jest podobne do JVM w tym sensie, że runtime zarządza dużym obszarem pamięci i nie oddaje każdej drobnej alokacji natychmiast do systemu. Różnica polega na tym, że w CPythonie dużo decyzji o życiu obiektu wynika z licznika referencji, a nie z globalnego przejścia GC po stercie.

### `pymalloc`: areny, poole i bloki

Dla małych obiektów CPython używa specjalizowanego alokatora nazywanego zwykle `pymalloc`. Jego zadaniem jest szybkie przydzielanie małych kawałków pamięci, bo programy w Pythonie tworzą ogromną liczbę niewielkich obiektów: liczb, krotek, słowników, ramek wywołań, iteratorów itd. Źródło: [Python/C API — The pymalloc allocator](https://docs.python.org/3/c-api/memory.html#the-pymalloc-allocator).

Uproszczony model wygląda tak:

```text
arena
  └── pool
        └── block
```

- **Arena** to większy obszar pamięci pobrany od systemu operacyjnego.
- **Pool** to fragment areny przeznaczony dla bloków określonego rozmiaru.
- **Block** to mały kawałek pamięci, w którym może zostać umieszczony konkretny obiekt lub jego część.

Dzięki temu CPython nie musi pytać systemu operacyjnego o pamięć przy każdej małej alokacji. Może ponownie używać bloków, pooli i aren. To poprawia wydajność, ale ma ważną konsekwencję praktyczną: po zwolnieniu obiektów zużycie pamięci procesu widoczne w narzędziach systemowych nie zawsze natychmiast spada.

W JVM analogiczną warstwą byłaby sterta zarządzana przez JVM oraz mechanizmy alokacji w Eden/Young Generation. Ale JVM zwykle organizuje pamięć pod potrzeby tracing GC, kopiowania obiektów, kompaktowania i pracy konkretnych kolektorów. CPython organizuje pamięć głównie pod szybkie tworzenie i niszczenie obiektów, a nie pod przesuwanie ich po stercie.

### Obiekty Pythona jako struktury C

W CPythonie każdy obiekt Pythona jest strukturą w C. Na bardzo wysokim poziomie każdy obiekt zawiera m.in.:

- licznik referencji,
- wskaźnik na typ obiektu,
- dane właściwe dla danego typu.

Dlatego nawet prosta liczba całkowita w Pythonie nie jest "gołym intem" znanym z Javy czy C. Jest pełnoprawnym obiektem CPythona. To daje elastyczność modelu "wszystko jest obiektem", ale ma koszt pamięciowy i wydajnościowy.

Przykład:

```python
x = 42
```

W CPythonie zmienna `x` nie przechowuje bezpośrednio surowej wartości `42` tak jak lokalna zmienna typu `int` w Javie. `x` jest nazwą wskazującą na obiekt reprezentujący liczbę całkowitą.

To ważne dla zrozumienia garbage collectora: Python nie musi śledzić "zmiennych" w takim sensie jak początkujący często to sobie wyobrażają. Runtime śledzi obiekty i referencje między nimi.

---

## 2. Reference Counting — podstawowy mechanizm (brak odpowiednika w Javie)

Reference counting to podstawowy mechanizm zarządzania czasem życia obiektów w CPythonie. Każdy obiekt ma licznik mówiący, ile aktywnych referencji do niego istnieje.

Jeśli licznik referencji rośnie, obiekt jest nadal potrzebny. Jeśli licznik spada do zera, CPython wie, że z poziomu programu nie ma już jak dostać się do tego obiektu. Może więc natychmiast uruchomić procedurę niszczenia obiektu i zwolnić jego pamięć albo oddać ją do wewnętrznego alokatora.

W uproszczeniu:

```python
user = {"name": "Ala"}  # powstaje obiekt dict, licznik referencji rośnie
same_user = user        # drugi alias do tego samego obiektu

del user                # licznik referencji spada, ale obiekt nadal żyje
del same_user           # licznik spada do 0, obiekt może zostać zniszczony
```

`del` nie "usuwa obiektu" bezpośrednio. `del` usuwa nazwę albo referencję. Dopiero jeśli była to ostatnia referencja, obiekt może zostać zwolniony.

### `ob_refcnt` w `PyObject`

W CPythonie licznik referencji jest częścią struktury obiektu. W dokumentacji i kodzie CPythona spotkasz nazwę `ob_refcnt`. To pole jest zwiększane i zmniejszane przez interpreter oraz rozszerzenia C, gdy pojawiają się lub znikają referencje. Źródło: [Python/C API — Reference Counting](https://docs.python.org/3/c-api/refcounting.html).

Przykład sytuacji, które zwiększają licznik referencji:

- przypisanie obiektu do kolejnej zmiennej,
- włożenie obiektu do listy, słownika, zbioru albo krotki,
- przekazanie obiektu jako argumentu funkcji,
- utrzymywanie obiektu przez domknięcie, generator, wyjątek albo cache.

Przykład sytuacji, które zmniejszają licznik referencji:

- wyjście z funkcji i zniszczenie jej lokalnych nazw,
- nadpisanie zmiennej innym obiektem,
- usunięcie elementu z kontenera,
- wykonanie `del`,
- zniszczenie kontenera, który trzymał referencje do innych obiektów.

### `sys.getrefcount()`

Licznik referencji można podejrzeć funkcją `sys.getrefcount()` ([dokumentacja `sys.getrefcount`](https://docs.python.org/3/library/sys.html#sys.getrefcount)):

```python
import sys

items = []

print(sys.getrefcount(items))
```

Wynik bywa zaskakujący, bo samo przekazanie obiektu do `sys.getrefcount()` tworzy tymczasową dodatkową referencję. Dlatego funkcja zwykle pokazuje wartość o 1 większą niż intuicyjnie oczekujesz.

Przykład:

```python
import sys

a = []
b = a

print(sys.getrefcount(a))  # obejmuje też tymczasową referencję argumentu funkcji
```

Ta funkcja jest dobra do demonstracji mechanizmu, ale w normalnym kodzie aplikacyjnym prawie nigdy nie powinno się opierać logiki na konkretnych wartościach refcounta.

### Czym to się różni od Javy?

Java nie używa reference countingu jako głównego mechanizmu zwalniania obiektów. JVM nie niszczy obiektu natychmiast tylko dlatego, że ostatnia lokalna zmienna przestała na niego wskazywać. Zamiast tego obiekt zostaje kiedyś uznany za nieosiągalny podczas pracy garbage collectora.

W Javie myślisz głównie tak:

> Czy obiekt jest osiągalny z GC roots?

W CPythonie podstawowe pytanie brzmi:

> Czy licznik referencji obiektu spadł do zera?

Dopiero drugi mechanizm, cykliczny GC, zajmuje się przypadkami, w których sam reference counting nie wystarcza.

### Zalety reference countingu

Największą zaletą jest deterministyczne zwalnianie wielu obiektów. Gdy ostatnia referencja znika, obiekt jest zwykle niszczony od razu.

To szczególnie ważne przy obiektach opakowujących zasoby systemowe:

- pliki,
- sockety,
- uchwyty systemowe,
- połączenia,
- bufory.

Przykład:

```python
f = open("data.txt")
data = f.read()
del f
```

W CPythonie usunięcie ostatniej referencji do obiektu pliku zwykle szybko zamknie plik. Ale nie należy na tym polegać jako na stylu programowania. Poprawnym idiomem jest context manager:

```python
with open("data.txt") as f:
    data = f.read()
```

`with` działa jawnie i przenośnie między implementacjami Pythona. Reference counting jest szczegółem CPythona, nie gwarancją całego języka Python.

### Wady reference countingu

Największa wada jest klasyczna: reference counting sam z siebie nie radzi sobie z cyklami.

Jeśli obiekt A wskazuje na B, a B wskazuje na A, to oba obiekty mogą mieć dodatni licznik referencji nawet wtedy, gdy program nie ma już żadnej zewnętrznej referencji do tego cyklu. Dla samego refcountingu te obiekty wyglądają na żywe, bo "ktoś" nadal na nie wskazuje. Problem w tym, że wskazują tylko na siebie nawzajem.

---

## 3. Problem cyklicznych referencji

Cykl referencji powstaje wtedy, gdy obiekty wskazują na siebie w taki sposób, że tworzą zamkniętą pętlę.

Najprostszy schemat:

```text
A -> B -> A
```

Albo dłuższy:

```text
A -> B -> C -> A
```

Z perspektywy programu taki cykl może być już całkowicie nieosiągalny. Problem polega na tym, że każdy obiekt w cyklu nadal ma dodatni licznik referencji, bo jest referowany przez inny obiekt z tego samego cyklu.

### Lista referująca samą siebie

Najprostszy przykład w Pythonie:

```python
items = []
items.append(items)

print(items)
```

Powstaje lista, której pierwszym elementem jest ona sama. Python pokaże to mniej więcej tak:

```text
[[...]]
```

Jeśli teraz usuniemy nazwę `items`, znika zewnętrzna referencja:

```python
del items
```

Ale sama lista nadal zawiera referencję do samej siebie. Jej licznik referencji nie musi spaść do zera tylko dzięki reference countingowi.

Właśnie dlatego CPython potrzebuje dodatkowego mechanizmu: cyklicznego garbage collectora.

### Dwa obiekty referujące się wzajemnie

Bardziej realistyczny przykład:

```python
class Parent:
    def __init__(self):
        self.child = None


class Child:
    def __init__(self):
        self.parent = None


parent = Parent()
child = Child()

parent.child = child
child.parent = parent
```

Graf wygląda tak:

```text
parent -> child
child  -> parent
```

Dopóki zmienne `parent` i `child` istnieją, wszystko jest normalne. Problem zaczyna się wtedy, gdy usuwamy zewnętrzne referencje:

```python
del parent
del child
```

Obiekty mogą być już nieosiągalne z kodu programu, ale nadal wskazują na siebie nawzajem.

### Dlaczego Java nie ma tego problemu jako osobnej kategorii?

W Javie cykl sam w sobie nie jest problemem. Tracing GC zaczyna od GC roots, czyli m.in. stosów wątków, zmiennych statycznych, aktywnych ramek wywołań i referencji z JNI. Następnie przechodzi po grafie obiektów.

Jeżeli cykl nie jest osiągalny z żadnego GC root, cały cykl jest martwy.

Przykład:

```text
GC roots
   |
   v
  X

A -> B -> A   # nieosiągalny cykl
```

Dla tracing GC obiekty A i B są śmieciami, bo nie da się do nich dojść od korzeni. Nie ma znaczenia, że referują się nawzajem.

W CPythonie sprawa jest bardziej złożona, bo podstawowy mechanizm, czyli reference counting, patrzy lokalnie na liczby referencji. Dlatego cykle są obsługiwane przez dodatkowy, okresowo uruchamiany GC.

### Cykle nie zawsze są błędem

Warto podkreślić: cykliczne referencje nie są automatycznie błędem projektowym. Struktury grafowe, drzewa z referencją do rodzica, obiekty domenowe z relacjami dwukierunkowymi albo cache mogą naturalnie tworzyć cykle.

Problemem stają się wtedy, gdy:

- cykl nie jest już potrzebny,
- nadal trzyma dużo pamięci,
- zawiera obiekty z kosztownymi zasobami,
- program przypadkowo utrzymuje zewnętrzną referencję, np. przez globalny cache, callback albo domknięcie.

---

## 4. Generacyjny Garbage Collector (moduł `gc`)

Cykliczny garbage collector w CPythonie jest dostępny przez moduł `gc`. Jego zadaniem nie jest zastąpienie reference countingu. On go uzupełnia. Źródło: [Python docs — `gc`](https://docs.python.org/3/library/gc.html).

Najważniejsza zasada:

> Reference counting zwalnia większość obiektów natychmiast, a moduł `gc` szuka cykli referencji, których reference counting sam nie potrafi usunąć.

To oznacza, że wyłączenie cyklicznego GC przez `gc.disable()` nie wyłącza reference countingu. Obiekty bez cykli nadal będą zwalniane, gdy ich licznik referencji spadnie do zera.

### Generacje w CPythonie

Historycznie CPython opisywano jako mający trzy generacje:

- generacja 0,
- generacja 1,
- generacja 2.

W starszych wersjach i w wielu artykułach nadal zobaczysz taki opis. Od Pythona 3.14 model widoczny w API został uproszczony: są obiekty młode i stare, a `generation=1` nie oznacza osobnej pełnej generacji z własnymi obiektami, tylko inkrementalną kolekcję starej generacji. `gc.get_objects(1)` zwraca pustą listę, bo generacja 1 nie przechowuje już obiektów. Źródło: [Python docs — `gc.get_objects()` i zmiany w 3.14](https://docs.python.org/3/library/gc.html#gc.get_objects).

Praktycznie warto więc myśleć tak:

- **young generation**: nowe obiekty, sprawdzane często,
- **old generation**: obiekty, które przeżyły kolekcję, sprawdzane rzadziej i częściowo.

To nadal jest podejście generacyjne, tylko szczegóły implementacyjne zmieniły się względem starszych opisów.

### Hipoteza generacyjna

CPython, podobnie jak JVM, korzysta z hipotezy generacyjnej:

> Większość obiektów żyje krótko.

Przykłady krótkotrwałych obiektów:

- lokalne listy pomocnicze,
- tymczasowe krotki,
- obiekty tworzone podczas parsowania danych,
- ramki i struktury pomocnicze,
- wyniki pośrednie wyrażeń.

Zamiast skanować za każdym razem wszystkie obiekty śledzone przez GC, interpreter częściej sprawdza młode obiekty. Jeśli obiekt przetrwa kolekcję, może trafić do starej generacji i być sprawdzany rzadziej.

To przypomina JVM:

```text
Java:    Eden -> Survivor -> Old
CPython: young -> old
```

Analogia jest użyteczna, ale nie idealna. JVM może kopiować i kompaktować obiekty między obszarami pamięci. CPython nie działa w ten sam sposób. Tu "promocja" dotyczy głównie klasyfikacji obiektu w strukturach GC, a niekoniecznie fizycznego przeniesienia obiektu w pamięci.

### Kiedy GC się uruchamia?

Progi można podejrzeć tak:

```python
import gc

print(gc.get_threshold())
print(gc.get_count())
```

`gc.get_threshold()` zwraca progi sterujące częstotliwością kolekcji. `gc.get_count()` pokazuje bieżące liczniki alokacji i dealokacji używane przez GC.

W uproszczeniu CPython patrzy na różnicę między liczbą alokacji i dealokacji od ostatniej kolekcji. Gdy ta różnica przekroczy próg `threshold0`, uruchamiana jest kolekcja młodej generacji.

Przykład:

```python
import gc

print(gc.get_threshold())  # np. (700, 10, 0) w nowszych wersjach
```

Znaczenie progów zależy od wersji Pythona. W Pythonie 3.14+ `threshold2` jest ignorowany, a `threshold1` wpływa na to, jaka część starej generacji jest skanowana podczas kolekcji. Im większy `threshold1`, tym wolniej skanowana jest stara generacja. Źródło: [Python docs — `gc.set_threshold()`](https://docs.python.org/3/library/gc.html#gc.set_threshold).

To jest dużo prostszy model tuningu niż w JVM. W Javie możesz dobrać kolektor, rozmiary generacji, limity pauz, regiony, tryby concurrent GC i wiele flag `-XX`. W Pythonie zwykle zostawia się domyślne ustawienia, a modułu `gc` używa się głównie diagnostycznie.

### Co właściwie robi cykliczny GC?

Cykliczny GC w CPythonie nie jest klasycznym odpowiednikiem mark-and-sweep z Javy. Jego głównym zadaniem jest wykrywanie nieosiągalnych cykli wśród obiektów śledzonych przez GC. Źródło: [CPython InternalDocs — Garbage collector design](https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md).

GC interesuje się przede wszystkim **obiektami kontenerowymi**, czyli takimi, które mogą trzymać referencje do innych obiektów:

- listy,
- słowniki,
- zbiory,
- krotki zawierające obiekty śledzone,
- instancje klas,
- inne obiekty rozszerzeń, jeśli wspierają protokół GC.

Proste obiekty, które nie mogą tworzyć cykli, nie muszą być śledzone przez cykliczny GC.

Można to sprawdzić:

```python
import gc

print(gc.is_tracked(123))
print(gc.is_tracked([]))
print(gc.is_tracked({}))
```

Wyniki mogą zależeć od wersji i optymalizacji, ale ogólna zasada zostaje: GC cykliczny skupia się na obiektach, które mogą być częścią cyklu.

### Ręczne uruchomienie kolekcji

Kolekcję można wymusić:

```python
import gc

collected = gc.collect()
print(collected)
```

To jest luźny odpowiednik `System.gc()` z Javy, ale z podobnym zastrzeżeniem: w normalnym kodzie biznesowym nie powinno się regularnie ręcznie wymuszać GC bez konkretnego powodu. Ręczne `gc.collect()` bywa przydatne w testach, diagnostyce, benchmarkach albo po kontrolowanym usunięciu bardzo dużych grafów obiektów.

### Jak obiekt "starzeje się" w CPythonie?

Nowy obiekt śledzony przez GC trafia do młodej generacji. Jeśli podczas kolekcji nadal jest potrzebny, czyli jest osiągalny albo nie należy do nieosiągalnego cyklu, przeżywa kolekcję. Obiekty, które przeżywają, są traktowane jako starsze i sprawdzane rzadziej.

To opiera się na tej samej intuicji co generacje w JVM: jeżeli obiekt już trochę żyje, statystycznie może żyć jeszcze dłużej. Nie warto więc sprawdzać go tak często jak świeżo utworzonych obiektów.

Najważniejsza różnica:

- w JVM generacyjny GC jest centralnym mechanizmem odzyskiwania pamięci,
- w CPythonie generacyjny GC jest dodatkiem do reference countingu i skupia się na cyklach.

---

## 5. Algorytm wykrywania cykli w CPython

CPythonowy cycle detector działa na innym poziomie niż większość kolektorów JVM. Nie próbuje regularnie analizować całej sterty w celu znalezienia wszystkich żywych obiektów. Interesuje go wybrany zbiór obiektów śledzonych przez GC, głównie kontenery, które mogą tworzyć cykle.

Techniczne źródła do tego rozdziału: [CPython InternalDocs — Garbage collector design](https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md) oraz [Python/C API — Supporting Cyclic Garbage Collection](https://docs.python.org/3/c-api/gcsupport.html).

### Tylko obiekty kontenerowe są istotne

Cykl może powstać tylko wtedy, gdy obiekt potrafi trzymać referencje do innych obiektów. `int`, `float`, prosty `str` albo `None` nie utworzą cyklu samodzielnie, bo nie zawierają referencji do innych obiektów Pythona w sensie widocznym dla GC.

Przykładowe obiekty, które mogą być śledzone:

- `list`,
- `dict`,
- `set`,
- instancje klas,
- krotki zawierające śledzone obiekty,
- obiekty rozszerzeń C, jeśli implementują obsługę cyklicznego GC.

Można to sprawdzić:

```python
import gc

print(gc.is_tracked(1))
print(gc.is_tracked("abc"))
print(gc.is_tracked([]))
print(gc.is_tracked({"x": []}))
```

Nie należy jednak budować logiki biznesowej na dokładnych wynikach `gc.is_tracked()`, bo CPython wykonuje optymalizacje zależne od typu i wersji.

### `tp_traverse`

Żeby obiekt mógł uczestniczyć w cyklicznym GC, jego typ musi umieć pokazać GC, do jakich innych obiektów trzyma referencje. W C API robi się to przez slot `tp_traverse`.

Intuicyjnie `tp_traverse` odpowiada na pytanie:

> Jakie inne obiekty są osiągalne bezpośrednio z tego obiektu?

Dla listy odpowiedzią są jej elementy. Dla instancji klasy będą to m.in. wartości atrybutów przechowywane w `__dict__` albo slotach. Dla słownika będą to klucze i wartości.

Bez takiego mechanizmu GC nie umiałby przejść po grafie referencji obiektów kontenerowych.

### `tp_clear`

Samo wykrycie cyklu nie wystarczy. Trzeba jeszcze przerwać referencje wewnątrz nieosiągalnego cyklu, żeby refcounty mogły spaść do zera. Do tego służy slot `tp_clear`.

Intuicyjnie `tp_clear` odpowiada na pytanie:

> Które referencje trzymane przez ten obiekt można wyczyścić, żeby rozbić cykl?

To jest delikatny etap, bo czyszczenie referencji zmienia stan obiektów. Dlatego obsługa finalizatorów, resurrection i kolejność czyszczenia miały historycznie dużo ostrych krawędzi.

### Jak wygląda detekcja

Uproszczony obraz algorytmu:

1. GC bierze zbiór obiektów z wybranej generacji.
2. Dla każdego obiektu kopiuje jego licznik referencji do roboczego pola używanego przez GC.
3. Przechodzi po referencjach wewnątrz analizowanego zbioru i odejmuje referencje pochodzące z tego samego zbioru.
4. Obiekty, które nadal mają dodatni roboczy licznik, są osiągalne z zewnątrz analizowanego zbioru.
5. Obiekty osiągalne z zewnątrz są traktowane jako żywe.
6. Pozostałe obiekty są kandydatami na nieosiągalny cykl.
7. Dla nieosiągalnych obiektów GC uruchamia finalizację i/lub czyszczenie referencji.

Kluczowa intuicja: GC próbuje odróżnić referencje "wewnętrzne", czyli takie, które obiekty z cyklu trzymają między sobą, od referencji "zewnętrznych", które dowodzą, że obiekt nadal jest dostępny dla programu.

Przykład:

```text
root -> A -> B -> A
```

Tutaj cykl `A <-> B` jest żywy, bo istnieje referencja z zewnątrz: `root -> A`.

Inny przypadek:

```text
A -> B -> A
```

Jeśli nie ma żadnej referencji z zewnątrz, para `A`, `B` jest cyklicznym śmieciem. Reference counting sam tego nie zobaczy, ale cycle detector może.

### Różnica względem tracing GC w JVM

JVM zwykle wychodzi od GC roots i oznacza obiekty osiągalne. To klasyczna perspektywa:

```text
roots -> reachable objects
```

CPythonowy cycle detector patrzy bardziej lokalnie:

```text
tracked containers in a generation -> internal vs external references
```

Dlatego nie należy mówić, że GC w CPythonie jest po prostu "mark-and-sweep jak w Javie". Pewne intuicje są podobne, bo oba mechanizmy analizują graf referencji, ale cel i zakres są inne.

---

## 6. Stop-the-world w Pythonie vs Java

CPythonowy cykliczny GC działa jako pauza w wykonywaniu kodu Pythona. W tym sensie można mówić o mechanizmie stop-the-world. Skala problemu jest jednak inna niż w typowej aplikacji JVM.

Źródła: [Python docs — `gc`](https://docs.python.org/3/library/gc.html), [Python/C API — Thread State and the GIL](https://docs.python.org/3/c-api/threads.html#thread-state-and-the-global-interpreter-lock), [Python docs — Free-threaded CPython](https://docs.python.org/3/howto/free-threading-python.html).

### Klasyczny CPython z GIL

W domyślnym CPythonie z GIL tylko jeden wątek naraz wykonuje bajtkod Pythona w danym interpreterze. Inne wątki mogą istnieć, mogą czekać na I/O, mogą wykonywać kod C, który zwolnił GIL, ale zwykły kod Pythona nie wykonuje się równolegle na wielu rdzeniach w tym samym procesie.

To zmienia praktyczny koszt pauzy GC. W Javie stop-the-world zwykle oznacza zatrzymanie wielu wątków aplikacyjnych, zsynchronizowanie ich w safepointach i wykonanie pracy GC. W CPythonie z GIL wykonanie bajtkodu i tak jest serializowane, więc pauza cyklicznego GC nie ma takiej samej dynamiki jak w wielowątkowej aplikacji JVM.

Nie oznacza to, że pauzy GC są zawsze nieistotne. Mogą przeszkadzać w:

- aplikacjach latency-sensitive,
- serwerach z dużą liczbą obiektów kontenerowych,
- workerach przetwarzających duże grafy obiektów,
- aplikacjach realtime lub prawie realtime,
- procesach, które forkują się po rozgrzaniu pamięci.

### Free-threaded CPython

Od Pythona 3.13 istnieje wariant CPythona z opcjonalnie wyłączonym GIL, a w Pythonie 3.14 dokumentacja opisuje free-threaded build jako wspierany tryb budowania i uruchamiania. To jest ważna zmiana dla przyszłości rozmów o GC i pauzach.

W klasycznym CPythonie wiele intuicji o STW było łagodzonych przez GIL. W free-threaded CPythonie część tej argumentacji przestaje być tak prosta, bo wiele wątków może wykonywać kod Pythona równolegle. Nadal jednak nie oznacza to automatycznie, że CPython staje się JVM z kolektorami typu ZGC. Model zarządzania pamięcią, refcounting i cykliczny GC pozostają inną architekturą.

### Porównanie do JVM

W JVM problem pauz GC jest jednym z centralnych tematów projektowania runtime'u. Stąd kolektory takie jak G1, ZGC czy Shenandoah, które próbują ograniczać pauzy, wykonywać część pracy współbieżnie i skalować się do dużych stert.

W CPythonie główne koszty są zwykle gdzie indziej:

- refcounting wykonuje pracę stale, przy zmianach referencji,
- cykliczny GC działa okresowo i dotyczy obiektów śledzonych,
- GIL historycznie ograniczał równoległość wykonania bajtkodu,
- wiele intensywnych obliczeń i tak przenosi się do bibliotek C, Rust, Fortran albo C++.

Dlatego tuning GC w Pythonie jest zwykle ostatnim etapem diagnostyki, a nie pierwszym narzędziem optymalizacji.

---

## 7. Moduł `gc` — API i kontrola nad odśmiecaniem

Moduł `gc` daje kontrolę nad cyklicznym garbage collectorem. Nie daje kontroli nad całym zarządzaniem pamięcią CPythona i nie wyłącza reference countingu.

Źródło dla całej sekcji: [Python docs — `gc` module](https://docs.python.org/3/library/gc.html).

### `gc.collect()`

`gc.collect()` wymusza kolekcję:

```python
import gc

collected = gc.collect()
print(collected)
```

Bez argumentu wykonuje pełną kolekcję. Można też podać generację:

```python
gc.collect(0)  # młoda generacja
gc.collect(1)  # młoda generacja + inkrement starej generacji w Pythonie 3.14+
gc.collect(2)  # pełna kolekcja
```

To przypomina `System.gc()` z Javy tylko na poziomie "ręcznie proszę runtime o GC". W praktyce semantyka i koszt są inne, bo CPythonowy GC dotyczy cykli, a nie całej sterty zarządzanej tracing GC.

### `gc.disable()` i `gc.enable()`

Można wyłączyć automatyczny cykliczny GC:

```python
import gc

gc.disable()
try:
    ...
finally:
    gc.enable()
```

To nie wyłącza reference countingu. Obiekty bez cykli nadal będą zwalniane, gdy ich licznik referencji spadnie do zera.

Wyłączenie GC ma sens tylko wtedy, gdy rozumiesz profil alokacji programu. Typowe przypadki:

- kontrolowany benchmark,
- krótki etap masowego tworzenia obiektów bez cykli,
- proces workerowy, który zaraz się zakończy,
- specjalna architektura z ręcznym `gc.collect()` w przewidywalnych punktach.

W kodzie aplikacyjnym ustawienie `gc.disable()` "bo będzie szybciej" jest ryzykowne. Jeśli jednak program tworzy cykle, pamięć może rosnąć aż do ręcznej kolekcji albo końca procesu.

### `gc.get_objects()`

`gc.get_objects()` zwraca obiekty śledzone przez cykliczny GC:

```python
import gc

objects = gc.get_objects()
print(len(objects))
```

To nie jest lista wszystkich obiektów w procesie. To lista obiektów śledzonych przez GC. Proste obiekty mogą się tu nie pojawiać.

W Pythonie 3.14+:

```python
gc.get_objects(0)  # młoda generacja
gc.get_objects(1)  # pusta lista
gc.get_objects(2)  # stara generacja
```

### `gc.get_referrers()` i `gc.get_referents()`

Te funkcje służą do eksploracji grafu referencji:

```python
import gc

target = []

print(gc.get_referrers(target))
print(gc.get_referents(target))
```

- `gc.get_referrers(obj)` odpowiada: kto wskazuje na ten obiekt?
- `gc.get_referents(obj)` odpowiada: na co wskazuje ten obiekt?

To są narzędzia diagnostyczne. Wyniki mogą zawierać obiekty wewnętrzne interpretera, ramki stosu, słowniki lokalnych zmiennych i inne struktury pomocnicze. Łatwo wyciągnąć błędne wnioski, jeśli traktuje się wynik jako czysty graf domenowy aplikacji.

### `gc.set_threshold()`

Progi można zmienić:

```python
import gc

old = gc.get_threshold()
gc.set_threshold(1000, 10, 0)
```

W Pythonie 3.14+ `threshold2` jest ignorowany. `threshold0` steruje momentem uruchomienia kolekcji młodej generacji, a `threshold1` wpływa na tempo skanowania starej generacji.

W praktyce tuning progów robi się dopiero po pomiarach. Sama zmiana progu może:

- zmniejszyć liczbę pauz GC,
- zwiększyć chwilowe zużycie pamięci,
- opóźnić usuwanie cykli,
- pogorszyć latency w innym miejscu.

### `gc.callbacks`

`gc.callbacks` pozwala podpiąć funkcję wywoływaną na początku i końcu kolekcji:

```python
import gc
import time

starts = {}

def on_gc(phase, info):
    generation = info["generation"]
    if phase == "start":
        starts[generation] = time.perf_counter()
    elif phase == "stop":
        duration = time.perf_counter() - starts.pop(generation, time.perf_counter())
        print(
            "gc",
            generation,
            "collected",
            info["collected"],
            "uncollectable",
            info["uncollectable"],
            "duration",
            duration,
        )

gc.callbacks.append(on_gc)
```

To dobre miejsce na metryki, ale z callbacków nie powinno się robić ciężkiej logiki. Callback działa podczas obsługi GC, więc sam może zaburzać pomiar.

### Porównanie do flag JVM

W Javie tuning GC to osobny obszar inżynierii: wybór kolektora, rozmiar sterty, rozmiary regionów, docelowe pauzy, logowanie GC, ergonomia kontenerów, NUMA itd.

W Pythonie API jest małe:

- włącz/wyłącz automatyczny cykliczny GC,
- wymuś kolekcję,
- podejrzyj obiekty śledzone,
- podejrzyj referencje,
- ustaw progi,
- dodaj callbacki.

To dobrze pasuje do roli GC w CPythonie: to mechanizm pomocniczy do cykli, nie pełny menedżer sterty jak w JVM.

---

## 8. Weak references (`weakref`)

Weak reference to referencja, która nie utrzymuje obiektu przy życiu. Jeśli do obiektu prowadzą już tylko weak references, obiekt może zostać usunięty przez mechanizmy zarządzania pamięcią.

Źródło: [Python docs — `weakref`](https://docs.python.org/3/library/weakref.html).

W Javie podobną rolę pełnią `WeakReference`, `WeakHashMap` i częściowo inne typy referencji z pakietu `java.lang.ref`. W Pythonie główny moduł to `weakref`.

### `weakref.ref()`

Podstawowy przykład:

```python
import weakref

class User:
    pass

user = User()
ref = weakref.ref(user)

print(ref() is user)  # True

del user

print(ref())          # None, jeśli obiekt został już zniszczony
```

Weak reference wywołuje się jak funkcję. Zwraca obiekt, jeśli nadal żyje, albo `None`, jeśli został już usunięty.

Poprawny wzorzec użycia:

```python
obj = ref()
if obj is not None:
    obj.do_something()
```

Nie rób osobnego testu "czy żyje", a potem drugiego pobrania, bo w kodzie wielowątkowym obiekt może zniknąć między tymi operacjami.

### Weak containers

Moduł `weakref` zawiera gotowe kontenery:

- `weakref.WeakValueDictionary`,
- `weakref.WeakKeyDictionary`,
- `weakref.WeakSet`.

`WeakValueDictionary` jest częsty w cache'ach:

```python
import weakref

class Image:
    def __init__(self, path):
        self.path = path

cache = weakref.WeakValueDictionary()

img = Image("logo.png")
cache["logo"] = img

print(cache["logo"])

del img

print(cache.get("logo"))  # może zwrócić None
```

Cache nie powinien zawsze utrzymywać obiektów przy życiu. Jeśli jedynym powodem istnienia dużego obiektu jest to, że został kiedyś dodany do cache'a, weak reference może być właściwym narzędziem.

### Typowe zastosowania

Weak references są przydatne w:

- cache'ach,
- rejestrach obiektów,
- mechanizmach observer/listener,
- mapowaniu metadanych do obiektów,
- unikaniu cykli w strukturach parent-child,
- finalizacji przez `weakref.finalize()`.

Przykład problemu z observerem:

```python
class EventBus:
    def __init__(self):
        self._listeners = []

    def subscribe(self, listener):
        self._listeners.append(listener)
```

Jeśli `EventBus` żyje długo, lista `_listeners` utrzyma wszystkie listenery przy życiu. Czasem to pożądane. Czasem to wyciek pamięci. Weak references pozwalają zaprojektować rejestr, który nie jest właścicielem listenerów.

### Ograniczenia

Nie każdy obiekt obsługuje weak references. Instancje zwykłych klas najczęściej tak, ale np. wiele podstawowych typów wbudowanych nie.

Przykład:

```python
import weakref

weakref.ref([])  # TypeError
```

Dla klas ze `__slots__` trzeba dodać slot `__weakref__`, jeśli instancje mają wspierać weak references:

```python
class User:
    __slots__ = ("name", "__weakref__")

    def __init__(self, name):
        self.name = name
```

### `weakref.finalize()`

`weakref.finalize()` pozwala zarejestrować funkcję sprzątającą wywoływaną, gdy obiekt jest usuwany:

```python
import tempfile
import shutil
import weakref

class TempDir:
    def __init__(self):
        self.name = tempfile.mkdtemp()
        self._finalizer = weakref.finalize(self, shutil.rmtree, self.name)

    def close(self):
        self._finalizer()
```

To często bezpieczniejsza alternatywa niż `__del__`, zwłaszcza gdy funkcja finalizująca nie trzyma referencji do całego obiektu.

---

## 9. `__del__` — finalizator w Pythonie

`__del__` to metoda finalizująca obiektu. Jest wywoływana, gdy obiekt ma zostać zniszczony, ale w praktyce trzeba traktować ją bardzo ostrożnie.

Źródła: [Python data model — `object.__del__`](https://docs.python.org/3/reference/datamodel.html#object.__del__), [PEP 442 — Safe object finalization](https://peps.python.org/pep-0442/), [Python docs — `weakref.finalize`](https://docs.python.org/3/library/weakref.html#weakref.finalize).

### Podobieństwo do Javy

Historycznie najbliższą analogią w Javie było `finalize()`, które jest dziś mechanizmem przestarzałym. W nowszym kodzie Javy preferuje się jawne zarządzanie zasobem przez `try-with-resources`, `AutoCloseable`, `Cleaner` albo inne jawne protokoły lifecycle.

W Pythonie analogiczna zasada brzmi:

> Nie używaj `__del__` do krytycznego zwalniania zasobów, jeśli możesz użyć context managera.

Lepszy kod:

```python
with open("data.txt") as f:
    data = f.read()
```

Gorszy pomysł:

```python
class FileWrapper:
    def __init__(self, path):
        self.file = open(path)

    def __del__(self):
        self.file.close()
```

### Dlaczego `__del__` jest problematyczny?

Problemy:

- nie zawsze masz pełną kontrolę nad momentem wywołania,
- przy zamykaniu interpretera część globali może być już wyczyszczona,
- wyjątki z `__del__` nie propagują normalnie,
- finalizator może przypadkowo wskrzesić obiekt,
- łatwo stworzyć cykl, który utrudnia sprzątanie,
- kod finalizatora działa w trudnym kontekście runtime'u.

W CPythonie obiekt bez cyklu często zostanie zfinalizowany natychmiast po spadku refcounta do zera. To jednak szczegół implementacyjny CPythona. Kod pisany z myślą o Pythonie jako języku nie powinien zakładać deterministycznej finalizacji przez `__del__`.

### Cykle z `__del__` i PEP 442

Przed Pythonem 3.4 cykle zawierające obiekty z finalizatorami były szczególnie problematyczne. GC mógł wykryć, że cykl jest nieosiągalny, ale nie zawsze mógł go bezpiecznie usunąć, bo nie było jasne, w jakiej kolejności uruchamiać finalizatory i czy finalizator nie odwoła się do obiektu, którego referencje zostały już wyczyszczone.

PEP 442 zmienił model finalizacji tak, żeby finalizatory można było wywoływać bezpieczniej także dla obiektów w cyklach. To nie znaczy, że `__del__` stał się dobrym narzędziem do zwykłego zarządzania zasobami. Znaczy tylko, że usunięto część historycznych pułapek.

### Resurrection

Finalizator może wskrzesić obiekt, tworząc do niego nową referencję podczas finalizacji:

```python
resurrected = None

class User:
    def __del__(self):
        global resurrected
        resurrected = self
```

To legalne, ale bardzo trudne do poprawnego rozumienia. Obiekt był przeznaczony do zniszczenia, ale finalizator przywrócił go do życia. Takich konstrukcji nie powinno być w normalnym kodzie aplikacyjnym.

### Zalecany wzorzec: context manager

Jeśli obiekt reprezentuje zasób, daj mu jawne `close()` i context manager:

```python
class Resource:
    def __init__(self):
        self.closed = False

    def close(self):
        if not self.closed:
            self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


with Resource() as resource:
    ...
```

Jeśli potrzebujesz awaryjnego sprzątania, rozważ `weakref.finalize()`, ale nadal traktuj jawne zamykanie jako główny mechanizm.

---

## 10. Porównanie Python vs Java GC — tabela podsumowująca

Źródła do porównania po stronie Pythona: [Python docs — `gc`](https://docs.python.org/3/library/gc.html), [CPython InternalDocs — Garbage collector design](https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md), [Python/C API — Reference Counting](https://docs.python.org/3/c-api/refcounting.html). Po stronie Javy szczegóły zależą od konkretnej wersji JVM i kolektora, więc tabela porównuje model koncepcyjny.

| Cecha | CPython | Java / JVM |
|---|---|---|
| Główny mechanizm | Reference counting | Tracing GC |
| Mechanizm uzupełniający | Cykliczny GC dla nieosiągalnych cykli | Zależny od kolektora: copying, mark-sweep, mark-compact, concurrent marking itd. |
| Kiedy obiekt zwykle znika? | Gdy refcount spadnie do zera | Gdy GC uzna go za nieosiągalny i wykona kolekcję |
| Cykle referencji | Wymagają cyklicznego GC | Naturalnie obsługiwane przez tracing GC |
| Generacje | Young/old w Pythonie 3.14+, historycznie 0/1/2 | Young/old albo regiony, zależnie od kolektora |
| Przenoszenie obiektów | Zwykle nie; promocja to klasyfikacja GC | Częste w kolektorach kopiujących/kompaktujących |
| Stop-the-world | Tak, ale w klasycznym CPythonie kontekst łagodzi GIL | Centralny problem wydajnościowy wielu aplikacji |
| Tuning | Kilka funkcji w `gc` | Dużo flag JVM i wybór kolektora |
| Determinizm zwalniania | Często tak w CPythonie przez refcount | Nie dla zwykłych obiektów |
| Finalizacja | `__del__`, `weakref.finalize`, context managers | `Cleaner`, `PhantomReference`, `try-with-resources` |

### Najważniejszy wniosek

W Javie garbage collector jest główną maszyną decydującą o czasie życia obiektów. W CPythonie większość obiektów jest usuwana przez reference counting, a cykliczny GC sprząta przypadki, których refcounting nie potrafi rozwiązać.

To wpływa na sposób myślenia o wydajności:

- W Javie często analizujesz rozmiar sterty, alokacje, promocje, pauzy GC i dobór kolektora.
- W Pythonie częściej analizujesz, kto trzyma referencję, czy istnieją cykle, czy cache nie rośnie bez limitu i czy duże obiekty nie są przypadkowo utrzymywane przez domknięcia, globalne struktury albo kolejki.

### Deterministyczne zwalnianie to nie kontrakt języka

W CPythonie często zobaczysz natychmiastowe sprzątanie:

```python
class User:
    def __del__(self):
        print("deleted")

user = User()
del user
```

W CPythonie napis może pojawić się od razu. W innej implementacji Pythona nie musi. Dlatego w kodzie przenośnym ważne zasoby zamyka się jawnie:

```python
with open("data.txt") as f:
    ...
```

### Tuning: Python jest mniej "GC-centric"

W aplikacji JVM tuning GC może dać ogromną różnicę, szczególnie przy dużych stertach i wysokich wymaganiach latency.

W Pythonie zmiana progów GC bywa przydatna, ale zwykle większe znaczenie mają:

- ograniczenie liczby tworzonych obiektów,
- usunięcie przypadkowych referencji,
- poprawa struktury cache'y,
- streaming zamiast ładowania wszystkiego do pamięci,
- użycie bibliotek natywnych dla dużych tablic danych,
- profilowanie pamięci narzędziami typu `tracemalloc`.

---

## 11. Praktyczne aspekty i narzędzia diagnostyczne

W praktyce problemy z pamięcią w Pythonie rzadko sprowadzają się do pytania "czy garbage collector działa?". Częściej pytanie brzmi:

> Kto nadal trzyma referencję do obiektu, który według mnie powinien już zniknąć?

### `tracemalloc`

`tracemalloc` to moduł standardowy do śledzenia alokacji pamięci wykonywanych przez Pythona. Pozwala robić snapshoty i porównywać je, żeby zobaczyć, które linie kodu odpowiadają za wzrost pamięci.

Źródło: [Python docs — `tracemalloc`](https://docs.python.org/3/library/tracemalloc.html).

Przykład:

```python
import tracemalloc

tracemalloc.start()

data = [str(i) for i in range(100_000)]

snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics("lineno")

for stat in top[:10]:
    print(stat)
```

Do szukania wycieków często używa się dwóch snapshotów:

```python
import tracemalloc

tracemalloc.start()

before = tracemalloc.take_snapshot()

run_suspicious_workload()

after = tracemalloc.take_snapshot()

for stat in after.compare_to(before, "lineno")[:10]:
    print(stat)
```

`tracemalloc` nie pokaże wszystkiego, np. pamięci zaalokowanej poza mechanizmami śledzonymi przez Pythona w bibliotekach natywnych, ale jest bardzo dobrym pierwszym narzędziem.

### `sys.getsizeof()`

`sys.getsizeof()` zwraca rozmiar konkretnego obiektu, ale nie liczy rekurencyjnie całego grafu obiektów.

Źródło: [Python docs — `sys.getsizeof`](https://docs.python.org/3/library/sys.html#sys.getsizeof).

Przykład:

```python
import sys

items = [1, 2, 3]

print(sys.getsizeof(items))
```

Wynik obejmuje sam obiekt listy, czyli m.in. strukturę listy i tablicę referencji. Nie oznacza pełnego kosztu wszystkich obiektów, do których lista wskazuje.

Pułapka:

```python
import sys

items = ["x" * 1000 for _ in range(1000)]

print(sys.getsizeof(items))  # nie jest pełnym rozmiarem stringów w środku
```

Do pełnego liczenia grafu trzeba użyć własnego przejścia po referencjach albo narzędzi zewnętrznych.

### `objgraph`

`objgraph` pomaga badać graf referencji i zobaczyć, dlaczego obiekt nadal żyje.

Źródło: [objgraph documentation](https://objgraph.readthedocs.io/).

Typowy scenariusz:

```python
import objgraph

objgraph.show_most_common_types(limit=20)
```

Można też szukać ścieżki od obiektu do rootów:

```python
import objgraph

obj = get_suspicious_object()
objgraph.show_backrefs([obj], max_depth=5)
```

To jest bardzo przydatne, gdy `tracemalloc` mówi "tu powstają obiekty", ale nadal nie wiesz, kto je utrzymuje przy życiu.

### `memory_profiler`

`memory_profiler` to zewnętrzne narzędzie do obserwowania zużycia pamięci procesu i profilowania linia po linii.

Źródło: [memory-profiler on PyPI](https://pypi.org/project/memory-profiler/).

Przykładowy styl użycia:

```python
from memory_profiler import profile

@profile
def load_data():
    data = [str(i) for i in range(1_000_000)]
    return data

load_data()
```

Potem uruchomienie:

```bash
python -m memory_profiler script.py
```

To narzędzie patrzy bardziej z perspektywy procesu i linii kodu niż samego grafu referencji.

### `gc.DEBUG_SAVEALL`

Do diagnozowania nieosiągalnych obiektów można użyć flag debugowania:

```python
import gc

gc.set_debug(gc.DEBUG_SAVEALL)

make_cycles()

gc.collect()

print(gc.garbage)
```

`DEBUG_SAVEALL` powoduje, że nieosiągalne obiekty trafiają do `gc.garbage` zamiast zostać zwolnione. To pomaga w analizie, ale łatwo samemu stworzyć sztuczny wyciek, bo `gc.garbage` trzyma referencje do tych obiektów.

### Kiedy rozważyć wyłączenie GC?

Wyłączenie cyklicznego GC bywa używane w bardzo specyficznych warunkach. Znany case study z Instagrama opisywał zysk wydajności po wyłączeniu GC w architekturze workerów, ale to był świadomy wybór oparty o charakter procesu, forkowanie i kontrolę cyklu życia. Źródło opisujące case: [Dismissing Python Garbage Collection at Instagram](https://sudonull.com/post/70738-About-how-Instagram-turned-off-the-Python-garbage-collector-and-started-living-Wunder-Fund-Blog).

Rozsądne pytania przed `gc.disable()`:

- Czy program tworzy cykle?
- Czy proces jest długo żyjący?
- Czy mamy metryki RSS, liczby obiektów i pauz GC?
- Czy potrafimy wymusić `gc.collect()` w kontrolowanym momencie?
- Czy mamy testy obciążeniowe, które pokażą wzrost pamięci po wielu godzinach?

W większości aplikacji odpowiedź brzmi: nie wyłączaj GC globalnie. Najpierw zmierz problem.

### Minimalny workflow diagnostyczny

Praktyczny workflow dla technicznej osoby:

1. Sprawdź RSS procesu i potwierdź, że problem naprawdę dotyczy pamięci.
2. Włącz `tracemalloc` i porównaj snapshoty przed/po podejrzanym workloadzie.
3. Jeśli obiekty nadal żyją, użyj `gc.get_referrers()` albo `objgraph`, żeby znaleźć właścicieli referencji.
4. Sprawdź cache'e, kolejki, globale, singletons, domknięcia, taski async i loggery.
5. Dopiero potem rozważ tuning `gc.set_threshold()` albo kontrolowane `gc.disable()`.

Najczęstszy "wyciek" w Pythonie to nie błąd garbage collectora, tylko poprawnie działający runtime, który nie usuwa obiektów, bo program nadal ma do nich referencje.

---

## Powiązane pliki

- [GIL w Pythonie](gil-w-pythonie.md)
- [Zrozumienie GIL w Pythonie](zrozumienie-gil-w-pythonie.md)
- [Wycieki pamięci w Pythonie](python-wycieki-pamieci.md)
- [Typy danych w Pythonie i zużycie pamięci](typy-danych-w-python-i-zuzycie-pamieci.md)
- [Zużycie pamięci w Pythonie](zużycie-pamięci-w-pythonie.md)
