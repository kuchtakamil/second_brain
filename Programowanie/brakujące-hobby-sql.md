# Brakujące hobby: SQL

**Data:** 2023-08-08

---

**User:**

Mam dwie tabele, jedna zawiera imiona ludzi i lucz obcy do ich hobby. Druga tabela to tabela z hobby. Napisz SQL wybierający wszystkich ludzi którzy nie mają hobby

---

**Assistant:**

Oczywiście, oto przykładowy zapytanie SQL, które wybierze wszystkich ludzi, którzy nie mają hobby:

```sql
SELECT imie
FROM ludzie
WHERE imie NOT IN (
    SELECT l.imie
    FROM ludzie l
    JOIN hobby h ON l.hobby_id = h.id
);
```

W tym zapytaniu wykorzystywane są dwie tabele: "ludzie" i "hobby". Zakładam, że tabela "ludzie" zawiera kolumny "imie" oraz "hobby_id", gdzie "hobby_id" to klucz obcy do tabeli "hobby". Kolumna "id" w tabeli "hobby" jest przyjętym identyfikatorem hobby.

W zapytaniu głównym wybierane są imiona ludzi z tabeli "ludzie", którzy nie mają odpowiadającego im wpisu w tabeli "hobby". Działa to na zasadzie podzapytania, które wybiera imiona ludzi, którzy mają hobbys, a następnie te imiona są wykluczone z wyniku głównego zapytania za pomocą klauzuli `NOT IN`.

---

**User:**

A czy zadziałąło by to?
Select imie From ludzie where ludzie.hobby_id = null

---

**Assistant:**

Zapytanie, które przedstawiłeś, ma pewne niedociągnięcia. Porównywanie wartości z NULL za pomocą operatora `=` nie zawsze działa poprawnie. Aby sprawdzić, czy wartość jest NULL, należy użyć operatora `IS NULL`. Oto poprawione zapytanie:

```sql
SELECT imie
FROM ludzie
WHERE ludzie.hobby_id IS NULL;
```

To zapytanie wybierze imiona ludzi, których pole "hobby_id" w tabeli "ludzie" ma wartość NULL, co oznacza, że nie mają przypisanego żadnego hobby.