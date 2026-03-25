# Webhook vs Endpoint

**Data:** 2024-12-20

---

**User:**

Miałem trochę teoretycznego kontaktu z Webhookami. I teraz mam wrażenie że webhook to nic innego niż endpoint serwera http. Czy to jest prawda?

---

**Assistant:**

Masz rację, że **webhook** w swojej istocie jest endpointem HTTP, ale warto podkreślić kilka szczegółów, które odróżniają webhooki od ogólnych endpointów HTTP.

### Czym jest webhook?
Webhook to mechanizm, który pozwala aplikacjom na **przesyłanie informacji w czasie rzeczywistym** do innych systemów. W praktyce jest to po prostu **endpoint HTTP** (np. `POST`), który aplikacja nasłuchuje na swoim serwerze, aby odbierać powiadomienia o zdarzeniach.

### Różnice między webhookiem a zwykłym endpointem:
1. **Cel działania**:
   - Webhook służy głównie do odbierania **asynchronicznych powiadomień** o zdarzeniach (np. "nowa płatność została zrealizowana" lub "użytkownik zmienił hasło").
   - Zwykły endpoint może być używany do różnych celów, np. obsługi żądań API, wyszukiwania danych, zapisu informacji itp.

2. **Inicjatywa wywołania**:
   - W przypadku webhooka to **zdalny system** (np. serwis zewnętrzny, jak Stripe, GitHub czy Slack) wykonuje żądanie HTTP do Twojego endpointu, kiedy coś się wydarzy.
   - W przypadku zwykłego endpointu to zazwyczaj klient (np. przeglądarka, aplikacja mobilna) wysyła żądania.

3. **Typowość metody HTTP**:
   - Webhooki zazwyczaj używają metody **POST**, ale mogą też korzystać z innych metod, jak np. GET.
   - Endpointy HTTP mogą używać pełnego zestawu metod (GET, POST, PUT, DELETE itd.).

4. **Forma danych**:
   - Webhooki często przesyłają dane w formacie JSON lub XML w treści żądania, aby poinformować o zdarzeniu.
   - Endpointy mogą obsługiwać różnorodne dane wejściowe, w zależności od swojego przeznaczenia.

5. **Asynchroniczność**:
   - Webhooki są zwykle asynchroniczne – nie oczekuje się natychmiastowej odpowiedzi poza potwierdzeniem (np. HTTP 200 OK).
   - Endpointy mogą być zarówno synchroniczne, jak i asynchroniczne.

### Przykład webhooka:
Webhook dla powiadomienia o nowej płatności:
- Endpoint: `https://example.com/webhooks/payment`
- Wysłany przez zewnętrzny serwis (np. Stripe).
- Przykładowa treść żądania:
  ```json
  {
    "event": "payment_succeeded",
    "amount": 1500,
    "currency": "USD",
    "transaction_id": "txn_123456"
  }
  ```

### Podsumowanie
Webhook to **specjalny przypadek endpointu HTTP**, który ma jasno zdefiniowaną funkcję: odbieranie automatycznych powiadomień od innych systemów. Wyróżnia się asynchronicznością i tym, że to zewnętrzny system inicjuje komunikację. 

Jeśli zrozumiesz, że webhook to w istocie "nasłuchujący endpoint", to masz solidne podstawy do pracy z nimi!