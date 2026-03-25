# Dziedziczenie adnotacji Jackson

**Data:** 2025-03-14

---

**User:**

W klasie modelu w Java mam adnotacje takie jak @JsonProperty, @JsonPropertyOrder. Czy jeśli tworze nową klasę która dziedziczy po tej pierwszej klasie to czy te adnotacje będą również dziedziczone?

---

**Assistant:**

Dobre pytanie!

### Odpowiedź:
W Javie **adnotacje takie jak `@JsonProperty` czy `@JsonPropertyOrder` z biblioteki Jackson _nie są dziedziczone automatycznie_ przez klasy potomne**, jeśli są zadeklarowane na polach lub metodach (czyli na poziomie członków klasy).

#### Szczegóły:

1. **`@JsonProperty` na polach/metodach** – **dziedziczenie działa w tym sensie, że jeśli klasa potomna nie nadpisze pola/metody z adnotacją `@JsonProperty`, to Jackson dalej ją widzi.** Ale jeśli klasa potomna wprowadza nowe pola (bez tej adnotacji), musisz dodać ją ponownie, jeśli chcesz konkretną nazwę w JSON-ie.

2. **`@JsonPropertyOrder` na poziomie klasy** – **ta adnotacja nie jest dziedziczona**, bo Jackson nie kopiuje adnotacji z klasy nadrzędnej. Jeśli chcesz mieć konkretną kolejność pól w JSON-ie w klasie pochodnej, musisz **dodać `@JsonPropertyOrder` także tam**, nawet jeśli kolejność jest taka sama.

---

### Przykład:

```java
@JsonPropertyOrder({ "id", "name" })
public class BaseDto {
    @JsonProperty("id")
    private Long id;

    @JsonProperty("name")
    private String name;
}
```

```java
public class ExtendedDto extends BaseDto {
    @JsonProperty("extra")
    private String extra;
}
```

Jeśli teraz serializujesz `ExtendedDto`, kolejność pól **nie będzie zgodna z `@JsonPropertyOrder` z `BaseDto`**, bo Jackson jej nie widzi w `ExtendedDto`. Trzeba ją powtórzyć:

```java
@JsonPropertyOrder({ "id", "name", "extra" })
public class ExtendedDto extends BaseDto {
    @JsonProperty("extra")
    private String extra;
}
```

---

### Podsumowanie:
- `@JsonProperty` – działa na polach/metodach klas nadrzędnych (jeśli są odziedziczone).
- `@JsonPropertyOrder` – **musisz dodać w każdej klasie osobno**.
- Jeśli zależy Ci na pełnej kontroli nad dziedziczeniem i konfiguracją JSON, można też używać `@JsonAutoDetect`, `@JsonInclude`, `@JsonIgnoreProperties`, itd., ale one też mają swoje zasady dziedziczenia.

Chcesz, żebym przygotował prosty przykład kodu do przetestowania tego w praktyce?