# Porównywanie plików tekstowych

**Data:** 2024-08-08

---

**User:**

Jak w Linux porównać treść 2 plików tekstowych linia po linii

---

**Assistant:**

W Linuksie istnieje kilka narzędzi, które pozwalają na porównanie zawartości dwóch plików tekstowych linia po linii. Oto kilka najczęściej używanych metod:

### 1. `diff`
Najpopularniejsze narzędzie do porównywania plików tekstowych w Linuksie. Wyświetla różnice między dwoma plikami.

```bash
diff plik1.txt plik2.txt
```

Możesz także użyć opcji `-u`, aby uzyskać bardziej czytelny format "unified diff":

```bash
diff -u plik1.txt plik2.txt
```

### 2. `comm`
To narzędzie służy do porównywania dwóch plików wiersz po wierszu. Pliki muszą być posortowane, aby `comm` działało poprawnie.

```bash
comm plik1.txt plik2.txt
```

Wynik jest podzielony na trzy kolumny:
- Pierwsza kolumna zawiera wiersze, które są tylko w `plik1.txt`.
- Druga kolumna zawiera wiersze, które są tylko w `plik2.txt`.
- Trzecia kolumna zawiera wiersze, które są wspólne dla obu plików.

Jeśli chcesz wykluczyć którąś z kolumn, użyj odpowiednich opcji `-1`, `-2`, `-3`.

### 3. `sdiff`
Wyświetla porównanie dwóch plików obok siebie, co ułatwia identyfikację różnic linia po linii.

```bash
sdiff plik1.txt plik2.txt
```

### 4. `vimdiff`
Jest to narzędzie, które wykorzystuje edytor `vim` do wizualnego porównania plików.

```bash
vimdiff plik1.txt plik2.txt
```

Vim otworzy oba pliki obok siebie, pokazując różnice w kolorach.

### 5. `meld`
Jest to narzędzie z graficznym interfejsem użytkownika, które umożliwia wygodne porównywanie plików i katalogów.

Aby użyć meld, najpierw zainstaluj go (jeśli jeszcze go nie masz):

```bash
sudo apt-get install meld
```

Następnie uruchom:

```bash
meld plik1.txt plik2.txt
```

Każda z tych metod ma swoje zalety, w zależności od tego, czy potrzebujesz prostego porównania tekstowego, czy bardziej zaawansowanego, graficznego narzędzia do analizy różnic.

---

**User:**

ok, używając jednego z tych narzędzi, wyświetl nazwy plików które nie istnieją w plik1.txt a istnieją w plik2txt

---

**Assistant:**

Do tego zadania najlepiej nadaje się narzędzie `comm`, które pozwala na porównanie dwóch posortowanych plików wiersz po wierszu. Poniżej znajduje się przykładowy sposób, w jaki możesz użyć tego narzędzia, aby wyświetlić linie (nazwy plików), które występują w `plik2.txt`, ale nie ma ich w `plik1.txt`.

### Krok 1: Posortuj oba pliki
Przed użyciem `comm`, upewnij się, że oba pliki są posortowane. Możesz to zrobić przy użyciu polecenia `sort`:

```bash
sort plik1.txt -o plik1_sorted.txt
sort plik2.txt -o plik2_sorted.txt
```

### Krok 2: Użyj `comm` do porównania plików
Następnie użyj `comm` z opcją `-23`, aby wyświetlić linie, które są tylko w drugim pliku (`plik2.txt`):

```bash
comm -23 plik2_sorted.txt plik1_sorted.txt
```

### Wyjaśnienie opcji:
- `-2`: Ukrywa linie, które występują tylko w `plik1.txt`.
- `-3`: Ukrywa linie, które są wspólne dla obu plików.

W ten sposób otrzymasz listę nazw plików, które są obecne w `plik2.txt`, ale brakuje ich w `plik1.txt`.

---

**User:**

Chciałbym mieć tę listę nazw pliku w jednym wierszu oddzielone spacjami

---

**Assistant:**

Aby uzyskać listę nazw plików, które są w `plik2.txt` ale nie ma ich w `plik1.txt`, w jednym wierszu oddzielonych spacjami, możesz wykonać poniższe kroki.

### Krok 1: Posortuj oba pliki

```bash
sort plik1.txt -o plik1_sorted.txt
sort plik2.txt -o plik2_sorted.txt
```

### Krok 2: Użyj `comm` i przekształć wynik w jedną linię

Następnie użyj `comm` i polecenia `tr` (lub `xargs`), aby przekształcić wynik w jedną linię:

```bash
comm -23 plik2_sorted.txt plik1_sorted.txt | tr '\n' ' '
```

### Wyjaśnienie:
- `comm -23 plik2_sorted.txt plik1_sorted.txt`: Porównuje dwa pliki i wyświetla linie, które są tylko w `plik2_sorted.txt`.
- `tr '\n' ' '`: Zastępuje wszystkie znaki nowej linii (`\n`) spacjami (` `).

To polecenie wyświetli wyniki w jednej linii, oddzielając poszczególne nazwy plików spacjami.