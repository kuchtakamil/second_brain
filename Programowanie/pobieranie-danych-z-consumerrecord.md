# Pobieranie danych z ConsumerRecord

**Data:** 2023-04-18

---

**User:**

Jak pobrać dane z klasy ConsumerRecord?

---

**Assistant:**

Klasa `ConsumerRecord` jest często używana w bibliotece Apache Kafka w języku Java do reprezentowania rekordu odczytanego przez konsumenta z klastra Kafka. Aby pobrać dane z obiektu `ConsumerRecord`, możesz skorzystać z jego metod dostępowych, takich jak:

1. `value()`: Zwraca wartość rekordu odczytanego przez konsumenta. Jest to zazwyczaj ciąg znaków reprezentujący przesyłane dane lub zserializowany obiekt.

2. `key()`: Zwraca klucz rekordu odczytanego przez konsumenta. Klucz może być używany do określenia, do jakiej partycji należy rekord, co jest przydatne podczas przetwarzania strumieniowego w klastrze Kafka.

3. `topic()`: Zwraca nazwę tematu Kafka, z którego pochodził rekord.

4. `partition()`: Zwraca numer partycji, z której pochodził rekord.

5. `offset()`: Zwraca offset, który wskazuje, którym rekordem z partycji jest dany rekord.

Aby pobrać dane z obiektu `ConsumerRecord`, możesz wywołać jedną lub więcej z powyższych metod. Na przykład, jeśli chcesz uzyskać wartość rekordu, możesz wywołać metodę `value()` na obiekcie `ConsumerRecord`. Przykład:

```java
ConsumerRecord<String, String> record = ...; // pobranie rekordu przez konsumenta
String value = record.value(); // pobranie wartości rekordu
```

Podobnie, jeśli chcesz uzyskać klucz rekordu, możesz wywołać metodę `key()` na obiekcie `ConsumerRecord`. Przykład:

```java
ConsumerRecord<String, String> record = ...; // pobranie rekordu przez konsumenta
String key = record.key(); // pobranie klucza rekordu
```