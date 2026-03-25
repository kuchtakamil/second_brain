# Python: programy

**Data:** 2023-02-16

---

**User:**

Co oznacza w języku Python [:-8]?

---

**Assistant:**

W języku Python [:-8] oznacza wycinek (slice) listy lub ciągu znaków (string), który zwraca elementy od początku aż do ósmego elementu od końca. 

Na przykład, jeśli mamy listę:

```
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

To wycinek `[ : -8 ]` zwróci listę elementów od początku aż do elementu 3, włącznie:

```
>>> my_list[: -8]
[1, 2, 3]
```

Podobnie, jeśli mamy ciąg znaków:

```
my_string = "Hello, World!"
```

To wycinek `[ : -8 ]` zwróci ciąg znaków od początku aż do ósmego znaku od końca, włącznie:

```
>>> my_string[: -8]
'Hello, '
```

---

**User:**

Co w Python oznacza type?

---

**Assistant:**

W języku Python funkcja `type()` służy do zwracania typu obiektu. Jej składnia jest następująca:

```python
type(object)
```

Gdzie `object` jest obiektem, dla którego chcemy uzyskać jego typ.

Funkcja `type()` zwraca typ obiektu jako wartość. Na przykład, jeśli chcemy sprawdzić typ zmiennej `x`, możemy użyć funkcji `type()` w następujący sposób:

```python
x = 42
print(type(x))  # wyświetli <class 'int'>
```

W tym przypadku funkcja `type()` zwraca typ obiektu `x`, który jest liczbą całkowitą (int). Funkcja `type()` może być używana do określenia typu dowolnego obiektu w języku Python, takiego jak lista, krotka, słownik, ciąg znaków (string), funkcja i wiele innych.

---

**User:**

Napisz w języku Python program pobierający w pętli strony internetowe o następującym adresie
https://aperiodic.net/phil/scala/s-99/pXY.scala
gdzie XY jest liczbą od 01 do 99

---

**Assistant:**

Oto przykładowy program w języku Python, który pobiera strony internetowe o adresie https://aperiodic.net/phil/scala/s-99/pXY.scala, gdzie XY to liczby od 01 do 99, wykorzystując pętlę:

```python
import urllib.request

# Pobierz strony dla liczb od 1 do 99
for i in range(1, 100):
    # Formatuj adres URL dla liczby i
    url = f"https://aperiodic.net/phil/scala/s-99/p{i:02d}.scala"
    # Otwórz stronę i pobierz jej zawartość
    with urllib.request.urlopen(url) as response:
        html = response.read()
        # Wyświetl zawartość strony
        print(html)
```

W powyższym programie wykorzystano funkcję `urlopen()` z modułu `urllib.request`, aby otworzyć stronę internetową o danym adresie URL i pobrać jej zawartość. Pętla `for` iteruje przez liczby od 1 do 99 i formatuje adres URL za pomocą f-stringów, z numerem z wiodącym zerem dla liczb jednocyfrowych. Zawartość każdej strony jest wyświetlana za pomocą funkcji `print()`.

---

**User:**

Zamiast wyświetlania - print(html), zmodyfikuj program tak aby pobrane strony zapisywane dostawały na dysk.

---

**Assistant:**

Oto zmodyfikowany program, który pobiera strony o adresie `https://aperiodic.net/phil/scala/s-99/pXY.scala`, gdzie XY to liczby od 01 do 99, i zapisuje je na dysku:

```python
import urllib.request

# Pobierz strony dla liczb od 1 do 99 i zapisz na dysku
for i in range(1, 100):
    # Formatuj adres URL dla liczby i
    url = f"https://aperiodic.net/phil/scala/s-99/p{i:02d}.scala"
    # Pobierz zawartość strony
    with urllib.request.urlopen(url) as response:
        html = response.read()
        # Zapisz zawartość strony do pliku
        with open(f"page_{i:02d}.scala", "wb") as f:
            f.write(html)
```

W powyższym programie wykorzystano funkcję `open()` z trybem "wb" (binary write), aby utworzyć plik o nazwie `page_XX.scala`, gdzie `XX` to liczby od 01 do 99, i zapisać zawartość pobranej strony do pliku. Funkcja `write()` zapisuje zawartość strony w formacie binarnym, dlatego tryb "wb" jest tutaj używany.

Po wykonaniu tego programu, pliki `page_01.scala`, `page_02.scala`, `page_03.scala`, itd., będą dostępne w katalogu roboczym.

---

**User:**

dodaj do programu obsługę wyjątków w sytuacji gdy żądana strona nie będzie dostępna

---

**Assistant:**

Oto zmodyfikowany program, który pobiera strony o adresie `https://aperiodic.net/phil/scala/s-99/pXY.scala`, gdzie XY to liczby od 01 do 99, zapisuje je na dysku i obsługuje wyjątki w przypadku niepowodzenia pobrania strony:

```python
import urllib.request
import urllib.error

# Pobierz strony dla liczb od 1 do 99 i zapisz na dysku
for i in range(1, 100):
    # Formatuj adres URL dla liczby i
    url = f"https://aperiodic.net/phil/scala/s-99/p{i:02d}.scala"
    try:
        # Pobierz zawartość strony
        with urllib.request.urlopen(url) as response:
            html = response.read()
            # Zapisz zawartość strony do pliku
            with open(f"page_{i:02d}.scala", "wb") as f:
                f.write(html)
    except urllib.error.URLError as e:
        print(f"Nie udało się pobrać strony {url}: {e}")
    except Exception as e:
        print(f"Wystąpił nieznany wyjątek podczas pobierania strony {url}: {e}")
```

W powyższym programie dodano klauzulę `try-except`, która obsługuje wyjątki `URLError` z modułu `urllib.error` oraz wyjątki ogólne `Exception`. W przypadku wystąpienia wyjątku, program wyświetla komunikat o błędzie i kontynuuje pobieranie kolejnych stron.

Po wykonaniu tego programu, pliki `page_01.scala`, `page_02.scala`, `page_03.scala`, itd., będą dostępne w katalogu roboczym, jeśli ich pobieranie zakończyło się sukcesem.

---

**User:**

Napisz program w języku Python który w każdej linijce każdego pliku o rozszerzeniu .sc w danym folderze, wstawia na początku znaki "//"

---

**Assistant:**

Oto program w języku Python, który wstawia znaki `//` na początku każdej linii w każdym pliku o rozszerzeniu `.sc` w danym folderze:

```python
import os

# Wstawia znaki // na początku każdej linii w pliku
def add_comment(filename):
    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            file.write('//'+line)
        file.truncate()

# Pobierz wszystkie pliki o rozszerzeniu .sc w bieżącym katalogu
files = [f for f in os.listdir('.') if f.endswith('.sc')]

# Wstaw znaki // na początku każdej linii w każdym pliku
for filename in files:
    add_comment(filename)
```

Program działa w następujący sposób:

1. Definiuje funkcję `add_comment`, która otrzymuje nazwę pliku i wstawia znaki `//` na początku każdej linii w pliku.
2. Pobiera listę nazw plików o rozszerzeniu `.sc` w bieżącym katalogu.
3. Dla każdego pliku z listy, wykonuje funkcję `add_comment`, wstawiając znaki `//` na początku każdej linii w pliku.

Po wykonaniu programu, każdy plik o rozszerzeniu `.sc` w bieżącym katalogu będzie miał na początku każdej linii wstawione znaki `//`. Warto jednak pamiętać, że operacja ta jest nieodwracalna, a pliki oryginalne zostaną nadpisane plikami zmodyfikowanymi.

---

**User:**

Do poprzedniego programu dodaj zapisywanie zmian w plikach

---

**Assistant:**

Oto zmodyfikowany program, który wstawia znaki `//` na początku każdej linii w każdym pliku o rozszerzeniu `.sc` w danym folderze oraz zapisuje zmodyfikowane pliki:

```python
import os

# Wstawia znaki // na początku każdej linii w pliku
def add_comment(filename):
    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            file.write('//'+line)
        file.truncate()

# Pobierz wszystkie pliki o rozszerzeniu .sc w bieżącym katalogu
files = [f for f in os.listdir('.') if f.endswith('.sc')]

# Wstaw znaki // na początku każdej linii w każdym pliku i zapisz zmiany
for filename in files:
    add_comment(filename)
    print(f"Zmieniono plik: {filename}")
```

W zmodyfikowanym programie po wykonaniu funkcji `add_comment`, dodano instrukcję `print`, która wyświetla nazwę pliku, którego zawartość została zmodyfikowana. Dzięki temu, po wykonaniu programu, będziemy mieli informację o zmianach w każdym pliku.

Warto jednak pamiętać, że operacja ta jest nieodwracalna, a pliki oryginalne zostaną nadpisane plikami zmodyfikowanymi. Przed wykonaniem programu warto wykonać kopię zapasową plików lub zapisywać zmodyfikowane pliki pod innymi nazwami.

---

**User:**

Napisz program w języku Python który w każdej linijce każdego pliku o rozszerzeniu .sc w danym folderze, usuwa na początku znaki "//" jeśli tam są.

---

**Assistant:**

Oto program w języku Python, który usuwa znaki `//` na początku każdej linii w każdym pliku o rozszerzeniu `.sc` w danym folderze:

```python
import os

# Usuwa znaki // na początku każdej linii w pliku
def remove_comment(filename):
    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line.startswith('//'):
                line = line[2:]
            file.write(line)
        file.truncate()

# Pobierz wszystkie pliki o rozszerzeniu .sc w bieżącym katalogu
files = [f for f in os.listdir('.') if f.endswith('.sc')]

# Usuń znaki // na początku każdej linii w każdym pliku i zapisz zmiany
for filename in files:
    remove_comment(filename)
    print(f"Zmieniono plik: {filename}")
```

Program działa w następujący sposób:

1. Definiuje funkcję `remove_comment`, która otrzymuje nazwę pliku i usuwa znaki `//` na początku każdej linii w pliku.
2. Pobiera listę nazw plików o rozszerzeniu `.sc` w bieżącym katalogu.
3. Dla każdego pliku z listy, wykonuje funkcję `remove_comment`, usuwając znaki `//` na początku każdej linii w pliku.

Po wykonaniu programu, każdy plik o rozszerzeniu `.sc` w bieżącym katalogu będzie miał usunięte znaki `//` na początku każdej linii. Warto jednak pamiętać, że operacja ta jest nieodwracalna, a pliki oryginalne zostaną nadpisane plikami zmodyfikowanymi. Przed wykonaniem programu warto wykonać kopię zapasową plików lub zapisywać zmodyfikowane pliki pod innymi nazwami.

---

**User:**

Napisz program w Python który dla każdego pliku o rozszerzeniu .sc, utworzy nowy katalog o tej nazwie co plik i przeniesie ten plik do tego nowego katalogu.

---

**Assistant:**

Oto program w języku Python, który tworzy nowy katalog o nazwie pliku bez rozszerzenia `.sc` i przenosi plik o rozszerzeniu `.sc` do tego nowego katalogu:

```python
import os
import shutil

# Pobierz wszystkie pliki o rozszerzeniu .sc w bieżącym katalogu
files = [f for f in os.listdir('.') if f.endswith('.sc')]

# Dla każdego pliku tworzy nowy katalog i przenosi plik do tego katalogu
for filename in files:
    dir_name = os.path.splitext(filename)[0] # Nazwa katalogu to nazwa pliku bez rozszerzenia
    os.makedirs(dir_name, exist_ok=True) # Tworzy nowy katalog lub ignoruje jeśli już istnieje
    shutil.move(filename, os.path.join(dir_name, filename)) # Przenosi plik do nowego katalogu
    print(f"Przeniesiono plik {filename} do katalogu {dir_name}")
```

Program działa w następujący sposób:

1. Pobiera listę nazw plików o rozszerzeniu `.sc` w bieżącym katalogu.
2. Dla każdego pliku z listy, tworzy nowy katalog o nazwie pliku bez rozszerzenia `.sc`.
3. Przenosi plik do nowego katalogu.
4. Wyświetla komunikat informujący o przeniesieniu pliku do nowego katalogu.

Po wykonaniu programu, każdy plik o rozszerzeniu `.sc` w bieżącym katalogu zostanie przeniesiony do nowego katalogu o tej samej nazwie, co nazwa pliku bez rozszerzenia `.sc`.