# Przestrzeń Survivor Garbage Collector

**Data:** 2023-04-25

---

**User:**

Dlaczego Garbage Collector posiada dwie przestrzenie survivour i dlaczego jedna przestrzeń jest zawsze pusta?

---

**Assistant:**



Garbage Collector w językach programowania, takich jak Java, korzysta z przestrzeni pamięci zwanej Heap, w której są przechowywane obiekty. Głównym zadaniem Garbage Collector'a jest usuwanie obiektów, które nie są już używane przez program, aby zwolnić pamięć i zapobiec wyciekom pamięci.

Przestrzeń Survivor jest jedną z trzech przestrzeni w Heap, obok przestrzeni Eden i Old. Przestrzeń Survivor służy do przechowywania obiektów, które przetrwały pierwszą rundę czyszczenia przeprowadzoną przez Garbage Collector'a w przestrzeni Eden. W ramach procesu GC, Garbage Collector przenosi te przetrwałe obiekty do Survivor, aby mogły dalej żyć i być wykorzystane przez program.

Przestrzeń Survivor jest zwykle podzielona na dwie części - odnawianą i starą. Podczas kolejnych rund czyszczenia, Garbage Collector przenosi przetrwałe obiekty między dwiema częściami przestrzeni Survivor i wykonuje operacje czyszczenia na obszarze, który nie jest używany. Przestrzeń Survivor jest podzielona na dwie części, ponieważ Garbage Collector używa algorytmu przeprowadzającego kopię (ang. copy collection algorithm), który wymaga dwóch obszarów docelowych, do których przetrwałe obiekty są kopiowane.

Jedna z części przestrzeni Survivor jest zawsze pusta, ponieważ Garbage Collector używa jej jako obszaru docelowego podczas pierwszej rundy czyszczenia, gdy przetrwałe obiekty są kopiowane z przestrzeni Eden. W następnych rundach czyszczenia, obszar docelowy jest zmieniany, a poprzednio używany obszar staje się pusty i gotowy do użycia w następnej rundzie.