# Kwantyle na wydatki

**Data:** 2023-12-31

---

**User:**

SELECT
  mn.name AS ministry_name,
  e.amount,
  NTILE(3) OVER(ORDER BY e.amount) AS expense_group
FROM
  expense e
JOIN
  ministry_name mn ON e.ministry_name_id = mn.id
ORDER BY
  e.amount;

Tutal kwantyle są tworzone na podstawie  e.amount zgadza się?

---

**Assistant:**

Tak, w Twoim zapytaniu SQL używasz funkcji okienkowej `NTILE(3)` do podziału danych na kwantyle (w tym przypadku na trzy grupy) na podstawie kolumny `e.amount`. Funkcja `NTILE` dzieli uporządkowany zestaw danych na określoną liczbę równych części, w tym przypadku na trzy grupy.

Zapytanie, które napisałeś, wykonuje następujące czynności:
1. Łączy tabelę `expense` (alias `e`) z tabelą `ministry_name` (alias `mn`) za pomocą klucza obcego `ministry_name_id`.
2. Dla każdego wpisu w tabeli `expense`, oblicza, do której grupy kwantylowej należy na podstawie wartości w kolumnie `amount`, dzieląc wszystkie rekordy na trzy równo liczebne grupy.
3. Wyniki są uporządkowane według wartości w kolumnie `amount`.

Dzięki temu możesz zobaczyć, jak wydatki każdego ministerstwa są rozłożone i do której grupy kwantylowej każdy wydatek należy.

---

**User:**

A co gdy zrobimy tak
SELECT
  mn.name AS ministry_name,
  e.amount,
  NTILE(3) OVER() AS expense_group
FROM
  expense e
JOIN
  ministry_name mn ON e.ministry_name_id = mn.id
ORDER BY
  e.amount;

Na jakiej podstawie tworzone są te kwantyle?

---

**Assistant:**

Jeśli użyjesz funkcji `NTILE(3)` bez określenia klauzuli `ORDER BY` wewnątrz funkcji okienkowej (jak w Twoim drugim zapytaniu), wynik będzie technicznie zależał od porządku, w jakim dane są przetwarzane przez bazę danych, ale jest to generalnie niezalecane i może prowadzić do nieprzewidywalnych wyników.

W SQL, kiedy nie podajesz jasno kryteriów porządkowania dla funkcji okienkowej, jak `NTILE`, baza danych może przyporządkować rekordy do grup kwantylowych w oparciu o wewnętrzny porządek przechowywania danych, który może nie być intuicyjny ani stały. W praktyce oznacza to, że wyniki mogą się różnić przy każdym wykonaniu zapytania, szczególnie gdy dane w tabeli się zmieniają.

Dlatego zawsze zaleca się używanie `ORDER BY` wewnątrz funkcji okienkowej (tak jak w pierwszym zapytaniu), aby jasno zdefiniować kryterium, na podstawie którego rekordy będą dzielone na grupy kwantylowe. Bez tego, wyniki mogą być mylące i trudne do interpretacji.