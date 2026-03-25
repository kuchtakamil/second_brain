# BPM flag sharing w Javie

**Data:** 2025-06-12

---

**User:**

Tworzę diagram BPM z użyciem Javy pod spodem. W jednym z początkowych tasków ustawiam sobie flagę pokazującą czy feature switch jest włączony. Kilka tasków dalej chciałbym odczytać to property ustawione w tasku o którym wspominałem na początku. Czy mogę to zrobić?

---

**Assistant:**

Tak, możesz to zrobić – w diagramach BPM (np. w Activiti, Camunda czy Flowable), dane ustawione w jednym tasku procesu są przechowywane w kontekście procesu (tzw. **process variables**), więc są dostępne w innych taskach tego samego procesu.

### Jak to działa:

#### 1. **Ustawienie zmiennej w tasku:**

W tasku (np. `JavaDelegate` albo `ExecutionListener`) możesz ustawić zmienną:

```java
execution.setVariable("featureSwitchEnabled", true);
```

#### 2. **Odczyt zmiennej w późniejszym tasku:**

W kolejnym tasku, nawet jeśli jest on kilka kroków dalej w BPMN, możesz odczytać zmienną tak samo:

```java
Boolean featureSwitchEnabled = (Boolean) execution.getVariable("featureSwitchEnabled");
```

### Uwagi:

- Zmienna ustawiona przez `execution.setVariable(...)` jest domyślnie ustawiana jako zmienna procesu (czyli widoczna w całym procesie).
- Możesz też użyć `execution.setVariableLocal(...)`, ale wtedy zmienna będzie widoczna tylko w danym tasku — tego raczej nie chcesz w tym przypadku.
- Jeśli masz subprocesy, zwróć uwagę, czy nie nadpisujesz lub nie ograniczasz widoczności zmiennych przez `local` scope.

### Dobre praktyki:

- Używaj nazw zmiennych z prefiksem lub w sposób jednoznaczny, żeby uniknąć kolizji.
- Jeśli masz wiele takich flag, rozważ grupowanie ich w obiekt (np. `ProcessContext`), i ustawienie/odczyt jednej zmiennej z obiektem jako wartość.

Przykład:

```java
public class ProcessContext {
    private boolean featureSwitchEnabled;
    // inne pola, gettery/settery
}

// zapis
ProcessContext context = new ProcessContext();
context.setFeatureSwitchEnabled(true);
execution.setVariable("processContext", context);

// odczyt
ProcessContext context = (ProcessContext) execution.getVariable("processContext");
```

Jeśli chcesz, mogę pomóc Ci dobrać sposób najlepiej pasujący do Twojego diagramu i stylu kodu.