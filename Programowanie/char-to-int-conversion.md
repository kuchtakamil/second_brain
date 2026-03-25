# Char to Int Conversion

**Data:** 2023-08-18

---

**User:**

Scala, char '3' chcę zamienić na Int = 3

---

**Assistant:**

W języku Scala można przeprowadzić konwersję typu Char na Int poprzez odjęcie kodu znaku '0' od kodu znaku, który reprezentuje cyfrę. W przypadku znaku '3', jego kod ASCII to 51, a kod znaku '0' to 48. Odejmując 48 od 51 otrzymujemy wartość 3. Oto jak można to zrobić:

```scala
val charValue: Char = '3'
val intValue: Int = charValue - '0'

println(intValue) // Wyświetli 3
```

Warto zaznaczyć, że ta metoda działa tylko wtedy, gdy znak jest rzeczywiście reprezentacją cyfry dziesiętnej. Jeśli próbujesz przekonwertować inny znak (np. litery) na liczbę, może to spowodować nieprzewidywalne wyniki lub błędy.