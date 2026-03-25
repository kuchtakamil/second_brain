# Funkcja NTILE w SQL

**Data:** 2023-12-28

---

**User:**

Opisz co robi funkcja NTILE w sql

---

**Assistant:**

Funkcja `NTILE` w SQL jest używana w zapytaniach SQL do podziału uporządkowanego zestawu danych na określoną liczbę prawie równych części, czyli tzw. kwantyli. Jest to szczególnie przydatne w analizie statystycznej i przy raportowaniu danych. Oto jak funkcja `NTILE` działa:

1. **Podział Danych**: `NTILE` dzieli posortowane wiersze z wynikowego zbioru zapytań na określoną liczbę grup. Liczba grup jest określana przez argument przekazywany do funkcji `NTILE`.

2. **Porządkowanie Danych**: Przed zastosowaniem `NTILE`, dane muszą być uporządkowane za pomocą klauzuli `ORDER BY`. Funkcja `NTILE` przydziela każdemu wierszowi numer grupy na podstawie tego porządku.

3. **Przydział Kwantyli**: Jeżeli ilość wierszy nie dzieli się równo przez liczbę grup, niektóre z ostatnich grup mogą mieć mniej elementów. Na przykład, jeśli mamy 10 wierszy i chcemy podzielić je na 4 grupy, pierwsze trzy grupy będą miały po 3 wiersze, a czwarta grupa będzie miała tylko 1 wiersz.

4. **Zastosowania**: Funkcja `NTILE` jest często wykorzystywana do identyfikacji percentyli, kwartylów, decyli itp. w zbiorach danych, co może być pomocne w analizie rozkładu wartości.

Przykład użycia `NTILE`:

```sql
SELECT NTILE(4) OVER (ORDER BY wynik_testu) AS Kwartyly,
       imie,
       wynik_testu
FROM uczniowie;
```

W tym przykładzie, funkcja `NTILE` podzieli uczniów na 4 grupy (kwartyly) na podstawie ich wyników w teście, uporządkowanych od najniższego do najwyższego. Każdy uczeń zostanie przypisany do jednej z czterech grup.