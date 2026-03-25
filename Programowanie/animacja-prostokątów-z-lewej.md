# Animacja prostokątów z lewej.

**Data:** 2023-12-07

---

**User:**

Mam obrazem składający się z kilku prostokątów. Chciałbym aby prostokąty pojawiały się w pewnej określonej kolejności, wjeżdżając na ekran z lewej strony. Jak mam to zrobić?

---

**Assistant:**

Aby zrealizować animację prostokątów wjeżdżających na ekran z lewej strony, możesz skorzystać z technologii webowych, takich jak HTML, CSS i JavaScript. Oto prosty przykład, jak to zrobić:

1. **HTML:**
   Utwórz strukturę HTML, w której będą umieszczone twoje prostokąty.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">
    <title>Animation</title>
</head>
<body>
    <div class="rectangle" id="rectangle1"></div>
    <div class="rectangle" id="rectangle2"></div>
    <!-- Dodaj więcej divów dla dodatkowych prostokątów -->
    <script src="script.js"></script>
</body>
</html>
```

2. **CSS:**
   Dodaj styl CSS do pliku `styles.css` w celu określenia wyglądu prostokątów i ich animacji.

```css
body {
    margin: 0;
    overflow: hidden;
}

.rectangle {
    width: 100px;
    height: 50px;
    background-color: blue;
    position: absolute;
    left: -100px; /* Początkowa pozycja poza ekranem z lewej strony */
    top: 50%;
    transform: translateY(-50%);
    animation: slideIn 2s forwards; /* Ustawienia animacji: czas trwania 2s, zatrzymaj na końcowej pozycji */
}

@keyframes slideIn {
    to {
        left: 50%; /* Końcowa pozycja na ekranie */
    }
}
```

3. **JavaScript:**
   Utwórz plik `script.js` i dodaj kod JavaScript, który kontroluje pojawianie się prostokątów w określonej kolejności.

```javascript
document.addEventListener("DOMContentLoaded", function() {
    // Pobierz wszystkie prostokąty
    const rectangles = document.querySelectorAll('.rectangle');

    // Iteruj przez prostokąty i ustaw opóźnienie animacji dla każdego z nich
    rectangles.forEach((rectangle, index) => {
        rectangle.style.animationDelay = `${index * 0.5}s`; // Dla przykładu, opóźnienie wynosi 0.5s dla każdego kolejnego prostokąta
    });
});
```

W powyższym kodzie, `animationDelay` jest ustawiane dla każdego prostokąta, aby opóźnić jego animację, tworząc wrażenie pojawiania się w kolejności. Możesz dostosować wartości i style w zależności od swoich potrzeb.

---

**User:**

nie chcę kożystać javascript, html itp. Ten obrazek jest zapisany w png

---

**Assistant:**

Jeśli chcesz uzyskać efekt wjeżdżania prostokątów w pewnej kolejności bez korzystania z HTML, CSS ani JavaScript, musisz użyć dedykowanego oprogramowania do edycji obrazów, takiego jak Adobe Photoshop, GIMP lub inny edytor graficzny.

Poniżej znajdziesz ogólną instrukcję, jak to zrobić w programie Adobe Photoshop:

1. **Otwórz obraz w programie Photoshop:**
   - Uruchom Photoshop i otwórz obraz PNG.

2. **Utwórz nowe warstwy dla prostokątów:**
   - Wybierz narzędzie "Prostokąt" i narysuj prostokąt na nowej warstwie.
   - Powtórz ten krok dla każdego prostokąta, którego chcesz użyć.

3. **Ustaw początkowe pozycje warstw:**
   - Wybierz narzędzie "Przesunięcie" (Move Tool).
   - Przesuń każdą warstwę prostokąta tak, aby była poza obszarem obrazu z lewej strony.

4. **Ustaw animację warstw:**
   - Przejdź do okna "Animacja" (Window > Timeline), aby otworzyć panel animacji.
   - Dla każdej warstwy:
     - Kliknij ikonę opcji warstwy (widoczna jako trzy poziome linie) w panelu warstw.
     - Wybierz "Klatka początkowa" (Initial Frame).

5. **Ustaw czas trwania animacji:**
   - Wybierz klatkę na końcu animacji w panelu animacji.
   - Zmniejsz czas trwania animacji, aby skrócić czas, w którym prostokąty wjeżdżają.

6. **Eksportuj animację:**
   - Wybierz "Eksportuj" (Export) > "Zapisz do pliku" (Save for Web).
   - Wybierz format pliku GIF, a następnie kliknij "Zapisz".

Teraz masz animowany plik GIF, który przedstawia prostokąty wjeżdżające na ekran z lewej strony. Możesz dostosować szczegóły i efekty w programie Photoshop zgodnie z własnymi preferencjami.