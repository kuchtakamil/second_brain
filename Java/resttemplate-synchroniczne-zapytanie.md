# RestTemplate synchroniczne zapytanie

**Data:** 2025-05-23

---

**User:**

Czy używając funkcji 
org.springframework.web.client.RestTemplate.exchange(RequestEntity<?> entity, Class<T> responseType) throws RestClientException
zapytanie http jest realizowane w sposób synchroniczny czy asynchroniczny?

---

**Assistant:**

Używając funkcji:

```java
org.springframework.web.client.RestTemplate.exchange(RequestEntity<?> entity, Class<T> responseType)
```

zapytanie HTTP **jest realizowane w sposób synchroniczny**.

### Co to oznacza?
Oznacza to, że metoda `exchange(...)`:
- **blokuje wątek wywołujący**, aż odpowiedź HTTP zostanie odebrana (lub wystąpi wyjątek np. timeout, błąd połączenia itp.),
- zwraca wynik dopiero po zakończeniu operacji HTTP.

### Jeśli chcesz podejścia asynchronicznego
W Springu podejście asynchroniczne można zrealizować na kilka sposobów:
- **`WebClient`** (od Spring 5) – nowoczesny, reaktywny klient HTTP (`Mono<T>`, `Flux<T>`),
- **`AsyncRestTemplate`** – przestarzały i odradzany (deprecated),
- użycie zewnętrznych bibliotek jak `OkHttp`, `Apache HttpAsyncClient`, itp.

Przykład z `WebClient` (asynchroniczne i nieblokujące):

```java
WebClient webClient = WebClient.create();
Mono<ResponseEntity<MyResponse>> response = webClient
    .get()
    .uri("http://example.com")
    .retrieve()
    .toEntity(MyResponse.class);

// Dalej możesz zareagować np. poprzez:
response.subscribe(resp -> System.out.println(resp.getBody()));
```

Podsumowując: `RestTemplate.exchange(...)` jest **synchronizującą i blokującą** metodą.