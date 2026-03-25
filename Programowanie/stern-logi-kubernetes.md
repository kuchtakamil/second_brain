# Stern logi Kubernetes

**Data:** 2025-05-20

---

**User:**

Co robi to polecenie i dlaczego nazwa poda jest powtórzona?
 stern itty-char-svc-kd -c itty-char-svc-kc > log.log

---

**Assistant:**

Polecenie:

```bash
stern itty-char-svc-kd -c itty-char-svc-kc > log.log
```

rozbija się na następujące elementy:

- `stern`: narzędzie do obserwowania logów z wielu podów w Kubernetes w czasie rzeczywistym.
- `itty-char-svc-kd`: **nazwa poda lub prefiks**, który `stern` wykorzystuje do filtrowania podów — w tym przypadku wybiera poda, którego nazwa zaczyna się od `itty-char-svc-kd`.
- `-c itty-char-svc-kc`: oznacza kontener (`-c` = `--container`) — w podzie można mieć wiele kontenerów, a to polecenie wybiera logi konkretnego kontenera o nazwie `itty-char-svc-kc`.
- `> log.log`: przekierowuje wynik (logi) do pliku `log.log`.

---

### Dlaczego nazwa poda i kontenera się różnią?
W Kubernetes nie ma obowiązku, żeby kontener w podzie miał taką samą nazwę jak pod. W praktyce często:
- **nazwa poda** = `nazwa-deploymentu` + hash lub suffix generowany przez K8s (czyli np. `itty-char-svc-kd-1234abcd`)
- **kontener** może mieć inną nazwę, np. `itty-char-svc-kc`, ustawioną w definicji deploymentu.

### Dlaczego wygląda, jakby nazwa była powtórzona?
Bo obie zaczynają się od `itty-char-svc-`, ale dalej różnią się końcówką:
- `kd` to część nazwy poda,
- `kc` to nazwa kontenera.

Możliwe, że są to skróty, np.:
- `kd` = "kubernetes deployment"
- `kc` = "kubernetes container"

lub po prostu różne komponenty tej samej aplikacji.

---

### Przykład działania
Jeśli masz deployment z jednym pod-em o nazwie `itty-char-svc-kd-xyz123` i w nim kontener `itty-char-svc-kc`, to polecenie:

```bash
stern itty-char-svc-kd -c itty-char-svc-kc
```

pobierze logi **tylko z tego jednego kontenera** i zapisze je do `log.log`.

---

Jeśli chcesz, mogę pomóc Ci napisać bardziej elastyczne polecenie `stern`, np. do zbierania logów z kilku podów lub kontenerów.