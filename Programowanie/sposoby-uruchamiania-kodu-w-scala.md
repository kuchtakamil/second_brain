# Sposoby uruchamiania kodu w Scala

**Data:** 2024-11-03

---

**User:**

Jaki jest najlepszy sposób na uruchomienie celem edukacyjnym dwóch, trzech linijek kodu w Scala?

---

**Assistant:**

Najlepszym sposobem na szybkie uruchomienie kilku linijek kodu w Scali do celów edukacyjnych jest skorzystanie z jednej z poniższych metod:

1. **Scala REPL** (Read-Eval-Print Loop):
   - Scala REPL to interaktywna konsola dostępna po zainstalowaniu Scali na komputerze.
   - Możesz ją uruchomić wpisując `scala` w terminalu, a następnie wpisywać kod bezpośrednio w konsoli, gdzie będzie natychmiast wykonywany.
   - REPL to świetne narzędzie do szybkiego testowania małych fragmentów kodu i eksperymentowania z językiem.

2. **Scala na Scastie** (https://scastie.scala-lang.org/):
   - Scastie to narzędzie online, które pozwala pisać, uruchamiać i dzielić się kodem w Scali bez konieczności instalowania czegokolwiek.
   - Wystarczy wejść na stronę Scastie, wkleić kod i kliknąć „Run”, aby zobaczyć wyniki.
   - Działa z różnymi wersjami Scali, więc można testować kod zarówno w Scala 2, jak i Scala 3, co jest przydatne, jeśli pracujesz z różnymi wersjami języka.

3. **Notebooki Jupyter z Kernalem dla Scali**:
   - Jeśli masz zainstalowane Jupyter Notebooki, możesz użyć kernela Almond dla Scali, który umożliwia pisanie kodu w Scali bezpośrednio w Jupyterze.
   - Notebooki są szczególnie przydatne do celów edukacyjnych, ponieważ można tworzyć dokumenty zawierające zarówno kod, jak i notatki.

4. **SBT Console**:
   - Jeśli projekt używa SBT (Scala Build Tool), możesz uruchomić interaktywną konsolę Scali wpisując `sbt console` w katalogu projektu.
   - Pozwala to na szybkie testowanie kodu w kontekście konkretnego projektu, z dostępem do wszystkich zależności projektu.

Każda z tych metod jest łatwa w użyciu i dostosowana do uruchamiania krótkich fragmentów kodu, dzięki czemu idealnie sprawdzają się do nauki i testowania Scali.