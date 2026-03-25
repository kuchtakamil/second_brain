# Przeglądanie logów Dockera

**Data:** 2025-09-16

---

**User:**

rozwijam lokalnie webaplikację i eployouję ją na docker. Poza przeglądaniem logów na dockerdesktop, jaki jest inny sposób przeglądania logów w kontenerze? sposób musi być wygodny i darmowy

---

**Assistant:**

Masz kilka darmowych i wygodnych sposobów na podglądanie logów z kontenerów Dockera, bez ograniczania się tylko do Docker Desktop:  

### 1. **`docker logs` (CLI)**
Podstawowe, ale często wystarczające:
```bash
docker logs -f <container_name_or_id>
```
- `-f` działa jak `tail -f` (śledzenie w czasie rzeczywistym).
- Możesz też ograniczyć np. do ostatnich 100 linii:
  ```bash
  docker logs --tail 100 -f <container_name_or_id>
  ```

---

### 2. **`docker-compose logs`**  
Jeśli używasz `docker-compose`, to wygodnie zbiera logi ze wszystkich serwisów:
```bash
docker-compose logs -f
```
Możesz dodać filtr dla konkretnego serwisu:
```bash
docker-compose logs -f backend
```

---

### 3. **`stern` (narzędzie CLI)**
- Bardzo wygodne, jeśli później przejdziesz na Kubernetes, ale działa też z Dockerem przez adaptery.  
- Pozwala kolorować i filtrować logi.  
Repo: [https://github.com/stern/stern](https://github.com/stern/stern)

---

### 4. **Lokalny stack z logami (ELK / Loki + Promtail + Grafana)**  
Jeśli chcesz coś bardziej rozbudowanego (np. filtrowanie, wyszukiwanie w historii):  
- **ELK (Elasticsearch + Logstash + Kibana)** – cięższe rozwiązanie, ale bardzo mocne.  
- **Grafana Loki** – lżejsza alternatywa, do tego panel w Grafanie, łatwy w konfiguracji i darmowy.  

---

### 5. **`dozzle`** – przeglądarka logów w webUI
- Bardzo lekkie narzędzie w formie kontenera Dockera.  
- Odpala prosty interfejs webowy z logami wszystkich kontenerów.  
- Instalacja:
  ```bash
  docker run --name dozzle -d -p 9999:8080 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    amir20/dozzle:latest
  ```
  Potem wchodzisz na `http://localhost:9999`.

---

👉 Jeśli chcesz **najprościej i wygodnie**, polecam **Dozzle** – zero konfiguracji, ładny webowy podgląd logów w czasie rzeczywistym.  
👉 Jeśli wolisz **CLI** – używaj `docker logs -f` albo `docker-compose logs -f`.  

Chcesz, żebym Ci rozpisał minimalny setup Dozzle do lokalnego developmentu (docker-compose.yml)?