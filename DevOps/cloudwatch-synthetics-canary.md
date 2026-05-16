# Amazon CloudWatch Synthetics (Canaries)

Amazon CloudWatch Synthetics to usługa pozwalająca na tworzenie tzw. "kanarków" (canaries) – lekkich, konfigurowalnych skryptów (np. w Node.js lub Python), które uruchamiane są automatycznie zgodnie z zadanym harmonogramem. Ich głównym zadaniem jest symulowanie ścieżek i zachowań użytkownika – nawigowanie po aplikacjach webowych, klikanie w przyciski czy wywoływanie punktów końcowych API. Służy to do ciągłego monitorowania dostępności, wydajności oraz poprawnego działania systemów z zewnątrz.

## Dlaczego to jest ważne i kiedy ma zastosowanie?

Tradycyjny monitoring infrastruktury opiera się na metrykach takich jak użycie procesora, pamięci czy analiza logów serwerowych (podejście Inside-Out). Z kolei CloudWatch Synthetics działa w podejściu Outside-In (z perspektywy klienta końcowego). Pozwala to na proaktywne wykrycie problemów z interfejsem użytkownika, wolnym ładowaniem stron czy psującymi się przepływami biznesowymi (np. proces logowania lub finalizacji zamówienia), zanim awarię odczują lub zgłoszą rzeczywiści klienci. 

Stosuje się to m.in. wtedy, gdy:
- Chcesz zapewnić dostępność i ciągłość działania kluczowych funkcji (np. płatności w e-commerce).
- Wymagasz natychmiastowego powiadomienia, jeśli wdrożenie nowej wersji aplikacji przypadkowo zepsuje kluczową zakładkę.
- Chcesz monitorować złożone mikroserwisy lub API ukryte za bramką.

## Jak działają kanarki?

1. **Uruchamianie skryptów:** Skrypty wykonywane są w bezpiecznym, specjalnie przygotowanym środowisku (często używającym bezgłowych przeglądarek internetowych, takich jak Puppeteer lub Selenium).
2. **Wykorzystanie szablonów (Blueprints):** AWS dostarcza gotowe szablony do popularnych zadań, co upraszcza wdrożenie. Można z łatwością uruchomić:
   - "Heartbeat" – regularne odpytywanie adresu URL w celu sprawdzenia, czy zwraca kod HTTP 200 OK.
   - Sprawdzanie niedziałających linków (Broken link checker) – pełzanie po aplikacji w poszukiwaniu ślepych zaułków i błędów 404.
   - Testowanie API – weryfikowanie czasów odpowiedzi oraz struktury danych zwracanych przez REST API.
   - Testy przepływów UI (GUI workflow builder) – krok po kroku automatyzowane przejście przez interfejs webowy (logowanie, dodanie do koszyka).
3. **Analiza awarii:** Kiedy kanarek zakończy się błędem, CloudWatch Synthetics automatycznie zapisuje użyteczne artefakty:
   - Zrzuty ekranu (Screenshots) z momentu przed awarią i w trakcie jej trwania.
   - Pliki HAR (HTTP Archive) obrazujące czasy ładowania poszczególnych zasobów sieciowych na stronie.
   - Logi z wykonania testu.
   - Zestawienie metryk sukcesu, błędów i czasu trwania, podłączone do usług powiadomień (np. SNS) wyzwalających alarm dla zespołu DevOps.

## Główne korzyści z używania CloudWatch Synthetics

- **Zrozumienie błędu z perspektywy UI:** Zrzuty ekranu i pliki HAR drastycznie ułatwiają szybkie diagnozowanie przyczyn awarii w aplikacjach przeglądarkowych.
- **Monitoring wewnątrz VPC:** Kanarki potrafią zostać uruchomione w obrębie Twojej wirtualnej chmury prywatnej (Virtual Private Cloud). Umożliwia to stałe monitorowanie wewnętrznych aplikacji i interfejsów API, które w ogóle nie są wystawione do publicznego Internetu.
- **Natychmiastowe alerty o degradacji usług:** Połączenie z CloudWatch Alarms pozwala na bezproblemową integrację np. z PagerDuty, Slackiem i kanałami reagowania na incydenty.
