# Pakiety do wielowątkowości i wieloprocesowości w Pythonie

Python oferuje kilka wbudowanych pakietów do zarządzania współbieżnością i zrównoleglaniem zadań. W zależności od charakteru problemu (I/O-bound czy CPU-bound) programiści najczęściej sięgają po pakiety `threading`, `multiprocessing` oraz abstrakcję wyższego poziomu – `concurrent.futures`.

Więcej na temat mechanizmów w tle możesz przeczytać w [zrozumienie-gil-w-pythonie.md](zrozumienie-gil-w-pythonie.md).

## 1. Moduł `threading` (Wielowątkowość)

Pakiet `threading` służy do pracy z wieloma wątkami (threads). Należy pamiętać, że z powodu istnienia blokady GIL (Global Interpreter Lock), tylko jeden wątek w danym momencie wykonuje kod bajtowy Pythona. Oznacza to, że wątki **nie przyśpieszą** zadań mocno obciążających procesor (CPU-bound). Sprawdzają się natomiast idealnie w zadaniach obciążających wejście/wyjście (I/O-bound), takich jak pobieranie danych z sieci, czytanie z dysku lub czekanie na odpowiedź z bazy danych.

### Jak to działa?
Gdy jeden wątek czeka na operację I/O, GIL jest zwalniany, a interpreter pozwala innemu wątkowi na wykonywanie kodu. Dzięki temu aplikacja nie blokuje się na pojedynczym zapytaniu sieciowym.

```python
import threading
import time

def worker(worker_id):
    print(f"Wątek {worker_id} zaczyna pracę")
    time.sleep(2)  # Symulacja operacji I/O (np. zapytanie sieciowe)
    print(f"Wątek {worker_id} kończy pracę")

# Tworzenie i uruchamianie wątków
threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

# Czekanie na zakończenie wszystkich wątków
for t in threads:
    t.join()

print("Wszystkie wątki zakończone.")
```

## 2. Moduł `multiprocessing` (Wieloprocesowość)

Pakiet `multiprocessing` omija ograniczenia GIL poprzez tworzenie oddzielnych procesów na poziomie systemu operacyjnego. Każdy nowo utworzony proces ma swój własny interpreter Pythona i własną przestrzeń pamięci (własny GIL). Dzięki temu `multiprocessing` pozwala na rzeczywiste zrównoleglenie zadań CPU-bound, czyli takich, które wymagają dużej mocy obliczeniowej (np. przetwarzanie obrazów, skomplikowane obliczenia numeryczne).

### Narzut (Overhead)
Tworzenie nowych procesów i komunikacja między nimi (np. przesyłanie danych poprzez obiekty typu `Queue` czy `Pipe`) jest znacznie droższe pamięciowo i czasowo niż w przypadku lekkich wątków z modułu `threading`. Należy to brać pod uwagę przy małych, bardzo krótkich zadaniach - narzut utworzenia procesu może przewyższyć zyski z paralelizacji.

```python
import multiprocessing
import time

def compute_heavy_task(number):
    print(f"Proces {number} rozpoczął pracę")
    # Symulacja intensywnych obliczeń
    result = sum(i * i for i in range(10**7))
    print(f"Proces {number} zakończył pracę")
    return result

if __name__ == '__main__':
    processes = []
    
    # Tworzymy procesy manualnie
    for i in range(3):
        p = multiprocessing.Process(target=compute_heavy_task, args=(i,))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    print("Wszystkie procesy zakończone.")
```

## 3. Moduł `concurrent.futures` (Wysokopoziomowa abstrakcja)

Chociaż można zarządzać wątkami i procesami ręcznie, nowoczesny kod Pythonowy preferuje używanie modułu `concurrent.futures`. Udostępnia on interfejs tzw. "pul roboczych" (Executors): 
- `ThreadPoolExecutor` (do zarządzania pulą wątków),
- `ProcessPoolExecutor` (do zarządzania pulą procesów).

Dzięki temu narzędziu nie musimy samodzielnie tworzyć wątków/procesów, ani wywoływać na nich `.start()` czy `.join()`. Moduł ten pozwala na zgłaszanie zadań (zadań do wykonania) wprost do puli. Zwraca on obiekty typu `Future`, które reprezentują odroczone w czasie (przyszłe) wyniki wykonanych zadań.

```python
import concurrent.futures
import time

def process_data(data_chunk):
    time.sleep(1) # Symulacja pracy I/O
    return f"Przetworzono: {data_chunk}"

if __name__ == '__main__':
    data = ['Plik A', 'Plik B', 'Plik C', 'Plik D']
    
    # Dla operacji I/O używamy ThreadPoolExecutor
    # Dla CPU-bound użylibyśmy ProcessPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Metoda map automatycznie przydziela zadania z listy i zwraca iterowalny
        # generator wyników (w tej samej kolejności co podane wejście)
        results = executor.map(process_data, data)
        
        for r in results:
            print(r)
```

## Podsumowanie i zasady kciuka:

- **Zadania I/O-bound** (zapytania HTTP, bazy danych, czytanie dużych plików z dysku): Użyj `threading` (a najlepiej `concurrent.futures.ThreadPoolExecutor`).
- **Zadania CPU-bound** (przetwarzanie i transformacje danych, szyfrowanie, kompresja, obliczenia uczenia maszynowego): Użyj `multiprocessing` (a najlepiej `concurrent.futures.ProcessPoolExecutor`).
- Dla większości standardowych przypadków preferuj abstrakcję `concurrent.futures` nad bezpośrednią obsługą API `threading` lub `multiprocessing`, ponieważ dzięki Executorom kod staje się dużo czystszy, bezpieczniejszy i łatwiejszy do skalowania.
