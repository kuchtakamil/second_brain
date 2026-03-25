# KStream vs KTable.

**Data:** 2023-03-19

---

**User:**

Czy w Kafka różni się KStream od KTable?

---

**Assistant:**

Tak, w Apache Kafka KStream i KTable to dwa różne rodzaje strumieni danych.

KStream to strumień zdarzeń (event stream) - ciągły, nieprzetworzony przepływ danych w Kafka, składający się z pojedynczych rekordów. KStream można interpretować jako nieskończony ciąg zdarzeń, w którym każde zdarzenie jest niezależne i ma wartość klucza oraz wartość wartości.

KTable natomiast reprezentuje strukturę danych, w której wartości są grupowane według kluczy. KTable jest zbiorem zrzutowanych (materialized) danych ze strumienia KStream i reprezentuje aktualny stan dla każdego klucza w danym momencie czasu. KTable może być używany do wykonywania operacji agregujących, filtrowania i łączenia danych.

Podsumowując, KStream reprezentuje strumień zdarzeń, natomiast KTable reprezentuje aktualny stan danych w czasie i jest używany do agregowania, filtrowania i łączenia danych.