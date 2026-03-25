# TS Code: Hash Names.

**Data:** 2023-07-24

---

**User:**

Podany kod w JS napisz w TypeScript
const H = require('crypto').createHash
for (let a of  ["Ana Santos", "José Silva", "Bryan Lee", "Maria Silva", "Vitor Santos"]) 
    console.log( a,  H('md5').update(a).digest("hex") )
    // of course, no error, but no reuse.

---

**Assistant:**

To rewrite the provided JavaScript code in TypeScript, we need to add type annotations and adjust the import statement. TypeScript allows us to specify types for variables, functions, and parameters, providing better type safety.

First, let's install the necessary types for the 'crypto' module using the `@types/node` package:

```bash
npm install @types/node --save-dev
```

Now, let's rewrite the code in TypeScript:

```typescript
import * as crypto from 'crypto';

const H = (algorithm: string) => crypto.createHash(algorithm);

const names: string[] = ["Ana Santos", "José Silva", "Bryan Lee", "Maria Silva", "Vitor Santos"];

for (const a of names) {
    console.log(a, H('md5').update(a).digest("hex"));
}
```

Changes made in the TypeScript version:
1. We import the 'crypto' module using the `import` syntax, which is standard in TypeScript.
2. We add a type annotation for the `H` variable, specifying that it's a function taking a string parameter (the algorithm) and returning a `Hash` object from the 'crypto' module.
3. We explicitly type the `names` array to be an array of strings using `: string[]`.

This TypeScript code should work the same as the original JavaScript code but with added type safety provided by TypeScript.

---

**User:**

super, dzięki

---

**Assistant:**

Nie ma sprawy, chętnie pomogłem! Jeśli masz jeszcze jakieś pytania dotyczące TypeScript lub czegokolwiek innego, śmiało pytaj. Powodzenia z nauką TypeScript i programowaniem! Have a great day!