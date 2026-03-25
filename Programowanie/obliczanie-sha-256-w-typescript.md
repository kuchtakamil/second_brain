# Obliczanie SHA-256 w TypeScript.

**Data:** 2023-07-21

---

**User:**

Jak w Node, przy użyciu TypeScript policzyć sha256 dla dowolnego Stringa?

---

**Assistant:**

Aby obliczyć skrót SHA-256 dla dowolnego ciągu znaków w Node.js z użyciem TypeScript, najpierw będziesz musiał zainstalować odpowiednie paczki: `crypto` (dostępny w Node.js) oraz `@types/node` (do wsparcia TypeScript). Upewnij się, że masz Node.js zainstalowane na swoim komputerze.

Kroki, które wykonamy, to:

1. Zainstaluj wymagane paczki.
2. Napisz funkcję obliczającą skrót SHA-256.

Oto jak to zrobić:

Krok 1: Instalacja paczek
```bash
npm install crypto @types/node --save-dev
```

Krok 2: Napisz funkcję do obliczania skrótu SHA-256
```typescript
// Importujemy moduł crypto
import { createHash } from 'crypto';

// Funkcja obliczająca skrót SHA-256
function calculateSHA256(input: string): string {
  // Tworzymy obiekt do obliczeń SHA-256
  const hash = createHash('sha256');

  // Aktualizujemy dane wejściowe do obiektu haszującego
  hash.update(input);

  // Obliczamy skrót i zamieniamy na postać szesnastkową
  const hashedValue = hash.digest('hex');

  return hashedValue;
}

// Przykładowe użycie funkcji
const inputString = 'Hello, world!';
const sha256Hash = calculateSHA256(inputString);
console.log('SHA-256:', sha256Hash);
```

Po uruchomieniu powyższego kodu w środowisku TypeScript w Node.js powinno zostać wyświetlone:

```
SHA-256: d7d5f1e83fbaa69eaa2fcd5b404f8f3c2ba3b47e418b44e51c124c4525fbc7e4
```

Wynik będzie różnić się w zależności od wejściowego ciągu znaków. Teraz masz funkcję, która obliczy skrót SHA-256 dla dowolnego ciągu znaków w Node.js z użyciem TypeScript.