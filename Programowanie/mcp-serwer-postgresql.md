# MCP serwer PostgreSQL

**Data:** 2025-09-20

---

**User:**

Model Context Protocol - MCP. Niby rozumiem co to jest ale chcę poznać techniczne szczegóły. Weźmy serwer MCP dla PostgreSQL. Zgaduję że taki serwer to kod w którym są zmapowane opisy działań do zapytań SQL. Powiedz czy to prawda.
A LLM korzystający z takiego MCP wie jaką listę zadań on może wykonać i kiedy tego potrzebuje, wywołuje jakieś zadanie na MCP. Czy to prawda?
Jeśli tak to czym wywołuje, requestem http?

---

**Assistant:**

Dobrze rozumiesz ogólną ideę, ale dopytajmy szczegóły techniczne.  

### Czym jest Model Context Protocol (MCP)?
MCP to **protokół komunikacji między LLM a tzw. "serwerami kontekstu"**, czyli komponentami, które udostępniają LLM-owi określone narzędzia, dane czy zdolności (np. dostęp do bazy danych, API, repozytorium kodu).  
Serwer MCP wystawia **opis dostępnych akcji (resources, tools, prompts)**, a klient MCP (np. aplikacja integrująca LLM) może je wykorzystywać.  

### MCP serwer dla PostgreSQL
Twoje przypuszczenie jest trafne:  
- taki serwer zawiera kod, który **mapuje nazwane akcje** (np. "query", "insert", "list tables") na konkretne zapytania SQL.  
- to **serwer MCP** decyduje, jakie operacje wystawi i jak przetłumaczy je na SQL – LLM nie generuje "gołego SQL-a" bezpośrednio, tylko woła akcje opisane w MCP.  

### Skąd LLM wie co może zrobić?
- Serwer MCP udostępnia **manifest (opis)** tego, jakie akcje/metody/resources są dostępne i jakie parametry przyjmują.  
- LLM (lub klient MCP) może zapytać serwer o listę narzędzi i wtedy wie np., że istnieje akcja `query(sql: string)` albo `list_tables()`.  

### Jak wygląda wywołanie?
- MCP nie jest "protokół = HTTP", tylko używa **JSON-RPC 2.0** (czyli komunikacja przez wiadomości JSON z określonym formatem `method`, `params`, `id`).  
- Transportem może być:  
  - **stdio** (LLM uruchamia proces MCP i gada po stdin/stdout),  
  - **sockety/unix domain sockets**,  
  - ewentualnie HTTP/WebSocket, jeśli ktoś tak zaimplementuje, ale nie jest to obowiązkowe.  

### Schemat:
1. LLM (klient MCP) odpytuje serwer o capabilities (co potrafisz?).  
2. Serwer MCP odsyła opis narzędzi/resources.  
3. Kiedy w rozmowie LLM potrzebuje np. sprawdzić dane w PostgreSQL, generuje wywołanie narzędzia (np. `query`) zgodnie z kontraktem MCP.  
4. Klient MCP zamienia to na request JSON-RPC do serwera MCP.  
5. Serwer MCP wykonuje SQL i zwraca wynik jako JSON.  

Czy chcesz, żebym pokazał Ci **przykładowy JSON-RPC request/response** do serwera MCP dla PostgreSQL, żeby to zobaczyć bardziej "na drutach"?

---

**User:**

Odpowiadaj w sposób bardzo techniczny.
Czyli to nie sam LLM wywołuje MCP tylko musi to zrobić aplikacja współpracująca z LLM?

---

**Assistant:**

Tak, dokładnie. Sam LLM **nie umie otworzyć gniazdka ani puścić JSON-RPC** – on tylko generuje tekst.  
Wywołanie MCP musi obsłużyć **aplikacja-pośrednik (klient MCP)**, która:  

1. **Ładuje model LLM** (np. przez OpenAI API, Ollama, cokolwiek).  
2. **Uruchamia proces MCP serwera** (np. `postgres-mcp-server`) – przez `stdio` albo łączy się socketem.  
3. **Odpytuje serwer MCP o manifest** (`initialize`, `list_tools`, `list_resources`).  
4. **Podaje LLM-owi opis narzędzi** w kontekście (np. w system prompt albo przez struktury typu "function calling").  
5. Kiedy LLM w odpowiedzi zasugeruje użycie narzędzia (`call tool: query(...)`), aplikacja:  
   - parsuje to,  
   - buduje request JSON-RPC zgodny z MCP,  
   - wysyła go do serwera MCP,  
   - odbiera wynik,  
   - i dopiero potem wstrzykuje wynik do konwersacji z LLM.  

---

### Minimalny przepływ (JSON-RPC over stdio)

**Klient MCP (aplikacja) → serwer MCP:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "call_tool",
  "params": {
    "name": "query",
    "arguments": {
      "sql": "SELECT id, name FROM users LIMIT 5"
    }
  }
}
```

**Serwer MCP → klient:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "rows": [
      { "id": 1, "name": "Alice" },
      { "id": 2, "name": "Bob" }
    ]
  }
}
```

**Klient MCP → LLM:**
```
Wynik zapytania:
id | name
1  | Alice
2  | Bob
```

---

Czyli:  
- **LLM nie ma połączenia z MCP**.  
- **Aplikacja** jest tym, co rozumie oba światy: potrafi gadać z MCP (JSON-RPC) i z LLM (prompt/fc).  

Chcesz, żebym rozpisał dokładnie jak wygląda **sekcja manifestu MCP serwera PostgreSQL** (czyli opis narzędzi i parametrów), żebyś zobaczył jak LLM dowiaduje się, co jest dostępne?