# Lokalna zależność w Gradle

**Data:** 2023-06-20

---

**User:**

w projekcie korzystającym z gradle mam zależność która jest ściągana jest ściągana ze zdalnego repo. Teraz chciałbym zbudować tę zależność lokalnie u siebie na komputerze i przestawić ustawienia tak aby aplikacja korzystała z lokalnej zależności a nie ze zdalnej. Czy to jest możliwe?

---

**Assistant:**

Tak, jest możliwe zbudowanie zależności lokalnie i skonfigurowanie projektu tak, aby korzystał z lokalnej wersji zamiast ściągać ją ze zdalnego repozytorium. Oto kilka kroków, które możesz podjąć, aby to osiągnąć:

1. Zainstaluj zależność lokalnie: Jeśli masz kod źródłowy zależności, możesz go zbudować lokalnie i zainstalować w swoim lokalnym repozytorium Maven lub Gradle. Możesz użyć polecenia `gradle install` w katalogu z kodem źródłowym zależności. Upewnij się, że zainstalowana wersja ma unikalny identyfikator grupy, nazwę i numer wersji.

2. Skonfiguruj projekt Gradle: Otwórz plik `build.gradle` w projekcie i zaktualizuj sekcję `dependencies`. Zamiast zdalnej zależności, dodaj zależność od lokalnego repozytorium. Na przykład, jeśli używasz MavenLocal jako lokalnego repozytorium, dodaj coś takiego:

   ```groovy
   repositories {
       mavenLocal()
       // Pozostałe repozytoria zdalne
   }

   dependencies {
       // Inne zależności
       implementation 'nazwa.grupy:nazwa-zaleznosci:wersja'
   }
   ```

   Upewnij się, że podajesz poprawną nazwę grupy, nazwę zależności i numer wersji dla lokalnej zależności, którą zbudowałeś i zainstalowałeś w kroku 1.

3. Zbuduj projekt: Uruchom polecenie `gradle build` w katalogu projektu, aby zbudować projekt i zaktualizować zależności.

Po wykonaniu tych kroków, Twój projekt Gradle będzie korzystał z lokalnej wersji zależności zamiast pobierać ją ze zdalnego repozytorium. Upewnij się, że masz zainstalowaną i zbudowaną najnowszą wersję lokalnej zależności przed uruchomieniem projektu.