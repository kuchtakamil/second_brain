# Java Library Path

**Data:** 2024-01-29

---

**User:**

W wywołaniu 
java -Djava.library.path=/sciezka/do/katalogu/biblioteki -jar TwojaAplikacja.jar
co oznacza -Djava.library.path

---

**Assistant:**

Parametr `-Djava.library.path` w wywołaniu `java` oznacza ustawienie systemowej właściwości (system property) dla maszyny wirtualnej Java (JVM). W tym konkretnym przypadku, jest to ścieżka do katalogu, w którym znajdują się biblioteki natywne (native libraries).

Kiedy maszyna wirtualna Java uruchamia aplikację, może być konieczne skorzystanie z bibliotek natywnych, które są napisane w językach niższego poziomu (np. C, C++). Aby JVM mogła znaleźć te biblioteki, musisz podać ścieżkę, gdzie są one przechowywane.

W przypadku twojego polecenia:

```bash
java -Djava.library.path=/sciezka/do/katalogu/biblioteki -jar TwojaAplikacja.jar
```

- `-Djava.library.path=/sciezka/do/katalogu/biblioteki` wskazuje JVM, gdzie szukać bibliotek natywnych.
- `-jar TwojaAplikacja.jar` uruchamia aplikację z pliku JAR o nazwie "TwojaAplikacja.jar".

Podsumowując, `-Djava.library.path` jest używane do ustawienia ścieżki do bibliotek natywnych, które są potrzebne dla działania aplikacji Java.