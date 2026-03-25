# Bezpieczne wywołanie stream()

**Data:** 2025-01-09

---

**User:**

Mam kod
        List<String> serviceDeliveriesChosen = Optional.ofNullable(params.get(MY_PARAM))
                .orElse(Collections.emptyList());


Czy teraz wywołanie 
serviceDeliveriesChosen.stream() 
jest bezpieczne?

---

**Assistant:**

Tak, wywołanie `serviceDeliveriesChosen.stream()` w przedstawionym przypadku jest bezpieczne. Oto dlaczego:

1. **`Optional.ofNullable` i `orElse(Collections.emptyList())`**  
   Dzięki temu konstruktorowi zawsze przypisujesz do zmiennej `serviceDeliveriesChosen` listę:
   - Jeśli `params.get(MY_PARAM)` zwraca `null`, zostanie przypisana pusta lista (`Collections.emptyList()`).
   - Jeśli `params.get(MY_PARAM)` zwraca nie-`null`, zostanie przypisana ta lista.

2. **`Collections.emptyList()`**  
   Metoda `Collections.emptyList()` zwraca niemutowalną pustą listę, która obsługuje wszystkie operacje na interfejsie `List`, w tym `stream()`.

3. **Gwarancja nie-`null`**  
   W wyniku tego kodu `serviceDeliveriesChosen` nigdy nie będzie miało wartości `null`. Może być tylko:
   - Pustą listą.
   - Listą zwróconą przez `params.get(MY_PARAM)`.

### Wnioski
Kod jest bezpieczny, a wywołanie `serviceDeliveriesChosen.stream()` nie spowoduje `NullPointerException`. Możesz go używać bez obaw.