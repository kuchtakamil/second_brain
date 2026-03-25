# Lokalizacja plików konfiguracyjnych

**Data:** 2024-11-28

---

**User:**

mam aplikacje springBoot zdeployowaną na kubernetes. Wchodzę na pod i chcę wyświetlić application.yaml lub properties z których korzysta aktualna instancja aplikacji na pod. Gdzie szukać tych plików

---

**Assistant:**

Pliki konfiguracyjne, takie jak `application.yaml` lub `application.properties`, w środowisku Spring Boot mogą być załadowane z różnych miejsc. Na Kubernetes zazwyczaj są one dostarczane do aplikacji w jeden z następujących sposobów:

### 1. **ConfigMap/Secret jako wolumen w podzie**
Jeśli konfiguracja została dostarczona jako ConfigMap lub Secret i zamontowana jako plik, znajdziesz ją w ścieżce zdefiniowanej w specyfikacji wolumenu w manifestach Kubernetes. Sprawdź konfigurację swojego deploymentu, aby zlokalizować ścieżkę, np.:

```yaml
volumes:
  - name: config-volume
    configMap:
      name: my-config-map
containers:
  - name: my-app
    volumeMounts:
      - name: config-volume
        mountPath: /config
```

W tym przypadku pliki konfiguracyjne znajdziesz pod `/config`.

### 2. **Zmienna środowiskowa `SPRING_CONFIG_LOCATION`**
Czasami konfiguracje są ładowane z niestandardowej ścieżki wskazanej przez zmienną środowiskową `SPRING_CONFIG_LOCATION`. Aby sprawdzić, czy taka zmienna jest ustawiona, wykonaj:

```bash
echo $SPRING_CONFIG_LOCATION
```

Jeśli zmienna wskazuje na określoną lokalizację, plik będzie się tam znajdował.

### 3. **Wbudowane pliki w aplikacji**
Jeśli pliki konfiguracyjne są zapakowane wewnątrz aplikacji (np. w katalogu `resources`), to nie będą dostępne jako osobne pliki w systemie plików. Możesz je jednak podejrzeć, przeszukując JAR, w którym znajduje się aplikacja:

1. Znajdź lokalizację JAR aplikacji w podzie, np. `/app/my-app.jar`.
2. Rozpakuj JAR za pomocą polecenia `unzip` lub `jar`:
   ```bash
   unzip /app/my-app.jar -d /tmp/unpacked
   ```
3. Plik konfiguracyjny znajdziesz w `/tmp/unpacked/BOOT-INF/classes/application.yaml` lub podobnej lokalizacji.

### 4. **Zmienna środowiskowa lub argument uruchomieniowy**
Konfiguracje mogą być również nadpisywane lub ustawiane za pomocą zmiennych środowiskowych albo argumentów linii komend. W takim przypadku nie będą znajdować się w pliku, lecz w definicji pod lub deploymentu.

Aby sprawdzić zmienne środowiskowe w podzie, użyj:

```bash
env
```

### Podsumowanie
- **ConfigMap/Secret**: Sprawdź manifest Kubernetes i lokalizację zamontowanego wolumenu.
- **Wbudowane pliki**: Rozpakuj JAR aplikacji.
- **Zmienna środowiskowa `SPRING_CONFIG_LOCATION`**: Sprawdź, czy wskazuje na konkretną ścieżkę.
- **Zmienne środowiskowe i argumenty**: Przejrzyj konfigurację deploymentu lub wylistuj zmienne środowiskowe.

Jeśli masz więcej informacji o tym, jak konfiguracje są dostarczane do Twojej aplikacji, mogę pomóc precyzyjniej. 😊