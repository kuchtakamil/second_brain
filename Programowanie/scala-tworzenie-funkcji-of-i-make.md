# Scala: tworzenie funkcji "of" i "make"

**Data:** 2023-04-10

---

**User:**

W Scala jaka jest zasada nadawania funkcjom tworzącym nazwy "of" i "make"?

---

**Assistant:**

W języku Scala, zasada nadawania nazw funkcjom "of" i "make" jest związana z konwencją nazewnictwa "Factory Method".

Metoda "of" służy do tworzenia nowych obiektów z istniejących wartości, natomiast metoda "make" tworzy nowy obiekt z nieokreślonych wartości.

Zastosowanie tych nazw funkcji ma na celu ułatwienie zrozumienia, że metoda ta jest odpowiedzialna za tworzenie nowego obiektu, a także ułatwia wskazanie konkretnego celu, dla którego metoda ta została utworzona.

Przykładowo, metoda "of" mogłaby być użyta do stworzenia nowego obiektu typu List na podstawie już istniejącej kolekcji, np. Array, natomiast metoda "make" mogłaby być użyta do stworzenia nowego obiektu typu Option z nieznanej wartości.

Zasada ta jest powszechnie stosowana w Scala i jest uważana za dobry styl programowania, ponieważ pomaga zwiększyć czytelność i zrozumiałość kodu.