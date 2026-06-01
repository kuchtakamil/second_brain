# Model Context Protocol (MCP) – Wywiad na AI Engineera

Model Context Protocol (MCP) to otwarty standard stworzony przez Anthropic, który ujednolica sposób, w jaki modele AI (klient) komunikują się z zewnętrznymi źródłami danych i narzędziami (serwer).

Poniżej znajduje się lista kluczowych zagadnień, które powinieneś znać na rozmowę kwalifikacyjną, przedstawiona w formie zwięzłych punktów (bez głębokiego wchodzenia w szczegóły).

## 1. Kluczowe pojęcia i architektura MCP

*   **Architektura Klient-Serwer**: Zrozumienie podziału ról. **MCP Host/Client** (np. aplikacja AI, Claude Desktop, Cursor) inicjuje połączenie i komunikuje się z LLMem. **MCP Server** udostępnia lokalne lub zdalne zasoby i narzędzia.
*   **Warstwy transportowe**: Znajomość sposobów komunikacji między klientem a serwerem. Obecnie najpopularniejsze to:
    *   **stdio**: komunikacja przez standardowe wejście/wyjście (najczęściej lokalne procesy).
    *   **SSE (Server-Sent Events) / HTTP**: komunikacja sieciowa (zdalne serwery).
*   **Trzy główne prymitywy (Capabilities) MCP**:
    *   **Resources (Zasoby)**: Umożliwiają serwerowi udostępnianie danych do odczytu dla modelu (np. pliki konfiguracyjne, logi, schematy baz danych). Są to dane, które model może pobrać.
    *   **Tools (Narzędzia)**: Funkcje, które model może wywołać, aby wykonać określoną akcję (np. modyfikacja pliku, wykonanie zapytania SQL, wywołanie zewnętrznego API). Różnica w stosunku do Resources polega na tym, że narzędzia często modyfikują stan i wymagają argumentów.
    *   **Prompts (Szablony promptów)**: Predefiniowane i parametryzowane szablony instrukcji udostępniane przez serwer.
*   **Decoupling (Rozprzęgnięcie)**: Zrozumienie głównego celu MCP, jakim jest oddzielenie kodu aplikacji AI (klienta) od integracji z konkretnymi danymi (serwera).

## 2. Implementacja i bezpieczeństwo

*   **SDK**: Świadomość istnienia oficjalnych bibliotek (Python, TypeScript) ułatwiających budowę serwerów i klientów MCP.
*   **Bezpieczeństwo**: MCP zakłada, że klient jest w domyśle środowiskiem niezaufanym. To serwer MCP powinien implementować mechanizmy uwierzytelniania, autoryzacji oraz ostro ograniczać zasięg działania narzędzi i zasobów (np. dostęp tylko do jednego wybranego folderu, tzw. *sandboxing*).
*   **Cykl życia połączenia**: Fazy inicjalizacji (handshake), negocjacji możliwości (capabilities negotiation - serwer mówi, co potrafi) oraz standardy obsługi błędów.

## 3. Różnica między MCP a standardowym Tool Callingiem

To jedno z najważniejszych pytań, pokazujące zrozumienie ewolucji architektury agentowej.

*   **Standardowy Tool Calling (Function Calling)**:
    *   **Zasada działania**: Aplikacja kliencka musi zdefiniować schemat narzędzia (np. JSON Schema), wysłać go do LLMa, a gdy model odpowie chęcią jego użycia, aplikacja **samodzielnie wykonuje logikę tego narzędzia** w swoim własnym kodzie.
    *   **Wady (Tight coupling)**: Integracja każdego nowego narzędzia lub usługi (np. GitHub, Jira, SQLite) wymaga napisania nowego kodu w aplikacji klienckiej. 
*   **Model Context Protocol (MCP)**:
    *   **Zasada działania (Plug-and-play)**: Aplikacja kliencka łączy się z serwerem MCP. Serwer dynamicznie zgłasza dostępne schematy narzędzi, które klient przekazuje do LLMa. Kiedy model prosi o użycie narzędzia, aplikacja kliencka nie wykonuje go u siebie, lecz wysyła żądanie wykonania (RPC) **do serwera MCP**. Serwer przetwarza żądanie i odsyła wynik.
    *   **Zalety**: Klient jest w pełni niezależny od implementacji narzędzi. Serwer MCP dla GitHuba raz napisany, może być natychmiast użyty przez Cursora, Claude Desktop czy Twojego autorskiego agenta bez żadnych modyfikacji w kodzie klienta.

**Podsumowanie**: **Tool calling** to wewnętrzna mechanika modelu (zdolność LLMa do zrozumienia schematu i poproszenia o wywołanie funkcji). **MCP** to zestandaryzowany protokół infrastrukturalny określający, jak aplikacje AI mają na dużą skalę odkrywać takie funkcje, wywoływać je na zewnętrznych serwerach i ujednolicać przepływ kontekstu.

## 4. Schemat komunikacji: Klient MCP, Serwer MCP a LLM

Najważniejszą rzeczą do zapamiętania jest to, że **LLM nigdy nie komunikuje się bezpośrednio z Serwerem MCP**. Zawsze robi to za pośrednictwem Klienta MCP (aplikacji AI).

*   **LLM (Mózg)**: Analizuje intencję użytkownika, decyduje, czy użyć narzędzia i prosi o jego wywołanie.
*   **MCP Client (Pośrednik)**: Aplikacja z którą wchodzi w interakcję użytkownik (np. Twój skrypt Python, Cursor). To on orkiestruje cały proces – rozmawia i z LLMem (przez API modelu) i z Serwerem MCP (przez protokół MCP).
*   **MCP Server (Wykonawca)**: Czeka na polecenia od Klienta. Wykonuje kod i zwraca surowe dane.

### Analiza komunikacji krok po kroku (np. zadanie "Podsumuj mój plik log.txt"):

1.  **Odkrywanie (Klient -> Serwer)**: Klient MCP pyta Serwera: "Jakie narzędzia oferujesz?". Serwer zwraca listę, np. narzędzie `read_file` wraz z jego schematem (jakich argumentów wymaga).
2.  **Kontekstualizacja (Klient -> LLM)**: Klient wysyła do LLMa prompt użytkownika ("Podsumuj plik log.txt") oraz listę dostępnych narzędzi pobraną od serwera (zwykły standardowy Tool Calling dla LLMa).
3.  **Decyzja (LLM -> Klient)**: LLM decyduje: "Nie znam zawartości, muszę użyć narzędzia. Zwracam żądanie: wywołaj `read_file` z argumentem `path='log.txt'`".
4.  **Egzekucja (Klient -> Serwer)**: Klient odbiera to żądanie, parsuje je i wysyła komendę przez protokół MCP do Serwera: "Wykonaj `read_file` ('log.txt')".
5.  **Wynik (Serwer -> Klient)**: Serwer odczytuje plik z dysku i zwraca jego treść (string) do Klienta.
6.  **Domknięcie pętli (Klient -> LLM)**: Klient wysyła kolejną wiadomość do LLMa: "Oto wynik działania narzędzia, o które prosiłeś: [treść log.txt]".
7.  **Odpowiedź końcowa (LLM -> Klient)**: LLM analizuje treść pliku i generuje dla użytkownika ładne podsumowanie na czacie.

## 5. Integracja MCP w architekturze aplikacji AI

Gdy tworzysz własnego agenta AI i chcesz zintegrować obsługę MCP (np. z użyciem frameworków takich jak LangChain lub czystego kodu), architektonicznie wygląda to następująco:

*   **Zarządzanie cyklem życia**: Twoja aplikacja (Klient) musi zainicjować i utrzymywać połączenie z Serwerem MCP. Jeśli jest to lokalny serwer (transport `stdio`), Twój kod musi uruchomić proces serwera w tle (np. poprzez komendę `npx` dla paczek NPM lub `python -m` dla paczek Pythona).
*   **Kto kogo wywołuje w kodzie?**:
    1.  Twój kod (Klient) używa SDK MCP (np. pakiet `mcp` w Pythonie), aby nawiązać sesję.
    2.  Wywołujesz asynchroniczną metodę `session.list_tools()`.
    3.  Pobraną listę konwertujesz na format akceptowany przez Twój model (np. schemat funkcji dla `gpt-4o`).
    4.  Wywołujesz API OpenAI/Anthropic, przekazując `tools`.
    5.  Kiedy API zwróci odpowiedź typu `tool_calls`, to Twój kod używa pętli do iteracji po tych żądaniach.
    6.  Dla każdego żądania wywołujesz `session.call_tool(nazwa, argumenty)` na serwerze MCP.
    7.  Pobierasz odpowiedź z serwera, dodajesz ją do historii wiadomości jako rolę "tool" (lub "function") i znów wywołujesz API LLMa, przekazując nowy kontekst.

Dzięki takiej integracji, zamiast pisać na nowo dziesiątki funkcji integrujących Twoją aplikację z GitHubem, Notion czy bazą PostgreSQL, Twój skrypt po prostu pobiera listę narzędzi z odpowiedniego Serwera MCP i pozwala modelowi ich używać w sposób w pełni ustandaryzowany.
