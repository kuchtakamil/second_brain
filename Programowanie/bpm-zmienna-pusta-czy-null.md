# BPM zmienna pusta czy null

**Data:** 2025-06-26

---

**User:**

Diagramy BPM. Czy ustawienie zmiennej na pusty string oznacza to samo, co nieustawienie tej zmiennej?

---

**Assistant:**

W kontekście diagramów **BPMN** (Business Process Model and Notation), a konkretnie w silnikach procesów takich jak **Activiti**, **Camunda** czy **Flowable**, **ustawienie zmiennej na pusty string (`""`) nie jest tym samym, co jej nieustawienie** (czyli brak tej zmiennej w kontekście procesu).

### Różnice:

| Sytuacja                        | Opis                                                                 |
|-------------------------------|----------------------------------------------------------------------|
| **Brak zmiennej (null)**       | Zmienna nie istnieje w kontekście procesu – jest `null` lub `niezdefiniowana`. |
| **Pusty string (`""`)**        | Zmienna istnieje i ma wartość pustego ciągu znaków – nie `null`, tylko `""`.    |

### Przykładowe konsekwencje:

1. **Warunki w gatewayach (exclusive gateways)**:
   - Warunek typu `${myVar == null}`:
     - Zadziała **tylko wtedy**, gdy zmienna nie istnieje lub ma wartość `null`.
     - Nie zadziała, jeśli zmienna to `""`.

2. **Skrypty i delegaty Java**:
   - `execution.getVariable("myVar") == null` będzie `true` tylko dla nieistniejącej lub nullowej zmiennej.
   - Jeśli zmienna to `""`, nadal jest to obiekt – pusty string, a nie `null`.

3. **Serializacja i zapisywanie historii procesu**:
   - Pusta zmienna może być zapisana w historii jako mająca konkretną (choć pustą) wartość.
   - Brak zmiennej to brak rekordu lub `null`.

4. **Wyzwalanie warunków, np. boundary eventów czy listeners**:
   - Czasem obecność zmiennej (nawet pustej) jest wystarczająca do wyzwolenia jakiegoś działania.

---

### Podsumowanie:

> **Nie – pusty string nie oznacza braku zmiennej.**

W logice procesów BPM (np. w Activiti), musisz traktować te dwa stany jako **odrębne** i odpowiednio je obsługiwać w warunkach oraz skryptach.

Jeśli chcesz, mogę podać przykład z XML BPMN albo kodu w Java delegate pokazujący różnicę.