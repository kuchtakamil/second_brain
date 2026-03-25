# Flaga przerwania wątków

**Data:** 2024-10-06

---

**User:**

Dlaczego w tym przykładzie została wywołana metoda Thread.currentThread().interrupt()?
Rozumiem, że we wnętrzu  Thread.sleep odbyło się sprawdzenie sprawdzenie flagi która jeśli była ustawiona na true, z powrotem została ustawiona na false. Więc  Thread.currentThread().interrupt() ponownie ustawia ją na true. Ale po co? Co dalej będzie się działo z tą flagą? Czy zostanie ponownie gdzieś sprawdzana? Gdzie?

try {
  Thread.sleep(100);
} catch (InterruptedException ex) {
  Thread.currentThread().interrupt(); // Here!
  throw new RuntimeException(ex);
}

---

**Assistant:**

W tym przykładzie metoda `Thread.currentThread().interrupt()` została wywołana po to, aby ponownie ustawić flagę przerwania wątku, którą metoda `Thread.sleep()` automatycznie resetuje (ustawia na `false`) po tym, jak zostanie zgłoszony wyjątek `InterruptedException`.

### Wyjaśnienie:

1. **Flaga przerwania:**
   Każdy wątek w Javie ma wewnętrzną flagę przerwania, która jest używana do sygnalizowania, że wątek został przerwany. Możesz ustawić tę flagę na `true` wywołując metodę `interrupt()` na danym wątku.

2. **Metoda `Thread.sleep()` i wyjątek `InterruptedException`:**
   Kiedy wątek wykonuje metodę `Thread.sleep()`, a w międzyczasie inny wątek wywoła metodę `interrupt()` na tym wątku, flaga przerwania zostaje ustawiona na `true` i zostaje rzucony wyjątek `InterruptedException`. Ważne jest to, że po rzuceniu wyjątku flaga przerwania wątku zostaje automatycznie zresetowana do `false`.

3. **Przywrócenie flagi przerwania:**
   W sytuacji, gdy nie chcesz ignorować tego przerwania, w catch blokach, takich jak w Twoim przykładzie, dobrą praktyką jest ponowne ustawienie tej flagi na `true` za pomocą `Thread.currentThread().interrupt()`. Dzięki temu flaga przerwania zostaje ponownie ustawiona, co może być istotne dla innych fragmentów kodu, które mogą sprawdzać tę flagę.

### Co się dzieje z flagą dalej?

Po ponownym ustawieniu flagi na `true` przy pomocy `Thread.currentThread().interrupt()`, inne części kodu mogą sprawdzać tę flagę, aby reagować na przerwanie. Niektóre metody i mechanizmy w Javie, które zależą od flagi przerwania wątku, mogą na jej podstawie podejmować decyzje, takie jak:

- **Metoda `Thread.interrupted()`:** zwraca wartość flagi przerwania i resetuje ją.
- **Metoda `Thread.currentThread().isInterrupted()`:** zwraca wartość flagi przerwania bez resetowania jej.
- **Blokady, warunki, semafory i inne mechanizmy synchronizacyjne:** wiele z tych mechanizmów sprawdza, czy wątek został przerwany, i mogą zgłaszać wyjątki (`InterruptedException`) lub reagować w inny sposób.

### Dlaczego to ważne?

Przerwania są używane jako mechanizm sygnalizacyjny, aby przerwać lub zakończyć długotrwałe operacje w wątku. Jeśli flaga przerwania zostanie zresetowana, wątek "nie będzie świadomy", że został przerwany, a inne mechanizmy, które bazują na tej fladze, mogą nie zareagować odpowiednio. Dlatego dobrą praktyką jest przywracanie flagi przerwania, aby inne fragmenty kodu mogły reagować na to przerwanie.