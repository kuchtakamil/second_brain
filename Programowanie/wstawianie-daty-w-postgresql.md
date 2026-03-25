# Wstawianie daty w PostgreSQL

**Data:** 2023-12-27

---

**User:**

Jak w postgresql zrobić insert do tabeli gdzie jedno z pól to data

---

**Assistant:**

Aby w PostgreSQL wykonać operację `INSERT` do tabeli, gdzie jedno z pól to data, należy użyć odpowiedniego formatu daty i czasu oraz dostarczyć dane w odpowiedniej postaci. Oto przykład, jak to zrobić:

Załóżmy, że masz tabelę o nazwie `moja_tabela` z następującymi kolumnami:

1. `id` - kolumna typu integer (np. SERIAL)
2. `nazwa` - kolumna typu text
3. `data` - kolumna typu date

Aby wstawić nowy rekord, w którym pole `data` będzie zawierać datę, możesz użyć polecenia `INSERT` w następujący sposób:

```sql
INSERT INTO moja_tabela (nazwa, data)
VALUES ('Przykładowa nazwa', '2023-12-27');
```

W powyższym przykładzie wprowadziliśmy nowy rekord do tabeli `moja_tabela` z dwoma kolumnami: `nazwa` i `data`. Wartość `'2023-12-27'` wstawiliśmy jako datę w formacie 'YYYY-MM-DD'. PostgreSQL rozpozna tę wartość jako datę i wstawi ją do kolumny `data`.

Jeśli potrzebujesz wstawić datę i godzinę, użyj formatu 'YYYY-MM-DD HH:MI:SS', a jeśli potrzebujesz przechowywać strefy czasowe, użyj odpowiedniego typu danych, na przykład `timestamp with time zone` lub `timestamp without time zone`, w zależności od Twoich potrzeb.

---

**User:**

jak wygląda create table dla takiej tabeli

---

**Assistant:**

Aby utworzyć tabelę w PostgreSQL dla Twojej tabeli z kolumnami `id`, `nazwa` i `data`, możesz użyć polecenia `CREATE TABLE`. Oto przykład definicji tabeli:

```sql
CREATE TABLE moja_tabela (
    id serial PRIMARY KEY,
    nazwa text,
    data date
);
```

W powyższym przykładzie użyliśmy `serial` do automatycznego generowania unikalnych wartości dla kolumny `id`. Jest to często używane w PostgreSQL do tworzenia klucza głównego, który jest jednocześnie kluczem głównym i ma automatycznie rosnące wartości.

Kolumna `nazwa` jest typu `text`, co pozwala na przechowywanie napisów o zmiennej długości.

Kolumna `data` jest typu `date`, co pozwala na przechowywanie daty (bez godziny i minuty).

Jeśli potrzebujesz bardziej zaawansowanych ustawień, takich jak indeksy, ograniczenia lub inne właściwości kolumn, możesz je dodać do definicji tabeli w zależności od swoich potrzeb.