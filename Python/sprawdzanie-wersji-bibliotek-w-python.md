# Sprawdzanie wersji bibliotek w Pythonie

Polecenie, z którym się spotkałeś:
```python
import langchain_aws
print(langchain_aws.__version__)
```
to jeden z najczęstszych sposobów na sprawdzanie wersji pakietu z poziomu samej aplikacji w Pythonie. 

Ten atrybut bazuje na dunder-zmiennej `__version__` (dunder to skrót od *double underscore*).

## Po co sprawdza się wersję bibliotek?

Praktyka ta jest stosowana głównie z poniższych powodów:

1. **Raportowanie błędów i debugowanie:** Kiedy napotykasz problem z biblioteką i chcesz zgłosić issue (np. na GitHubie), deweloperzy potrzebują informacji, na której konkretnie wersji on występuje. Wrzucenie do kodu takiego printa pozwala upewnić się, na jakiej wersji jest aktualnie odpalany skrypt.
2. **Zachowanie kompatybilności wstecznej:** Ekosystem bardzo dynamicznie ewoluuje. Różne wersje (np. Pydantic v1 vs v2) mogą mieć zupełnie inne formy API i reguły. Pisząc kod, który ma obsługiwać różne warianty paczek w zależności co ma użytkownik, możesz sprawdzić tę wersję warunkowo:
   ```python
   import pydantic
   if pydantic.__version__.startswith("1"):
       # Użyj starego API
       pass
   else:
       # Użyj nowego API z v2
       pass
   ```
3. **Środowiska interaktywne:** Podczas pracy z Jupyter Notebook lub Google Colab często odpalasz notatnik w predefiniowanym środowisku. Sprawdzenie w ten sposób `__version__` na samym początku daje 100% pewność, z jakimi bibliotekami pracujesz.
4. **Logowanie podczas uruchamiania:** W dużych aplikacjach aplikacja na starcie może logować (lub upewniać się za pomocą asercji), czy dysponuje kompatybilnymi bibliotekami kluczowych komponentów, żeby uniknąć wywalania się (tzw. "fail fast") podczas normalnej pracy.

## Inne sposoby na sprawdzanie wersji

Oprócz wspomnianego sposobu odpytania poprzez import w kodzie, istnieją również nowocześniejsze, wbudowane metody lub narzędzia CLI.

### 1. Moduł `importlib.metadata` (Rekomendowany w aplikacjach)

Samo używanie `__version__` to głównie konwencja społecznościowa. Niektóre biblioteki nie definiują w ten sposób swoich wersji. Prawidłowym podejściem w Python 3.8+ jest zaglądanie do metadanych paczek:

```python
import importlib.metadata

# Argumentem jest nazwa paczki, pod jaką jest zainstalowana przez pipesa (z myślnikami), a nie jak z niej importujesz
version = importlib.metadata.version('langchain-aws')
print(version)
```

Zaletą tej metody jest to, że nie musisz w całości importować ciężkiego modułu, tylko by wyciągnąć jego wersję z atrybutu – czyta ona po prostu metadane z instalacji.

### 2. Za pomocą konsoli (CLI)

Gdy po prostu potrzebujesz wiedzieć środowiskowo, co jest zainstalowane, używasz komend konsolowych dla pip lub managerów paczek (`uv`, `poetry`):

- **Stam pip `show`:** Pokazuje wszystkie szczegóły związane z podaną paczką (twórca, zależne paczki oraz numer wersji).
  ```bash
  pip show langchain-aws
  ```

- **Za pomocą nowoczesnego uv:**
  ```bash
  uv pip show langchain-aws
  ```

- **Listowanie wszystkich wersji we wdrożeniu:** Jeśli chcesz otrzymać kompletną listę wszystkich zainstalowanych zależności i ich wersji (np. w celu wrzucenia do pliku `requirements.txt`), służy do tego polecenie freeze.
  ```bash
  pip freeze 
  # albo zapisać od razu: `pip freeze > requirements.txt`
  ```

## Powiązane tematy
- [Instalacja zależności w Pythonie (uv vs pip)](uv-pip-vs-pip.md)
- [Błąd uruchamiania i środowiska (Externally Managed)](błąd-externally-managed-environment.md)
- [Pydantic V2 walidacja (Różnice między wersją v1 a v2)](pydantic-v2-walidacja.md)
