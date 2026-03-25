# Zmienna w pliku properties

**Data:** 2025-04-07

---

**User:**

Chcę w pliku properties dodać nowy property ale chcę odczytać wartość z innego miejsca i dołączyć nowe.
BLACKLIST=$BLACKLIST,MYNEW1,MYNEW2
Czy to ma sens? Czy w razie braku $BLACKLIST przecinek nie będzie problemem?

---

**Assistant:**

Tak, to ma sens, ale zależy, **jak i gdzie** używasz tego pliku `.properties` oraz **jak interpretowany jest `$BLACKLIST`**.

### Zakładam, że:
- To plik `.properties` w stylu Java / Spring.
- Wartość `BLACKLIST` chcesz rozszerzyć o dodatkowe elementy, np.:  
  `BLACKLIST=$BLACKLIST,MYNEW1,MYNEW2`

Ale ważne są szczegóły.

---

## 🔍 Analiza:

### 1. **Plik `.properties` sam w sobie nie rozwija zmiennych środowiskowych ani innych kluczy**
Tzn. zapis:
```properties
BLACKLIST=$BLACKLIST,MYNEW1,MYNEW2
```
**nie zadziała tak, jak w bashu** — czyli `$BLACKLIST` nie zostanie automatycznie zastąpione poprzednią wartością tego samego klucza.

Aby to działało, musisz mieć:
- Spring Boot i użyć **własnej** składni, np. `${BLACKLIST}`:
  ```properties
  BLACKLIST=${BLACKLIST},MYNEW1,MYNEW2
  ```
- Ale nawet wtedy — to działa tylko, jeśli `BLACKLIST` pochodzi z innego źródła (np. zmienna środowiskowa, inny plik, args, etc.).

### 2. **Co jeśli `${BLACKLIST}` jest puste?**
Jeśli `${BLACKLIST}` nie istnieje:
- W Spring Boot dostaniesz wartość: `,MYNEW1,MYNEW2`  
- Czyli będzie się zaczynać od przecinka — **co może być problemem**, jeśli aplikacja nie toleruje pustych elementów w liście.

---

## ✅ Rozwiązania:

### 🟢 Jeśli używasz Spring Boot:
I chcesz dodać domyślną wartość tylko, jeśli `$BLACKLIST` nie jest ustawione:
```properties
BLACKLIST=${BLACKLIST:MYNEW1,MYNEW2}
```

Ale jeśli chcesz **dołączyć** coś do istniejącej wartości, to niestety nie zrobisz tego "czysto" w `.properties`.

Możesz:
```properties
BLACKLIST=${BLACKLIST:},MYNEW1,MYNEW2
```
Ale to spowoduje przecinek na początku, jeśli `${BLACKLIST}` jest puste.

### 🛠️ Alternatywa (czystsza logika):
Zrób to w kodzie Javy:
```java
String raw = env.getProperty("BLACKLIST");
List<String> blacklist = new ArrayList<>();
if (raw != null && !raw.isBlank()) {
    blacklist.addAll(Arrays.asList(raw.split(",")));
}
blacklist.add("MYNEW1");
blacklist.add("MYNEW2");
```

---

## 💡 Podsumowanie:

- `BLACKLIST=$BLACKLIST,MYNEW1,MYNEW2` **nie zadziała** w zwykłym `.properties` — potrzebujesz `${...}` i wsparcia zewnętrznego (np. Spring Boot).
- Przecinek na początku może być problemem, jeśli nie oczyszczasz pustych wartości.
- Najbezpieczniej: dodawaj programistycznie, lub zrób to osobno na poziomie builda/skryptu.

Chcesz to robić w Springu, skrypcie bashowym, czy czymś innym? Mogę podrzucić gotowy przykład.