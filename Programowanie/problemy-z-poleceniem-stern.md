# Problemy z poleceniem stern

**Data:** 2025-03-10

---

**User:**

co jest nie tak z poleceniem stern ipt-fgr-svc-kd-fffsdfgb9-h5v2m -n sst2-cw

---

**Assistant:**

Polecenie, które podałeś:

```
stern ipt-fgr-svc-kd-fffsdfgb9-h5v2m -n sst2-cw
```

jest składniowo poprawne dla narzędzia `stern`, ale może być kilka powodów, dla których ono **nie działa tak, jak oczekujesz**.

Sprawdź poniższe punkty:

---

### ✅ **1. Czy `stern` jest zainstalowany?**
Upewnij się, że masz zainstalowane narzędzie `stern`:
```bash
stern --version
```
Jeśli nie — zainstaluj:  
https://github.com/stern/stern

---

### ✅ **2. Czy podałeś prawidłową nazwę podu (albo wzorzec)?**
`s‍tern` używa **wzorców nazw podów (regex)**. Czy `ipt-fgr-svc-kd-fffsdfgb9-h5v2m` to dokładna nazwa poda, czy jego pełna nazwa zawiera np. suffix jak `-abc123`?

Może powinno być np.:
```bash
stern ipt-fgr-svc-kd -n sst2-cw
```
albo:
```bash
stern 'ipt-fgr-svc-kd.*' -n sst2-cw
```

---

### ✅ **3. Czy namespace `sst2-cw` istnieje?**
Sprawdź, czy namespace jest poprawny:
```bash
kubectl get ns
```
i
```bash
kubectl get pods -n sst2-cw
```

---

### ✅ **4. Czy masz dostęp do klastru K8s i namespace?**
Sprawdź, czy Twój `kubectl` działa:
```bash
kubectl get pods -n sst2-cw
```

Jeśli nie — może masz nie ten kontekst (`kubectl config get-contexts`, `kubectl config use-context`) albo brak uprawnień.

---

### ✅ **5. Czy jest jakikolwiek pod o tej nazwie?**
Upewnij się, że pod istnieje:
```bash
kubectl get pods -n sst2-cw | grep ipt-fgr-svc-kd
```

---

### ✅ **6. Czy `stern` pokazuje jakiś błąd?**
Podaj komunikat błędu — będzie łatwiej znaleźć przyczynę.

---

Jeśli chcesz — wklej, co zwraca:
```bash
kubectl get pods -n sst2-cw
```
i
```bash
stern ipt-fgr-svc-kd-fffsdfgb9-h5v2m -n sst2-cw
```

to podpowiem konkretniej 🙂

Chcesz, żebym pomógł z regexem do `stern`, żeby odpalać logi niezależnie od suffixów poda?

---

**User:**

czy jest możliwość żeby wyświetlić wszystkie context które można użyć w stern?

---

**Assistant:**

Świetne pytanie!

`stern` **nie ma wbudowanego polecenia do listowania dostępnych kontekstów Kubernetes**, ponieważ sam nie zarządza kontekstami — używa po prostu tego, co masz ustawione w `kubectl config`.

Ale **możesz wyświetlić wszystkie dostępne konteksty** w systemie używając `kubectl`:

```bash
kubectl config get-contexts
```

Przykład:
```
CURRENT   NAME                     CLUSTER                  AUTHINFO             NAMESPACE
*         dev-cluster              dev-cluster              dev-user             default
          prod-cluster             prod-cluster             prod-user            default
```

Jeśli chcesz użyć konkretnego kontekstu w `stern`, możesz go podać przez opcję:

```bash
stern <pattern> --context <context-name>
```

np.
```bash
stern myapp -n mynamespace --context prod-cluster
```

---

### Bonus: Jak zmienić kontekst "na stałe"
```bash
kubectl config use-context <context-name>
```

---

Chcesz, żebym napisał prosty alias lub skrypt bashowy, który wylistuje dostępne konteksty i odpala `stern` z wybranym? 😊

---

**User:**

które z tych to context którego używa się w stern
NAME         CLUSTER      AUTHINFO     NAMESPACE

---

**Assistant:**

Świetnie, pytasz konkretnie — już tłumaczę:

W `kubectl config get-contexts` widzisz taką tabelę:

```
NAME         CLUSTER      AUTHINFO     NAMESPACE
```

👉 **To właśnie kolumna `NAME` zawiera nazwę kontekstu**, którego używa się w `stern` (i również w `kubectl config use-context`).

### Czyli:
Jeśli chcesz odpalić `stern` z konkretnym kontekstem, to używasz **wartości z kolumny `NAME`**, np.:

```bash
stern myapp -n mynamespace --context <NAME>
```

Przykład:
```bash
stern myapp -n sst2-cw --context dev-cluster
```
*(zakładając, że `dev-cluster` to wartość z kolumny `NAME`)*

---

### 🔍 Dodatkowe wyjaśnienie:
- `CLUSTER` – wskazuje nazwę klastra K8s skonfigurowanego w kubeconfigu.
- `AUTHINFO` – mówi, jakiego użytkownika (credentials) używasz.
- `NAMESPACE` – opcjonalny namespace domyślny (jeśli nie podasz `-n` w `kubectl`).

---

Jeśli chcesz, mogę przygotować Ci prosty skrypt typu:
```bash
select-k8s-context-and-run-stern.sh
```
który pokaże listę kontekstów i odpali `stern` z wybranym. Chcesz? :)

---

**User:**

żeby wyświetlić logi tylko głównego kontenera bez sidecarów trzeba
stern charts-svc-kd -c charts-svc-kc
+ charts-svc-kd-22csdfcbf-lrct2 › charts-svc-kc
ale skąd mam wiedzieć że mam np podać taką nazwę charts-svc-kc

---

**Assistant:**

Świetne pytanie — to jest częsty problem przy pracy z `stern`, gdy masz pody z kilkoma kontenerami (np. sidecar + główny kontener).

Faktycznie:
```bash
stern charts-svc-kd -c charts-svc-kc
```
wyświetla logi tylko dla kontenera `charts-svc-kc` w podach pasujących do wzorca `charts-svc-kd`.

Ale skąd wziąć **nazwę kontenera**, np. `charts-svc-kc`? Już pokazuję:

---

### 🔍 Jak sprawdzić nazwę kontenera w podzie?

#### 1️⃣ Najprościej:
```bash
kubectl get pod <pod-name> -n <namespace> -o jsonpath="{.spec.containers[*].name}"
```

Przykład:
```bash
kubectl get pod charts-svc-kd-22csdfcbf-lrct2 -n sst2-cw -o jsonpath="{.spec.containers[*].name}"
```

Wyjście może być np.:
```
charts-svc-kc istio-proxy
```

Czyli masz:
- `charts-svc-kc` → Twój główny kontener
- `istio-proxy` → sidecar (np. z Istio)

Teraz możesz powiedzieć sternowi:
```bash
stern charts-svc-kd -n sst2-cw -c charts-svc-kc
```

---

#### 2️⃣ Alternatywa — YAML z `kubectl describe`:
```bash
kubectl describe pod charts-svc-kd-22csdfcbf-lrct2 -n sst2-cw
```

W sekcji `Containers:` zobaczysz wszystkie kontenery z nazwami.

---

#### 3️⃣ Ewentualnie pełny pod YAML:
```bash
kubectl get pod charts-svc-kd-22csdfcbf-lrct2 -n sst2-cw -o yaml
```
Tam też znajdziesz `.spec.containers.name`.

---

### ➕ Pro tip:
Jeśli często potrzebujesz głównego kontenera, a sidecar ma zawsze konkretną nazwę (np. `istio-proxy`, `envoy`, `sidecar`, itp.), możesz użyć exclude/include w `stern`:
```bash
stern charts-svc-kd -n sst2-cw --exclude-container istio-proxy
```

---

Chcesz, żebym przygotował alias/skrypt typu `stern-main-container`, który automatycznie pobierze nazwę pierwszego kontenera w podzie i uruchomi `stern` z tym kontenerem? :)