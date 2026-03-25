# Typ prymitywny long - pamięć.

**Data:** 2023-07-12

---

**User:**

w jvm w jakiej części pamięci trzymane są wartości typów prymitywnych no. long?

---

**Assistant:**

W przypadku maszyny wirtualnej Java (JVM) wartości typów prymitywnych, takich jak `long`, są przechowywane w stosie (stack). Stos jest używany do przechowywania lokalnych zmiennych i wartości metod. 

W przypadku typów prymitywnych, takich jak `long`, wartość jest przechowywana bezpośrednio na stosie, a nie jako referencja do obiektu. Wartość `long` zajmuje 8 bajtów pamięci, więc w przypadku innych typów prymitywnych o różnych rozmiarach, wymagana ilość pamięci będzie inna.

Stos jest zarządzany automatycznie przez JVM i jest stosowany do obsługi wywołań metod oraz przechowywania zmiennych lokalnych. Każda metoda ma swój własny ramka stosu, która zawiera miejsce na przechowywanie zmiennych lokalnych i wartości typów prymitywnych, takich jak `long`, podczas wykonywania metody.

---

**User:**

A gdzie trzymane są obiekty?

---

**Assistant:**

Obiekty w języku Java są przechowywane w stercie (heap) w pamięci JVM. Sterta to obszar pamięci przeznaczony do przechowywania dynamicznie tworzonych obiektów i tablic. 

Kiedy tworzysz obiekt za pomocą operatora `new` lub przy użyciu mechanizmu alokacji pamięci, obiekt jest umieszczany w stercie. Obiekty są przechowywane jako instancje klas i zajmują większą ilość pamięci niż typy prymitywne, ponieważ zawierają dodatkowe informacje, takie jak nagłówek obiektu, wskazniki na metody itp.

Sterta jest zarządzana przez mechanizm zarządzania pamięcią JVM i ma elastyczną strukturę danych, która pozwala na dynamiczne przydzielanie i zwalnianie pamięci podczas tworzenia i usuwania obiektów. Sterta jest wspólna dla wszystkich wątków wewnątrz JVM i jest zarządzana za pomocą mechanizmu odśmiecania pamięci (garbage collection), który automatycznie usuwa nieużywane obiekty i zwalnia zajętą przez nie pamięć.

Warto zauważyć, że referencje do obiektów są przechowywane na stosie lub w rejestrach, a same obiekty znajdują się na stercie. Stos przechowuje wskaźniki na obiekty, co umożliwia dostęp do nich i manipulację nimi w kodzie programu.

---

**User:**

Gdzie trzymana jest wartość typu prymitywnego np. long która jest polem w obiekcie?

---

**Assistant:**

Wartość typu prymitywnego, takiego jak `long`, która jest polem w obiekcie, jest przechowywana bezpośrednio w samym obiekcie. Każdy obiekt ma zarezerwowaną odpowiednią ilość pamięci dla wszystkich swoich pól, w tym pól prymitywnych.

W przypadku pola typu `long`, które zajmuje 8 bajtów, rezerwowane jest 8 bajtów pamięci w obiekcie, aby przechować tę wartość. Wartość `long` jest zapisywana bezpośrednio w tej lokalizacji pamięci, a nie jako referencja do innego miejsca w pamięci.

Podczas tworzenia i inicjalizacji obiektu, pamięć jest przydzielana w stercie dla całego obiektu, wraz z pamięcią dla wszystkich pól prymitywnych i referencji do innych obiektów. Wartości prymitywne są przechowywane w swoich wydzielonych obszarach wewnątrz obiektu, co oznacza, że wartość `long` przechowywana jest bezpośrednio w pamięci tego obiektu.

---

**User:**

czyli na w stack czy heap?

---

**Assistant:**

Przepraszam za wcześniejsze zamieszanie. Wartości pól typów prymitywnych, takich jak `long`, które są polami obiektów, są przechowywane w stercie (heap). 

Główna różnica polega na tym, że same obiekty są przechowywane w stercie, a nie na stosie. Stos jest używany do przechowywania zmiennych lokalnych i wartości tymczasowych w trakcie wykonywania metod. Wartości pól obiektów przechowywane są w pamięci sterty, której zarządzanie jest bardziej elastyczne i umożliwia dynamiczne przydzielanie i zwalnianie pamięci dla obiektów.

Podsumowując, obiekty są przechowywane w stercie (heap), a wartości pól typów prymitywnych, takich jak `long`, znajdują się bezpośrednio w pamięci przypisanej do obiektu w stercie.