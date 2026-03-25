# CSS do zwizualizowania danych

**Data:** 2023-05-10

---

**User:**

Dla podanego html zaproponuj jak zwizualizować te dane poprzez podanie css
<div>
<div><h3>Carriage Speed</h3><div>142</div><div>invalid</div><div>18:27:29 10-05-2023</div></div>
<div><h3>Bed Temperature</h3><div>0</div><div>valid</div><div>18:27:29 10-05-2023</div></div>
</div>

---

**Assistant:**

Oto zaproponowany CSS, który pomoże zwizualizować podane dane:

```html
<style>
  .data-container {
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
  }

  h3 {
    margin: 0;
    font-size: 16px;
    font-weight: bold;
  }

  .data-item {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    margin-top: 5px;
  }

  .data-item div {
    margin-left: 10px;
  }

  .valid {
    color: green;
  }

  .invalid {
    color: red;
  }
</style>

<div class="data-container">
  <div class="data-item">
    <h3>Carriage Speed</h3>
    <div>142</div>
    <div class="invalid">invalid</div>
    <div>18:27:29 10-05-2023</div>
  </div>
</div>

<div class="data-container">
  <div class="data-item">
    <h3>Bed Temperature</h3>
    <div>0</div>
    <div class="valid">valid</div>
    <div>18:27:29 10-05-2023</div>
  </div>
</div>
```

Ten kod CSS definiuje styl dla każdego elementu wewnętrznego diva, który zawiera dane. Klasa `data-container` definiuje styl dla kontenera, który zawiera cały blok danych. Klasa `data-item` definiuje styl dla pojedynczego wiersza danych. Klasa `valid` i `invalid` nadaje odpowiednie kolory dla stanu danych.

Możesz wkleić ten kod CSS do sekcji `<style>` w swoim pliku HTML, aby zwizualizować dane zgodnie z proponowanym stylem.