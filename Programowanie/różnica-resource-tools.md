# Różnica Resource Tools

**Data:** 2025-09-24

---

**User:**

w kontekście serwerów MCP podaj różnicę między Resource a Tools. Możesz podać przykład

---

**Assistant:**

W kontekście **MCP (Model Context Protocol)**:  

- **Resource** – to źródło danych, które model może odczytać lub do którego może się odwołać. Zwykle są to rzeczy statyczne lub pół-statyczne, np. plik, baza wiedzy, dokumentacja API, repozytorium kodu, baza danych. Model nie „wywołuje” Resource, tylko ma do niego dostęp (np. do odczytu treści).  
  👉 Możesz o tym myśleć jak o „danych wejściowych” lub „kontekście”, który serwer MCP udostępnia modelowi.  

- **Tool** – to funkcja/operacja, którą model może wywołać. To aktywne możliwości serwera MCP – coś, co model uruchamia, przekazuje parametry i dostaje wynik.  
  👉 Możesz o tym myśleć jak o „akcji”, a nie o „danych”.  

### Przykład  
Wyobraź sobie serwer MCP integrujący się z systemem do zarządzania zadaniami:  

- **Resource**: lista zadań w bazie (np. `tasks.json`, albo endpoint udostępniający aktualny stan zadań). Model może przeczytać aktualne zadania i statusy, ale sam ich nie zmienia bezpośrednio.  
- **Tool**: funkcje takie jak `createTask(title, description)` albo `updateTaskStatus(taskId, status)`. Model może wywołać te narzędzia, żeby dodać nowe zadanie lub zmienić status istniejącego.  

Chcesz, żebym przygotował prosty schemat (np. w ASCII albo mermaid) pokazujący różnicę między Resource a Tool?