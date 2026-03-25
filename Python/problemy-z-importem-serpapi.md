# Problemy z importem serpapi

**Data:** 2025-11-07

---

**User:**

uruchomiłem uv pip install serpapi, w pliku mam "from serpapi import GoogleSearch" ale GoogleSearch nie jest znajdywane

---

**Assistant:**

To może wynikać z kilku przyczyn — poniżej lista kroków diagnostycznych:  

1. **Sprawdź, czy pakiet rzeczywiście jest zainstalowany w tym środowisku:**  
   ```bash
   uv pip show serpapi
   ```
   Jeśli nic nie pokazuje, to oznacza, że instalacja była w innym środowisku lub się nie udała.  

   Możesz też sprawdzić:
   ```bash
   uv pip list | grep serpapi
   ```

2. **Upewnij się, że importujesz z właściwego pakietu:**  
   Czasem istnieją kolizje nazw. Sprawdź, czy moduł jest faktycznie dostępny:
   ```python
   import serpapi
   print(dir(serpapi))
   ```
   Jeśli nie ma tam `GoogleSearch`, to znaczy, że import nie działa poprawnie.  

3. **Zobacz, co naprawdę masz w środowisku:**  
   Możesz sprawdzić lokalizację modułu:
   ```python
   import serpapi
   print(serpapi.__file__)
   ```
   Jeśli pokazuje coś w stylu `.../site-packages/serpapi/__init__.py`, otwórz ten plik i zobacz, czy eksportuje `GoogleSearch`.  

4. **Zamień sposób importu na pełny (czasem pomaga):**  
   ```python
   from serpapi.google_search_results import GoogleSearch
   ```
   – to jest oficjalna i właściwa ścieżka zgodna z dokumentacją biblioteki [serpapi-python](https://github.com/serpapi/google-search-results-python).  

5. **Jeśli nadal nie działa, upewnij się, że to właściwa biblioteka:**  
   Być może zainstalował się inny pakiet o tej samej nazwie. Spróbuj usunąć i zainstalować ponownie:
   ```bash
   uv pip uninstall serpapi
   uv pip install google-search-results
   ```
   Następnie w kodzie:
   ```python
   from serpapi import GoogleSearch
   ```

---

Najczęstsza przyczyna to właśnie to, że `google-search-results` jest właściwym pakietem, a nie `serpapi`.  
Sprawdź, czy instalacja:
```bash
uv pip install google-search-results
```
rozwiązuje problem — w 99% przypadków to wystarczy.