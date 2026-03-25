# Czyszczenie logów w Kubernetes

**Data:** 2025-05-29

---

**User:**

Mam działające pody w kubernetes. Chciałbym z części z nich wyrzucić stare logi. Czy istnieje taka możliwość?

---

**Assistant:**

W Kubernetesie logi z podów są domyślnie przechowywane na dysku węzłów (zwykle w `/var/log/containers`, które są linkami do `/var/log/pods` i ostatecznie do plików w `/var/lib/docker/containers` lub `/var/log/cri-containerd/...`, zależnie od CRI). Kubernetes sam z siebie **nie oferuje komendy do czyszczenia logów w podach**, bo te logi są generowane przez kontenery i przechowywane przez runtime kontenerowy (Docker, containerd itd.).

### Możliwości wyczyszczenia logów:

#### 1. **Czyszczenie logów na poziomie węzła**
Jeśli masz dostęp do węzłów (SSH), możesz ręcznie usunąć lub obciąć logi:

```bash
sudo truncate -s 0 /var/log/containers/<nazwa-poda>*.log
```

Albo:

```bash
sudo find /var/log/containers -name '<nazwa-poda>*' -exec truncate -s 0 {} \;
```

Uwaga: Wymaga to dostępu do hostów, więc to działa tylko w klastrach, gdzie masz kontrolę nad infrastrukturą (bare metal, EC2, itp.).

---

#### 2. **Log rotation – konfiguracja na poziomie węzła**
Zamiast ręcznego czyszczenia, możesz skonfigurować logrotate dla katalogów logów kontenerów (np. `/etc/logrotate.d/docker-containers` lub podobne dla containerd). Przykład dla Docker:

```bash
/var/lib/docker/containers/*/*.log {
  rotate 5
  daily
  compress
  missingok
  delaycompress
  copytruncate
}
```

W przypadku containerd log rotation można ustawić w jego konfiguracji (`/etc/containerd/config.toml`).

---

#### 3. **Restart poda (jeśli logi nie są utrzymywane przez wolumeny)**
Jeśli zrestartujesz poda (czyli pod zostanie usunięty i zreutworzony), to standardowe logi (stdout/stderr) zostaną utracone.

```bash
kubectl delete pod <nazwa-poda>
```

**Uwaga:** Jeśli logi są zbierane przez log collectora typu Fluentd, Loki, itp., to restart poda nie usunie ich z backendu.

---

#### 4. **Jeśli logi są przechowywane wewnątrz kontenera (np. w plikach w wolumenie)**
Jeśli logi są zapisywane w wolumenach (np. w `/app/logs/app.log`), możesz wejść do poda i je usunąć:

```bash
kubectl exec -it <nazwa-poda> -- sh
rm /ścieżka/do/logu.log
```

Albo z poziomu hosta:

```bash
kubectl exec <pod> -- truncate -s 0 /app/logs/app.log
```

---

### Podsumowanie

| Sposób | Kiedy stosować | Wymaga dostępu do... |
|-------|----------------|------------------------|
| Truncate logów w `/var/log/containers` | Logi stdout/stderr | Węzeł |
| Logrotate | Utrzymanie porządku | Węzeł |
| Restart poda | Szybko i brudno | Kubernetes |
| Usunięcie plików w kontenerze | Logi aplikacji w plikach | Kubernetes |

Jeśli chcesz — możesz powiedzieć, jaki masz CRI (Docker, containerd) i czy logi są zbierane przez jakiś system (np. Fluent Bit, EFK, Grafana Loki) – mogę wtedy podpowiedzieć dokładniej.