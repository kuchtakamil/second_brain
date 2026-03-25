# Stern i logi Kubernetes

**Data:** 2025-03-17

---

**User:**

chcę za pomocą stern ściągnąć wszystkie logi ze wszystkich podów ipt-chkval-svc-kd. Jak to zorbić
stern ipt-chkval-svc-kd --context atlas3 -n feat-i-cw-atlas3

---

**Assistant:**

Komenda, którą podałeś, jest już bliska poprawnej. `stern` domyślnie strumieniuje logi „na żywo” z podów, które pasują do wzorca nazwy. Jeśli chcesz pobrać **wszystkie logi historyczne**, `stern` sam w sobie **nie ma opcji do pobierania pełnych logów wstecznych**, bo jest narzędziem do podglądu strumienia logów (jak `kubectl logs -f`). Można jednak wyciągnąć więcej logów przy pomocy opcji `--since`.

Przykład:
```bash
stern ipt-chkval-svc-kd --context atlas3 -n feat-i-cw-atlas3 --since 24h
```

To pobierze logi z ostatnich 24 godzin dla wszystkich podów pasujących do `ipt-chkval-svc-kd`.

### Jeśli chcesz wszystkie logi (maksymalnie, co trzyma kubelet):
Możesz spróbować dać duży zakres czasu:
```bash
stern ipt-chkval-svc-kd --context atlas3 -n feat-i-cw-atlas3 --since 168h
```
(= 7 dni)

### Alternatywa: `kubectl logs`
Jeśli chcesz _pełne logi_ jednorazowo (nie strumień), to `kubectl logs` daje większą kontrolę. Przykład pobrania logów ze wszystkich replik podów:

```bash
kubectl get pods -n feat-i-cw-atlas3 --context atlas3 | grep ipt-chkval-svc-kd
```

Potem np. (dla każdego poda):

```bash
kubectl logs <pod-name> -n feat-i-cw-atlas3 --context atlas3 > <pod-name>.log
```

Możesz też zrobić to pętlą:

```bash
for pod in $(kubectl get pods -n feat-i-cw-atlas3 --context atlas3 -o name | grep ipt-chkval-svc-kd); do
  kubectl logs $pod -n feat-i-cw-atlas3 --context atlas3 > "${pod##*/}.log"
done
```

### Podsumowanie:
- `stern` jest świetne do podglądu bieżącego logowania, ale do "ściągania pełnych logów" lepszy będzie `kubectl logs`.
- `stern` możesz używać z `--since`, ale nie da się nim pobrać „pełnej historii” jak w `kubectl logs`.
- Jeśli zależy Ci na historii, warto pisać logi do zewnętrznego systemu (np. Loki, Elasticsearch, Datadog itp.).

Chcesz, żebym napisał skrypt bashowy, który automatycznie pobierze wszystkie logi ze wszystkich podów i zapisze je do plików?

---

**User:**

jak zacząć zbierać logi od teraz ?

---

**Assistant:**

Świetne pytanie — jeśli chcesz **zacząć zbierać logi "od teraz"**, możesz po prostu uruchomić `stern`, który będzie strumieniował logi bieżące z pasujących podów.

### ✅ Najprostszy sposób:
```bash
stern ipt-chkval-svc-kd --context atlas3 -n feat-i-cw-atlas3
```
To uruchomi strumień logów w terminalu od momentu wywołania — czyli zbierasz "od teraz".

### 💡 Jeśli chcesz zapisać je do pliku:
```bash
stern ipt-chkval-svc-kd --context atlas3 -n feat-i-cw-atlas3 > logs_ipt-chkval_$(date +%F_%H-%M-%S).log
```

Ten sposób pozwala Ci zbierać logi na bieżąco do pliku — dopóki nie przerwiesz `stern` (`Ctrl+C`).

### 📌 Uwaga: logi nie będą zapisywane w tle po zamknięciu terminala

Jeśli chcesz zbierać logi **ciągle, nawet po zamknięciu terminala**, użyj np.:

#### Opcja 1: `nohup`
```bash
nohup stern ipt-chkval-svc-kd --context atlas3 -n feat-i-cw-atlas3 > logs_ipt-chkval.log 2>&1 &
```

#### Opcja 2: `screen` lub `tmux`
Uruchom `screen` lub `tmux`, odpal `stern`, zostaw go tam — logi będą się zbierać.

---

Chcesz może gotowy mini-skrypt, który odpala to z `nohup` i zapisuje logi z timestampem? Albo wolisz coś bardziej automatycznego — np. cron job na zbieranie logów co godzinę?

---

**User:**

Gdy uruchamiam stern ipt-chkval-svc-kd --context atlas3 -n feat-i-cw-atlas3 zbierają się logi również z sidecarów np. filebeat. Czy jest możliwość aby się ich pozbyć?

---

**Assistant:**

Tak, dokładnie — `stern` domyślnie zbiera logi ze **wszystkich kontenerów w podzie**, czyli także z sidecarów takich jak `filebeat`, `istio-proxy`, itp.

### ✅ Jak filtrować logi tylko z wybranych kontenerów?

Możesz użyć opcji `-c` / `--container` w `stern`, żeby ograniczyć logi tylko do konkretnego kontenera w podzie.

#### Przykład:
```bash
stern ipt-chkval-svc-kd --context atlas3 -n feat-i-cw-atlas3 -c main-container-name
```

Zastąp `main-container-name` nazwą kontenera, z którego **faktycznie chcesz logi** (czyli ten, który zawiera Twoją aplikację, a nie sidecary).

---

### 🔍 Jak sprawdzić nazwę kontenera?

Możesz sprawdzić nazwy kontenerów w podach np. tak:
```bash
kubectl get pod <nazwa-poda> -n feat-i-cw-atlas3 -o jsonpath="{.spec.containers[*].name}"
```

albo z listą:
```bash
kubectl describe pod <nazwa-poda> -n feat-i-cw-atlas3
```

Przykład odpowiedzi:
```
Containers:
  - app
  - filebeat
```
Wtedy używasz `-c app`.

---

### ✨ Alternatywnie: filtrowanie za pomocą regexa

Jeśli masz wiele kontenerów aplikacyjnych o wspólnej nazwie (np. `app`, `svc`, `api`), możesz podać wzorzec kontenera:

```bash
stern ipt-chkval-svc-kd --context atlas3 -n feat-i-cw-atlas3 --container "^(app|svc)$"
```

To pozwoli pominąć np. `filebeat`, `istio-proxy`, itp.

---

Chcesz, żebym przygotował gotowy skrypt, który automatycznie wykrywa właściwe kontenery i odpala `stern` tylko dla nich?