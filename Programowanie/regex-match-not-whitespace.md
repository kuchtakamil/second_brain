# Regex Match Not Whitespace

**Data:** 2023-07-25

---

**User:**

co oznacza regex [^\s@]+

---

**Assistant:**

The regular expression `[^\s@]+` has the following meaning:

1. `[]`: Square brackets in a regular expression denote a character class, which matches any single character from the set of characters specified within the brackets.

2. `^`: The caret symbol at the beginning of the character class negates it, meaning it matches any character NOT present in the character class.

3. `\s`: The `\s` is a special shorthand character class that represents any whitespace character, such as spaces, tabs, and newlines.

4. `@`: The "@" symbol is a literal character that will be matched as itself.

5. `+`: The plus symbol is a quantifier that means "one or more occurrences of the preceding expression."

Combining all the above points, the regular expression `[^\s@]+` will match one or more occurrences of any character that is not a whitespace character (`\s`) or the "@" symbol.

In simpler terms, it will match any sequence of characters that does not contain spaces or "@" symbols. For example, it would match strings like "hello123", "example.com", "user123", etc., but it would not match strings containing spaces or "@" symbols, such as "hello world", "user@example", etc.

---

**User:**

napisz po polsku

---

**Assistant:**

Wyrażenie regularne `[^\s@]+` oznacza:

1. `[]`: Kwadratowe nawiasy w wyrażeniu regularnym tworzą tzw. klasę znaków, która dopasowuje dowolny pojedynczy znak spośród tych, które zostały wymienione wewnątrz nawiasów.

2. `^`: Symbol daszka na początku klasy znaków neguje jej zawartość, co oznacza, że dopasowuje znaki NIE będące w klasie.

3. `\s`: Skrótowy zapis `\s` reprezentuje dowolny znak białego (whitespace), takie jak spacje, tabulatory czy nowe linie.

4. `@`: Symbol "@" jest traktowany dosłownie i będzie dopasowywany jako znak "@".

5. `+`: Symbol plusa oznacza, że dopasowywany jest jeden lub więcej wystąpień poprzedniego wyrażenia.

Podsumowując, wyrażenie regularne `[^\s@]+` dopasowuje jeden lub więcej znaków, które nie są spacjami ani znakiem "@". Na przykład, dopasuje ciągi znaków takie jak "hello123", "example.com", "user123", itp., ale nie dopasuje ciągów zawierających spacje lub znaki "@" jak "hello world", "user@example", itp.