# Jak wczytać 10GB plik logów w Pythonie

**Data:** 19 maja 2026, 17:20:27 CET

---

**User:**

Pytanie na job interview: 10gb log plik, wczytaj go. Rozważ jak to można zrobić. Czy asynchroniczność to jedyna droga?

---

**Gemini:**

Wczytywanie 10 GB pliku w Pythonie to klasyczne pytanie rekrutacyjne, które ma sprawdzić Twoje zrozumienie zarządzania pamięcią oraz operacji wejścia/wyjścia (I/O). Głównym problemem jest to, że **nie możemy wczytać całego pliku do pamięci RAM na raz** (np. za pomocą `file.read()` lub `file.readlines()`), ponieważ spowodowałoby to błąd `MemoryError` na maszynach z mniejszą ilością pamięci, lub drastycznie spowolniło system z powodu *swappowania*.

Odpowiadając od razu na Twoje pytanie: **Nie, asynchroniczność absolutnie nie jest jedyną, ani nawet domyślną drogą do rozwiązania tego problemu.**

Oto główne podejścia, jak sobie z tym poradzić:

---

### 1. Podejście standardowe: Leniwe iterowanie i Generatory (Synchronicznie)

W Pythonie obiekt pliku otwartego funkcją `open()` jest **iteratorem**. Oznacza to, że pętla `for` wczytuje plik leniwie (ang. *lazy evaluation*), linia po linii. W danym momencie w pamięci RAM znajduje się tylko **jedna linia pliku**.

To najbardziej idiomatyczne, wydajne i poprawne podejście. Żeby uczynić kod jeszcze lepszym i bardziej modułowym, warto użyć słowa kluczowego `yield`, co zamienia funkcję w **generator**. Dzięki temu oddzielamy logikę czytania i filtrowania pliku od akcji, która ma być na nim wykonana (np. wypisanie na ekran vs zapisanie do bazy).

```python
def get_error_logs(file_path):
    """Generator wyszukujący błędy w dużym pliku logów."""
    # 'with' zapewnia bezpieczne zamkniecie pliku po zakonczeniu
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if "ERROR" in line:
                # Zwracamy linię i wstrzymujemy działanie (leniwe ewaluowanie)
                yield line.strip()

# Użycie 1: Wypisywanie na ekran
# for error_line in get_error_logs('server_logs_10GB.txt'):
#     print(f"Znaleziono błąd: {error_line}")

# Użycie 2: Zapis do mniejszego pliku (nadal bez obciążania RAM-u)
# with open('only_errors.txt', 'w', encoding='utf-8') as out_file:
#     for error_line in get_error_logs('server_logs_10GB.txt'):
#         out_file.write(error_line + '\n')
```

**Zalety:**
- **Minimalne zużycie pamięci:** W danej chwili tylko jedna linia w pamięci RAM.
- **Zasada jednej odpowiedzialności (Separation of Concerns):** Funkcja jedynie filtruje dane, nie narzucając operacji takich jak `print`.
- **Reużywalność:** Ten sam generator można wykorzystać w różnych kontekstach.
- Niskie narzuty wydajnościowe – działa tak szybko, jak pozwala na to Twój dysk (I/O bound).

---

### 2. Generatory (Chunking / Porcjowanie)

Jeśli przetwarzanie pojedynczej linii jest zbyt uciążliwe i wolisz przetwarzać dane w większych, ale nadal kontrolowanych paczkach (tzw. *chunks*), możesz wczytywać określoną liczbę bajtów lub linii.

W bibliotekach takich jak **Pandas** to podejście realizuje się gotowym parametrem `chunksize`, co jest niezwykle przydatne przy dużych plikach CSV/logów ustrukturyzowanych:

```python
import pandas as pd

# Wczytuje po 100 000 wierszy naraz - zużycie RAM jest stabilne
for chunk in pd.read_csv('10gb_log.csv', chunksize=100000):
    # przetwarzanie całego dataframe'u (chunk) naraz
    filtered_chunk = chunk[chunk['level'] == 'ERROR']
    print(filtered_chunk)
```

Jeśli nie używasz Pandasa, możesz czytać np. po 1MB za pomocą metody `read(size)` i użyć `yield` do stworzenia własnego generatora.

---

### 3. Moduł `mmap` (Memory-Mapped File)

Moduł `mmap` mapuje plik bezpośrednio do wirtualnej przestrzeni adresowej systemu operacyjnego. Plik zachowuje się w kodzie tak, jakby był zwykłą tablicą bajtów (lub ciągiem znaków) w całości załadowaną do pamięci, ale **to system operacyjny decyduje, co faktycznie załadować do fizycznego RAM-u** i wymienia strony pamięci w locie.

To rozwiązanie jest **niesamowicie szybkie**, zwłaszcza gdy musimy przeskakiwać w przód i w tył (ang. *seek*) po wielkim pliku, wyszukiwać konkretne bajty, lub gdy ten sam plik jest czytany przez wiele procesów jednocześnie (OS współdzieli mapowanie w pamięci).

```python
import mmap

def process_with_mmap(file_path):
    with open(file_path, 'r+b') as f:
        # 0 oznacza zmapowanie całego pliku (obsługiwane bezpiecznie przez OS)
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            # Możemy szukać tekstu za pomocą wydajnych operacji na bajtach
            index = mm.find(b"CRITICAL_ERROR")
            if index != -1:
                mm.seek(index)
                print(mm.readline().decode('utf-8'))
```

---

### 4. A co z asynchronicznością (`async` / `await`)?

Pytanie brzmi: *Czy asynchroniczność to jedyna droga?*
**Odpowiedź:** Nie. Do samego wczytywania i procesowania dużego lokalnego pliku, asynchroniczność **nie jest domyślnym wyborem**.

Użycie asynchroniczności (np. za pomocą biblioteki `aiofiles`) ma sens **tylko wtedy, gdy Twoja aplikacja już wykorzystuje pętlę zdarzeń (np. jest to serwer HTTP napisany w FastAPI) i nie chcesz jej zablokować**.

Wyobraź sobie, że serwer API musi odczytać fragment z tego 10GB pliku w odpowiedzi na request użytkownika. Gdybyś użył standardowego, synchronicznego iterowania `for line in file:`, serwer "zamroziłby się" na czas czytania i zignorował inne zapytania HTTP. W takim przypadku asynchroniczność pozwala pętli zdarzeń obsługiwać innych klientów w czasie, gdy dysk wykonuje pracę.

```python
import asyncio
import aiofiles

async def process_async_log(file_path):
    async with aiofiles.open(file_path, mode='r') as f:
        async for line in f:
            if "ERROR" in line:
                print(line.strip())
                # Szybkie operacje; w tle pętla zdarzeń obsługuje inne żądania
```

**Kluczowe niezrozumienie:**
Wielu początkujących uważa, że "asynchronicznie oznacza szybciej". Zastosowanie `aiofiles` **nie przyspieszy** czytania pliku (często bywa o ułamek sekundy wolniejsze ze względu na narzut pętli zdarzeń). Asynchroniczność **nie jest** po to, żeby radzić sobie z dużym rozmiarem pliku (to rozwiązuje iterowanie). Asynchroniczność jest po to, aby **zwolnić wątek dla innych zadań, podczas gdy czekasz na dysk**.

---

### Podsumowanie (Jak odpowiadać na rekrutacji)

Jeśli zostaniesz zapytany o to na rozmowie, idealnie jest odpowiedzieć w takich krokach:

1. **Zrozumienie problemu:** Zaznacz, że głównym wyzwaniem jest unikanie wyczerpania RAM-u (OOM - Out of Memory). Nie wolno robić `.read()` ani `.readlines()`.
2. **Standardowe rozwiązanie (Złoty środek):** Zaproponuj synchroniczne, leniwe iterowanie (`for line in open(...):`), co jest eleganckie, zjada mało RAM-u i w 90% wypadków w zupełności wystarcza.
3. **Optymalizacja wydajnościowa:** Wspomnij o plikach mapowanych w pamięci (`mmap`), jeśli problemem byłaby konieczność szybkiego wyszukiwania wzorców lub skakania po pliku. 
4. **Odpowiedź na haczyk z asynchronicznością:** Jasno stwierdź, że asynchroniczność (`async`/`await`) nie zmniejsza zużycia pamięci ani nie przyspiesza czytania pojedynczego pliku. Należy jej użyć tylko w aplikacjach współbieżnych (np. serwery webowe), żeby operacja I/O nie blokowała pętli zdarzeń (Event Loop).
