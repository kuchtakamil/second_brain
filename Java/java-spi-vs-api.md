# Java SPI vs API

**Data:** 2024-10-21

---

**User:**

W kontekście języka Java, czym jest SPI? Możesz na końcu porównać SPI i API

---

**Assistant:**

W kontekście języka Java, **SPI** (Service Provider Interface) to mechanizm umożliwiający rozszerzanie funkcjonalności aplikacji lub bibliotek poprzez dostarczanie różnych implementacji usług. Jest to wzorzec projektowy używany często w bibliotekach i frameworkach, który pozwala twórcom aplikacji na dostarczanie własnych wersji usług bez konieczności modyfikowania kodu źródłowego biblioteki. **SPI** jest szczególnie przydatne, gdy chcemy umożliwić łatwe dodawanie nowych dostawców (ang. *providers*) lub komponentów do istniejącego systemu.

### Jak działa SPI?
1. **Definicja interfejsu usługi**: Tworzymy interfejs, który opisuje usługę, np. `public interface PaymentService { void processPayment(); }`.
2. **Implementacje usługi**: Dostawcy usług (ang. *service providers*) implementują ten interfejs zgodnie z własnymi potrzebami, np. `class PayPalPaymentService implements PaymentService { /* implementacja */ }`.
3. **Deklaracja usług**: Implementacje są rejestrowane w pliku konfiguracyjnym, który Java odnajduje za pomocą mechanizmu klas, np. w katalogu `META-INF/services/` znajduje się plik o nazwie zgodnej z pełną nazwą interfejsu (np. `META-INF/services/com.example.PaymentService`), a jego zawartością jest nazwa klasy implementującej usługę.
4. **Załadowanie usług**: Java dostarcza klasę `ServiceLoader`, która umożliwia ładowanie i iterowanie po dostępnych implementacjach usług. Przykład:
   ```java
   ServiceLoader<PaymentService> loader = ServiceLoader.load(PaymentService.class);
   for (PaymentService service : loader) {
       service.processPayment();
   }
   ```

### Zastosowania SPI
SPI jest często stosowane w bibliotekach takich jak:
- **JDBC** (Java Database Connectivity), gdzie różni dostawcy baz danych (np. MySQL, PostgreSQL) dostarczają swoje implementacje interfejsu.
- **Java Cryptography Architecture** (JCA), gdzie różne algorytmy kryptograficzne są implementowane przez różnych dostawców.

### Różnice między API a SPI

1. **API (Application Programming Interface)**: Zestaw interfejsów, metod i klas, które udostępnia aplikacja lub biblioteka, aby inne aplikacje mogły się z nią komunikować. API definiuje, *jak* korzystać z funkcji aplikacji lub biblioteki.
   - Przykład: Interfejs `List` w Java Collection Framework.

2. **SPI (Service Provider Interface)**: Zestaw interfejsów, które umożliwiają dostarczanie *implementacji* usług przez różne moduły lub dostawców. SPI definiuje, *jak* tworzyć nowe rozszerzenia lub implementacje usługi.
   - Przykład: `JDBC Driver` to implementacja interfejsu SPI dostarczana przez dostawcę bazy danych.

### Podsumowanie
- **API** to umowa między twórcą biblioteki a jej użytkownikiem, która określa, jak korzystać z biblioteki.
- **SPI** to mechanizm rozszerzania funkcjonalności systemu, który umożliwia dostarczanie różnych implementacji usług przez zewnętrznych dostawców.

W skrócie: API jest używane przez programistów do korzystania z funkcji, natomiast SPI jest używane przez dostawców, aby dostarczyć własne implementacje funkcji.