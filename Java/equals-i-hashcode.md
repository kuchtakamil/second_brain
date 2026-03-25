# equals() i hashCode()

**Data:** 2023-07-07

---

**User:**

java, czy gdy w klasie przeciążysz metodę equals to czy koniecznym jest przeciążanie hashCode?

---

**Assistant:**

Tak, jeśli przeciążasz metodę `equals()` w klasie w Javie, to zgodnie z kontraktem obiektów w kolekcjach, powinieneś również przeciążyć metodę `hashCode()`. 

Metoda `equals()` jest używana do porównywania dwóch obiektów pod kątem równości, podczas gdy metoda `hashCode()` zwraca wartość skrótu (hasz) obiektu. Wiele struktur danych w Javie, takich jak `HashMap` czy `HashSet`, korzysta z metod `equals()` i `hashCode()` do identyfikowania i zarządzania obiektami.

Zgodnie z wymaganiami, jeśli dwa obiekty są sobie równe w sensie metody `equals()`, to muszą mieć również takie same wartości zwracane przez metodę `hashCode()`. W przeciwnym razie, jeśli przeciążasz tylko metodę `equals()` bez przeciążania `hashCode()`, mogą wystąpić nieprawidłowe wyniki, kiedy będziesz próbował używać takich obiektów w strukturach danych opartych na haszowaniu.

Dlatego, aby zapewnić spójność i poprawne działanie kolekcji, należy zawsze przeciążać zarówno `equals()` jak i `hashCode()` w klasach, które mają być używane w kolekcjach, jeśli przeciążasz jeden z nich.