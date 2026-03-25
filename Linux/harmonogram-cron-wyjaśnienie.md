# Harmonogram Cron wyjaśnienie

**Data:** 2024-11-28

---

**User:**

Cron co to oznacza "30 20 * * 1-5"

---

**Assistant:**

Wyrażenie Cron `30 20 * * 1-5` określa harmonogram dla zadania, które ma być wykonywane zgodnie z poniższymi zasadami:

- **Minuta** (`30`): o 30. minucie.
- **Godzina** (`20`): o godzinie 20:00.
- **Dzień miesiąca** (`*`): każdego dnia miesiąca.
- **Miesiąc** (`*`): każdego miesiąca.
- **Dzień tygodnia** (`1-5`): od poniedziałku do piątku (gdzie 1 to poniedziałek, a 5 to piątek).

### Interpretacja:
Zadanie zostanie uruchomione o godzinie **20:30** od poniedziałku do piątku, każdego dnia miesiąca i każdego miesiąca. 

### Przykład:
Jeśli dziś jest poniedziałek, to zadanie uruchomi się o 20:30. Jeśli dziś jest sobota, to zadanie nie zostanie uruchomione.