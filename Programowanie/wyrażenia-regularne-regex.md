# Wyrażenia regularne - Regex.

**Data:** 2023-07-26

---

**User:**

wyjaśnij regex w j. polskim
(?<=Obowiazkowe)[\\s\\S]*?(?=posting)

---

**Assistant:**

Ten wyrażenie regularne w języku polskim można wyjaśnić w następujący sposób:

1. `(?<=Obowiazkowe)`: To tzw. "wyrażenie wyzerowania szerokości wstecznej" (lookbehind). Oznacza to, że jest to punkt dopasowania, który ma wystąpić po frazie "Obowiazkowe". Wyrażenie to nie zostanie uwzględnione w wyniku dopasowania, ale jest wymagane, aby występowało przed właściwym dopasowaniem.

2. `[\\s\\S]*?`: To fragment, który faktycznie dopasowuje treść. Składa się z:
   - `[\\s\\S]`: To jest klasa znaków, która dopasowuje dowolny znak, zarówno biały (spacje, tabulacje itp.) jak i niebiały (tekst, liczby, znaki specjalne itp.). Jest to konieczne, ponieważ wyrażenie regularne w tym przypadku może dopasować znaki nowej linii i inne znaki specjalne.
   - `*?`: To jest kwantyfikator, który oznacza, że poprzedzający wzorzec (w tym przypadku klasa znaków `[\\s\\S]`) może występować dowolną ilość razy (także zero razy). `*?` jest kwantyfikatorem "leniwym" (nongreedy), co oznacza, że dopasowanie będzie jak najkrótsze.

3. `(?=posting)`: To jest tzw. "wyrażenie wyzerowania szerokości do przodu" (lookahead). Oznacza to, że jest to punkt dopasowania, który ma wystąpić przed frazą "posting". Wyrażenie to nie zostanie uwzględnione w wyniku dopasowania, ale jest wymagane, aby występowało po właściwym dopasowaniu.

Podsumowując, wyrażenie regularne `(?<=Obowiazkowe)[\\s\\S]*?(?=posting)` dopasowuje dowolny fragment tekstu, który znajduje się pomiędzy frazą "Obowiazkowe" a frazą "posting" w wyrażeniu wejściowym. Warto zaznaczyć, że frazy "Obowiazkowe" i "posting" same w sobie nie zostaną uwzględnione w wyniku dopasowania.

---

**User:**

a jak zmodyfikować regex aby Obowiazkowe i posting zawierały się w wyniku dopasowania?

---

**Assistant:**

Aby uwzględnić także frazy "Obowiazkowe" i "posting" w wyniku dopasowania, musimy po prostu przesunąć wyrażenie lookbehind `(?<=Obowiazkowe)` i lookahead `(?=posting)` tak, aby były częścią właściwego dopasowania. Możemy to osiągnąć poprzez przeniesienie ich do zwykłych nawiasów, które nie są wyrażeniami wyzerowania szerokości, czyli usunięcie `(?<=` i `(?=` oraz odpowiednie ich umieszczenie.

Oto zmodyfikowane wyrażenie regularne:

```
(Obowiazkowe[\\s\\S]*?posting)
```

W skrócie:
1. `Obowiazkowe`: Dopasowuje frazę "Obowiazkowe".
2. `[\\s\\S]*?`: Dopasowuje dowolny fragment tekstu, w tym spacje, nowe linie itp. Opcja `*?` sprawia, że dopasowanie będzie jak najkrótsze.
3. `posting`: Dopasowuje frazę "posting".

Teraz cała fraza, zaczynając od "Obowiazkowe" i kończąc na "posting", zostanie uwzględniona w wyniku dopasowania.