# Regular Expression for Alphanumeric

**Data:** 2023-02-11

---

**User:**

napisz wyrażenie regularne które sprawdza czy ciąg znaków składa się wyłącznie z dużych liter lub cyfr lub kombinacji dużych liter i cyfr.

---

**Assistant:**

Wyrażenie regularne, które sprawdza czy ciąg znaków składa się wyłącznie z dużych liter lub cyfr lub kombinacji dużych liter i cyfr może wyglądać następująco:

```
^[A-Z0-9]+$
```

^ oznacza początek ciągu znaków, a $ oznacza jego koniec. [A-Z0-9]+ oznacza, że ciąg znaków może składać się z jednej lub więcej dużych liter (A-Z) lub cyfr (0-9).

---

**User:**

w języku scala sprawdź czy ciąg znaków "sd32" spełnia to wyrażenie regularne

---

**Assistant:**

Można to zrobić w następujący sposób w języku Scala:

```
val regex = "^[A-Z0-9]+$".r
val string = "sd32"
val result = regex.findFirstIn(string)

if (result.isDefined) {
  println("Ciąg znaków spełnia wyrażenie regularne.")
} else {
  println("Ciąg znaków nie spełnia wyrażenia regularnego.")
}
```

W tym przypadku, wynik będzie brzmiał: "Ciąg znaków nie spełnia wyrażenia regularnego.".

---

**User:**

Wiedziałeś że można to szybciej zrobić w ten sposób? "sd32".matches("^[A-Z0-9]+$")

---

**Assistant:**

Tak, wiedziałem. Szybszym sposobem jest użycie metody `matches` w celu sprawdzenia, czy ciąg znaków spełnia dane wyrażenie regularne:

```
val string = "sd32"
val result = string.matches("^[A-Z0-9]+$")

if (result) {
  println("Ciąg znaków spełnia wyrażenie regularne.")
} else {
  println("Ciąg znaków nie spełnia wyrażenia regularnego.")
}
```

Wynik będzie taki sam, jak w poprzedniej odpowiedzi.

---

**User:**

Ale ten sposób jest dużo bardziej elegancki i szybszy.

---

**Assistant:**

Tak, użycie metody `matches` jest bardziej eleganckim i szybszym sposobem sprawdzenia, czy ciąg znaków spełnia wyrażenie regularne. Dziękuję za uwagę!