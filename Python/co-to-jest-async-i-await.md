# Co to jest async i await? (Temat na job interview)

**Podsumowanie**
`async` i `await` to słowa kluczowe w Pythonie służące do programowania asynchronicznego, które zyskało ogromną popularność za sprawą frameworków takich jak FastAPI czy `asyncio`. Pozwalają na pisanie kodu współbieżnego (concurrent), który w strukturze przypomina standardowy, synchroniczny kod. Ich głównym celem jest efektywne zarządzanie czasem przy operacjach wejścia/wyjścia (I/O-bound), takich jak: zapytania sieciowe, czytanie/zapis do bazy danych, obsługa plików.

## Co tworzą te instrukcje?

1. **`async def`**: Postawienie słowa `async` przed funkcją sprawia, że tworzymy **korutynę** (ang. *coroutine*). Gdy wywołasz taką funkcję, kod w jej wnętrzu nie wykonuje się od razu. Zamiast tego funkcja zwraca obiekt typu coroutine, który mówi "oto kawałek pracy do wykonania". Żeby kod zaczął działać, ten obiekt musi zostać przekazany do pętli zdarzeń (Event Loop).
2. **`await`**: Słowo kluczowe `await` można stosować tylko wewnątrz korutyn (tzn. funkcji `async def`). Położenie `await` przed operacją asynchroniczną zatrzymuje działanie *obecnej* korutyny i oddaje kontrolę z powrotem do Event Loopa. Dzięki temu system się nie zawiesza i pętla zdarzeń może wykonywać w tym czasie inny fragment kodu. Gdy oczekiwane zdarzenie (np. pobranie danych z internetu) się zakończy, korutyna, która użyła `await`, zostanie wznowiona.

## Jak używać?

Korzystamy z nich w miejscach, w których program musiałby bezczynnie czekać na zewnętrzny czynnik. 

**Kluczowe koncepcje, którymi zabłyśniesz na rozmowie rekrutacyjnej:**
- **Event Loop (Pętla Zdarzeń):** Jest "dyrygentem" całego procesu. Ciągle sprawdza, które korutyny można wznowić, a które jeszcze na coś czekają, zarządzając przełączaniem kontekstu między zadaniami w sposób inteligentny.
- **Kooperatywna wielozadaniowość (Cooperative multitasking):** Poszczególne korutyny muszą współpracować. To one (poprzez wywołanie `await`) "świadomie" zwalniają procesor, aby inna korutyna mogła zająć się swoją pracą. Nie robi tego system operacyjny w sposób wymuszony.
- **I/O Bound vs CPU Bound:** Jeśli coś liczy silnię z ogromnej liczby, zablokuje całą pętlę zdarzeń (CPU Bound). `async` i `await` używa się dla operacji (I/O Bound).

### Przykład użycia

```python
import asyncio
import time

async def fetch_data(id_zadania: int) -> dict:
    print(f"[{id_zadania}] Rozpoczynam pobieranie danych...")
    # Symulacja czekania na odpowiedź z zewnętrznego API
    await asyncio.sleep(2)
    print(f"[{id_zadania}] Zakończono pobieranie.")
    return {"id": id_zadania, "dane": "sukces"}

async def main():
    start = time.time()
    
    # asyncio.gather przyjmuje wiele zadań asynchronicznych 
    # i pozwala wykonać je współbieżnie.
    wyniki = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    
    czas_trwania = time.time() - start
    print(f"Wszystkie zadania wykonane w: {czas_trwania:.2f} sekund")
    print("Wyniki:", wyniki)

if __name__ == "__main__":
    # Punkt wejścia - asyncio.run uruchamia nową pętlę zdarzeń 
    # i przekazuje jej główną korutynę do wykonania.
    asyncio.run(main())
```

Gdyby ten kod napisano klasycznie (z użyciem synchronicznego `time.sleep()`), wykonanie całości potrwałoby 6 sekund. Dzięki `async` i `await` program uwalnia kontrolę podczas czekania, a cały skrypt wykonuje się w nieco ponad 2 sekundy.

## O co na 100% dopytają na rekrutacji?

- **"Czy `async/await` pozwala obejść GIL (Global Interpreter Lock)?"**
  - **Nie.** Cały kod i wszystkie korutyny w powyższym przykładzie wykonują się i tak w **jednym procesie** i w **jednym wątku systemu operacyjnego**. Nie wykorzystujemy wielu rdzeni procesora. Zysk z wydajności wynika ze sprytnego "upychania" roboty w wolnych szczelinach czasu (kiedy czekamy na odpowiedź serwera, robimy coś innego).
- **"Dlaczego asynchroniczność w Pythonie nazywa się "wirusową/zaraźliwą"?"**
  - Ponieważ jeśli użyjesz `await` w środku funkcji, sama funkcja musi stać się `async`. Skoro ona stała się `async`, to jej rodzic, żeby z niej skorzystać i jej nie zablokować, również musi użyć `await` i stać się `async`. Rozprzestrzenia się to w górę łańcucha wywołań (aż do samego uruchomienia event loopa na start aplikacji, lub aż framework to sam obsłuży za nas, np. w FastAPI).

## Powiązane pliki w Twojej bazie
- [Opisz async i await w Python](opisz-async-i-await-w-python.md)
- [Async await w Pythonie (praktyczne rozwiązanie)](async-await-w-pythonie.md)
- [Gil w Pythonie](gil-w-pythonie.md)
- [Zrozumienie GIL w Pythonie](zrozumienie-gil-w-pythonie.md)
