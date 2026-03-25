# Typ `Literal` w Pythonie: Dlaczego jest lepszy niż zwykły `str`?

Ten fragment dokumentacji wyjaśnia zalety używania typu `Literal` z modułu `typing` do definiowania z góry określonych, dozwolonych wartości zmiennych, w przeciwieństwie do używania zwykłego typu tekstowego (`str`).

Spójrzmy na podany przykład:

```python
from typing import Literal

ChunkType = Literal["text", "table", "code", "figure_caption"]
```

## O co w tym chodzi? (Prosto i po ludzku)

Zamiast pisać nad funkcją zwykły komentarz w stylu: *"hej, ta zmienna może przyjmować tylko wartości 'text', 'table', 'code' lub 'figure_caption'"*, **definiujemy te twarde reguły w samym kodzie (w systemie typów)**.

Dzięki temu zyskujemy następujące korzyści:

### 1. Wczesne wykrywanie błędów (przed uruchomieniem programu)

Jeśli przez pomyłkę przekażesz wartość, której nie ma na liście – np. wpiszesz `chunk_type = "image"` – narzędzia sprawdzające typy (tzw. *type checkery*, np. MyPy, Pyright) od razu podświetlą Ci to na czerwono i zgłoszą błąd.
Dowiadujesz się o pomyłce **w trakcie pisania kodu** (*"at write time"*), a nie dopiero po uruchomieniu programu, gdy ta część kodu akurat zadziała i aplikacja się "wywali" (*"at runtime"*).

### 2. Autouzupełnianie w edytorze kodu (Autocomplete)

Kiedy w IDE (np. Visual Studio Code, PyCharm) deklarujesz, że jakaś funkcja przyjmuje argument typu `ChunkType`, podczas wywoływania tej funkcji edytor sam rozwinie Ci listę podpowiedzi: `"text", "table", "code", "figure_caption"`.
Nie musisz skakać po plikach ani szukać w dokumentacji, żeby przypomnieć sobie poprawne wartości. Trudniej też o głupią literówkę.

### 3. Jedno źródło prawdy (Single Source of Truth)

Lista dozwolonych wartości istnieje tylko w jednym miejscu w kodzie — właśnie w tej jednej definicji `Literal`.
Gdybyśmy użyli zwykłego `str`, musielibyśmy w wielu miejscach w systemie ręcznie sprawdzać te warunki w kodzie za pomocą spamu instrukcji `if`:

```python
# Tego chcemy uniknąć:
if chunk_type == "text":
    pass
elif chunk_type == "table":
    pass
elif chunk_type not in ["text", "table", "code", "figure_caption"]:
    raise ValueError("Nieznany typ!") # Kod rozrzucony po całej aplikacji
```

### Podsumowanie

Można by po prostu zdefiniować tę zmienną jako `chunk_type: str`. Jest to teoretycznie "prostsze", ale tracimy wtedy **gwarancję poprawności** (*correctness guarantee*). Zwykły typ string (`str`) przyjmie każdy tekst – od "text", przez puste "", aż po "Ala ma kota". Zastosowanie `Literal` sprawia, że zasady gry są jasne, a Twój kod staje się dużo bezpieczniejszy i przyjemniejszy we współpracy z innymi programistami.

## `Literal` vs `Enum`: Co wybrać?

Często zadawanym pytaniem jest, czy do definiowania stałych wartości nie lepiej użyć modułu `enum` i specjalnej klasy dziedziczącej po wyliczeniach? Obie koncepcje mają swoje mocne strony, więc wybór zależy od konkretnego przypadku użycia.

### Kiedy lepiej użyć `Literal`?

1. **Praca z danymi wejściowymi/wyjściowymi (JSON, zewnętrzne API, FastAPI/Pydantic):**
   Gdy Twoja funkcja przyjmuje lub zwraca surowe dane z zewnątrz (np. parametry zapytania z sieci), przeważnie są to bezpośrednie ciągi znaków. W takich przypadkach ciąg typu `"text"` pod maską pozostaje zwykłym obiektem `str`. Jeżeli użył(a)byś `Enum`, na pewnym etapie musiał(a)byś tłumaczyć z pobranego stringa na postać obiektu Twojej nowej klasy, i z obiektu z powrotem na stringa w trakcie przygotowywania odpowiedzi do sieci. `Literal` chroni przed taką konwersją.
2. **Minimalizm i brak narzutu:**
   `Literal` zapisujemy zwięźle w jednej linijce kodu bez konieczności tworzenia pełnoprawnej klasy i przypisywania polom wartości, unikamy też dłuższego importowania z innych plików.

### Kiedy lepiej uciec się do klasy `Enum`?

1. **Gdy potrzebujesz metod, właściwości lub logiki dodanej do wartości:**
   `Enum` jest w świecie Pythona klasą, i tak samo funkcjonuje. Oznacza to, że do elementu z wyliczenia podpiąć można wewnętrzne funkcje, skomplikowane formatowanie, czy rozszerzyć zachowanie.
2. **Potrzeba wygodnej iteracji (wylistowania dostępnych flag):**
   Jeśli chcesz na bazie dozwolonych opcji automatycznie budować element interfejsu (np. pole wyboru w HTML, lub iterować w pętli), `Enum` zrobi to błyskawicznie (np. poprzez zwykłą pętlę `for opcja w MojEnum:` lub tworząc listę wszystkich dozwolonych stringów w ten sposób `[x.value for x in MojEnum]`). Aby zrobić to samo z `Literal`, musisz odwoływać się do `typing.get_args()`, co jest bardziej kruche i sztuczne.
3. **Refaktorowanie i duże systemy:**
   Jeśli opcji w `Literal` zrobi się aż piętnaście i chcesz udostępniać listę takich dozwolonych opcji w trzydziestu miejscach rozsianych w aplikacji, powinieneś zamienić je na wyliczenie klasowe. Obiekt wyliczenia łatwiej odnaleźć w całym systemie i zmieniać z poziomu IDE.
4. **Weryfikacja w trakcie działania programu (Runtime):**
   Własności `Literal` są sprawdzane głównie *statycznie* – przez lintery (Mypy/Pyright) w trakcie pisania kodu. Jeśli dodasz po prostu `chunk_type: Literal["text"] = "niepoprawny_tekst"` bez sprawdzarki typów, Python uruchomi to tak samo jak każdy inny kod i błąd wyjdzie dopiero głębiej. Z kolei przypisanie wymuszone przez `Enum`, np. `StatusZamowienia("niepoprawny_tekst")`, wywoła od razu błąd `ValueError` **w samym Pythonie w momencie uruchomienia**. Klasa `Enum` chroni przed niespodziankami podczas działania aplikacji, jeżeli nie masz rygorystycznych sprawdzarek przed uruchomieniem.

**Przykład, jak wielofunkcyjny potrafi być `Enum` w porównaniu do `Literal`:**

```python
from enum import Enum

class StatusZamowienia(Enum):
    NOWE = "nowe"
    W_REALIZACJI = "w_realizacji"
    WYSLANE = "wyslane"

    # W Enum możemy dodawać logikę biznesową bezpośrednio do naszego wyliczenia
    def czy_mozna_anulowac(self) -> bool:
        return self in (StatusZamowienia.NOWE, StatusZamowienia.W_REALIZACJI)

# 1. Łatwa iteracja (czego nie ma wprost Literal):
dostepne_opcje = [status.value for status in StatusZamowienia]
print(dostepne_opcje) 
# Wynik: ['nowe', 'w_realizacji', 'wyslane']

# 2. Wykonywanie powiązanej logiki przez zdefiniowane wcześniej metody:
moj_status = StatusZamowienia.WYSLANE
if not moj_status.czy_mozna_anulowac():
    print("Za późno na anulowanie!")
```

**Krótko mówiąc:** Używaj `Literal` na pierwszą linię obrony w luźniejszych, prostych danych (szczególnie JSON-owych/z zewnątrz) oraz do szybkich adnotacji. Przerzuć się na `Enum` dla powtarzalnych elementów we wnętrzu dużej architektury aplikacji, które potrzebują iterowania lub dodanej logiki.
