# Wywołanie super w POJO

**Data:** 2024-12-13

---

**User:**

Java, tworząc za pomocą konstruktora zwykły obiekt POJO, czy jest sens wywoływać super() w pierwszej linii konstruktora kiedy klasa nie dziedziczy po innej klasie?

---

**Assistant:**

Nie, wywoływanie `super()` w pierwszej linii konstruktora klasy POJO, która **nie dziedziczy po żadnej innej klasie poza domyślną klasą `Object`**, jest zbędne. Dzieje się tak, ponieważ:

1. **Automatyczne wywołanie `super()`**  
   Jeśli klasa nie dziedziczy od innej klasy, kompilator automatycznie dodaje wywołanie domyślnego konstruktora klasy nadrzędnej (`super()`), czyli w tym przypadku konstruktora klasy `Object`. Nie trzeba tego robić ręcznie.

2. **Nie wpływa na działanie kodu**  
   Wywołanie `super()` w tej sytuacji nie zmienia żadnych właściwości ani zachowania klasy, ponieważ klasa `Object` nie ma stanu, który trzeba zainicjalizować w jej konstruktorze.

### Przykład:
```java
public class MyPojo {
    private String name;

    public MyPojo(String name) {
        super(); // Zbędne, kompilator i tak zrobi to automatycznie
        this.name = name;
    }
}
```

Można to uprościć do:
```java
public class MyPojo {
    private String name;

    public MyPojo(String name) {
        this.name = name;
    }
}
```

### Wyjątek:
Jeśli klasa **dziedziczy po innej klasie**, wtedy wywołanie `super()` (lub innego konstruktora nadrzędnego) może być wymagane, jeśli klasa nadrzędna nie ma konstruktora domyślnego lub jeśli chcemy jawnie zainicjalizować jej stan.

### Podsumowanie:
W klasach POJO, które nie dziedziczą po innych klasach niż `Object`, ręczne wywoływanie `super()` w konstruktorze nie jest potrzebne i można je pominąć.