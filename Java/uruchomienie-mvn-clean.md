# Uruchomienie mvn clean

**Data:** 2025-06-14

---

**User:**

czy możliwe jest uruchomienie mvn clean bez zainstalowanego pluginu maven-clean-plugin ?

---

**Assistant:**

Tak, **uruchomienie `mvn clean` jest możliwe nawet jeśli `maven-clean-plugin` nie jest jawnie zdefiniowany w Twoim `pom.xml`**, ponieważ:

### 🔹 Maven domyślnie korzysta z wbudowanych pluginów
Jeśli nie określisz wersji `maven-clean-plugin`, Maven automatycznie używa wersji domyślnej z tzw. **"super POM-a"** i własnej konfiguracji.

### 🔹 Co się dzieje przy `mvn clean`?
Polecenie `mvn clean` wywołuje fazę `clean`, która domyślnie używa `maven-clean-plugin`. Maven pobiera (jeśli jeszcze nie ma) odpowiednią wersję z repozytorium centralnego – zwykle np. `3.1.0` lub inną zgodną z Twoją wersją Mavena.

### 🔹 Kiedy może nie zadziałać?
`mvn clean` może nie działać **tylko wtedy, gdy Maven nie ma dostępu do internetu** (a plugin nie był wcześniej zainstalowany w lokalnym repozytorium), albo:
- Gdy repozytorium lokalne (`~/.m2/repository`) jest uszkodzone,
- Gdy centralne repozytorium jest niedostępne (w trybie offline),
- Gdy projekt wymusza konkretną wersję pluginu, a ta wersja nie istnieje.

---

### 🔧 Jak sprawdzić, jakiej wersji pluginu Maven używa?
Uruchom:

```bash
mvn help:effective-pom
```

I znajdź sekcję:

```xml
<plugin>
  <artifactId>maven-clean-plugin</artifactId>
  <version>...</version>
</plugin>
```

---

### ✅ Podsumowując:
- **Nie musisz jawnie instalować `maven-clean-plugin`, aby `mvn clean` działało.**
- Maven pobierze i użyje domyślnej wersji pluginu z repozytorium, o ile nie jesteś offline.
- Jeśli chcesz mieć pełną kontrolę, możesz jawnie dodać plugin i jego wersję do `pom.xml`.

Chcesz przykład takiego wpisu do `pom.xml`?