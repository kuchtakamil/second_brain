# Różnice między JOIN a LEFT JOIN

**Data:** 2024-09-25

---

**User:**

Mam takiego sqla
select a.id, a.name, b.title from author a left join book b on a.id = b.author_id
Jaka byłaby różnica gdybym zastosował join zamiast left join

---

**Assistant:**

Różnica między `JOIN` (czyli domyślnym `INNER JOIN`) a `LEFT JOIN` polega na tym, jakie dane zostaną zwrócone z tabeli po lewej stronie w przypadku, gdy nie ma dopasowanych rekordów w tabeli po prawej stronie.

1. **LEFT JOIN**:
   - Zwróci **wszystkie** rekordy z tabeli `author` (czyli tabeli po lewej stronie), nawet jeśli nie ma pasujących rekordów w tabeli `book`. 
   - Jeśli nie ma pasujących rekordów w tabeli `book`, kolumny z tej tabeli (`b.title`) będą miały wartość `NULL`.

   Przykład:
   - Jeśli autor nie napisał żadnej książki, nadal zobaczysz tego autora, a pole `b.title` będzie `NULL`.

2. **JOIN** (czyli **INNER JOIN**):
   - Zwróci **tylko te rekordy**, które mają dopasowanie w obu tabelach. Oznacza to, że zwróci tylko autorów, którzy mają co najmniej jedną książkę w tabeli `book`.
   - Jeśli autor nie napisał żadnej książki, taki rekord nie zostanie uwzględniony w wynikach.

Przykład:
```sql
-- LEFT JOIN
SELECT a.id, a.name, b.title
FROM author a
LEFT JOIN book b ON a.id = b.author_id;

-- INNER JOIN (domyślny JOIN)
SELECT a.id, a.name, b.title
FROM author a
JOIN book b ON a.id = b.author_id;
```

**Podsumowanie:**
- `LEFT JOIN`: zwraca wszystkich autorów, nawet jeśli nie mają książek.
- `JOIN` (INNER): zwraca tylko tych autorów, którzy mają książki.