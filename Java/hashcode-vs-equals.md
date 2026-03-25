# hashCode vs equals

**Data:** 2023-07-07

---

**User:**

java, czy gdy w klasie przeciążysz metodę hashCode to czy koniecznym jest przeciążanie equals?

---

**Assistant:**

W javie, jeśli przeciążasz metodę `hashCode()` w klasie, nie jest konieczne przeciążanie metody `equals()`. 

Metoda `hashCode()` służy do generowania kodu skróconego (hash code) dla obiektu, który jest używany przez niektóre struktury danych, takie jak haszmapy. Metoda ta ma na celu zwrócenie unikalnego kodu dla każdego obiektu, który różni się od innych obiektów, ale dla obiektów o takiej samej wartości powinna zwracać ten sam kod skrócony.

Z drugiej strony, metoda `equals()` służy do porównywania dwóch obiektów pod względem ich wartości. Standardowa implementacja metody `equals()` porównuje referencje obiektów, czyli sprawdza, czy dwa obiekty wskazują na ten sam obszar w pamięci. Jeśli chcesz zmienić sposób porównywania obiektów, na przykład porównując ich pola, powinieneś przeciążyć metodę `equals()`.

Choć zazwyczaj zaleca się przeciążanie zarówno metody `hashCode()`, jak i `equals()` dla spójności, nie jest to wymagane. Jednak ważne jest, aby w przypadku przeciążania jednej z tych metod zachować zgodność z kontraktami, które opisują zależności między nimi. Kontrakt ten mówi, że jeśli dwa obiekty są równe zgodnie z metodą `equals()`, to ich wartości kodów skróconych (`hashCode()`) powinny być również równe.

Jeśli przeciążasz metodę `hashCode()`, pamiętaj, że powinieneś również przeciążyć metodę `equals()` zgodnie z tym samym sposobem porównywania wartości, aby zapewnić spójność między tymi dwoma metodami.