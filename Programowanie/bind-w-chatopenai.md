# Bind w ChatOpenAI

**Data:** 2024-12-01

---

**User:**

Co robi tutaj bind?
import {addSchema, multiplySchema, subtractSchema} from "./schema"; 
import {parseFunctionCall} from "./helper.ts";
const model = new ChatOpenAI({
    modelName: "gpt-4-0613",
}).bind({functions: [addSchema, multiplySchema, subtractSchema]});

---

**Assistant:**

W tym kontekście `bind` jest metodą, która wiąże podane funkcje (tu: `addSchema`, `multiplySchema` i `subtractSchema`) z modelem `ChatOpenAI`. Dzięki temu model wie, jakie funkcje może wywołać w trakcie swojej pracy, np. podczas realizowania zapytań użytkownika. 

W przypadku bibliotek do integracji z modelami językowymi, takich jak OpenAI, funkcje dodane przez `bind` mogą być interpretowane jako dostępne "akcje", które model może wybrać, aby odpowiedzieć na pytanie użytkownika lub przetworzyć dane. 

W Twoim kodzie wygląda to tak:
1. **Import funkcji i schematów**: `addSchema`, `multiplySchema` i `subtractSchema` są schematami (np. walidatorami danych), które definiują funkcje do obsługi przez model.
2. **Konfiguracja modelu**: Tworzysz instancję `ChatOpenAI` z określonym modelem językowym (`gpt-4-0613`).
3. **Bind**: `bind` dodaje te schematy do modelu jako dostępne funkcje, które model może wykorzystać w kontekście funkcji, które obsługujesz w aplikacji.

### Przykładowe zastosowanie
Jeśli użytkownik poprosi o dodanie dwóch liczb, model może:
1. Rozpoznać, że musi użyć `addSchema`.
2. Wykonać funkcję `addSchema` i zwrócić wynik użytkownikowi.

Podsumowując, `bind` sprawia, że Twój model staje się bardziej interaktywny, potrafiąc wywoływać zdefiniowane funkcje w odpowiedzi na zadania użytkownika.