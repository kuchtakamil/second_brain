# MCP server prompt

**Data:** 2025-09-20

---

**User:**

Jestem programistą z 10 letnim stażem więc odpowiadaj w sposób techniczny i szczegółowy.
Napisz mi prompt po angielsku dla narzędzia deweloperskiego wspomaganego przez AI, które utworzy prosty serwer MCP dla PostgreSQL i jednej dedykowanej bazy danych. 

Baza danych nazywa się perfumarket. Schemat bazy zostanie dostarczony dodatkowo do prompta który wygenerujesz.

To ma być projekt edukacyjny. Chcę się dowiedzieć jak najwięcej o MCP, tym mechaniźmie i jak trzeba go obsługiwać.

Chcę użyć Python i najbardziej popularnych frameworków / bibliotek dla Python i AI.

---

**Assistant:**

Oto gotowy prompt w języku angielskim, który możesz wykorzystać w narzędziu deweloperskim wspomaganym przez AI. Jest przygotowany w taki sposób, żeby generowało projekt edukacyjny prostego MCP-serwera obsługującego PostgreSQL i dedykowaną bazę danych **perfumarket**.  

---

**Prompt (English):**

```
Create an educational Python project that implements a simple MCP (Model Context Protocol) server for PostgreSQL.  
The server should be able to connect to a dedicated PostgreSQL database named `perfumarket`.  

The database schema will be provided separately and must be applied to the project.  

Requirements:  
1. Programming language: Python 3.11+  
2. Use popular frameworks and libraries from the Python ecosystem:
   - `psycopg2` or `asyncpg` for PostgreSQL communication  
   - `FastAPI` or `Flask` for server implementation  
   - `pydantic` for data validation  
   - Optionally `SQLAlchemy` for ORM support  
   - AI/LLM integration should rely on `openai`, `langchain`, or `llama-index` to demonstrate how MCP servers can be combined with AI assistants.  
3. The MCP server should expose:
   - Connection initialization to the `perfumarket` database  
   - Basic CRUD operations on the provided schema  
   - An interface (via MCP protocol) to query the database and retrieve structured results  
4. Provide detailed comments in the code explaining:
   - What MCP is and how it works  
   - How this MCP server communicates with the database  
   - How to extend the server with new tools or queries  
   - How the AI assistant (client) would consume and interpret the MCP server responses  
5. Provide a minimal client example that connects to the MCP server, runs a query against the `perfumarket` database, and returns the results in JSON.  
6. Add setup instructions in `README.md`, including:
   - How to install dependencies  
   - How to set up PostgreSQL locally and create the `perfumarket` database  
   - How to run migrations using the provided schema  
   - How to start the MCP server and test it with the minimal client.  

The goal is to build an educational example showing how to integrate MCP with Python, PostgreSQL, and AI frameworks in a clear and extendable way.  
```

---

Chcesz, żebym od razu przygotował też **schemat struktury projektu** (np. podział katalogów, pliki, przykładowy `main.py`, `requirements.txt`, `README.md`), żeby łatwiej było to wygenerować i rozszerzać?