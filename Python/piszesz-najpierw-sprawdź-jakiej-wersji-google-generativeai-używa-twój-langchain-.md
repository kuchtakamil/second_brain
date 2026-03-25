# Piszesz "Najpierw sprawdź, jakiej wersji google-generativeai używa Twój langchai

**Data:** 16 sty 2026, 13:32:16 CET

---

**User:**

Piszesz "Najpierw sprawdź, jakiej wersji google-generativeai używa Twój langchain-google-genai. Możesz to zrobić komendą pip show langchain-google-genai lub sprawdzając metadane pakietu."

pip show langchain-google-genai                                                                                                              
Name: langchain-google-genai
Version: 3.2.0
Summary: An integration package connecting Google's genai package and LangChain
Home-page: https://docs.langchain.com/oss/python/integrations/providers/google
Author: 
Author-email: 
License: MIT
Location: /home/kamil/repos/eng_short_scraper/.venv/lib/python3.12/site-packages
Requires: filetype, google-ai-generativelanguage, langchain-core, pydantic
Required-by:

---

**Gemini:**

Z przedstawionego wyjścia `pip show` wynika kluczowa informacja: `langchain-google-genai` w wersji `3.2.0` nie zależy bezpośrednio od `google-generativeai` (SDK wysokopoziomowego), lecz od `google-ai-generativelanguage` (niskopoziomowego klienta wygenerowanego z definicji gRPC).

Konflikt pojawia się, ponieważ `google-generativeai` również posiada zależność od `google-ai-generativelanguage`, ale prawdopodobnie w innym zakresie wersji niż ten narzucony przez `langchain-google-genai`.

### 1. Źródło konfliktu: Zależność tranzytywna

Wspólnym mianownikiem i punktem zapalnym jest biblioteka **`google-ai-generativelanguage`**.

- **LangChain:** `langchain-google-genai` v3.2.0 wymaga `google-ai-generativelanguage` w konkretnym przedziale (np. `>=0.6.0, <0.7.0`).
- **Google SDK:** Najnowsze `google-generativeai` (instalowane przez `*`) może wymagać `google-ai-generativelanguage >= 0.7.0`.

Kiedy manager pakietów widzi te dwie sprzeczne instrukcje, przerywa operację lub wyrzuca błąd "Incompatible definitions".

### 2. Identyfikacja ograniczeń

Aby precyzyjnie naprawić `pyproject.toml`, sprawdź, jakie ograniczenia narzuca zainstalowana wersja LangChain na bibliotekę bazową:

```
pip show google-ai-generativelanguage
```

Sprawdź również wymagania wersji 3.2.0 bezpośrednio w metadanych (możesz to zrobić sprawdzając plik `site-packages/langchain_google_genai-3.2.0.dist-info/METADATA`). Zazwyczaj znajdziesz tam wpis typu:
`Requires-Dist: google-ai-generativelanguage (>=0.6.4,<0.7.0)`

### 3. Rozwiązanie: Synchronizacja wersji w pyproject.toml

Aby rozwiązać problem, musisz przestać używać gwiazdki `*` dla `google-generativeai` i dopasować ją do tego, co akceptuje `langchain-google-genai`.

Najbezpieczniejszą konfiguracją dla stosu opartego o `3.2.0` jest:

```
[tool.poetry.dependencies]
python = "^3.12"
# Przypięcie wersji LangChain którą posiadasz
langchain-google-genai = "3.2.0" 

# Zamiast "*", użyj wersji kompatybilnej z obecnym ekosystemem Google AI
# Wersja 0.7.x lub 0.8.x zazwyczaj współgra z nowymi wersjami LangChain
google-generativeai = ">=0.7.0, <0.8.0"

# Najczęstszy powód błędów runtime przy modelach Google:
# Wymuś protobuf w wersji 4.x, wersja 5.x często powoduje błędy 
# w deserializacji deskryptorów w bibliotekach Google.
protobuf = "^4.25.3"
```

### 4. Problem z Protobuf w środowisku mieszanym

Jeśli po dodaniu `google-generativeai` otrzymujesz błędy dotyczące `DescriptorPool` lub `TypeError`, wynika to z faktu, że `google-generativeai` próbuje wymusić najnowszy `protobuf` (v5), podczas gdy `langchain-google-genai` lub `google-ai-generativelanguage` mogą wciąż polegać na v4.

W takim przypadku zastosuj restrykcję:

```
# Jeśli używasz pip
pip install "protobuf<5.0.0" "google-generativeai~=0.7.2"
```

### 5. Kolejność działań naprawczych

Jeśli używasz managera typu `Poetry` lub `uv`:

1. Zmień `google-generativeai = "*"` na `google-generativeai = "^0.7.0"`.
2. Zmień `protobuf = "*"` na `protobuf = "<5.0.0"`.
3. Uruchom proces aktualizacji blokady:

   ```
   poetry lock --no-update
   poetry install
   ```

Jeśli używasz standardowego `pip`:

```
pip install google-generativeai==0.7.2 protobuf==4.25.3
```

Chcesz, abym sprawdził konkretny komunikat błędu (Traceback), który otrzymujesz przy próbie instalacji?