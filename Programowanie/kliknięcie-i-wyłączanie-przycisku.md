# Kliknięcie i wyłączanie przycisku

**Data:** 2025-06-06

---

**User:**

<div onClick=this.disabled>
<button....>
</div>
Czy to zadziała i sprawi że klawisz będzie wyszarzony po kliknieciu

---

**Assistant:**

Nie, taki kod **nie zadziała** tak, jak oczekujesz. Przypisanie `this.disabled` w `onClick` na `<div>` nie spowoduje wyłączenia `<button>` wewnątrz tego `<div>`.

### Dlaczego?
- `this` w `onClick=this.disabled` odnosi się do samego `<div>`, a **nie do przycisku**.
- Atrybut `disabled` **nie działa na `<div>`**, tylko na elementy form, takie jak `<button>`, `<input>`, itp.
- Wyrażenie `this.disabled` w tym kontekście po prostu **odczytuje wartość** (prawdopodobnie `undefined`), ale nic nie robi.

---

### Jak to zrobić dobrze?

Aby kliknięcie spowodowało wyszarzenie (`disabled`) przycisku, najlepiej użyć JavaScriptu, np.:

#### 1. W czystym HTML + JS (inline):
```html
<div onclick="this.querySelector('button').disabled = true;">
  <button>Kliknij mnie</button>
</div>
```

#### 2. Lub z `id`:
```html
<div onclick="document.getElementById('myButton').disabled = true;">
  <button id="myButton">Kliknij mnie</button>
</div>
```

---

### Uwaga:
Jeśli chcesz, żeby sam **przycisk** się wyłączał po kliknięciu, prostsze i lepsze podejście to:
```html
<button onclick="this.disabled = true;">Kliknij mnie</button>
```

To działa bez potrzeby opakowywania w `<div>` i jest bardziej semantyczne.

Chcesz to zrobić w czystym HTML/JS, czy np. w React/Angular?

---

**User:**

<div onclick="this.disabled = true;"><button></div>
Ato zadziała?

---

**Assistant:**

Nie, ten kod:

```html
<div onclick="this.disabled = true;"><button></div>
```

**nie zadziała** i dodatkowo jest **błędny składniowo** – brakuje zamknięcia taga `<button>`.

Ale nawet po poprawieniu na:

```html
<div onclick="this.disabled = true;"><button>Kliknij</button></div>
```

nadal nie osiągniesz oczekiwanego efektu, czyli wyłączenia przycisku (`<button disabled>`), ponieważ:

---

### 🔴 Problemy:

1. **`this.disabled = true` działa tylko na elementy, które mają atrybut `disabled`**, czyli np. `<button>`, a **`<div>` nie ma takiego atrybutu**, więc `this.disabled` nie robi nic.

2. `this` w `onclick="this.disabled = true;"` odnosi się do `<div>`, **nie do przycisku**.

---

### ✅ Poprawne rozwiązanie:

Jeśli chcesz wyłączyć `<button>` po kliknięciu **dowolnego miejsca w `<div>`**, użyj:

```html
<div onclick="this.querySelector('button').disabled = true;">
  <button>Kliknij mnie</button>
</div>
```

Jeśli chcesz wyłączyć przycisk **po kliknięciu w niego samego**, to najprościej tak:

```html
<button onclick="this.disabled = true;">Kliknij mnie</button>
```

---

### Bonus: Styl przycisku po wyłączeniu
Aby przycisk wyglądał „wyszarzony”, warto dodać trochę CSS (opcjonalnie):

```html
<style>
  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
```

---

Chcesz coś bardziej zaawansowanego, np. z animacją, odliczaniem, ponownym włączeniem itp.?