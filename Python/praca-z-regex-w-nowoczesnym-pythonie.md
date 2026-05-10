# Praca z Regex w nowoczesnym Pythonie

## Krótkie podsumowanie
Wyrażenia regularne (regex) w Pythonie obsługuje wbudowany moduł `re`. Służą do zaawansowanego dopasowywania, wyszukiwania, dzielenia i podmieniania wzorców tekstowych. W nowoczesnym kodzie stawia się na czytelność: używanie surowych ciągów znaków (raw strings `r""`), nazwanych grup oraz kompilację wzorców dla optymalizacji wydajności.

## Dlaczego i kiedy to ma znaczenie
- **Walidacja danych:** Sprawdzanie poprawności formatów (np. e-mail, numer telefonu, PESEL, kody pocztowe).
- **Ekstrakcja informacji (Web Scraping / Parsowanie logów):** Wyciąganie konkretnych danych ustrukturyzowanych z nieustrukturyzowanego, długiego tekstu.
- **Zaawansowana modyfikacja tekstu:** Masowa i warunkowa zmiana określonych wzorców (metoda `re.sub()`).

*Zasada kciuka:* Stosuj regexy tam, gdzie wbudowane metody ciągów znaków (`str.split()`, `str.replace()`, `str.startswith()`) stają się niewystarczające lub wymagają zagnieżdżonych pętli/instrukcji warunkowych. Unikaj ich przy prostych operacjach, ponieważ są trudniejsze w utrzymaniu i wolniejsze w wykonaniu.

## Jak to działa w praktyce

### 1. Surowe ciągi znaków (Raw Strings)
Zawsze definiuj regex jako surowy ciąg, dodając przedrostek `r` (np. `r"wzorzec"`). Zapobiega to interpretacji znaków ucieczki (backslash `\`) przez Pythona, pozostawiając je dla silnika wyrażeń regularnych.

```python
import re

# Zamiast "\\bword\\b" (escape backslasha)
pattern = r"\bword\b" 
```

### 2. Główne metody modułu `re`
- `re.search()`: Szuka pierwszego dopasowania w dowolnym miejscu ciągu znaków.
- `re.match()`: Wymaga dopasowania od samego początku ciągu znaków.
- `re.fullmatch()`: Wymaga, aby wzorzec dopasował cały ciąg znaków (od początku do końca).
- `re.findall()`: Zwraca listę wszystkich znalezionych dopasowań jako stringi (lub krotki, jeśli są grupy).
- `re.finditer()`: Zwraca iterator obiektów `Match`. Zalecane przy pracy z dużymi tekstami, mniejsze zużycie pamięci i dostęp do indeksów/grup.
- `re.sub()`: Podmienia znalezione wystąpienia na nowy tekst.

### 3. Kompilacja wzorców (Optymalizacja)
Jeśli używasz konkretnego regexa wielokrotnie (np. w pętli walidującej listę), skompiluj go wcześniej. 

```python
import re

# Kompilacja wzorca zwraca obiekt re.Pattern
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

def extract_emails(text: str) -> list[str]:
    return EMAIL_PATTERN.findall(text)
```

### 4. Nazwane grupy (Named Groups)
Stanowią kluczową funkcjonalność zwiększającą czytelność. Pozwalają "nazwać" konkretny fragment dopasowania i pobrać go jako słownik.
Składnia definiowania: `(?P<nazwa>wzorzec)`

```python
import re

log = "Error 404 at 2023-10-01: Not Found"
pattern = re.compile(r"Error (?P<code>\d+) at (?P<date>\d{4}-\d{2}-\d{2}): (?P<msg>.*)")

match = pattern.search(log)
if match:
    # Pobieranie wyekstrahowanych danych w postaci słownika
    data = match.groupdict() 
    print(data) # {'code': '404', 'date': '2023-10-01', 'msg': 'Not Found'}
    
    # Pobieranie po nazwie
    print(match.group('code')) # '404'
```

### 5. Flagi w nowoczesnym kodzie
Modyfikują domyślne zachowanie wyrażeń. Należy przekazywać je jako bitowe operatory OR (`|`).
- `re.IGNORECASE` (lub `re.I`): Brak rozróżniania wielkości liter.
- `re.VERBOSE` (lub `re.X`): Umożliwia pisanie regexów wieloliniowych z komentarzami, ignorując przy tym białe znaki (bardzo przydatne dla skomplikowanych wzorców!).
- `re.MULTILINE` (lub `re.M`): Zmienia zachowanie znaków `^` i `$`, aby dopasowywały odpowiednio początek i koniec każdej linii, a nie całego ciągu.

```python
import re

# re.VERBOSE drastycznie poprawia czytelność skomplikowanego regexa
pattern = re.compile(r"""
    ^                   # Dopasowanie do początku
    (?P<user>[a-z]+)    # Grupa user: Nazwa użytkownika
    @                   # Małpa
    (?P<domain>[a-z]+)  # Grupa domain: Domena
    \.com               # TLD
    $                   # Dopasowanie do końca
""", re.VERBOSE | re.IGNORECASE)
```

### 6. Alternatywa: moduł `regex`
Dla bardzo zaawansowanych zastosowań (np. parsowanie bardzo złożonych struktur) moduł wbudowany `re` bywa niewystarczający. W takich wypadkach korzysta się z zewnętrznej biblioteki `regex` (`pip install regex`). Zapewnia ona pełną wsteczną kompatybilność z modułem wbudowanym, a dodaje m.in.:
- Lookbehind o zmiennej długości (np. `(?<=a+)b`).
- Dopasowania rozmyte (Fuzzy matching, z tolerancją na literówki).
- Wsparcie dla rekurencji wyrażeń (np. obsługiwanie dowolnie zagnieżdżonych nawiasów).
- Kwantyfikatory posesywne i grupy atomowe.

## Powiązane pliki
- [Wyjaśnienie regexa w pythonie](wyjaśnienie-regexa-w-pythonie.md)
- [Nawiasy w wyrażeniu regularnym](nawiasy-w-wyrażeniu-regularnym.md)
- [Wyrażenie regularne dla e-mail](../Java/wyrażenie-regularne-dla-e-mail.md)
