# Problem N+1 w Hibernate

**Data:** 2024-09-25

---

**User:**

Przy artykule opisującym problem Hibernate N+1 znalazłem następujące wyjaśnienie. Oceń czy jest ono prawdziwe i jeśli tak opisz w jaki sposób tworząc zapytanie tylko o książki może dojść do problemu bo autor ma też np. komiksy.

Podejście z własnym zapytaniem i JOIN FETCH jest bardzo popularne 
Należy jednak uważać, ponieważ nadmierne używanie JOIN FETCH dla wielu relacji może prowadzić do problemu iloczynu kartezjańskiego.
Jeśli autor byłby powiązany nie tylko z tabelą z książkami, ale także z tabelami z postami i komiksami,  i dociągnelibyśmy te relacje w taki sam sposób jak na filmie to doprowadzilibyśmy do iloczynu kartezjańskiego. 
Na przykład, jeśli autor miałby X książek, Z postów i Y komiksów, to zapytanie SQL zwróciłoby nam  X * Z * Y wyników.

---

**Assistant:**

Tak, wyjaśnienie jest poprawne. Problem opisywany jako **iloczyn kartezjański** (kartesian product) może wystąpić, gdy w zapytaniu używamy wielu relacji z JOIN FETCH. Jest to spowodowane tym, że zapytanie SQL, które dołącza wiele kolekcji (np. książki, posty i komiksy autora), zwróci kombinacje wszystkich rekordów z tych kolekcji, co prowadzi do nadmiarowych wyników.

W praktyce problem ten można zilustrować w następujący sposób:

### Przykład:

Załóżmy, że mamy tabelę `Author`, która jest powiązana z trzema innymi tabelami: `Books`, `Posts` i `Comics`. Relacje te są **wielu-do-jednego** lub **jednego-do-wielu**. Jeśli użyjemy zapytania z `JOIN FETCH`, aby pobrać wszystkie te dane naraz, tak jak w poniższym przykładzie:

```sql
SELECT a 
FROM Author a 
JOIN FETCH a.books b 
JOIN FETCH a.posts p 
JOIN FETCH a.comics c
```

Gdy autor ma:
- 3 książki (X = 3),
- 2 posty (Z = 2),
- 4 komiksy (Y = 4),

to zapytanie zwróci **3 \* 2 \* 4 = 24 wiersze**, czyli iloczyn kartezjański wyników z powiązanych tabel, nawet jeśli w rzeczywistości mamy tylko:
- 3 książki,
- 2 posty,
- 4 komiksy.

Każda książka zostanie "złączona" z każdym postem i każdym komiksem, tworząc nadmiarowe rekordy.

### Jak to się dzieje?

Przy wykonywaniu JOIN FETCH, Hibernate próbuje pobrać wszystkie złączone dane w jednym zapytaniu, tworząc jeden zestaw wyników. Gdy mamy do czynienia z relacjami, które są kolekcjami (np. książki, posty, komiksy), powstaje kartesian product, ponieważ każde połączenie między dwiema kolekcjami generuje kombinację wszystkich możliwych par elementów tych kolekcji.

### Problem N+1 w tym kontekście:

Jeśli pobieramy tylko książki autora, ale autor ma również komiksy i posty, możemy doświadczyć tego problemu przy nieoptymalnym fetchowaniu. Załóżmy, że w pierwszym kroku pobierzemy autora i jego książki, a potem osobno dla każdego autora pobieramy jego komiksy i posty. W takim scenariuszu, zamiast jednego optymalnego zapytania, Hibernate generuje dodatkowe zapytania dla każdej z kolekcji (komiksów, postów), co prowadzi do nadmiernej liczby zapytań (problem N+1).

### Rozwiązanie:

Aby uniknąć problemu z iloczynem kartezjańskim, można:
1. Stosować `JOIN FETCH` tylko dla jednej kolekcji, a pozostałe relacje ładować w inny sposób (np. lazy loading).
2. Skorzystać z podzapytań lub z bardziej zaawansowanych technik fetchowania, takich jak `BATCH FETCHING`.
3. Użyć dodatkowych narzędzi, jak np. `@EntityGraph`, aby dokładnie kontrolować, które relacje są pobierane.

Ważne jest, aby przy dużych i złożonych relacjach zawsze monitorować generowane zapytania SQL i ich wydajność.

---

**User:**

Wyjaśnij różnicę miedzy JOIN a JOIN FETCH

---

**Assistant:**

Różnica między `JOIN` a `JOIN FETCH` w Hibernate dotyczy przede wszystkim sposobu ładowania danych powiązanych z encjami oraz tego, jak zachowuje się mechanizm pobierania relacji (tzw. **fetching**).

### 1. **JOIN**
W standardowym `JOIN` w Hibernate, relacje między encjami nie są automatycznie ładowane do pamięci. Użycie `JOIN` dotyczy zapytania **JPQL** (Java Persistence Query Language), w którym dołączamy dane z powiązanych tabel, ale **bez automatycznego ładowania** relacji.

#### Przykład:
```java
SELECT a 
FROM Author a 
JOIN a.books b
```

W tym zapytaniu pobierasz encję `Author` i dołączasz dane z tabeli `Books`, ale relacje między `Author` a `Books` **nie są automatycznie wczytywane do pamięci** (jeśli na przykład masz relację z `@OneToMany`). Jeśli później próbujesz odczytać książki autora, Hibernate **może wykonać dodatkowe zapytanie**, jeśli tryb fetchowania ustawiono na `LAZY`.

#### Główne cechy:
- Dane są pobierane tylko na poziomie zapytania.
- Encje powiązane (np. książki) nie są w pełni zainicjowane w pamięci (jeśli są `LAZY`).
- Może skutkować dodatkowym zapytaniem, jeśli potrzebujesz powiązanych danych później.

### 2. **JOIN FETCH**
`JOIN FETCH` jest rozszerzeniem `JOIN`, które służy do **natychmiastowego wczytania powiązanych danych do pamięci**. Stosuje się go do unikania **problemu N+1**. Gdy używasz `JOIN FETCH`, Hibernate pobiera zarówno encję główną (np. autora), jak i powiązaną encję (np. książki), **w jednym zapytaniu** SQL.

#### Przykład:
```java
SELECT a 
FROM Author a 
JOIN FETCH a.books b
```

To zapytanie pobiera autora oraz natychmiast ładuje jego książki do pamięci. Oznacza to, że kiedy uzyskasz dostęp do książek autora, Hibernate nie wygeneruje dodatkowego zapytania, ponieważ dane są już załadowane (tryb fetchowania jest efektywnie `EAGER`).

#### Główne cechy:
- Powiązane dane są natychmiast załadowane do pamięci.
- Unika problemu N+1 (nie generuje dodatkowych zapytań w przyszłości).
- Przy ładowaniu wielu kolekcji może prowadzić do iloczynu kartezjańskiego.

### Różnice podsumowane:

| **JOIN**                    | **JOIN FETCH**               |
|-----------------------------|------------------------------|
| Dołącza dane, ale ich nie ładuje do pamięci. | Dołącza dane i ładuje je do pamięci. |
| Może skutkować dodatkowym zapytaniem, jeśli potrzebujemy powiązanych danych (przy fetchowaniu `LAZY`). | Powiązane dane są ładowane natychmiast, bez dodatkowych zapytań. |
| Nie zmienia zachowania mechanizmu fetchowania (np. relacje mogą pozostać `LAZY`). | Zmienia mechanizm fetchowania na natychmiastowy (jak `EAGER`). |
| Może być bardziej wydajne, gdy nie potrzebujemy powiązanych danych. | Może być bardziej wydajne, gdy chcemy uniknąć problemu N+1. |
| Używane do samego zapytania bez wpływu na sposób ładowania encji. | Używane do ładowania relacji razem z główną encją. |

### Kiedy używać:
- **JOIN**: Gdy potrzebujesz danych w jednym zapytaniu, ale nie chcesz jeszcze ładować powiązanych relacji (np. zależy Ci na wydajności i wiesz, że nie będziesz potrzebować dodatkowych danych w tej sesji).
- **JOIN FETCH**: Gdy wiesz, że będziesz potrzebować powiązanych danych, i chcesz uniknąć dodatkowych zapytań (np. w przypadku problemu N+1).