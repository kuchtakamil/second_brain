# Weryfikacja Access Tokenów OAuth2

**Data:** 2024-01-06

---

**User:**

W mechaniźmie OAuth2, Authorization Server wysyła klientowi Access Token którego to później klient używa w komunikacji z Resource Server. Ale skąd Resource Server wie że ten Access Token jest poprawny i ważny?

---

**Assistant:**

W mechanizmie OAuth 2.0, Resource Server weryfikuje ważność i autentyczność Access Tokena, otrzymanego od klienta, poprzez kilka metod:

1. **Wewnętrzna Weryfikacja:** Jeśli Authorization Server i Resource Server są ściśle zintegrowane (np. w ramach tej samej platformy lub aplikacji), Resource Server może mieć bezpośredni dostęp do informacji o tokenach i może wewnętrznie zweryfikować token.

2. **Introspection Endpoint:** W niektórych implementacjach OAuth 2.0, istnieje specjalny endpoint na Authorization Server, znany jako introspection endpoint. Resource Server wysyła zapytanie do tego endpointu, przekazując Access Token, a Authorization Server odpowiada, potwierdzając ważność i szczegóły tokena.

3. **Podpis Cyfrowy:** Access Tokeny często są podpisywane cyfrowo przez Authorization Server. Resource Server może użyć publicznego klucza Authorization Server do weryfikacji podpisu, co potwierdza, że token nie został zmodyfikowany i jest autentyczny.

4. **Tokeny JWT (JSON Web Tokens):** W wielu przypadkach, Access Tokeny są w formacie JWT, które zawierają informacje o ważności (expiry time) oraz inne metadane. Resource Server może zweryfikować te dane i upewnić się, że token jest nadal ważny.

5. **Scope i inne atrybuty:** Resource Server może również sprawdzić, czy token ma odpowiednie uprawnienia (scope) do dostępu do żądanych zasobów.

Warto zauważyć, że dokładny mechanizm weryfikacji może się różnić w zależności od konkretnego wdrożenia OAuth 2.0 i używanych technologii.