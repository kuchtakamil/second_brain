# Wycieki pamięci w Pythonie

## Czym są wycieki pamięci w Pythonie?

Wyciek pamięci ma miejsce, gdy aplikacja rezerwuje pamięć na obiekty lub dane, ale nigdy jej nie zwalnia — mimo że te dane nie są już nigdzie w programie wykorzystywane. W konsekwencji zużycie pamięci operacyjnej (RAM) z biegiem czasu stale wzrasta.

W przeciwieństwie do języków takich jak C czy C++, Python korzysta z automatycznego zarządzania pamięcią za pomocą **zliczania referencji (reference counting)** oraz **Garbage Collectora (GC)** wykrywającego cykle. Dlatego większość pamięci jest zwalniana automatycznie, gdy tylko przestajemy jej używać. Niemniej jednak, w Pythonie wciąż możliwe są tzw. **logiczne wycieki pamięci**, gdy nieświadomie utrzymujemy referencje do obiektów.

## Czy są groźne?

**Tak.** Sam wyciek nie uderza od razu, lecz narasta.
Dla skryptów działających przez kilka sekund lub minut zasoby zawsze zwolni system operacyjny po zakończeniu pracy programu. Jednak w aplikacjach typu *long-running* (np. serwery sieciowe uvicorn/gunicorn, aplikacje FastAPI, daemon-y, boty Discord, czy wielkoskalowe potoki danych) powolny wzrost zasobów doprowadzi w końcu do wyczerpania dostępnej pamięci. Wtedy mogą wystąpić groźne skutki:
- Skrajne spowolnienie maszyny przez korzystanie z pamięci wymiany (swap space),
- Przerwanie działania procesu na poziomie systemu (OOM Killer - Out Of Memory Manager w Linuxie ubije dany proces i aplikacja nagle "spadnie z rowerka").

## Jak można je spowodować w Pythonie?

1. **Globalne kolekcje bez usuwania (Caches / Słowniki)**
   Często budujemy aplikacje z mechanizmem pamięci podręcznej (np. globalny `dict` lub `list`), w których dopisujemy wyniki danych na przyszłość. Bez mechanizmu czyszczenia lub ograniczania rozmiaru takiej kolekcji, będzie ona puchła w nieskończoność.

2. **Pozostawione zasoby plikowe lub połączenia wgrywane w systemie operacyjnym**
   Brak zamknięcia uchywytu za pomocą metody `.close()` ewentualnie zapominanie o klauzuli `with`.

3. **Cykliczne referencje, trudne do zniszczenia**
   Dwa obiekty nawzajem trzymają referencję na siebie (nawet zjawiska takie jak funkcje łapiące `self` we wbudowanych domknięciach, callbacks lub handlerach błędów w GUI). O ile wbudowany GC radzi sobie z takimi zależnościami regularnie odpytując, to w określonych i zawikłanych przypadkach (kiedyś były to nadpisane metody `__del__`, z których Python 3.3 i starsze sobie nie radziły) program może nie zwolnić pamięci.

4. **Wycieki wywołane bibliotekami z kompilowanymi rozszerzeniami (C-Extensions)**
   Zewnętrzne biblioteki (np. pisane w C) korzystające z FFI / ctypes, mogą przydzielić pamięć, o jakiej główny interpretator języka nie ma pojęcia i nie wie, że musi po niej posprzątać.

   
## Przykłady

### Wyciek w zmiennych globalnych (Nieskończony cache)

```python
results_cache = {}

def fetch_and_store_data(user_id, data):
    # Wyciek: Do słownika non stop dodajemy wartości,
    # nigdy ich nie wyrzucając / uplywając im ważności ttl
    results_cache[user_id] = data 
    return "Saved!"
```

### Wyciek poprzez callbacki w klasie

```python
class EventManager:
    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)
        
manager = EventManager()

class MyComponent:
    def __init__(self):
        # Trzymamy referencje, ten obiekt nie zniknie
        # nawet gdy usuniemy główne instancje klasy MyComponent 
        manager.register(self.on_event) 

    def on_event(self):
        pass
```


## Jak sobie z nimi radzić (rozwiązania)?

1. **Stosuj narządzia do profilowania pamięci**
   Jeżeli diagnozujesz wyciek, używaj domyślnych modułów w takich jak `tracemalloc` lub bibliotek zewnętrznych (`memory_profiler`, `objgraph`), aby znaleźć miejsce przydziału:
   
   ```python
   import tracemalloc
   
   tracemalloc.start()
   # ... kod wywolujacy problemy ...
   snapshot = tracemalloc.take_snapshot()
   top_stats = snapshot.statistics('lineno')
   for stat in top_stats[:5]:
       print(stat)
   ```

2. **Zastosowanie gotowych struktur do cachowania**
   Zamiast pisać cache i własne wózki w oparciu o globalne pola, korzystaj z narządzi w bibliotece standardowej. Na przykład wbudowane `@lru_cache` czy `@cache` z modułu `functools`, wprowadzając limity parametrów.
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=128)
   def fetch_data(item_id):
       return "Data"
   ```

3. **Weak references - 'Słabe referencje'**
   Pomagają, dając możliwość budowania referencji do obiektów z gwarancją "nie blokowaniu Garbage Collectora". Standardowa biblioteka `weakref` umożliwia stworzenie mapy wygasających powiązań. Gdy inny wskaźnik na ten zasób spada do zera i usuwany jest przez śmieciarza, wyparowuje on również stąd.

   ```python
   import weakref
   cache = weakref.WeakValueDictionary()
   ```

4. **Menedżery Kontekstu (Context Managers)**
   Gdy korzystasz z zasobów zamykaj je, co jest standardem - obiekty systemowe takie jak pliki znikną zaraz po opuszczeniu bloku bez obciążeń ze strony dewelopera:

   ```python
   # DO:
   with open('log.txt') as file:
       content = file.read()
       
   # NIE RÓB:
   f = open('log.txt') 
   # brak f.close() w przypadku podniesienia złośliwego błędu!
   ```
