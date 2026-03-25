# Kubernetes: NodePort vs ClusterIP

**Data:** 2024-06-19

---

**User:**

W Kubernetes jaka jest różnica między NodePort aClusterIP

---

**Assistant:**

W Kubernetes, `NodePort` i `ClusterIP` to dwa różne typy usług (`Service`), które mają na celu udostępnianie aplikacji zdefiniowanych w klastrze. Oto główne różnice między nimi:

### ClusterIP
- **Domyślny typ usługi**: Jeśli nie określisz typu usługi, Kubernetes domyślnie ustawia `ClusterIP`.
- **Dostępność**: Usługa jest dostępna tylko wewnątrz klastra Kubernetes. Użytkownicy spoza klastra nie mają dostępu do usługi.
- **Adres IP**: Tworzy wirtualny adres IP dostępny tylko w obrębie klastra. Inne podzespoły w klastrze mogą komunikować się z usługą używając tego IP.
- **Przeznaczenie**: Idealny do komunikacji między podzespołami (pods) w ramach tego samego klastra.

### NodePort
- **Zewnętrzny dostęp**: Udostępnia usługę na zewnętrznym porcie na każdym węźle (node) w klastrze. Umożliwia to dostęp do usługi spoza klastra, korzystając z adresu IP dowolnego węzła oraz zdefiniowanego portu.
- **Porty**: Rezerwuje statyczny port w zakresie od 30000 do 32767 na każdym węźle, aby przekierować ruch do usługi.
- **Adres IP**: Usługa jest dostępna poprzez adres IP dowolnego węzła w klastrze i port NodePort.
- **Przeznaczenie**: Umożliwia dostęp do usługi spoza klastra, na przykład z zewnętrznych klientów lub użytkowników.

### Podsumowanie
- **ClusterIP** jest używany, gdy potrzebujesz wewnętrznej komunikacji między podzespołami w klastrze Kubernetes.
- **NodePort** jest używany, gdy chcesz udostępnić usługę na zewnątrz, tak aby była dostępna spoza klastra.

Ostateczny wybór zależy od wymagań dotyczących dostępności usługi i scenariusza jej użycia. Jeśli potrzebujesz, aby usługa była dostępna tylko wewnątrz klastra, `ClusterIP` jest odpowiednią opcją. Jeśli chcesz, aby usługa była dostępna spoza klastra, użyj `NodePort`.