# REST API vs Webhook

**Data:** 2024-08-13

---

**User:**

jaka jest praktyczna różnica między standardowym endpointem np. REST API a webhookiem?

---

**Assistant:**

Standardowy endpoint w REST API i webhooki to dwa różne mechanizmy komunikacji pomiędzy systemami, które mogą na pierwszy rzut oka wydawać się podobne, ale różnią się znacząco pod względem działania i zastosowania. Oto praktyczne różnice między nimi:

### REST API

1. **Model komunikacji**: REST API działa w modelu klient-serwer, gdzie klient (np. aplikacja front-end) wysyła żądania do serwera (endpointu API), a serwer odpowiada na te żądania.

2. **Inicjacja**: W przypadku REST API to klient inicjuje komunikację poprzez wysyłanie żądań HTTP (GET, POST, PUT, DELETE, itp.) do serwera. Serwer odpowiada na te żądania odpowiednimi danymi.

3. **Zarządzanie**: Klient ma pełną kontrolę nad tym, kiedy i jakie żądania są wysyłane do serwera. To oznacza, że klient decyduje, kiedy chce pobrać nowe dane lub zaktualizować istniejące.

4. **Stosowanie**: REST API jest szeroko stosowane w aplikacjach webowych i mobilnych do realizacji różnorodnych funkcjonalności, takich jak pobieranie danych z serwera, tworzenie nowych zasobów, aktualizacja istniejących lub ich usuwanie.

5. **Odpowiedź serwera**: Po otrzymaniu żądania serwer przetwarza je i zwraca odpowiedź w formacie JSON, XML lub innym uzgodnionym formacie.

### Webhook

1. **Model komunikacji**: Webhook działa w modelu push, gdzie to serwer wysyła dane do klienta w momencie wystąpienia określonego zdarzenia. Klient nie musi pytać o dane, ponieważ serwer automatycznie je wysyła.

2. **Inicjacja**: W przypadku webhooków to serwer inicjuje komunikację poprzez wysyłanie wiadomości HTTP do zdefiniowanego endpointu klienta. Dzieje się to, gdy na serwerze zajdzie określone zdarzenie (np. nowa płatność, nowe zamówienie).

3. **Zarządzanie**: Klient musi skonfigurować adres URL (endpoint), na który serwer będzie wysyłał informacje. W ten sposób klient otrzymuje dane automatycznie, bez konieczności ich ręcznego pobierania.

4. **Stosowanie**: Webhooki są często używane w systemach, gdzie ważne jest natychmiastowe powiadomienie o zdarzeniach, takich jak płatności, aktualizacje w czasie rzeczywistym, powiadomienia o zmianach, itp.

5. **Odpowiedź serwera**: Po wysłaniu danych przez serwer klient zazwyczaj zwraca prostą odpowiedź HTTP, potwierdzającą otrzymanie danych (np. kod statusu 200 OK). Nie ma potrzeby, aby klient przetwarzał odpowiedź serwera w taki sam sposób, jak w przypadku REST API.

### Podsumowanie

W praktyce główna różnica polega na kierunku i inicjacji komunikacji:

- **REST API**: Klient inicjuje żądania do serwera, aby uzyskać dane lub wykonać akcje.
- **Webhook**: Serwer automatycznie wysyła dane do klienta po wystąpieniu określonych zdarzeń.

Wybór między tymi mechanizmami zależy od specyficznych wymagań aplikacji oraz oczekiwań dotyczących komunikacji między systemami.