# Porównanie Comparable i Comparator

**Data:** 2024-02-16

---

**User:**

Java Comparator vs Comparable. Odpowiedz po polsku

---

**Assistant:**

W języku Java, interfejsy Comparator i Comparable służą do porównywania obiektów, ale różnią się w swoim podejściu i zastosowaniach.

1. **Comparable:**
   - Interfejs Comparable jest używany do określenia porządku naturalnego obiektów danego typu.
   - Klasa implementująca interfejs Comparable musi dostarczyć metodę `compareTo`, która określa, jak porównać dany obiekt z innym obiektem tego samego typu.
   - Metoda `compareTo` zwraca liczbę ujemną, zero lub dodatnią, w zależności od tego, czy obiekt jest mniejszy, równy czy większy od porównywanego obiektu.

Przykład implementacji Comparable:

```java
public class MojaKlasa implements Comparable<MojaKlasa> {
    private int wartosc;

    // konstruktor, metody itp.

    @Override
    public int compareTo(MojaKlasa inna) {
        return Integer.compare(this.wartosc, inna.wartosc);
    }
}
```

2. **Comparator:**
   - Interfejs Comparator jest używany do dostarczenia zewnętrznego porównania dla klas, które same nie implementują interfejsu Comparable lub gdy chcemy dostarczyć alternatywne porównanie.
   - Klasa implementująca interfejs Comparator musi dostarczyć metodę `compare`, która określa, jak porównać dwa różne obiekty tego samego typu.
   - Comparator może być używany do porównywania obiektów w różny sposób, w zależności od wymagań.

Przykład implementacji Comparator:

```java
import java.util.Comparator;

public class MojaKomparator implements Comparator<MojaKlasa> {
    @Override
    public int compare(MojaKlasa obiekt1, MojaKlasa obiekt2) {
        // Logika porównania obiektów wg własnych kryteriów
        return Integer.compare(obiekt1.getWartosc(), obiekt2.getWartosc());
    }
}
```

Podsumowując, jeśli chcemy określić naturalny porządek dla obiektów danej klasy, używamy interfejsu Comparable. Jeśli natomiast chcemy dostarczyć zewnętrzne kryteria porównawcze dla obiektów, używamy interfejsu Comparator. Oba podejścia pozwalają na elastyczne porównywanie obiektów w zależności od naszych potrzeb.