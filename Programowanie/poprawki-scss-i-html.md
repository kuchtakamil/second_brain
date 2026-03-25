# Poprawki SCSS i HTML

**Data:** 2025-01-24

---

**User:**

mam taki scss
#questions {
    table{
        input[type=radio],{
            height: 11px;
            width: 11px;
        }
    }

Gdzie w html mam dodać class="questions"?

---

**Assistant:**

Masz błąd składniowy w swoim SCSS – po `input[type=radio],` jest zbędny przecinek. Poprawiona wersja:  

```scss
#questions {
    table {
        input[type=radio] {
            height: 11px;
            width: 11px;
        }
    }
}
```

Teraz odnośnie pytania – w HTML musisz dodać `id="questions"` do elementu, który zawiera tabelę, np.:

```html
<div id="questions">
    <table>
        <tr>
            <td><input type="radio" name="option"></td>
            <td>Opcja 1</td>
        </tr>
        <tr>
            <td><input type="radio" name="option"></td>
            <td>Opcja 2</td>
        </tr>
    </table>
</div>
```

Jeśli chciałeś użyć `class="questions"`, to musiałbyś zmienić w SCSS `#questions` na `.questions`:

```scss
.questions {
    table {
        input[type=radio] {
            height: 11px;
            width: 11px;
        }
    }
}
```

Wtedy w HTML:

```html
<div class="questions">
    <table>
        <tr>
            <td><input type="radio" name="option"></td>
            <td>Opcja 1</td>
        </tr>
    </table>
</div>
```

Podsumowując:  
- `id="questions"` → selektor `#questions`  
- `class="questions"` → selektor `.questions`  

Czy o to Ci chodziło? 😊

---

**User:**

a nie mogę tego zrobić na <table>?

---

**Assistant:**

Tak, możesz dodać `id="questions"` (lub `class="questions"`) bezpośrednio do `<table>`, wtedy SCSS będzie wyglądał tak:  

### **SCSS dla `id="questions"`**  
```scss
#questions {
    input[type=radio] {
        height: 11px;
        width: 11px;
    }
}
```
**HTML:**
```html
<table id="questions">
    <tr>
        <td><input type="radio" name="option"></td>
        <td>Opcja 1</td>
    </tr>
</table>
```

---

### **SCSS dla `class="questions"`**  
```scss
.questions {
    input[type=radio] {
        height: 11px;
        width: 11px;
    }
}
```
**HTML:**
```html
<table class="questions">
    <tr>
        <td><input type="radio" name="option"></td>
        <td>Opcja 1</td>
    </tr>
</table>
```

W obu przypadkach reguły SCSS będą działały poprawnie. 🚀