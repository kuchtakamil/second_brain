# 30 pytań rekrutacyjnych - Kubernetes (poziom Mid/Senior)

Poniższa lista zawiera 30 pytań rekrutacyjnych dotyczących Kubernetesa, z pominięciem absolutnych podstaw (np. "czym jest K8s" czy "jakie ma zalety"). Skupiają się one na architekturze, zarządzaniu stanem, bezpieczeństwie, sieci, troubleshootingu oraz dobrych praktykach. Pytania te mają na celu sprawdzić praktyczne zrozumienie działania klastra.

## Architektura i komponenty
1. W jaki sposób komunikuje się Kubelet z API Serverem i jakie informacje mu przekazuje?
2. Jaką rolę pełni `etcd` w klastrze i jak zapobiec utracie zapisanych w nim danych?
3. Co to jest Control Plane i co się stanie z uruchomionymi aplikacjami w klastrze, jeśli wszystkie węzły Control Plane ulegną awarii?
4. Jak działa Kube-proxy i jakie znasz tryby jego działania (np. iptables, IPVS)? Czym się one różnią pod kątem wydajności?
5. Na czym polega rola Cloud Controller Managera (CCM)?

## Pody, workloady i cykl życia
6. Czym różni się Deployment od StatefulSet z punktu widzenia zarządzania tożsamością, dyskami i kolejnością uruchamiania Podów?
7. W jakich przypadkach użyłbyś DaemonSet zamiast standardowego Deploymentu?
8. Jak działają initContainers i do jakich zadań najczęściej się je wykorzystuje?
9. Czym są i jak różnią się od siebie Liveness Probe, Readiness Probe oraz Startup Probe?
10. Jak Kubernetes zarządza ewakuacją Podów z węzła (Pod Eviction)? Do czego służy mechanizm `PodDisruptionBudget`?
11. Jak zachowa się klaster, gdy brakuje zasobów, by zaplanować Poda (stan Pending), a jak, gdy na istniejącym Nodzie zacznie brakować pamięci RAM (OOMKilled, Evicted)?

## Zarządzanie ruchem i sieć (Networking)
12. Jak w praktyce różni się działanie serwisu typu ClusterIP od NodePort i LoadBalancer?
13. Czym jest Ingress, jak działa Ingress Controller i dlaczego samo wdrożenie zasobu Ingress nie wystarczy do trasowania ruchu z zewnątrz?
14. W jaki sposób działa mechanizm Service Discovery wewnątrz klastra Kubernetes (jaka jest rola CoreDNS)?
15. Jak zaimplementowałbyś odseparowanie od siebie dwóch przestrzeni nazw (Namespace), aby Pody z jednej nie mogły nawiązywać połączeń z Podami z drugiej? (Network Policies)
16. Czym jest CNI (Container Network Interface) i z jakimi pluginami CNI miałeś do czynienia (np. Calico, Flannel, Cilium)? Co dają zaawansowane pluginy CNI?

## Storage i zarządzanie stanem
17. Opisz relację i różnice pomiędzy PersistentVolume (PV), PersistentVolumeClaim (PVC) a StorageClass.
18. Jak działa mechanizm dynamicznego provisioningu storage'u w Kubernetesie?
19. W jaki sposób Kubernetes gwarantuje, że Pod ze StatefulSet otrzyma po restarcie (nawet na innym węźle) podpięty dokładnie ten sam dysk z danymi?

## Bezpieczeństwo i uwierzytelnianie
20. Jak działa RBAC (Role-Based Access Control) w Kubernetesie? Wyjaśnij różnicę między `Role` a `ClusterRole` oraz `RoleBinding` a `ClusterRoleBinding`.
21. W jaki sposób bezpiecznie zarządzać sekretami w K8s? Dlaczego standardowe zasoby `Secret` nie są w 100% bezpieczne do trzymania w repozytorium kodu i jak temu zaradzić (np. SOPS, Sealed Secrets, External Secrets Operator)?
22. Czym są Security Contexts w konfiguracji Poda i kontenera? (Podaj przykłady: `runAsNonRoot`, `readOnlyRootFilesystem`, zrzucanie capabilities).
23. Czym różnią się Service Accounts od normalnych użytkowników w klastrze i jak Pody autoryzują się do API Servera?

## Skalowanie
24. Jak działa Horizontal Pod Autoscaler (HPA) i z jakiego komponentu czerpie on informacje do podjęcia decyzji o skalowaniu?
25. Na czym polega rola Cluster Autoscalera i dlaczego używa się go w parze z HPA?
26. Co to jest Vertical Pod Autoscaler (VPA) i dlaczego zazwyczaj nie stosuje się go jednocześnie z HPA dla skalowania na podstawie CPU/RAM?

## Troubleshooting i operacje (Day 2)
27. Masz Poda w statusie `CrashLoopBackOff`. Opisz krok po kroku komendy i proces, jak zabierzesz się za diagnozę tego problemu.
28. Jakie narzędzia lub metody zastosujesz, by rozwiązać problem z brakiem komunikacji sieciowej (Timeout) między dwoma Podami w klastrze?
29. Czym są mechanizmy Taints i Tolerations oraz jak można z nich korzystać wspólnie z Node Affinity/Anti-Affinity do kontrolowania, gdzie lądują Pody?
30. Jak poprawnie i bezpiecznie przeprowadzić aktualizację wersji Kubernetesa (upgrade węzłów klastra), aby zminimalizować czas niedostępności działających aplikacji (koncepcja cordon i drain)?
## Podstawowe komponenty z perspektywy programisty (Developer focus)

### Pod

**31. Co to jest Pod w Kubernetesie i dlaczego jest najmniejszą jednostką wdrożeniową?**

Pod to najmniejsza i najbardziej podstawowa jednostka wdrożeniowa w Kubernetesie. Reprezentuje on jeden lub więcej kontenerów, które współdzielą:
- **Sieć** — wszystkie kontenery w Podzie mają ten sam adres IP i mogą komunikować się przez `localhost`.
- **Storage** — mogą współdzielić wolumeny (volumes).
- **Cykl życia** — kontenery w Podzie są uruchamiane i zatrzymywane razem.

Kubernetes nie zarządza pojedynczymi kontenerami — zawsze operuje na poziomie Poda. Nawet jeśli Pod zawiera tylko jeden kontener, to Pod jest tą „opakowującą" abstrakcją.

**32. Czy jeden Pod może zawierać więcej niż jeden kontener? Jeśli tak, podaj przykład zastosowania (wzorzec sidecar).**

Tak. Klasyczne wzorce multi-kontenerowe:
- **Sidecar** — dodatkowy kontener, który rozszerza funkcjonalność głównego (np. kontener zbierający logi z pliku i wysyłający je do systemu centralnego).
- **Ambassador** — proxy pośredniczące w ruchu sieciowym (np. kontener z envoy proxy).
- **Adapter** — kontener transformujący dane wyjściowe głównego kontenera do ustandaryzowanego formatu (np. eksporter metryk Prometheus).

Kontenery w jednym Podzie komunikują się przez `localhost` i współdzielą wolumeny, co czyni ten wzorzec bardzo wydajnym.

**33. Co się dzieje z danymi zapisanymi wewnątrz kontenera po restarcie lub usunięciu Poda?**

Dane zapisane w warstwie zapisu kontenera (writable layer) są **efemeryczne** — zostają utracone po restarcie lub usunięciu Poda. Aby dane przetrwały, należy użyć wolumenów:
- `emptyDir` — przetrwa restart kontenera w ramach tego samego Poda, ale nie przetrwa usunięcia Poda.
- `PersistentVolume` (PV) via `PersistentVolumeClaim` (PVC) — dane przetrwają nawet usunięcie Poda.

---

### ReplicaSet

**34. Co to jest ReplicaSet i jaka jest jego główna odpowiedzialność w klastrze?**

ReplicaSet to kontroler, którego jedynym zadaniem jest **utrzymanie żądanej liczby replik (kopii) Poda** w danym momencie. Jeśli Pod ulegnie awarii lub zostanie usunięty, ReplicaSet automatycznie utworzy nowy, aby przywrócić stan do zadeklarowanej liczby replik (`spec.replicas`).

**35. W jaki sposób ReplicaSet wie, którymi Podami ma zarządzać (pojęcie selektorów etykiet / label selectors)?**

ReplicaSet używa mechanizmu **label selectors** (`spec.selector.matchLabels`). Każdy Pod tworzony przez ReplicaSet otrzymuje zestaw etykiet (labels). ReplicaSet monitoruje klaster i zlicza Pody pasujące do selektora — jeśli jest ich za mało, tworzy nowe; jeśli za dużo, usuwa nadmiarowe.

```yaml
selector:
  matchLabels:
    app: my-api
    version: v2
```

**36. Dlaczego w codziennej pracy programisty rzadko tworzy się zasób ReplicaSet bezpośrednio, a zamiast tego używa się Deploymentu?**

Ponieważ Deployment jest abstrakcją wyższego poziomu, która **zarządza ReplicaSetami automatycznie** i dodatkowo oferuje:
- Strategie aktualizacji (RollingUpdate, Recreate).
- Historię wersji i możliwość rollbacku.
- Deklaratywne zarządzanie cyklem życia aplikacji.

Bezpośrednie tworzenie ReplicaSetu nie daje żadnego z tych mechanizmów — programista musiałby ręcznie zarządzać wymianą Podów przy każdej aktualizacji obrazu.

---

### Deployment

**37. Co to jest Deployment i jakie dodatkowe możliwości deklaratywne oferuje w stosunku do samego ReplicaSetu?**

Deployment to zasób wyższego poziomu, który zarządza ReplicaSetami. Oferuje:
- **Deklaratywne aktualizacje** — zmiana obrazu kontenera w specyfikacji powoduje automatyczne wdrożenie nowej wersji.
- **Strategie wdrożenia** — kontrola nad tym, jak nowe Pody zastępują stare.
- **Historia rewizji** — Kubernetes przechowuje poprzednie ReplicaSety, umożliwiając rollback.
- **Pause/Resume** — możliwość wstrzymania wdrożenia w trakcie.

**38. Jakie znasz strategie aktualizacji aplikacji (strategie wdrożenia) dostępne domyślnie w Deploymencie?**

- **RollingUpdate** (domyślna) — stopniowo zastępuje stare Pody nowymi. Parametry `maxSurge` (ile dodatkowych Podów może istnieć ponad żądaną liczbę) i `maxUnavailable` (ile Podów może być niedostępnych) kontrolują tempo aktualizacji.
- **Recreate** — najpierw usuwa **wszystkie** stare Pody, a dopiero potem tworzy nowe. Powoduje krótką przerwę w działaniu (downtime), ale gwarantuje, że nigdy nie działają jednocześnie dwie wersje aplikacji.

**39. W jaki sposób można wycofać (rollback) błędną wersję aplikacji używając Deploymentu?**

```bash
# Sprawdzenie historii wdrożeń
kubectl rollout history deployment/my-app

# Cofnięcie do poprzedniej wersji
kubectl rollout undo deployment/my-app

# Cofnięcie do konkretnej rewizji
kubectl rollout undo deployment/my-app --to-revision=3
```

Kubernetes przechowuje poprzednie ReplicaSety (domyślnie 10 — `spec.revisionHistoryLimit`). Rollback polega na przeskalowaniu starego ReplicaSetu w górę i nowego w dół.

---

### Service

**40. Co to jest Service w Kubernetesie i jaki problem z Podami on rozwiązuje?**

Pody są efemeryczne — mogą być tworzone, usuwane i przenoszone między węzłami, a ich adresy IP zmieniają się przy każdym restarcie. **Service** zapewnia:
- **Stały adres IP** (ClusterIP) i **stałą nazwę DNS**, które nie zmieniają się niezależnie od cyklu życia Podów.
- **Load balancing** — automatyczne rozdzielanie ruchu pomiędzy wszystkie zdrowe Pody pasujące do selektora.

Service jest abstrakcją warstwy L4 (TCP/UDP), która oddziela konsumenta usługi od jej konkretnych instancji.

> **Ile Podów agreguje jeden Service?**
>
> Jeden Service agreguje **wiele Podów tego samego rodzaju** — wszystkie, które pasują do jego selektora etykiet (`selector`). Jeśli masz Deployment z `replicas: 10`, to powstaje 10 Podów, ale potrzebujesz tylko **jednego Service'a**, który je wszystkie obsługuje. Service automatycznie rozdziela ruch (load balancing) pomiędzy te 10 instancji.
>
> **Nie** tworzy się osobnego Service'a dla każdego Poda — to właśnie jest sedno abstrakcji Service: jeden stabilny punkt dostępu do dynamicznie zmieniającego się zestawu Podów.
>
> Service **nie agreguje** Podów różnych typów aplikacji w jednym obiekcie. Każda aplikacja (mikroserwis) ma swój własny Service. Przykładowo:
> - `user-api` (Deployment, 5 replik) → 1× Service `user-api-svc`
> - `order-api` (Deployment, 3 repliki) → 1× Service `order-api-svc`
>
> Łącznie 8 Podów, ale tylko 2 Service'y.

**41. Jak aplikacje wewnątrz klastra mogą odwoływać się do Service'u bez znajomości jego adresu IP?**

Poprzez **CoreDNS** (wbudowany DNS klastra). Każdy Service automatycznie otrzymuje rekord DNS w formacie:

```
<nazwa-service>.<namespace>.svc.cluster.local
```

Np. serwis `user-api` w namespace `production` jest dostępny pod adresem `user-api.production.svc.cluster.local`. W obrębie tego samego namespace wystarczy sama nazwa: `user-api`.

**42. Jaka jest różnica pomiędzy typami Service?**

W Kubernetesie istnieją **4 typy** Service:

| Typ | Dostępność | Opis |
|---|---|---|
| **ClusterIP** (domyślny) | Tylko wewnątrz klastra | Przydziela wirtualny IP widoczny wyłącznie w klastrze. Używany do komunikacji między mikroserwisami. |
| **NodePort** | Z zewnątrz (przez IP węzła) | Otwiera stały port (zakres 30000-32767) na **każdym węźle** klastra. Tworzy pod spodem ClusterIP. |
| **LoadBalancer** | Z zewnątrz (przez LB chmury) | Provisionuje zewnętrzny load balancer u dostawcy chmury (AWS ELB, GCP LB itp.). Tworzy pod spodem NodePort + ClusterIP. |
| **ExternalName** | Alias DNS | Nie tworzy żadnego proxy — zwraca rekord CNAME wskazujący na zewnętrzną nazwę DNS (np. `my-db.rds.amazonaws.com`). Przydatny do mapowania zewnętrznych usług pod wewnętrzną nazwę klastra. |

Hierarchia: `LoadBalancer` ⊃ `NodePort` ⊃ `ClusterIP` — każdy wyższy typ zawiera w sobie funkcjonalność niższego.

---

### ConfigMap i Secret

**43. Co to jest ConfigMap i w jaki sposób można przekazać jego wartości do kontenera?**

ConfigMap przechowuje dane konfiguracyjne w postaci par klucz-wartość. Można je przekazać do kontenera na dwa sposoby:

1. **Zmienne środowiskowe** — wartość jest wstrzykiwana przy starcie kontenera:
```yaml
envFrom:
  - configMapRef:
      name: app-config
```

2. **Wolumen (plik)** — ConfigMap jest montowany jako katalog z plikami:
```yaml
volumes:
  - name: config-vol
    configMap:
      name: app-config
```

**44. Czym się różni Secret od ConfigMapy i w jakim formacie przechowywane są dane?**

| Cecha | ConfigMap | Secret |
|---|---|---|
| Przeznaczenie | Konfiguracja niejawna (np. URL-e, flagi) | Dane wrażliwe (hasła, tokeny, certyfikaty) |
| Format danych | Tekst jawny | Zakodowane w **Base64** (uwaga: to nie jest szyfrowanie!) |
| Przechowywanie w etcd | Tekst jawny | Domyślnie też tekst jawny (Base64) — szyfrowanie wymaga włączenia encryption at rest |
| Dostęp | Bez ograniczeń | Może być ograniczony przez RBAC |

Base64 to jedynie **kodowanie**, nie zapewnia żadnego bezpieczeństwa. Dlatego Secrety w repozytorium kodu powinny być szyfrowane narzędziami jak SOPS, Sealed Secrets lub External Secrets Operator.

> **W jaki sposób szyfruje się zawartość Secrets w Kubernetesie?**
>
> Domyślnie Kubernetes **nie szyfruje** Secretów — przechowuje je w `etcd` zakodowane jedynie w Base64 (czyli praktycznie jako tekst jawny). Aby włączyć prawdziwe szyfrowanie, należy skonfigurować **Encryption at Rest**:
>
> 1. Tworzy się plik `EncryptionConfiguration`, w którym definiuje się **klucz szyfrowania** i algorytm (np. `aescbc`, `aesgcm`, `secretbox`):
> ```yaml
> apiVersion: apiserver.config.k8s.io/v1
> kind: EncryptionConfiguration
> resources:
>   - resources:
>       - secrets
>     providers:
>       - aescbc:
>           keys:
>             - name: key1
>               secret: <base64-encoded-32-byte-key>  # klucz szyfrujący
>       - identity: {}  # fallback — odczyt niezaszyfrowanych danych
> ```
>
> 2. Plik ten jest przekazywany do **kube-apiserver** poprzez flagę `--encryption-provider-config`.
>
> **Gdzie przechowywany jest klucz szyfrujący?**
> - W podstawowej konfiguracji klucz jest zapisany **na dysku węzła Control Plane** (w pliku `EncryptionConfiguration`). To oznacza, że kto ma dostęp do tego węzła, może odczytać klucz.
> - W środowiskach produkcyjnych stosuje się **KMS (Key Management Service)** — np. AWS KMS, GCP Cloud KMS, Azure Key Vault lub HashiCorp Vault. Wówczas kube-apiserver nie przechowuje klucza lokalnie, lecz deleguje operacje szyfrowania/deszyfrowania do zewnętrznego serwisu KMS poprzez provider `kms` w konfiguracji. Sam klucz nigdy nie opuszcza KMS.
>
> **Podsumowując**: Secret bez encryption at rest → Base64 w etcd (brak ochrony). Secret z encryption at rest → zaszyfrowany kluczem AES w etcd, klucz trzymany lokalnie lub (lepiej) w zewnętrznym KMS.

**45. Co się stanie z aplikacją, jeśli ConfigMap podpięty jako wolumen zostanie zaktualizowany, a co jeśli jako zmienna środowiskowa?**

- **Wolumen** — Kubelet automatycznie zaktualizuje zamontowane pliki (z opóźnieniem do ~1 minuty). Aplikacja musi jednak samodzielnie wykryć zmianę i przeładować konfigurację (np. watch na plik).
- **Zmienna środowiskowa** — **nie zostanie zaktualizowana**. Zmienne środowiskowe są ustawiane tylko raz, przy starcie kontenera. Aby aplikacja otrzymała nową wartość, Pod musi zostać zrestartowany.

---

### StatefulSet

**46. Co to jest StatefulSet i w jakich scenariuszach należy go użyć zamiast Deploymentu?**

StatefulSet to kontroler przeznaczony do aplikacji **stanowych** (stateful), które wymagają:
- **Stałej tożsamości sieciowej** — każdy Pod ma przewidywalną nazwę (np. `mysql-0`, `mysql-1`).
- **Stałego storage'u** — każdy Pod ma własny PVC, który nie jest współdzielony.
- **Uporządkowanego uruchamiania i zatrzymywania** — Pody są tworzone sekwencyjnie (0, 1, 2...) i usuwane w odwrotnej kolejności.

Typowe zastosowania: bazy danych (PostgreSQL, MySQL), klastry Kafka, Elasticsearch, Redis Cluster, ZooKeeper.

**47. Czym jest headless service i dlaczego jest często używany z StatefulSet?**

Headless Service to Service z ustawionym `clusterIP: None`. Zamiast przydzielać jeden wirtualny IP z load balancingiem, tworzy **indywidualne rekordy DNS dla każdego Poda**:

```
mysql-0.mysql-headless.default.svc.cluster.local
mysql-1.mysql-headless.default.svc.cluster.local
```

Jest to kluczowe dla aplikacji stanowych, ponieważ klient musi mieć możliwość połączenia się z **konkretną instancją** (np. z liderem klastra bazy danych), a nie z losowym Podem.

**48. Jak StatefulSet gwarantuje stabilność tożsamości i stałość storage'u?**

- **Tożsamość** — nazwy Podów są deterministyczne (`<statefulset-name>-<ordinal>`). Po restarcie Pod otrzymuje tę samą nazwę i ten sam rekord DNS.
- **Storage** — StatefulSet używa `volumeClaimTemplates`, które tworzą dedykowany PVC dla każdego Poda. Nawet jeśli Pod zostanie usunięty i odtworzony (np. na innym węźle), zostanie podpięty do **tego samego PVC** i tym samym do tych samych danych.

---

### DaemonSet

**49. Co to jest DaemonSet i jaka jest jego główna funkcja?**

DaemonSet to kontroler, który gwarantuje, że **na każdym węźle** klastra (lub na wybranych węzłach) działa dokładnie **jedna kopia Poda**. Gdy do klastra dołączy nowy węzeł, DaemonSet automatycznie uruchomi na nim Poda. Gdy węzeł zostanie usunięty, Pod jest garbage-collectowany.

**50. W jakich przypadkach użyłbyś DaemonSetu?**

- **Zbieranie logów** — np. Fluentd, Filebeat na każdym węźle.
- **Monitorowanie** — np. Node Exporter (Prometheus), Datadog Agent.
- **Sieć** — pluginy CNI (np. Calico, Cilium) działają jako DaemonSety.
- **Storage** — agenci CSI (Container Storage Interface).
- **Bezpieczeństwo** — agenci skanujący (np. Falco).

**51. Czy można wymusić DaemonSet tylko na wybranych węzłach?**

Tak, za pomocą:
- **`nodeSelector`** — prosty mechanizm, wybiera węzły po etykiecie:
```yaml
nodeSelector:
  disk-type: ssd
```
- **`affinity.nodeAffinity`** — bardziej zaawansowany mechanizm z operatorami (`In`, `NotIn`, `Exists`).
- **Tolerations** — aby DaemonSet mógł działać na węzłach z taintami (np. na węzłach master/control-plane).

---

### Job i CronJob

**52. Co to jest Job i czym różni się od Poda w Deploymencie?**

Job to zasób przeznaczony do **jednorazowych zadań**, które mają się zakończyć (np. migracja bazy danych, generowanie raportu, przetwarzanie batch). Kluczowe różnice:

| Cecha | Deployment | Job |
|---|---|---|
| Cel | Pod działa ciągle (long-running) | Pod wykonuje zadanie i kończy pracę |
| Restart | Zawsze restartowany po awarii | Restartowany do osiągnięcia sukcesu (lub limitu prób) |
| Sukces | Pod ma działać w nieskończoność | Sukces = kontener zakończył się z kodem 0 |

**53. Czym różni się Job od CronJoba?**

- **Job** — jednorazowe uruchomienie zadania.
- **CronJob** — tworzy Joby według **harmonogramu** (cron schedule), np.:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-backup
spec:
  schedule: "0 2 * * *"   # codziennie o 2:00
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: backup-tool:latest
          restartPolicy: OnFailure
```

Format harmonogramu jest zgodny ze standardem cron: `minuta godzina dzień_miesiąca miesiąc dzień_tygodnia`.

**54. Co się stanie, jeśli zadanie w Jobie zakończy się błędem?**

Zachowanie zależy od dwóch parametrów:
- **`restartPolicy`** — `OnFailure` (restart kontenera w tym samym Podzie) lub `Never` (tworzony jest nowy Pod).
- **`backoffLimit`** (domyślnie 6) — maksymalna liczba prób. Po przekroczeniu limitu Job jest oznaczany jako **Failed**.

Między kolejnymi próbami Kubernetes stosuje **exponential backoff** (10s, 20s, 40s... do max 6 minut).

---

### Ingress

**55. Co to jest Ingress i dlaczego programiści używają go do wystawiania aplikacji HTTP/HTTPS?**

Ingress to zasób warstwy L7 (HTTP/HTTPS), który definiuje reguły trasowania ruchu zewnętrznego do serwisów wewnątrz klastra. Oferuje:
- **Routing oparty na ścieżce** (`/api` → serwis A, `/web` → serwis B).
- **Routing oparty na hoście** (`api.example.com` → serwis A, `app.example.com` → serwis B).
- **Terminację TLS/SSL** — obsługa certyfikatów HTTPS w jednym miejscu.
- **Jeden punkt wejścia** — zamiast wielu LoadBalancerów (które kosztują), jeden Ingress obsługuje wiele serwisów.

**56. Czym różni się zasób Ingress od Ingress Controllera?**

- **Ingress** (zasób) — to **deklaracja** (plik YAML), która opisuje reguły trasowania. Sama w sobie nic nie robi.
- **Ingress Controller** — to **działający w klastrze komponent** (np. NGINX Ingress Controller, Traefik, HAProxy, AWS ALB Ingress Controller), który odczytuje zasoby Ingress i konfiguruje rzeczywisty reverse proxy.

Bez zainstalowanego Ingress Controllera zasób Ingress jest ignorowany — reguły nie będą miały żadnego efektu.

**57. Jak Ingress kieruje ruch na podstawie ścieżki lub hosta?**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
spec:
  rules:
    # Host-based routing
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
    # Path-based routing (ten sam host)
    - host: example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
          - path: /dashboard
            pathType: Prefix
            backend:
              service:
                name: dashboard-service
                port:
                  number: 80
```

---

### PersistentVolume (PV) i PersistentVolumeClaim (PVC)

**58. Co to jest PersistentVolumeClaim (PVC) z perspektywy programisty?**

PVC to **żądanie (request)** programisty na przestrzeń dyskową. Programista nie musi wiedzieć, skąd fizycznie pochodzi dysk — deklaruje jedynie:
- Ile miejsca potrzebuje (`storage: 10Gi`).
- Jaki tryb dostępu (`ReadWriteOnce`, `ReadWriteMany`, `ReadOnlyMany`).
- Opcjonalnie jaką klasę storage'u (`storageClassName`).

Kubernetes automatycznie dopasowuje PVC do istniejącego PV (lub dynamicznie tworzy nowy, jeśli skonfigurowano StorageClass).

**59. Jak aplikacja w Podzie uzyskuje dostęp do przestrzeni dyskowej z PVC?**

Poprzez montowanie wolumenu w specyfikacji Poda:

```yaml
spec:
  containers:
    - name: app
      image: my-app:latest
      volumeMounts:
        - name: data-volume
          mountPath: /app/data       # ścieżka wewnątrz kontenera
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: my-app-pvc        # nazwa istniejącego PVC
```

Aplikacja widzi zamontowany dysk jako zwykły katalog w systemie plików — nie musi wiedzieć, że pod spodem jest np. dysk EBS w AWS czy dysk GCE PD w Google Cloud.

**60. Czym jest StorageClass i dlaczego ułatwia dynamiczne tworzenie wolumenów?**

StorageClass to szablon definiujący **jak** tworzony jest fizyczny dysk. Zawiera:
- **Provisioner** — wtyczka odpowiedzialna za tworzenie dysku (np. `ebs.csi.aws.com`, `pd.csi.storage.gke.io`).
- **Parametry** — typ dysku (SSD/HDD), strefa dostępności, szyfrowanie itp.
- **Reclaim policy** — co zrobić z dyskiem po usunięciu PVC (`Retain` zachowuje dane, `Delete` kasuje dysk).

Bez StorageClass administrator musiałby ręcznie tworzyć PV dla każdego żądania programisty. Ze StorageClass proces jest w pełni automatyczny — programista tworzy PVC, a Kubernetes sam provisionuje odpowiedni dysk.

## Powiązane tematy
- [Czym różni się AWS ECS od AWS Fargate](czym-rozni-sie-aws-ecs-od-aws-fargate.md)
- [Docker Exec vs Attach](docker-exec-vs-attach.md)
