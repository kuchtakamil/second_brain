# Regex dla adresów email

**Data:** 2023-07-21

---

**User:**

W TypeScript napisz regex dla adresów email

---

**Assistant:**

Oczywiście! Poniżej znajduje się przykład wyrażenia regularnego w TypeScript dla adresów email:

```typescript
const emailRegex: RegExp = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
```

To wyrażenie regularne ma następujące znaczenie:

- `^` - Początek ciągu znaków.
- `[a-zA-Z0-9._%+-]+` - Adres email może zawierać litery (zarówno małe, jak i duże), cyfry oraz znaki specjalne: ".", "_", "%", "+", "-". Przynajmniej jeden z tych znaków musi wystąpić co najmniej raz.
- `@` - Znak '@' występuje po nazwie użytkownika.
- `[a-zA-Z0-9.-]+` - Nazwa domeny może zawierać litery (zarówno małe, jak i duże), cyfry oraz znaki specjalne: ".", "-". Przynajmniej jeden z tych znaków musi wystąpić co najmniej raz.
- `\.` - Kropka '.' jest znakiem specjalnym w wyrażeniach regularnych, więc musi być ujęta w nawiasy wsteczne, aby została potraktowana jako zwykły znak kropki.
- `[a-zA-Z]{2,}` - Domena musi składać się z co najmniej dwóch liter (zarówno małych, jak i dużych).

- `$` - Koniec ciągu znaków.

Ten regex powinien obsługiwać większość standardowych adresów email. Należy jednak pamiętać, że ze względu na różnorodność adresów email, niestandardowe przypadki mogą wymagać dostosowania tego wyrażenia regularnego.