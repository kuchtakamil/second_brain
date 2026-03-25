# Wyjaśnienie kodu Typescript

**Data:** 2025-10-12

---

**User:**

Wyjaśnij kod w typescript

export const CollectionActivity: React.FC<CollectionActivityProps> = ({ limit = 20 }) => {

Następnie wyjaśnij kiedy komponenty w Next.js i Typescript tworzy się przy pomocy export function... a kiedy export const....

---

**Assistant:**

Okej, rozłóżmy to na części.  

---

## 1️⃣ Wyjaśnienie kodu:

```typescript
export const CollectionActivity: React.FC<CollectionActivityProps> = ({ limit = 20 }) => {
```

To linia, która definiuje **komponent funkcyjny React** w TypeScript, a konkretnie:

- `export const` — eksportuje zmienną o nazwie `CollectionActivity`, dzięki czemu może być użyta w innych plikach (np. `import { CollectionActivity } from "./CollectionActivity"`).

- `CollectionActivity` — nazwa komponentu.

- `: React.FC<CollectionActivityProps>` — to adnotacja typów:
  - `React.FC` (skrót od *React Functional Component*) to **typ ogólny** dostarczany przez React dla komponentów funkcyjnych.
  - `CollectionActivityProps` to interfejs opisujący **typy propsów**, jakie komponent przyjmuje.
  - Dzięki temu TypeScript wie, jakie właściwości (propsy) komponent akceptuje i jakiego typu są.

- `= ({ limit = 20 }) => { ... }` — to definicja **funkcji strzałkowej**, czyli ciała komponentu.
  - W tym przypadku komponent przyjmuje prop `limit`, który domyślnie ma wartość `20`.

Czyli w uproszczeniu:  
➡️ To komponent React napisany jako **funkcja strzałkowa**, z typowanymi propsami i eksportem.

---

## 2️⃣ Różnica: `export function ...` vs `export const ... = () => { ... }`

W React + TypeScript oba podejścia są poprawne. Różnice są subtelne i wynikają głównie z **preferencji** i **drobnych różnic semantycznych** w języku JavaScript.

---

### **A. `export function MyComponent(props: Props) { ... }`**

To tzw. **function declaration** (deklaracja funkcji).

✅ Zalety:
- Ma nazwę w stosie błędów (stack trace) — czyli jak coś się wykrzaczy, w konsoli zobaczysz dokładnie nazwę komponentu.
- Jest hoistowana — można jej użyć **zanim** zostanie zdefiniowana w kodzie.
- Nie wymaga `React.FC`, więc możesz precyzyjniej kontrolować typy propsów (np. nie ma automatycznego `children?: ReactNode`).

👎 Wady:
- Nie można łatwo przypisać np. `defaultProps` lub `displayName` bezpośrednio po deklaracji (choć to rzadko potrzebne w nowym kodzie).

---

### **B. `export const MyComponent: React.FC<Props> = (props) => { ... }`**

To **funkcja strzałkowa przypisana do stałej**.

✅ Zalety:
- Stylowo spójna z nowoczesnym podejściem Reacta (hooki, arrow functions).
- Można łatwo dodać `React.memo`, `forwardRef`, itp.:
  ```typescript
  export const MyComponent = React.memo((props: Props) => { ... });
  ```
- Często używana w kodzie Next.js i współczesnych projektach z TS.

👎 Wady:
- Nie jest hoistowana — musisz ją zdefiniować **zanim** zostanie użyta.
- `React.FC` dodaje automatycznie `children?: ReactNode`, co czasem jest niepożądane (ale można to nadpisać).

---

## 3️⃣ Kiedy używać którego

| Kontekst | Rekomendowane podejście | Dlaczego |
|-----------|-------------------------|-----------|
| Nowoczesny kod z hookami, `memo`, `forwardRef` | `export const` | Spójny styl, elastyczność |
| Prosty komponent bez hooków, preferujesz klasyczny styl | `export function` | Czystsza składnia, nie wymaga `React.FC` |
| Kod wewnątrz Next.js (np. strony w `app/` lub `pages/`) | Dowolnie | Next.js nie narzuca stylu — oba działają identycznie |
| Potrzebujesz typów `children` bez `React.FC` | `export function` lub ręcznie typowany `props` w `const` | Większa kontrola nad typami |

---

💡 **Podsumowanie praktyczne:**

W większości nowoczesnych projektów z React + TypeScript (w tym Next.js):
```tsx
export const MyComponent = ({ title }: { title: string }) => {
  return <h1>{title}</h1>;
};
```
lub jeśli chcesz lepsze typowanie:
```tsx
type Props = { title: string };

export const MyComponent: React.FC<Props> = ({ title }) => (
  <h1>{title}</h1>
);
```

ale jeśli wolisz prostotę:
```tsx
export function MyComponent({ title }: { title: string }) {
  return <h1>{title}</h1>;
}
```
— też będzie w pełni poprawne.

---

Chcesz, żebym pokazał przykładowe typowanie komponentu w obu wersjach (function vs const) z wykorzystaniem `props` i `children`?