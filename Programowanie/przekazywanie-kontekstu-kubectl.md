# Przekazywanie kontekstu kubectl

**Data:** 2025-03-10

---

**User:**

jak przekazać context do polecenia kubectl

---

**Assistant:**

Można przekazać **kontekst (context)** do polecenia `kubectl` na kilka sposobów – najczęściej stosuje się flagę `--context`. Oto szczegóły:

### ✅ 1. Przez flagę `--context`
Najprostszy i najczęściej używany sposób:
```bash
kubectl --context=<nazwa_kontekstu> get pods
```

Przykład:
```bash
kubectl --context=dev-cluster get pods
```

---

### ✅ 2. Przez zmianę aktywnego kontekstu (tymczasowo lub na stałe)
Jeśli chcesz pracować cały czas z jednym kontekstem, możesz ustawić go jako domyślny:

```bash
kubectl config use-context <nazwa_kontekstu>
```

Sprawdzenie obecnego kontekstu:
```bash
kubectl config current-context
```

---

### ✅ 3. Przez zmienne środowiskowe (rzadziej stosowane)

Można wskazać alternatywny plik kubeconfig z kontekstem:
```bash
KUBECONFIG=/ścieżka/do/kubeconfig.yaml kubectl get pods
```

Jeśli plik kubeconfig zawiera wiele kontekstów, nadal można użyć `--context`, by wskazać konkretny.

---

### ✅ Sprawdzenie dostępnych kontekstów
```bash
kubectl config get-contexts
```

---

Chcesz, żebym podpowiedział jak dodać nowy kontekst do kubeconfig, albo jak odczytać kontekst z innego pliku kubeconfig i dodać do aktualnego?