# Mapa PersonId do PersonId

**Data:** 2025-05-31

---

**User:**

W java mam mapę Person do Person. Jak zrobić z niej mapę PersonId do PersonId

---

**Assistant:**

Aby przekształcić mapę `Map<Person, Person>` na `Map<PersonId, PersonId>` w Javie, możesz użyć strumieni (Java 8+) lub klasycznej pętli. Zakładam, że klasa `Person` ma metodę `getId()` zwracającą `PersonId`.

### Przykład z użyciem stream API:

```java
Map<PersonId, PersonId> idToIdMap = personMap.entrySet().stream()
    .collect(Collectors.toMap(
        entry -> entry.getKey().getId(),
        entry -> entry.getValue().getId()
    ));
```

### Przykład z użyciem pętli:

```java
Map<PersonId, PersonId> idToIdMap = new HashMap<>();
for (Map.Entry<Person, Person> entry : personMap.entrySet()) {
    idToIdMap.put(entry.getKey().getId(), entry.getValue().getId());
}
```

### Uwaga
Jeśli istnieje ryzyko, że różni `Person` mogą mieć to samo `PersonId`, to przy użyciu `Collectors.toMap()` może wystąpić `IllegalStateException` z powodu duplikatów kluczy. Wtedy można to obsłużyć tak:

```java
Map<PersonId, PersonId> idToIdMap = personMap.entrySet().stream()
    .collect(Collectors.toMap(
        entry -> entry.getKey().getId(),
        entry -> entry.getValue().getId(),
        (existing, replacement) -> existing // lub replacement, zależnie od potrzeb
    ));
```

Daj znać, jeśli `PersonId` to np. `UUID`, `long` czy coś innego — mogę doprecyzować.

---

**User:**

Gdy mam stworzoną mapę, chciałbym ją przetestować jednostkowo. Jak w JUnit, używając asserti, przetestować klucze i wartości mapy?

---

**Assistant:**

Aby przetestować mapę w JUnit używając AssertJ (czyli "asserti"), możesz sprawdzać jej klucze, wartości, a także dokładną zawartość.

Załóżmy, że masz mapę:

```java
Map<PersonId, PersonId> actualMap = ...; // mapa, którą chcesz przetestować
```

I masz oczekiwane wartości:

```java
PersonId key1 = new PersonId(1L);
PersonId value1 = new PersonId(10L);
Map<PersonId, PersonId> expectedMap = Map.of(key1, value1);
```

### Przykład użycia AssertJ:

#### 1. Sprawdzenie, że mapa zawiera dokładnie te same wpisy (klucze i wartości):

```java
assertThat(actualMap).isEqualTo(expectedMap);
```

#### 2. Sprawdzenie, że mapa zawiera konkretny wpis:

```java
assertThat(actualMap).containsEntry(key1, value1);
```

#### 3. Sprawdzenie, że mapa zawiera klucz:

```java
assertThat(actualMap).containsKey(key1);
```

#### 4. Sprawdzenie, że mapa zawiera wartość:

```java
assertThat(actualMap).containsValue(value1);
```

#### 5. Sprawdzenie kluczy lub wartości jako zbiorów:

```java
assertThat(actualMap.keySet()).containsExactlyInAnyOrder(key1 /*, inne */);
assertThat(actualMap.values()).containsExactlyInAnyOrder(value1 /*, inne */);
```

---

### Bonus: Jeśli `PersonId` nie implementuje `equals()`/`hashCode()`, to:
Musisz to dodać, inaczej `Map` i porównania nie będą działać poprawnie.

---

Daj znać, czy chcesz przykład z mockowaniem `Person` albo budowaniem tej mapy w teście.

---

**User:**

AssertDead jest funkcją deprecated. Ponadto, gdy przekażę mu mapę i jej keyset, dostaję błąd, że CannotResolveMethod. Ale podoba mi się ten pomysł. Czy możesz zaproponować coś nowszego, co nie jest deprecated i co działa?

---

**Assistant:**

Dzięki za doprecyzowanie — świetnie, że używasz AssertJ, ale faktycznie:

- `assertThat(...)` nie jest przestarzałe, **ale może być problem z nieprawidłowym importem**.
- `assertThat(map).contains(...)` itp. działają, **o ile masz poprawnie skonfigurowaną bibliotekę AssertJ**.
- Jeśli IDE (np. IntelliJ) mówi `Cannot resolve method`, możliwe powody to:
  - Zły typ argumentu (np. `Set` vs `Map`)
  - Niepoprawne importy
  - Brak zależności do AssertJ w `pom.xml` / `build.gradle`

---

### ✅ Prawidłowy sposób testowania mapy z AssertJ (aktualny i nie deprecated)

Zakładam, że używasz JUnit 5 i AssertJ 3.x.

#### 🔹 1. Poprawny import:
Upewnij się, że masz:

```java
import static org.assertj.core.api.Assertions.assertThat;
```

#### 🔹 2. Przykład działania – test kluczy, wartości i par:

```java
@Test
void shouldContainExpectedEntries() {
    // given
    PersonId id1 = new PersonId(1L);
    PersonId id2 = new PersonId(2L);
    Map<PersonId, PersonId> map = Map.of(id1, id2);

    // then
    assertThat(map)
        .containsEntry(id1, id2)
        .containsKey(id1)
        .containsValue(id2)
        .hasSize(1);
    
    assertThat(map.keySet())
        .containsExactly(id1);

    assertThat(map.values())
        .containsExactly(id2);
}
```

#### 🔹 3. Sprawdzenie, że mapa ma dokładnie te same wpisy co inna mapa:

```java
Map<PersonId, PersonId> expected = Map.of(id1, id2);
assertThat(map).isEqualTo(expected);
```

---

### ❌ Przykład problemu, który może generować `Cannot resolve method`

```java
// Błąd: próbujesz użyć assertThat(Set) z metodami dla Map
Map<PersonId, PersonId> map = ...;
Set<PersonId> keys = map.keySet();
assertThat(keys).containsEntry(...) // ❌ Błąd, bo Set nie ma wpisów
```

**Poprawnie:**

```java
assertThat(keys).containsExactly(...); // np. containsExactly(id1)
```

---

### ✅ Zależność Maven dla AssertJ (jeśli nie masz):

```xml
<dependency>
  <groupId>org.assertj</groupId>
  <artifactId>assertj-core</artifactId>
  <version>3.25.3</version> <!-- lub najnowsza -->
  <scope>test</scope>
</dependency>
```

---

Jeśli nadal masz `Cannot resolve method`, podeślij konkretny kod lub typ zmiennej, której używasz w `assertThat(...)` — wtedy dokładnie powiem, co zmienić.

---

**User:**

Chyba już wiem, w czym leży problem. assert.dat używam z biblioteki JUnit, nie assert.j. Nie używam biblioteki assert.j w projekcie i nie mogę jej używać. Czy mogę coś podobnego zrobić z biblioteką JUnit?

---

**Assistant:**

Aha, to wszystko wyjaśnia — jeśli **nie możesz używać AssertJ**, tylko samego **JUnit (np. JUnit 5)**, to masz do dyspozycji klasyczne metody asercji z `org.junit.jupiter.api.Assertions`.

Nie są one tak ekspresywne jak w AssertJ, ale nadal pozwalają dobrze przetestować mapy.

---

### ✅ Co możesz zrobić z czystym JUnit (bez AssertJ)

Importuj:
```java
import static org.junit.jupiter.api.Assertions.*;
```

#### 🔹 Sprawdzenie, że mapa zawiera klucz i wartość:

```java
Map<PersonId, PersonId> map = Map.of(id1, id2);

assertTrue(map.containsKey(id1));
assertTrue(map.containsValue(id2));
assertEquals(id2, map.get(id1));
```

#### 🔹 Sprawdzenie dokładnej zawartości mapy:

```java
Map<PersonId, PersonId> expected = Map.of(id1, id2);
assertEquals(expected, map);
```

#### 🔹 Sprawdzenie kluczy i wartości osobno:

```java
Set<PersonId> expectedKeys = Set.of(id1);
Collection<PersonId> expectedValues = List.of(id2); // lub Set.of(...) jeśli porządek nie ma znaczenia

assertEquals(expectedKeys, map.keySet());
assertEquals(expectedValues, map.values());
```

#### 🔹 Sprawdzenie rozmiaru mapy:

```java
assertEquals(1, map.size());
```

---

### 🟡 Uwaga

JUnit nie ma takich metod jak `.containsEntry()` — wszystko musisz robić przez:

- `containsKey(...)`
- `containsValue(...)`
- `get(...)`
- `equals(...)`

Jeśli chcesz testy bardziej czytelne, możesz sobie napisać pomocnicze metody np.:

```java
private static <K, V> void assertContainsEntry(Map<K, V> map, K key, V value) {
    assertTrue(map.containsKey(key), "Brak klucza: " + key);
    assertEquals(value, map.get(key), "Niezgodna wartość dla klucza: " + key);
}
```

I używać jej w testach:

```java
assertContainsEntry(map, id1, id2);
```

---

Daj znać, jeśli chcesz gotowy snippet testu jednostkowego, który możesz wkleić do projektu.