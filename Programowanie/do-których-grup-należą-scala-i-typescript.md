# Do których grup należą Scala i TypeScript?

**Data:** 13 sty 2026, 23:14:37 CET

---

**User:**

Do których grup należą Scala i TypeScript?

---

**Gemini:**

### Scala

**Typowanie: Statyczne / Mocne**

Scala łączy paradygmat obiektowy z funkcjonalnym, opierając się na wyrafinowanym systemie typów statycznych.

- **Statyczność:** Typy są sprawdzane w czasie kompilacji przez kompilator `scalac`. Scala wykorzystuje zaawansowane **wnioskowanie typów (type inference)**, co pozwala uniknąć nadmiarowości kodu przy zachowaniu pełnego bezpieczeństwa statycznego.
- **Mocne typowanie:** Język nie pozwala na niejawne konwersje, które prowadziłyby do utraty precyzji lub błędów logicznych (np. dodawanie ciągu znaków do liczby).
- **Zaawansowane aspekty:**
  - **Nominal Typing:** System typów opiera się głównie na nazwach (klasach, traitach), w przeciwieństwie do strukturalnego podejścia TypeScriptu.
  - **Scala 3 (Dotty):** Wprowadziła unie typów (`TypeA | TypeB`), iloczyny typów (`TypeA & TypeB`) oraz typy nieprzezroczyste (`opaque type aliases`), co jeszcze bardziej zbliża jej system typów do teorii typów wyższego rzędu.
  - **Type Erasure:** Podobnie jak w Javie, ze względu na działanie na JVM, informacje o typach generycznych są usuwane w czasie wykonywania programu (runtime).

```
// Static and Strong Typing in Scala
val x: Int = 10
// x = "text" // Compile-time error

def add(a: Int, b: Int): Int = a + b

// Union types in Scala 3
type ID = String | Int
val userId: ID = 123
val userName: ID = "admin"
```

---

### TypeScript

**Typowanie: Statyczne / Mocne (z zastrzeżeniami)**

TypeScript jest nadzbiorem JavaScriptu, który wprowadza opcjonalne statyczne typowanie do dynamicznego środowiska.

- **Statyczność:** TypeScript jest językiem statycznym na etapie kompilacji (transpilacji do JS). Po sprawdzeniu typów przez `tsc`, metadane o typach są całkowicie usuwane (**Type Erasure**), a wynikowy kod JavaScript jest wykonywany dynamicznie.
- **Mocne vs. Słabe:** TypeScript dąży do bycia językiem o mocnym typowaniu, oferując mechanizmy takie jak `strict` mode, które blokują niejawne konwersje. Jednak ze względu na interoperacyjność z JavaScriptem i istnienie typu `any` oraz rzutowania (`as`), system ten jest określany jako **unsound** (niegwarantujący pełnego bezpieczeństwa w runtime).
- **Zaawansowane aspekty:**
  - **Structural Typing (Duck Typing):** TypeScript stosuje typowanie strukturalne. Jeśli dwa obiekty mają tę samą strukturę (te same pola i typy), są uznawane za ten sam typ, niezależnie od ich deklaracji.
  - **Gradual Typing:** Pozwala na stopniowe wprowadzanie typów do istniejących projektów JS, co jest unikalnym komprosem między elastycznością a bezpieczeństwem.

```
// Structural Typing in TypeScript
interface Point {
    x: number;
    y: number;
}

function logPoint(p: Point) {
    console.log(`${p.x}, ${p.y}`);
}

const obj = { x: 1, y: 2, z: 3 };
logPoint(obj); // Valid, because 'obj' has x and y properties
```

### Porównanie w matrycy

| Język | Model Typowania | System | Charakterystyka |
| --- | --- | --- | --- |
| **Scala** | Statyczne / Mocne | Nominalny | Rygorystyczny, silnie osadzony w matematycznej teorii kategorii, zintegrowany z JVM. |
| **TypeScript** | Statyczne / Mocne\* | Strukturalny | Elastyczny, nakładka na dynamiczne środowisko, skupiony na deweloperskim DX (Developer Experience). |

\*W TypeScript siła typowania zależy od konfiguracji (np. `strict: true`) oraz unikania typu `any`.