# Wypisz i objaśnij typy plików służące do opisów projektu jakie są używane w Gemi

**Data:** 24 sie 2025, 22:07:20 CET

---

**User:**

Wypisz i objaśnij typy plików służące do opisów projektu jakie są używane w Gemini CLI

---

**Gemini:**

W Gemini CLI, do opisu i konfiguracji projektu, wykorzystuje się kilka kluczowych typów plików. Każdy z nich pełni odrębną rolę w dostosowywaniu interakcji z modelem i definiowaniu środowiska pracy.

---

### `GEMINI.md`

Plik `GEMINI.md` jest podstawowym plikiem służącym do dostarczania kontekstu i instrukcji dla modelu Gemini. Jego celem jest ukierunkowanie odpowiedzi modelu tak, aby były one jak najbardziej adekwatne do specyfiki projektu, jego struktury, stylu kodowania oraz wymagań.

#### Główne cechy:

- **Format Markdown**: Plik jest tworzony w formacie Markdown, co ułatwia jego czytelną i ustrukturyzowaną edycję.
- **Hierarchiczne wczytywanie**: Gemini CLI wczytuje pliki `GEMINI.md` w sposób hierarchiczny. Oznacza to, że instrukcje z plików znajdujących się bliżej bieżącego katalogu mają wyższy priorytet i nadpisują bardziej ogólne dyrektywy. Kolejność wczytywania jest następująca:
  1. **Kontekst globalny**: `~/.gemini/GEMINI.md` – instrukcje stosowane do wszystkich projektów użytkownika.
  2. **Kontekst projektu**: Pliki `GEMINI.md` znalezione w katalogu nadrzędnym, aż do korzenia projektu.
  3. **Kontekst podkatalogu**: Pliki `GEMINI.md` w bieżącym i podkatalogach.
- **Modularność**: Możliwe jest importowanie zawartości innych plików Markdown do głównego `GEMINI.md` za pomocą składni `@nazwa_pliku.md`. Pozwala to na organizację i reużywalność instrukcji.
- **Polecenia**: Za pomocą polecenia `/memory show` można wyświetlić finalny, połączony kontekst, który jest przekazywany do modelu. Polecenie `/memory refresh` pozwala na ponowne załadowanie wszystkich plików `GEMINI.md` bez restartu sesji.

**Przykład zawartości `GEMINI.md`:**

```
# Kontekst projektu: Aplikacja w Pythonie

## Główne założenia
- Język programowania: Python 3.11+
- Framework: FastAPI
- Baza danych: PostgreSQL z użyciem SQLAlchemy 2.0 ORM.
- Styl kodowania: Zgodny z PEP 8, maksymalna długość linii 88 znaków (konfiguracja `black`).

## Struktura projektu
- `app/api/`: Zawiera endpointy API.
- `app/models/`: Definicje modeli SQLAlchemy.
- `app/schemas/`: Schematy Pydantic do walidacji danych.

## Dyrektywy dla modelu
- Zawsze generuj kod z adnotacjami typów (type hints).
- Unikaj używania `print()`, zamiast tego korzystaj z modułu `logging`.
- Przy generowaniu testów jednostkowych używaj biblioteki `pytest`.
```

---

### `settings.json`

Plik `settings.json` służy do konfiguracji samego narzędzia Gemini CLI. Pozwala na dostosowanie jego zachowania, wyglądu oraz integracji z zewnętrznymi narzędziami.

#### Poziomy konfiguracji:

Podobnie jak `GEMINI.md`, pliki `settings.json` są wczytywane z różnych lokalizacji, a ich ustawienia są scalane, przy czym bardziej szczegółowe konfiguracje nadpisują te globalne:

1. **Systemowe**: `/etc/gemini-cli/settings.json` (najwyższy priorytet, dotyczy wszystkich użytkowników).
2. **Użytkownika**: `~/.gemini/settings.json` (globalne ustawienia dla zalogowanego użytkownika).
3. **Projektu (Workspace)**: `.gemini/settings.json` w katalogu głównym projektu (ustawienia specyficzne dla danego projektu).

#### Przykładowe opcje konfiguracyjne:

- **`theme`**: Ustawienie motywu wizualnego interfejsu.
- **`selectedAuthType`**: Metoda autentykacji (np. `oauth-personal`).
- **`coreTools`**: Lista dozwolonych, wbudowanych narzędzi, z których może korzystać agent.
- **`excludeTools`**: Lista narzędzi, które mają być wykluczone z użycia.
- **`contextFileName`**: Umożliwia zmianę domyślnej nazwy pliku kontekstowego z `GEMINI.md` na inną.

**Przykład zawartości `settings.json`:**

```
{
  "theme": "gruvbox-dark",
  "coreTools": [
    "ReadFile",
    "WriteFile",
    "Shell"
  ],
  "excludeTools": [
    "GoogleSearch"
  ]
}
```

---

### `.geminiignore`

Plik `.geminiignore` pełni funkcję analogiczną do pliku `.gitignore` w systemie kontroli wersji Git. Służy do wykluczania określonych plików i katalogów z kontekstu przekazywanego do modelu Gemini. Zapobiega to analizowaniu przez model plików nieistotnych, wrażliwych lub binarnych.

#### Składnia i zasady:

Składnia jest w dużej mierze zgodna z tą znaną z `.gitignore`:

- Puste linie oraz linie zaczynające się od `#` są ignorowane.
- Obsługiwane są standardowe wzorce glob (np. `*`, `?`, `[]`).
- Ukośnik (`/`) na końcu wzorca dopasowuje tylko katalogi.
- Ukośnik na początku wzorca zakotwicza ścieżkę względem lokalizacji pliku `.geminiignore`.
- Wykrzyknik (`!`) na początku wzorca neguje go, co pozwala na ponowne włączenie plików pasujących do wcześniejszej, szerszej reguły wykluczającej.

**Przykład zawartości `.geminiignore`:**

```
# Zależności i środowiska wirtualne
node_modules/
.venv/
__pycache__/

# Logi i pliki tymczasowe
*.log
*.tmp

# Pliki konfiguracyjne z danymi wrażliwymi
.env
secret_config.json

# Wyklucz wszystkie pliki markdown, z wyjątkiem plików dokumentacji
*.md
!docs/*.md
```