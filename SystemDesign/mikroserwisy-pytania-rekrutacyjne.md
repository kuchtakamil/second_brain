# Mikroserwisy: Pytania Rekrutacyjne

Lista pytań na rozmowę kwalifikacyjną z zakresu **architektury mikroserwisowej**. Pytania pogrupowane tematycznie — od fundamentów po zaawansowane wzorce operacyjne. Obejmują poziomy od Mid do Senior/Staff.

---

## 1. Fundamenty i koncepcje

1. Czym jest architektura mikroserwisowa i czym różni się od monolitu?
2. Jakie są główne zalety i wady mikroserwisów w porównaniu z architekturą monolityczną?
3. Czym jest **Bounded Context** z Domain-Driven Design (DDD) i jak wpływa na granulację mikroserwisów?
4. Na jakiej podstawie decydujesz, gdzie przebiega granica jednego mikroserwisu? Jakie heurystyki stosujesz?
5. Kiedy **nie** warto rozdzielać monolitu na mikroserwisy?
6. Czym jest wzorzec **Strangler Fig** i jak go zastosować przy migracji z monolitu?
7. Jakie zasady SOLID mają bezpośrednie przełożenie na projektowanie mikroserwisów?
8. Czym różni się **orkiestracja** od **choreografii** w kontekście koordynacji mikroserwisów?
9. Czym jest **autonomia serwisu** i dlaczego jest kluczowa w architekturze rozproszonej?

---

## 2. Komunikacja między serwisami

10. Jakie są różnice między komunikacją **synchroniczną** (REST, gRPC) a **asynchroniczną** (message broker)?
11. Kiedy wybrałbyś gRPC zamiast REST i odwrotnie? Jakie są kompromisy?
12. Czym jest wzorzec **API Gateway** i jakie problemy rozwiązuje?
13. Jak działa **service discovery**? Porównaj podejście client-side vs server-side.
14. Czym jest **service mesh** (np. Istio, Linkerd) i jakie problemy komunikacyjne rozwiązuje?
15. Jak zaprojektować **idempotentne** endpointy i dlaczego jest to istotne w systemach rozproszonych?
16. Czym jest wzorzec **Backend for Frontend (BFF)** i kiedy go stosować?
17. Jak zarządzać **wersjonowaniem API** w ekosystemie mikroserwisów?
18. Czym jest **contract testing** (np. Pact) i jak zapobiega regresji w komunikacji między serwisami?

---

## 3. Zarządzanie danymi

19. Czym jest wzorzec **Database per Service** i dlaczego jest zalecany w mikroserwisach?
20. Jak realizować zapytania wymagające danych z wielu serwisów, skoro każdy ma swoją bazę? Opisz wzorzec **API Composition**.
21. Czym jest wzorzec **CQRS** (Command Query Responsibility Segregation) i kiedy go stosować?
22. Czym jest **Event Sourcing** i jakie problemy rozwiązuje? Jakie wprowadza?
23. Jak zapewnić **spójność danych** między mikroserwisami bez transakcji rozproszonych?
24. Czym jest wzorzec **Saga** i jakie są różnice między sagą opartą na orkiestracji a choreografii?
25. Jak obsłużyć **kompensację** (rollback) w Sadze, gdy jeden z kroków zakończy się niepowodzeniem?
26. Czym jest **eventual consistency** i jak wytłumaczyć ją biznesowi?
27. Czym jest **Change Data Capture (CDC)** i jak narzędzia takie jak Debezium wspierają synchronizację danych?

---

## 4. Odporność i niezawodność (Resilience)

28. Czym jest wzorzec **Circuit Breaker** i jak zapobiega awariom kaskadowym?
29. Jak działają mechanizmy **retry z exponential backoff i jitter**? Dlaczego sam retry bez backoff jest niebezpieczny?
30. Czym jest wzorzec **Bulkhead** i jak izoluje awarie w systemie?
31. Jak działa **rate limiting** i **throttling**? Jakie algorytmy znasz (Token Bucket, Leaky Bucket, Sliding Window)?
32. Czym jest **timeout budget** (deadline propagation) i jak go propagować przez łańcuch wywołań?
33. Jak zaprojektować system odporny na **thundering herd** po awarii?
34. Czym jest wzorzec **fallback** i jakie strategie degradacji jakości (graceful degradation) stosujesz?
35. Jak przetestować odporność systemu? Czym jest **Chaos Engineering** (np. Chaos Monkey)?

---

## 5. Deployment i DevOps

36. Jak wygląda pipeline **CI/CD** dla ekosystemu mikroserwisów? Czym różni się od monorepo vs polyrepo?
37. Czym jest **konteneryzacja** (Docker) i jak wspiera mikroserwisy?
38. Jak **Kubernetes** orkiestruje mikroserwisy? Opisz rolę Podów, Deploymentów i Service'ów.
39. Czym jest strategia **Blue-Green Deployment** i jak minimalizuje ryzyko wdrożeń?
40. Czym jest **Canary Deployment** i jak się różni od Blue-Green?
41. Jak realizować **rolling update** bez przestojów (zero-downtime deployment)?
42. Czym jest **Infrastructure as Code** (Terraform, Pulumi) i dlaczego jest kluczowe w środowisku mikroserwisowym?
43. Jak zarządzać **konfiguracją** w rozproszonym systemie (Config Server, Consul, Vault)?
44. Czym jest wzorzec **Sidecar** i jak jest wykorzystywany np. w Service Mesh?

---

## 6. Obserwowalność (Observability)

45. Jakie są trzy filary obserwowalności (**logi, metryki, tracing**) i dlaczego wszystkie trzy są konieczne?
46. Jak działa **distributed tracing** (np. Jaeger, Zipkin, OpenTelemetry)? Czym jest **trace ID** i **span**?
47. Jak implementować **centralne logowanie** w ekosystemie mikroserwisów (ELK Stack, Loki)?
48. Jak zaprojektować **health checks** i **readiness/liveness probes** w Kubernetes?
49. Jakie **metryki** (RED: Rate, Errors, Duration / USE: Utilization, Saturation, Errors) monitorujesz w mikroserwisach?
50. Jak skonfigurować **alerting** tak, aby unikać alert fatigue, a jednocześnie nie przegapić krytycznych incydentów?
51. Czym jest **correlation ID** i jak go propagować przez cały łańcuch wywołań?

---

## 7. Bezpieczeństwo

52. Jak działa **uwierzytelnianie** i **autoryzacja** w architekturze mikroserwisowej?
53. Czym jest **OAuth 2.0** i **OpenID Connect**? Jak wpisują się w ekosystem mikroserwisów?
54. Jak działa wzorzec **API Gateway jako centralny punkt autoryzacji** vs autoryzacja na poziomie każdego serwisu?
55. Czym jest **JWT** (JSON Web Token) i jakie są jego zalety oraz ryzyka w komunikacji między serwisami?
56. Jak zarządzać **sekretami** (hasła, klucze API) w rozproszonym systemie (HashiCorp Vault, Kubernetes Secrets)?
57. Czym jest zasada **Zero Trust** w kontekście mikroserwisów?
58. Jak zabezpieczyć komunikację między serwisami (**mTLS** — mutual TLS)?
59. Jak chronić się przed atakami **SSRF** (Server-Side Request Forgery) w systemie mikroserwisowym?

---

## 8. Skalowalność i wydajność

60. Jak **skalować mikroserwisy horyzontalnie** i jakie warunki musi spełniać serwis, aby to było możliwe?
61. Czym jest zasada **statelessness** i dlaczego jest kluczowa dla skalowalności?
62. Jak działa **auto-scaling** (HPA w Kubernetes) i jakie metryki są najlepsze do wyzwalania skalowania?
63. Jak zaprojektować efektywne **cache'owanie** w architekturze mikroserwisowej (local cache vs distributed cache)?
64. Czym jest **cache invalidation** i dlaczego jest to „jeden z dwóch najtrudniejszych problemów w informatyce"?
65. Jak zaprojektować system obsługujący **10x lub 100x wzrost ruchu** (capacity planning)?
66. Czym jest **backpressure** i jak go zaimplementować w systemie opartym na kolejkach komunikatów?
67. Jak wykorzystać **sharding** i **partycjonowanie** do skalowania warstwy danych?

---

## 9. Event-Driven Architecture

68. Czym jest architektura **zdarzeniowa** (Event-Driven) i jak współgra z mikroserwisami?
69. Jakie są różnice między **event notification**, **event-carried state transfer** a **event sourcing**?
70. Jak działa **Apache Kafka** w kontekście mikroserwisów? Czym jest topic, partition, consumer group?
71. Jak zapewnić **kolejność zdarzeń** w systemie opartym na message brokerze?
72. Czym jest **dead letter queue (DLQ)** i jak obsługiwać wiadomości, których nie udało się przetworzyć?
73. Jak zagwarantować semantykę **exactly-once** delivery (lub dlaczego jest to praktycznie niemożliwe)?
74. Czym jest wzorzec **Outbox** i jak zapobiega utracie zdarzeń przy zapisie do bazy i wysyłce na kolejkę?
75. Jak zaprojektować **schema evolution** w zdarzeniach (Avro, Protobuf, Schema Registry)?

---

## 10. Testowanie mikroserwisów

76. Jak wygląda **piramida testów** w kontekście mikroserwisów?
77. Czym jest **testowanie kontraktowe** (contract testing) i jak różni się od testów integracyjnych?
78. Jak testować mikroserwis w **izolacji** (mockowanie zależności, WireMock, Testcontainers)?
79. Czym są **testy End-to-End (E2E)** w ekosystemie mikroserwisów i dlaczego są trudne do utrzymania?
80. Jak wykorzystać **Testcontainers** do testów integracyjnych z bazą danych i brokerem komunikatów?
81. Czym jest **Consumer-Driven Contract Testing** i jakie problemy rozwiązuje w architekturze mikroserwisowej?

---

## 11. Wzorce organizacyjne i zespołowe

82. Jak **Prawo Conwaya** wpływa na projektowanie mikroserwisów?
83. Czym jest model **„You build it, you run it"** i jak zmienia odpowiedzialność zespołów?
84. Jak zorganizować zespoły wokół mikroserwisów — **feature teams** vs **platform teams**?
85. Czym jest **wewnętrzna platforma deweloperska (Internal Developer Platform)** i jak wspiera ekosystem mikroserwisów?
86. Jak zarządzać **zależnościami między zespołami** w dużym ekosystemie mikroserwisowym?
87. Kiedy mikroserwisy wprowadzają więcej problemów niż rozwiązują (**distributed monolith** antipattern)?

---

## Powiązane materiały

- [System Design: Pytania Rekrutacyjne](system-design-pytania-rekrutacyjne.md)
