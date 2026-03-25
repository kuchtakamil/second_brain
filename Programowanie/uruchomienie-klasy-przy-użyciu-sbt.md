# Uruchomienie klasy przy użyciu sbt.

**Data:** 2023-05-06

---

**User:**

Projekt składa się z wielu modułów. W kilku modułach znajdują się klasy przeznaczone do uruchomienia czyli z def main. 
Jak przy użyciu sbt runMain można uruchomić klasę o nazwie DevMain znajdujący się w module sensor-simulator

---

**Assistant:**

Aby uruchomić klasę o nazwie DevMain znajdującą się w module sensor-simulator przy użyciu sbt runMain, należy wykonać następujące kroki:

1. Otwórz konsolę systemową.
2. Przejdź do katalogu głównego projektu, w którym znajduje się plik build.sbt.
3. Uruchom sbt, wpisując w konsoli polecenie "sbt".
4. Zaczekaj, aż sbt wczyta wszystkie zależności i wyświetli wiersz poleceń.
5. Wpisz polecenie "project sensor-simulator", aby przełączyć się do modułu sensor-simulator.
6. Wpisz polecenie "runMain DevMain", aby uruchomić klasę DevMain z modułu sensor-simulator.

Po wykonaniu powyższych kroków sbt powinien skompilować i uruchomić klasę DevMain z modułu sensor-simulator.

---

**User:**

To rozwiązanie w sesyjnym trybie działania sbt działa. A czy można to samo wykonać w trybie batchowym czyli w jednym poleceniu w stylu 
sbt project sensor-simulator runMain DevMain?

---

**Assistant:**

Tak, można to wykonać w trybie batchowym, czyli poprzez jedno polecenie w stylu `sbt "project sensor-simulator" "runMain DevMain"`. 

Powyższe polecenie uruchomi projekt `sensor-simulator` i następnie klasę `DevMain` w trybie wsadowym, co pozwoli uniknąć konieczności interakcji z konsolą sbt.

Warto jednak zauważyć, że w przypadku bardziej złożonych projektów, które wymagają wczytania wielu zależności i przetwarzają dużo danych, uruchamianie ich w trybie wsadowym może zajmować więcej czasu i zasobów niż w trybie sesyjnym.