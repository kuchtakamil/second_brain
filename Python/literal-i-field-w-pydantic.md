# Wyjaśnienie Literal i Field w Pydantic

Ten dokument wyjaśnia zastosowanie `Literal[1] = 1` oraz wielokropka (`...`) wraz z `Field` w klasach opartych na `BaseModel` z biblioteki Pydantic, na podstawie poniższego fragmentu kodu:

```python
from typing import Literal
from pydantic import BaseModel, Field

class KnowledgeChunk(BaseModel):
    schema_version: Literal[1] = 1
    build_id: str = Field(..., min_length=1)
```

## `schema_version: Literal[1] = 1`

Ta linijka definiuje pole `schema_version`, które ma bardzo restrykcyjne zasady:

1. **`Literal[1]` (Typowanie):**
   Użycie `Literal` z modułu `typing` (lub `typing_extensions`) oznacza, że zmienna może przyjąć **tylko i wyłącznie** jedną konkretną wartość: liczbę całkowitą `1`. Podanie jakiejkolwiek innej wartości (np. `2`, `"1"`) spowoduje błąd walidacji podczas tworzenia obiektu (tzw. `ValidationError`).
   
2. **`= 1` (Wartość domyślna):**
   Ponieważ przypisujemy `1`, staje się to wartością domyślną. Zatem w momencie tworzenia instancji `KnowledgeChunk()` nie trzeba w ogóle podawać `schema_version` – ustawi się automatycznie na `1`.

**Kiedy się to stosuje?**
Jest to bardzo popularny wzorzec do **wersjonowania schematów danych** (np. przy zapisywaniu do bazy lub plików JSON). W przyszłości, gdy struktura danych się zmieni, można utworzyć nową klasę z `Literal[2] = 2` (np. `KnowledgeChunkV2`) i na tej podstawie łatwo identyfikować lub rutować, z jaką wersją struktury mamy do czynienia. Zabezpiecza nas to przed zmianą na nieobsługiwaną wersję z poziomu kodu.

## `build_id: str = Field(..., min_length=1)`

Ta linijka definiuje właściwość `build_id`, która przechowuje identyfikator typu `str`:

1. **`Field(...)`:**
   Funkcja `Field` z Pydantic pozwala na określenie dodatkowych reguł walidacji i metadanych dla danego pola. 
   
2. **Wielokropek (`...`):**
   Wielokropek w Pythonie (obiekt `Ellipsis`) podany jako pierwszy argument w funkcji `Field` jest specjalnym wskaźnikiem Pydantic oznaczającym, że to **pole jest absolutnie wymagane**. Nie ma ono żadnej wartości domyślnej i użytkownik zawsze musi podać `build_id` przy tworzeniu nowej instancji klasy.
   *(Uwaga: W nowszych wersjach Pydantic v2, samo zadeklarowanie `build_id: str = Field(min_length=1)` wystarczy, by pole było wymagane, jednak notacja z `...` jest bardzo czytelna, powszechna i szeroko stosowana w bazach kodu migrowanych z v1 do v2).*

3. **`min_length=1`:**
   Oznacza dodatkową regułę walidacyjną: przekazany łańcuch znaków musi składać się z przynajmniej jednego znaku. Zapobiega to omyłkowemu przekazaniu pustego stringa `""` jako identyfikatora (co często się zdarza, gdy pobieramy dane z pustego formularza lub brakuje zmiennej środowiskowej).

## Podsumowanie - jak to działa w praktyce?

```python
# To zadziała poprawnie:
chunk1 = KnowledgeChunk(build_id="abc-123")
print(chunk1.schema_version)  # Wypisze: 1

# BŁĄD WALIDACJI (build_id nie może być puste - min_length=1):
chunk2 = KnowledgeChunk(build_id="")

# BŁĄD WALIDACJI (brak wymaganego pola build_id):
chunk3 = KnowledgeChunk()

# BŁĄD WALIDACJI (schema_version musi być równe dokładnie 1):
chunk4 = KnowledgeChunk(build_id="abc", schema_version=2)
```

Dzięki zastosowaniu Pydantic na tak podstawowym poziomie aplikacja zyskuje pewność, że tworzone i przekazywane przez nią dane są wolne od błędów typu pusty identyfikator czy nieprawidłowa wersja struktury.
