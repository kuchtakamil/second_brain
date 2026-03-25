# Skrypt do monitorowania logów

**Data:** 2025-06-06

---

**User:**

Utwórz skrypt który można uruchomić w powłoce zsh który będzie robił następujące czynności:
Używając narzędzia stern zbierz logi z danego typu kontenerów używając komendy
stern ipt-regist-svc-kd -c ipt-registr-svc-kc
Teraz filtruj logi w poszukiwaniu logu
offca22 pfa: xxxxxxxxx
W miejscu xxxxxxxxx pojawi się ciąg cyfr o nieznanej długości. 

Teraz wykorzystaj ten ciąg cyfr aby co 1 sekundę uruchomić GET request http:
http://ipt-ms.co.hp.de/serviceDelicery/xxxxxxxxx 
Ten request zwróci JSONa. Teraz Przejdź jakimś dedykowanym narzędziem do konkretnego węzła tego JSONa a konkretnie do 
sd.details.process
i wyświetl zawartość na ekranie za każdym razem gdy otrzymasz odpowiedź od endpoint http.

---

**Assistant:**

Oto skrypt w ZSH, który realizuje opisany przez Ciebie scenariusz:

1. **Używa `stern`** do nasłuchiwania logów.
2. **Filtruje linie zawierające** wzorzec `offca22 pfa: xxxxxxxxx`.
3. **Wydobywa `xxxxxxxxx`**, czyli ID z logów.
4. Co sekundę wysyła **żądanie GET** do `http://ipt-ms.co.hp.de/serviceDelicery/xxxxxxxxx`.
5. **Parsuje JSON** i wyświetla zawartość `sd.details.process`.

Zakłada, że masz zainstalowane narzędzia `jq`, `curl` i `stern`.

### 📜 Skrypt `monitor_logs.zsh`

```zsh
#!/bin/zsh

# Funkcja do obsługi jednego ID (ciągu cyfr)
monitor_id() {
  local id=$1
  echo "Monitoring ID: $id"

  while true; do
    response=$(curl -s "http://ipt-ms.co.hp.de/serviceDelicery/${id}")
    if [[ -n "$response" ]]; then
      echo ">>> $(date):"
      echo "$response" | jq '.sd.details.process'
    else
      echo ">>> $(date): No response or invalid JSON"
    fi
    sleep 1
  done
}

# Uruchom stern i parsuj wyjście
stern ipt-regist-svc-kd -c ipt-registr-svc-kc | while read -r line; do
  if [[ "$line" =~ "offca22 pfa: "([0-9]+) ]]; then
    id="${match[1]}"
    echo "Found ID: $id"
    
    # Tylko pierwszy znaleziony ID uruchamia pętlę monitorującą
    # Jeśli chcesz uruchamiać monitorowanie dla wielu ID – zmodyfikuj tę część
    monitor_id "$id"
    break
  fi
done
```

### 🔧 Wymagania

- `stern`: do pobierania logów z K8s
- `jq`: do parsowania JSON-a
- `curl`: do wykonywania requestów HTTP

### ✅ Uruchomienie

Nadaj uprawnienia i uruchom:

```bash
chmod +x monitor_logs.zsh
./monitor_logs.zsh
```

---

Jeśli chcesz obsługiwać **wiele ID jednocześnie** (np. jeśli logi zawierają wiele `offca22 pfa: ...`), mogę zmodyfikować skrypt, by uruchamiał monitorowanie w osobnych procesach w tle. Chcesz taką wersję?

---

**User:**

czy ten skrypt dlla bash czymś by się różnił?

---

**Assistant:**

Tak, **zsh** i **bash** są do siebie bardzo podobne, więc Twój skrypt działałby niemal identycznie w obu powłokach. Różnice są minimalne i zazwyczaj dotyczą:

1. **Składni dopasowywania regexów w `[[ ... =~ ... ]]`**
2. **Obsługi tablic i rozbudowanych funkcji**
3. **Dostępu do grup dopasowań z regexów**

### 🔍 Konkretnie w Twoim przypadku:
Ten fragment:

```zsh
if [[ "$line" =~ "offca22 pfa: "([0-9]+) ]]; then
  id="${match[1]}"
```

Zadziała w **zsh**, bo `zsh` udostępnia tablicę `${match[n]}` z grupami regex.

W **bash** jednak **`match` nie istnieje**. Zamiast tego trzeba użyć `BASH_REMATCH`.

---

### ✅ Wersja dla **Bash**

Oto zmodyfikowany skrypt działający w `bash`:

```bash
#!/bin/bash

# Funkcja do obsługi jednego ID (ciągu cyfr)
monitor_id() {
  local id=$1
  echo "Monitoring ID: $id"

  while true; do
    response=$(curl -s "http://ipt-ms.co.hp.de/serviceDelicery/${id}")
    if [[ -n "$response" ]]; then
      echo ">>> $(date):"
      echo "$response" | jq '.sd.details.process'
    else
      echo ">>> $(date): No response or invalid JSON"
    fi
    sleep 1
  done
}

# Uruchom stern i parsuj wyjście
stern ipt-regist-svc-kd -c ipt-registr-svc-kc | while read -r line; do
  if [[ "$line" =~ offca22\ pfa:\ ([0-9]+) ]]; then
    id="${BASH_REMATCH[1]}"
    echo "Found ID: $id"
    
    monitor_id "$id"
    break
  fi
done
```

### 🔄 Różnice podsumowane:

| Element                  | ZSH                             | Bash                            |
|--------------------------|----------------------------------|----------------------------------|
| Grupa dopasowania regex  | `match[1]`                      | `BASH_REMATCH[1]`               |
| Tablice                  | `array=(a b)`                   | `array=(a b)`                   |
| Pętla `read`             | `while read -r line; do ...`    | tak samo                        |
| Wersja `[[ ... =~ ... ]]`| działa w obu, ale grupy inaczej | różni się tylko obsługa grup    |

---

Jeśli nie masz potrzeby korzystania z jakichś bardziej zaawansowanych funkcji `zsh`, to śmiało używaj `bash`. Ten skrypt jest w pełni przenośny między powłokami po drobnej korekcie.

---

**User:**

Pogubiłem się której wersji mam używać. Chcę uruchomić ten skrypt na macos. Który powinienem użyć?

---

**Assistant:**

Na **macOS**:

- **domyślną powłoką od Catalina (macOS 10.15)** jest **zsh**
- ale **bash też jest dostępny**, choć w wersji 3.2 (dość stara)

---

### ✅ Rekomendacja: **Użyj wersji dla zsh**

#### Dlaczego:
- Masz gwarancję, że skrypt będzie działał bez dodatkowej konfiguracji.
- macOS uruchamia `zsh` automatycznie jako powłokę logowania i interaktywną.
- Skrypt korzysta z wygodnej składni specyficznej dla `zsh` (`$match[1]`), której **bash 3.2 nie obsługuje poprawnie**.

---

### 🔧 Jak sprawdzić swoją powłokę:

```bash
echo $SHELL
```

Jeśli zobaczysz coś takiego:

```bash
/bin/zsh
```

to wszystko gra – użyj skryptu `zsh`.

---

### 🚀 Uruchomienie krok po kroku:

1. Stwórz plik:

```bash
nano monitor_logs.zsh
```

2. Wklej zawartość wersji `zsh` (tej pierwszej, którą Ci podałem).

3. Nadaj prawa do wykonania:

```bash
chmod +x monitor_logs.zsh
```

4. Uruchom:

```bash
./monitor_logs.zsh
```

---

Jeśli jednak **z jakiegoś powodu chcesz używać basha (np. do uruchamiania na innych systemach z bash 4+)**, wtedy lepiej użyj wersji `bash`, ale na macOS wymaga to dodatkowych kroków (np. instalacja nowszego basha przez Homebrew i przestawienie powłoki).

Chcesz takie instrukcje też?