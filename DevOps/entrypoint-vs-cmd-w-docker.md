# Różnice między ENTRYPOINT a CMD w Dockerze

Zarówno `ENTRYPOINT`, jak i `CMD` to instrukcje w pliku `Dockerfile`, które określają, jakie polecenie zostanie wykonane podczas uruchamiania kontenera. Choć na pierwszy rzut oka mogą wydawać się podobne, pełnią różne funkcje i mają odmienne zasady nadpisywania.

## Dlaczego to jest ważne?

Zrozumienie różnicy między tymi dwiema instrukcjami jest kluczowe podczas tworzenia obrazów Dockerowych, z których będą korzystać inni programiści lub procesy CI/CD. Pozwala to na stworzenie kontenerów, które domyślnie działają jako użyteczne aplikacje, jednocześnie dając użytkownikowi elastyczność w modyfikowaniu argumentów przekazywanych do tych aplikacji.

## Jak to działa?

### CMD (Domyślne polecenie lub argumenty)

Instrukcja `CMD` służy do ustawienia **domyślnego** polecenia do wykonania lub **domyślnych parametrów**, które mogą zostać łatwo nadpisane z poziomu wiersza poleceń podczas uruchamiania kontenera (`docker run`).

Jeśli użytkownik poda polecenie na końcu `docker run`, instrukcja `CMD` z `Dockerfile` zostanie całkowicie zignorowana i zastąpiona poleceniem użytkownika.

**Przykład:**
```dockerfile
FROM ubuntu
CMD ["echo", "Witaj świecie!"]
```
- Uruchomienie `docker run <obraz>` wypisze: `Witaj świecie!`
- Uruchomienie `docker run <obraz> echo "Witaj Dockerze!"` nadpisze `CMD` i wypisze: `Witaj Dockerze!`

### ENTRYPOINT (Główny punkt wejścia)

Instrukcja `ENTRYPOINT` określa polecenie, które **zawsze** zostanie uruchomione podczas startu kontenera. Jej głównym celem jest sprawienie, aby kontener zachowywał się jak pojedyncza, ściśle określona aplikacja.

Wszelkie dodatkowe argumenty przekazane podczas `docker run` zostaną **dołączone** na końcu polecenia zdefiniowanego w `ENTRYPOINT`, zamiast go nadpisywać. Aby całkowicie nadpisać `ENTRYPOINT`, należy jawnie użyć flagi `--entrypoint`.

**Przykład:**
```dockerfile
FROM ubuntu
ENTRYPOINT ["echo", "Witaj"]
```
- Uruchomienie `docker run <obraz>` wypisze: `Witaj`
- Uruchomienie `docker run <obraz> świecie!` wypisze: `Witaj świecie!` (ponieważ słowo "świecie!" zostało dołączone jako argument do "echo Witaj").

### Używanie ENTRYPOINT i CMD razem (Najlepsza praktyka)

Bardzo często najlepszym podejściem jest użycie obu instrukcji jednocześnie. W takim scenariuszu:
- `ENTRYPOINT` definiuje niezmienny program do uruchomienia.
- `CMD` dostarcza domyślne argumenty do tego programu, które użytkownik może łatwo nadpisać.

**Przykład:**
```dockerfile
FROM python:3.9
ENTRYPOINT ["python"]
CMD ["main.py"]
```
- Uruchomienie `docker run <obraz>` uruchomi domyślny plik: `python main.py`.
- Uruchomienie `docker run <obraz> skrypt.py` spowoduje wykonanie `python skrypt.py` (argument "skrypt.py" nadpisał domyślne `CMD ["main.py"]`, ale został dołączony do niezmiennego `ENTRYPOINT ["python"]`).

## Podsumowanie i najlepsze praktyki

| Cecha | `CMD` | `ENTRYPOINT` |
| :--- | :--- | :--- |
| **Główny cel** | Domyślne polecenie lub argumenty | Punkt wejścia (główny proces) |
| **Nadpisywanie** | Łatwe (`docker run <obraz> <nowe_polecenie>`) | Trudniejsze (wymaga flagi `--entrypoint`) |
| **Współpraca** | Argumenty z `CMD` są dołączane do `ENTRYPOINT` | Definiuje główny program bazowy, nie do nadpisania argumentami |

- Używaj **`ENTRYPOINT`**, gdy budujesz kontener służący jako konkretne narzędzie, np. uruchomienie bazy danych, serwera www, czy gotowego CLI.
- Używaj **`CMD`**, gdy chcesz podać domyślne argumenty do `ENTRYPOINT` lub gdy obraz ma na celu bycie środowiskiem ogólnym, pozwalającym użytkownikowi na swobodne podanie dowolnej komendy startowej.
