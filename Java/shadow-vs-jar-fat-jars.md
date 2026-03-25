# Shadow vs Jar: Fat JARs

**Data:** 2024-02-13

---

**User:**

Dlaczego w gradle powinienem używać johnrengelman/shadow for creating fat/uber JARs gdy dostępny jest plugin wbudowany o nazwie jar?

---

**Assistant:**

Plugin Gradle o nazwie "jar" służy do tworzenia standardowych plików JAR, które zawierają tylko kod źródłowy i zasoby z projektu, ale nie zawierają zależności. Natomiast plugin "johnrengelman/shadow" (Shadow) umożliwia tworzenie tzw. "fat" lub "uber" JAR, które są jednym plikiem JAR zawierającym zarówno kod źródłowy i zasoby z projektu, jak i wszystkie zależności.

Istnieje kilka powodów, dla których może być preferowane użycie pluginu Shadow do tworzenia fat JAR zamiast wbudowanego pluginu "jar":

1. **Samowystarczalność:** Fat JAR stworzony przy użyciu pluginu Shadow jest samowystarczalny, co oznacza, że ​​może być uruchamiany bezpośrednio bez potrzeby dostępu do oryginalnych zależności. Jest to przydatne w przypadku przenoszenia aplikacji na inne środowisko, gdzie nie są dostępne te same zależności.

2. **Prostota dystrybucji:** Dzięki fat JAR, dystrybucja aplikacji staje się łatwiejsza, ponieważ wszystkie zależności są zawarte w jednym pliku. To ułatwia przesyłanie aplikacji między różnymi środowiskami i uruchamianie jej bez konieczności pobierania zależności z zewnętrznych źródeł.

3. **Zarządzanie klasami:** Plugin Shadow automatycznie rozwiązuje potencjalne konflikty klas między różnymi zależnościami poprzez przesuwanie je do różnych pakietów lub zmianę nazw klas. Pozwala to na uniknięcie problemów związanych z konfliktami nazw klas podczas uruchamiania aplikacji.

4. **Wsparcie dla pluginów:** Shadow oferuje różne funkcje, takie jak zintegrowane wsparcie dla wielu pluginów, dzięki którym możesz zoptymalizować kod, zasoby i inne aspekty Twojej aplikacji podczas procesu budowania.

Podsumowując, choć wbudowany plugin "jar" w Gradle jest przydatny do standardowego tworzenia plików JAR, to plugin Shadow dostarcza dodatkowych funkcji i ułatwień, zwłaszcza jeśli chodzi o zarządzanie zależnościami i tworzenie samowystarczalnych fat JARów. Decyzja o użyciu jednego lub drugiego pluginu zależy od konkretnych wymagań i potrzeb projektu.