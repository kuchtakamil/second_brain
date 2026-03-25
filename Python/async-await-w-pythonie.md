# Async await w Pythonie

**Data:** 2025-09-13

---

**User:**

Python i async await. Mam problem ze zrozumieniem praktycznej strony użycia tego mechanizmu. 
await może być użyte tylko w funkcjach które są async. Więc gdy w pewnym momecie chciałbym użyć await na jakimś corouitne (async),  muszę to miejsce wywołania również oznaczyć jako async. A to zmienione miejsce trzeba już w następnym miejscu wywołać w inny sposób używając await i znowu dodać async i tak w górę stosu wywołania aż do samego końca. Czy mam rację? jeśli tak to chybabardzo niepraktyczne

---

**Assistant:**

Masz rację co do zasady – jeśli w pewnym miejscu chcesz użyć `await`, to ta funkcja musi być oznaczona jako `async`. To „wymusza” propagację asynchroniczności w górę stosu wywołań. I rzeczywiście, czasami wygląda to niepraktycznie, zwłaszcza gdy zaczynasz dopiero używać tego modelu.  

Ale jest kilka rzeczy, które pomagają to zrozumieć:  

---

### 1. Dlaczego tak to działa?
Asynchroniczność w Pythonie (`async/await`) nie działa jak „magiczne wątki”, tylko jako **kooperatywne coroutines**. To oznacza, że:
- `await` zatrzymuje wykonywanie bieżącej funkcji *w tym miejscu*, oddaje kontrolę do event loopa, a ta funkcja „obudzi się” później, gdy rezultat będzie gotowy.  
- Aby to było możliwe, cała funkcja musi być w stanie zostać przerwana i wznowiona → dlatego jest `async def`.

Czyli: jeśli jedna funkcja „czeka”, jej wywołująca także musi umieć poczekać → i to idzie w górę stosu.

---

### 2. Gdzie ta „drabinka async” się kończy?
Zwykle na samym szczycie programu:
- w **aplikacjach webowych** (FastAPI, aiohttp, Django async) to framework uruchamia Twój kod w event loopie → Ty możesz wszędzie pisać `async` i `await`, a na samym początku nie martwisz się o wywołanie.
- w **skryptach** pisanych samodzielnie kończy się to na `asyncio.run(...)`, np.:

```python
import asyncio

async def main():
    result = await do_something()
    print(result)

asyncio.run(main())
```

`asyncio.run` to taki „pomost” między zwykłym kodem synchronicznym (który startuje Pythona) a światem `async`.

---

### 3. Czy to faktycznie niepraktyczne?
Na pierwszy rzut oka tak, bo async „rozlewa się” po kodzie. Ale ma to sens:  
- Wymusza jawność – wiesz, które funkcje mogą się zatrzymać (yieldować kontrolę).  
- Masz kontrolę nad równoległością (np. `await asyncio.gather(...)`).  
- Unikasz ukrytych blokad, bo gdy coś jest `await`, od razu widać, że może „czekać”.

W praktyce w dużych aplikacjach jest tak, że:
- na styku ze „światem zewnętrznym” (np. web serwer, CLI) masz jedno miejsce, które odpala `asyncio.run`.
- potem cały kod aplikacji jest już async i używa `await` tam, gdzie trzeba.  

To trochę jak z `const` w C++: na początku wkurza, że propaguje się wszędzie, ale finalnie daje spójność.

---

### 4. Hybryda sync i async
Możesz też mieć kod synchroniczny i asynchroniczny obok siebie. Typowy pattern:
- Funkcje „biznesowe” możesz pisać jako synchroniczne (`def`), jeśli nie używają `await`.  
- Tylko tam, gdzie musisz robić I/O (sieć, pliki, sleep), dajesz `async`.  

---

Chcesz, żebym pokazał Ci prosty przykład **dwóch wersji tej samej aplikacji** (jedna synchroniczna, druga async), żeby było widać praktyczną różnicę?

---

**User:**

OK. 
Skoro w Python jest Global Interpreter Lock to dlaczego istnieje potrzeba używając Coroutines aby synchornizować pewne rzeczy np. używając asyncio.Lock()?

---

**Assistant:**

Dobre pytanie. To, że w Pythonie istnieje **GIL** (Global Interpreter Lock), nie oznacza, że nie potrzeba synchronizacji w świecie `asyncio`.  

---

### 1. Co robi GIL?
- GIL pilnuje, żeby w **danym procesie** tylko **jeden wątek naraz** wykonywał kod Pythona (bytecode).  
- Dzięki temu interpreter nie musi synchronizować dostępu do wielu struktur wewnętrznych (np. zarządzania pamięcią).  
- Ale GIL **nie chroni Twojej logiki biznesowej** ani nie daje gwarancji atomowości operacji na obiektach wyższego poziomu.  

---

### 2. Jak działa `asyncio`?
- `asyncio` to **jednowątkowa pętla zdarzeń**.  
- W danym momencie działa tylko jedna coroutine, ale może się zatrzymać w `await` i wtedy w jej miejsce wchodzi inna.  
- To oznacza, że nawet bez wielu wątków masz **współbieżność**: dwie coroutines mogą naprzemiennie modyfikować ten sam obiekt.  

---

### 3. Dlaczego potrzebny `asyncio.Lock`?
Weź przykład:

```python
import asyncio

counter = 0

async def increment(name):
    global counter
    tmp = counter
    await asyncio.sleep(0.1)  # oddanie sterowania!
    counter = tmp + 1
    print(f"{name} -> {counter}")

async def main():
    await asyncio.gather(increment("A"), increment("B"), increment("C"))

asyncio.run(main())
```

Wynik może być np.:

```
A -> 1
B -> 1
C -> 1
```

Dlaczego?  
1. `A` czyta `counter = 0`, odkłada go w `tmp`, robi `await asyncio.sleep`.  
2. Wchodzi `B`, robi to samo.  
3. Wchodzi `C`.  
4. Potem każdy nadpisuje `counter` swoją wersją `tmp + 1`.  

Czyli klasyczny race condition — mimo że wszystko działa w jednym wątku i z GIL-em.  

---

### 4. Rozwiązanie: `asyncio.Lock`

```python
import asyncio

counter = 0
lock = asyncio.Lock()

async def increment(name):
    global counter
    async with lock:
        tmp = counter
        await asyncio.sleep(0.1)
        counter = tmp + 1
        print(f"{name} -> {counter}")

async def main():
    await asyncio.gather(increment("A"), increment("B"), increment("C"))

asyncio.run(main())
```

Tutaj `asyncio.Lock` gwarantuje, że tylko jedna coroutine naraz może wejść do sekcji krytycznej. Pozostałe muszą poczekać.  

---

### 5. Podsumowanie
- **GIL** rozwiązuje problem bezpieczeństwa samego interpretera Pythona (pamięć, struktury wewnętrzne).  
- **`asyncio.Lock`** rozwiązuje problem współbieżnego dostępu do Twoich danych, bo coroutines mogą być przełączone w dowolnym miejscu, gdzie używasz `await`.  

---

Chcesz, żebym pokazał Ci przykład podobnej sytuacji, ale z **prawdziwym I/O** (np. zapis do pliku albo wysyłka do API), gdzie brak locka może wywołać bałagan?