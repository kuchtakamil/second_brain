# Serwery MCP i dokumentacja

**Data:** 2026-01-23

---

**User:**

Servery MCP które umożliwiają wgląd w aktualną dokumentację frameworków

---

**Assistant:**

Poniżej znajdziesz przegląd **serwerów Model Context Protocol (MCP)**, które — poprzez protokół MCP — umożliwiają dostęp do **aktualnej dokumentacji i wiedzy o frameworkach, API i zasobach developerskich**. MCP to otwarty standard służący do łączenia asystentów AI z zewnętrznymi źródłami danych i narzędziami. citeturn0search1

---

## 1. Microsoft Learn Docs MCP Server  
**Cel:** Dostęp do **oficjalnej i aktualnej dokumentacji Microsoft Learn**, w tym dokumentacji .NET, Azure, Microsoft 365, API, przykładów kodu i najlepszych praktyk.  
**Zastosowanie:** Gdy chcesz, aby AI korzystało z najnowszych dokumentów Microsoft podczas pracy z frameworkami takimi jak ASP.NET Core, Entity Framework, Azure SDK itp.  
**Endpoint:** `https://learn.microsoft.com/api/mcp`  
**Fonctionalności:** semantyczne wyszukiwanie dokumentów, pobieranie przykładów kodu i API reference. citeturn0search5turn0search7

---

## 2. AWS Knowledge MCP Server  
**Cel:** Umożliwia agentowi AI dostęp w czasie rzeczywistym do **aktualnej wiedzy o usługach AWS** — dokumentacji, przewodników architektonicznych, kodów źródłowych i API reference.  
**Zastosowanie:** Praca z dokumentacją AWS (CloudFormation, CDK, Amplify itd.) na potrzeby tworzenia i debugowania aplikacji w chmurze.  
**Funkcje:** przegląd dokumentów, przykłady kodu, dostęp do informacji o regionach i usługach AWS. citeturn0search0

---

## 3. AWS Documentation MCP Server  
**Cel:** Specjalna implementacja serwera MCP oferująca narzędzia do **szukania i pobierania stron dokumentacji AWS**, konwersji ich do formatu markdown oraz rekomendacji podobnych treści.  
**Zastosowanie:** Gdy potrzebujesz przeszukiwać dokumentację AWS programowo lub udostępniać ją agentom AI w kontekście projektów.  
**Funkcje:** `read_documentation`, `search_documentation`, `recommend`. citeturn0search9

---

## 4. MCP Documentation Server (PyPI / lokalny)  
**Cel:** Serwer MCP do **lokalnego hostowania technicznej dokumentacji** (plików .md/.txt) z możliwością semantycznego wyszukiwania w treści.  
**Zastosowanie:** Gdy chcesz, aby LLM miał kontekst w dokumentacji projektowej, wewnętrznych frameworków lub wiki zespołu.  
**Funkcje:** wyszukiwanie semantyczne, listowanie dokumentów, usuwanie i przegląd treści. citeturn0search14

---

## 5. MCP Docs Server – projekt open source  
**Cel:** Lekki serwer MCP, który udostępnia zawartość pliku `context.md` jako kontekst dla klienta MCP.  
**Zastosowanie:** Idealne do szybkiego wdrożenia dokumentacji projektu lub specyfikacji w formacie markdown jako źródła wiedzy dla AI.  
**Funkcje:** `get_context_overview()` i `search_context(query)` — operacje proste, ale skuteczne przy mniejszych dokumentacjach. citeturn0search2

---

## 6. Salesforce i inne MCP serwery specjalne  
Oprócz powyższych istnieją także **branżowe i platformowe serwery MCP**, przykładowo w Salesforce — które oferują integracje MCP do narzędzi programistycznych i danych platformowych (np. **Salesforce DX MCP Server**). citeturn0search16

---

## 7. Rejestry i zasoby MCP  
Jeżeli chcesz zobaczyć **szerszy katalog serwerów MCP**, możesz przeglądać repozytoria i rejestry projektów:  
- **modelcontextprotocol/servers** – oficjalne i referencyjne serwery MCP (GitHub). citeturn0search4

---

## Podsumowanie — typy serwerów MCP wg. zastosowania

| Serwer MCP | Źródło dokumentacji | Użycie praktyczne |
|------------|--------------------|------------------|
| **Microsoft Learn Docs MCP Server** | Oficjalna dokumentacja Microsoft Learn | .NET, Azure, Microsoft 365 |
| **AWS Knowledge MCP Server** | AWS docs, przykłady, architektura | AWS API, CloudFormation, CDK |
| **AWS Documentation MCP Server** | AWS docs + search | Programowe pobieranie i analiza treści |
| **MCP Documentation Server** | Własna dokumentacja projectowa | Lokalna, projekty wewnętrzne |
| **MCP Docs Server (context.md)** | Dokumentacja w markdown | Proste repozytoria projektowe |

---

## Jak ich używać
1. **Dodaj serwer MCP do konfiguracji klienta MCP** (np. Claude Desktop, Cursor, VS Code). citeturn0search1  
2. **Skonfiguruj transport (HTTP/stdio)** zgodnie z obsługą klienta. citeturn0search1  
3. **Używaj narzędzi MCP** (np. wyszukiwanie dokumentów, pobieranie treści) w zapytaniach LLM.

---

Jeśli chcesz, mogę przygotować **praktyczny przykład konfiguracji MCP w Twoim środowisku (np. z Claude Desktop lub VS Code)** lub wskazać **gotowe adresy publicznych MCP endpoints** dla tych serwerów. Napisz, którą technologię/framework chcesz dokumentować przez MCP.