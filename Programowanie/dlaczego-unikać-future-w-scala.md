# Dlaczego unikać Future w Scala?

**Data:** 2023-03-16

---

**User:**

Dlaczego używanie Future w języku Scala jest niepolecane?

---

**Assistant:**

Używanie konstrukcji Future w języku Scala może być niepolecane z kilku powodów:

1. Brak kontroli nad wyjątkami: Kiedy używasz Future, nie masz pełnej kontroli nad obsługą wyjątków, które mogą wystąpić wewnątrz Future. Zamiast tego musisz zdefiniować funkcje obsługi błędów i przekazać je jako argument do metody onComplete. To może prowadzić do kodu, który jest trudny do debugowania i utrzymania.

2. Trudności z asynchroniczną komunikacją: Jeśli chcesz skorzystać z kilku Future, aby wykonać asynchroniczne zadanie, może to być trudne do zaimplementowania. W takim przypadku potrzebujesz bardziej zaawansowanych narzędzi, takich jak Akka, aby umożliwić komunikację między różnymi wątkami i zaimplementować wydajny system asynchroniczny.

3. Trudność w tworzeniu testów jednostkowych: Testowanie kodu korzystającego z Future może być trudne, ponieważ kod wykonywany jest asynchronicznie. Wymaga to zastosowania specjalnych narzędzi testowych, takich jak ScalaTest lub Akka TestKit, aby umożliwić testowanie kodu, który korzysta z Future.

4. Możliwe problemy z pamięcią: Używanie Future może prowadzić do problemów z pamięcią w sytuacjach, gdy duża ilość Future zostanie utworzona i przetwarzana jednocześnie. Może to prowadzić do problemów z wydajnością i wykorzystaniem pamięci.

Dlatego też, zamiast korzystać z Future, w niektórych przypadkach lepiej jest korzystać z innych narzędzi do obsługi asynchronicznego kodu, takich jak Akka Actors lub ZIO.

---

**User:**

a co z referential transparency?

---

**Assistant:**

Referential transparency to własność funkcji, która polega na tym, że wywołanie funkcji zawsze zwróci ten sam wynik dla tych samych argumentów, bez wpływu na kontekst, w którym funkcja jest wywoływana. Używanie Future w Scala niekoniecznie narusza referential transparency, ponieważ zwracana wartość Future jest zawsze taka sama dla danego wejścia. 

Jednakże, korzystanie z Future może prowadzić do kodu, który nie jest referentially transparent, jeśli Future jest wykorzystywany w sposób, który zmienia stan systemu lub zależy od zmiennych zewnętrznych, takich jak czas lub stan bazy danych. W takim przypadku wywołanie funkcji z Future może zwrócić różne wyniki dla tych samych argumentów, co prowadzi do utraty referential transparency.

Dlatego też, aby zachować referential transparency, ważne jest, aby zastosować odpowiednie techniki programowania funkcyjnego, takie jak unikanie efektów ubocznych, oddzielanie stanu od obliczeń i wykorzystywanie niemutowalnych struktur danych. W ten sposób można uniknąć problemów związanych z referential transparency przy korzystaniu z Future w języku Scala.