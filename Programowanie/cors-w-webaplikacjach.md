# CORS w webaplikacjach

**Data:** 2025-01-14

---

**User:**

W kontkście programowania webaplikacji co to jest CORS?

---

**Assistant:**

CORS (ang. **Cross-Origin Resource Sharing**) to mechanizm bezpieczeństwa stosowany w przeglądarkach internetowych, który pozwala kontrolować, jakie zasoby mogą być udostępniane między różnymi źródłami (**origin**).

### **Origin w kontekście CORS**
Origin to kombinacja:
- **schematu** (np. `http` lub `https`),
- **hosta** (np. `example.com`),
- **portu** (np. `:80` dla HTTP, `:443` dla HTTPS).

Dwa URL-e mają ten sam origin tylko wtedy, gdy wszystkie trzy elementy są identyczne.

Przykład:
- `https://example.com` (origin 1)
- `https://api.example.com` (origin 2) → różne hosty, różne originy
- `http://example.com:8080` (origin 3) → różne porty, różne originy

### **Problem, który rozwiązuje CORS**
Domyślnie przeglądarki stosują **politykę jednego źródła** (**Same-Origin Policy**), która blokuje żądania HTTP do zasobów na innym originie niż ten, z którego pochodzi strona. CORS umożliwia bezpieczne obejście tej restrykcji i pozwala na wymianę danych między różnymi originami w sposób kontrolowany.

### **Jak działa CORS**
1. **Proste żądania**: Jeśli żądanie jest prostego typu (np. `GET` lub `POST` z podstawowymi nagłówkami), przeglądarka sprawdza odpowiedź serwera. Serwer musi dodać nagłówek:
   ```
   Access-Control-Allow-Origin: <dozwolony_origin> lub *
   ```
   Jeśli nagłówek jest obecny i dopuszcza origin klienta, przeglądarka umożliwia dostęp.

2. **Preflight request**: Dla bardziej złożonych żądań (np. z niestandardowymi nagłówkami, innymi metodami HTTP jak `PUT` czy `DELETE`) przeglądarka wysyła żądanie **OPTIONS** w celu sprawdzenia, czy serwer pozwala na takie operacje. Serwer odpowiada nagłówkami:
   - `Access-Control-Allow-Methods` – dozwolone metody HTTP,
   - `Access-Control-Allow-Headers` – dozwolone nagłówki,
   - `Access-Control-Allow-Origin` – dozwolony origin.

### **Przykład nagłówków CORS**
Nagłówki w odpowiedzi serwera:
```
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

### **Typowe problemy z CORS**
- Brak nagłówka `Access-Control-Allow-Origin` na serwerze.
- Zbyt restrykcyjne ustawienia (np. brak obsługi `OPTIONS`).
- Serwer nie obsługuje preflight requestów poprawnie.
- Klient próbuje uzyskać dostęp z originu, który nie jest dozwolony.

### **Przykładowa konfiguracja**
Dla serwera Express.js w Node.js:
```javascript
const express = require('express');
const cors = require('cors');
const app = express();

// Prosta konfiguracja CORS
app.use(cors({
  origin: 'https://example.com', // Lub '*' dla wszystkich originów
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.listen(3000, () => console.log('Serwer działa na porcie 3000'));
```

CORS to kluczowy mechanizm w nowoczesnych aplikacjach webowych, umożliwiający bezpieczną wymianę danych między różnymi domenami.