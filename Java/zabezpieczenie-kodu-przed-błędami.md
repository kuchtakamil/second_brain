# Zabezpieczenie kodu przed błędami

**Data:** 2023-12-04

---

**User:**

Jak poprawić ten kod w java tak aby zabezoieczyć go przed brakiem properties
KEY, PRIORITY, DISCIPLINE_CODE

    JsonObject awareProperties = new JsonObject();
    for (JsonElement dispatcher : dispatchers) {
      JsonObject dispatcherJson = dispatcher.getAsJsonObject();
      String key = dispatcherJson.get(KEY).getAsString();
      String priority = dispatcherJson.get(PRIORITY).getAsString();
      String disciplineCode = dispatcherJson.get(DISCIPLINE_CODE).getAsString();

      String awarePriority = calculateAwarePriority(priority);
      String icon = calculateIcon(disciplineCode, awarePriority);

      JsonObject keyJson = new JsonObject();
      keyJson.addProperty(AWARE_PRIORITY, awarePriority);
      JsonObject displayIconJson = new JsonObject();
      displayIconJson.addProperty(ICON, icon);
      keyJson.add(DISPLAY_ICON, displayIconJson);

      awareProperties.add(key, keyJson);
    }

---

**Assistant:**

Aby zabezpieczyć kod przed brakiem właściwości (properties) kluczy `KEY`, `PRIORITY`, `DISCIPLINE_CODE`, możesz dodać sprawdzenie, czy te klucze istnieją przed próbą ich pobrania. Możesz to zrobić za pomocą metody `has` na obiekcie `JsonObject`. Poniżej znajduje się poprawiony kod:

```java
JsonObject awareProperties = new JsonObject();
for (JsonElement dispatcher : dispatchers) {
    JsonObject dispatcherJson = dispatcher.getAsJsonObject();

    // Sprawdzenie, czy klucze istnieją
    if (dispatcherJson.has(KEY) && dispatcherJson.has(PRIORITY) && dispatcherJson.has(DISCIPLINE_CODE)) {
        String key = dispatcherJson.get(KEY).getAsString();
        String priority = dispatcherJson.get(PRIORITY).getAsString();
        String disciplineCode = dispatcherJson.get(DISCIPLINE_CODE).getAsString();

        String awarePriority = calculateAwarePriority(priority);
        String icon = calculateIcon(disciplineCode, awarePriority);

        JsonObject keyJson = new JsonObject();
        keyJson.addProperty(AWARE_PRIORITY, awarePriority);
        JsonObject displayIconJson = new JsonObject();
        displayIconJson.addProperty(ICON, icon);
        keyJson.add(DISPLAY_ICON, displayIconJson);

        awareProperties.add(key, keyJson);
    } else {
        // Obsługa przypadku braku jednego z kluczy
        System.err.println("Brak jednego z kluczy: KEY, PRIORITY lub DISCIPLINE_CODE");
        // Możesz dodać odpowiednią obsługę błędu lub zignorować ten element
    }
}
```

W tym kodzie przed pobraniem wartości dla kluczy `KEY`, `PRIORITY`, `DISCIPLINE_CODE`, używamy metody `has`, aby sprawdzić, czy dany klucz istnieje w obiekcie `dispatcherJson`. Jeśli któryś z kluczy nie istnieje, możesz obsłużyć ten przypadek, dodając odpowiednie logowanie błędu lub inny sposób obsługi braku właściwości.

---

**User:**

a czy można tu użyć Optional?

---

**Assistant:**

Tak, możesz użyć `Optional` do zabezpieczenia się przed brakiem właściwości. Jednak należy pamiętać, że biblioteka `Optional` jest dostępna od wersji Java 8. Oto jak można to zrobić:

```java
JsonObject awareProperties = new JsonObject();
for (JsonElement dispatcher : dispatchers) {
    JsonObject dispatcherJson = dispatcher.getAsJsonObject();

    // Użycie Optional do pobrania wartości z obiektu JSON
    Optional<String> keyOptional = Optional.ofNullable(dispatcherJson.get(KEY)).map(JsonElement::getAsString);
    Optional<String> priorityOptional = Optional.ofNullable(dispatcherJson.get(PRIORITY)).map(JsonElement::getAsString);
    Optional<String> disciplineCodeOptional = Optional.ofNullable(dispatcherJson.get(DISCIPLINE_CODE)).map(JsonElement::getAsString);

    // Sprawdzenie, czy wszystkie wymagane wartości są obecne
    if (keyOptional.isPresent() && priorityOptional.isPresent() && disciplineCodeOptional.isPresent()) {
        String key = keyOptional.get();
        String priority = priorityOptional.get();
        String disciplineCode = disciplineCodeOptional.get();

        String awarePriority = calculateAwarePriority(priority);
        String icon = calculateIcon(disciplineCode, awarePriority);

        JsonObject keyJson = new JsonObject();
        keyJson.addProperty(AWARE_PRIORITY, awarePriority);
        JsonObject displayIconJson = new JsonObject();
        displayIconJson.addProperty(ICON, icon);
        keyJson.add(DISPLAY_ICON, displayIconJson);

        awareProperties.add(key, keyJson);
    } else {
        // Obsługa przypadku braku jednej z wartości
        System.err.println("Brak jednej z wartości: KEY, PRIORITY lub DISCIPLINE_CODE");
        // Możesz dodać odpowiednią obsługę błędu lub zignorować ten element
    }
}
```

Użycie `Optional` pomaga zwięźlej zarządzać przypadkiem braku wartości, eliminując potrzebę ręcznego sprawdzania nulli. Jednak niektórzy programiści preferują unikanie `Optional` w sytuacjach, gdzie zwykłe sprawdzanie nulli jest wystarczająco czytelne i zwięzłe. Warto rozważyć, które podejście lepiej pasuje do stylu programowania w danej sytuacji.