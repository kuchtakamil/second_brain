# FlatMap vs Map w Java

**Data:** 2024-12-15

---

**User:**

W takim kodzie 
Optional<String> tokenChosen = Optional.ofNullable(params.get(TOKEN)).map(t -> t.get(0));
Optional<Token> chosenToken = tokenChosen.flatMap(token -> 
    someParam ? createTokenDiff(Optional.of(token)) : createToken(Optional.of(token))
);

dlaczego jest potrzebne flatMap a nie np map?

---

**Assistant:**

W Twoim kodzie potrzebne jest użycie `flatMap` zamiast `map`, ponieważ metoda `flatMap` w `Optional` służy do "spłaszczenia" zagnieżdżonej struktury `Optional<Optional<T>>`, która mogłaby powstać, gdybyś użył `map`.

Przeanalizujmy dokładnie, co się dzieje:

### Działanie `map`
Metoda `map` przyjmuje funkcję, która przekształca wartość zawartą w `Optional` na dowolny inny obiekt. Wynik tej funkcji zawsze jest opakowany w `Optional`. To oznacza, że jeśli metoda zwrócona w `map` zwraca `Optional<Token>`, wynik będzie miał strukturę `Optional<Optional<Token>>`.

### Działanie `flatMap`
Metoda `flatMap` działa podobnie do `map`, ale zakłada, że funkcja przekazana jako argument zwraca już obiekt typu `Optional<T>`. W takim przypadku `flatMap` "spłaszcza" wynik, usuwając jedno opakowanie `Optional`, dzięki czemu wynik ma strukturę `Optional<T>` zamiast `Optional<Optional<T>>`.

### Dlaczego w Twoim kodzie używamy `flatMap`?
Przyjrzyjmy się fragmentowi kodu:
```java
Optional<Token> chosenToken = tokenChosen.flatMap(token -> 
    someParam ? createTokenDiff(Optional.of(token)) : createToken(Optional.of(token))
);
```

- Funkcje `createTokenDiff` i `createToken` zwracają wartości typu `Optional<Token>`.
- Jeśli użyłbyś `map`, wynik miałby typ `Optional<Optional<Token>>`.
- Aby uzyskać płaski `Optional<Token>`, konieczne jest użycie `flatMap`.

Przykład, co by się stało, gdybyś użył `map`:
```java
Optional<Optional<Token>> chosenToken = tokenChosen.map(token -> 
    someParam ? createTokenDiff(Optional.of(token)) : createToken(Optional.of(token))
);
```

### Podsumowanie
`flatMap` jest potrzebne w Twoim przypadku, ponieważ funkcje `createTokenDiff` i `createToken` już zwracają `Optional<Token>`, a Ty chcesz, aby wynik końcowy miał typ `Optional<Token>`, a nie `Optional<Optional<Token>>`. Dlatego `flatMap` jest tutaj odpowiednim wyborem.