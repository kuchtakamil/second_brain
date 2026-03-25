# Komunikacja z LLM w LangChain

**Data:** 2025-09-25

---

**User:**

LangChain oferuje kilka sposobów komunikacji aplikacji z LLM. Objaśnij te sposoby. Najbardziej interesuje mnie spsoób gdy LLM odpowiada w sposób strumieniowy. Wyjaśnij szczegółowo i technicznie. Przeszukaj internet jeśli trzeba i dokumentację LangChain.

---

**Assistant:**

# Sposoby komunikacji aplikacji z LLM w LangChain — przegląd
Krótko: LangChain udostępnia kilka modeli komunikacji między aplikacją a LLM, które można ze sobą łączyć:

1. **Bezpośrednie wywołanie (sync / async)** — wywołujesz LLM/ChatModel i dostajesz cały wynik (np. `invoke()` / `ainvoke()` albo `call()` / `acall()` / `generate()` / `agenerate()`). To domyślne, blokujące zachowanie. (więcej: dokumentacja modeli). citeturn6search0  
2. **Asynchroniczne wywołania** — tę samą funkcjonalność masz w wariancie async (`ainvoke()`, `astream()`, `agenerate()` itp.), potrzebne do integracji z serwerami/async frameworks. citeturn0search5turn6search3  
3. **Streaming (strumieniowanie)** — LLM zwraca tokeny/chunki na bieżąco; LangChain wystawia mechanizmy `stream()` / `astream()` oraz system callbacków, żeby aplikacja mogła odbierać przyrostowe wyniki. To jest temat, który rozwijam poniżej. citeturn0search5turn1search0  
4. **Runnables / Chains / Agents** — LangChain składa elementy (prompty → model → parsery → narzędzia) jako „runnables”. Każdy runnable ma metody `invoke`/`astream`/`stream` i może propagować streaming dalej — streaming działa tylko gdy wszystkie kroki potrafią przetwarzać chunk po chunku. citeturn0search5turn2search15

---

# Strumieniowe odpowiedzi — szczegółowo, technicznie

## 1) Jak to działa („pipeline” strumieniowy)
1. **Provider (np. OpenAI, Anthropic, Azure)** generuje tokeny stopniowo i przesyła je po sieci (SSE / websocket / HTTP chunking).  
2. **Integracja LangChain (np. `ChatOpenAI`, `ChatAnthropic` itd.)** odbiera te eventy i w trybie streaming buduje „chunki” / `AIMessageChunk`. Model wrapper może mieć parametr `streaming=True`. citeturn1search0turn6search3  
3. **Callback Manager** w LangChain emituje zdarzenia (np. `on_llm_new_token`) dla każdego otrzymanego tokena lub chunku. Do tych zdarzeń podpinamy własne handler-y (sync lub async). citeturn0search7  
4. **Aplikacja** otrzymuje tokeny poprzez callbacky, queue, generator async, WebSocket/SSE itp. — i może je natychmiast przesłać do klienta UI (chat na żywo).  

Schemat logiczny: Provider → LangChain model wrapper (streaming=True) → CallbackManager (on_llm_new_token) → Twój handler (np. enqueue) → endpoint (SSE/WebSocket) → przeglądarka.

## 2) Gdzie włączyć streaming (najważniejsze ustawienia)
- W modelach (przykład Python): `ChatOpenAI(streaming=True, callbacks=[...])` — `streaming=True` włącza obsługę strumieniową w wrapperze. citeturn1search0turn1search6  
- Alternatywnie korzystasz z runnable-ów/chainów i wywołujesz `.stream()` / `.astream()` — wtedy LangChain będzie emitować chunk po chunku, jeśli każdy krok obsługuje streaming. citeturn0search5

## 3) Callbacky — interfejs i zdarzenia
Kluczowe eventy (podstawowe, które będziesz używać przy streamingu):
- `on_llm_start(...)` — LLM wystartował.  
- `on_llm_new_token(token, **kwargs)` — **nowy token / chunk** (to najważniejsze do streamingu).  
- `on_llm_end(response, **kwargs)` — zakończenie generacji (masz finalny wynik / metadata).  
- Dodatkowo są zdarzenia `on_chain_start/on_chain_end`, `on_chat_model_start`, `on_tool_start` itp. citeturn0search7

W Pythonie jest `BaseCallbackHandler` i asynchroniczny `AsyncCallbackHandler` (rozszerzalne klasy, które nadpisujesz). W JS tworzy się obiekt z metodami typu `onLLMNewToken(run, token, kwargs)` (nazwa w JS: `onLLMNewToken`/`onLLMNew Token` w API). citeturn4search1turn3search1

## 4) Typy „chunków” i dodatkowe komplikacje
- **Token chunks**: czyste tokeny / fragmenty tekstu (zwykle emitowane przez `on_llm_new_token`).  
- **Message chunks / AIMessageChunk**: obiekt opisujący fragment wiadomości (może zawierać metadane). W trybie tool-calling chunk może zawierać specjalne pola `tool_call_chunks`. citeturn6search3turn6search1  
- **Tool-calls streaming**: kiedy agent wywołuje narzędzie w trakcie generacji, LangChain może strumieniować kolejne części wywołania narzędzia i dołączać je jako `tool_call_chunks` — nie wszyscy providerzy to wspierają. citeturn6search1turn5search2

## 5) Kiedy streaming *nie* zadziała
- Streaming wymaga, żeby dany model/provider wspierał strumieniowanie. **Nie wszystkie integracje/providery zachowują się identycznie** (np. zgłaszane były różnice między OpenAI a Google/Gemini — `on_llm_new_token` może nie odpalać u niektórych providerów). citeturn5search2turn0search6  
- Jeśli którykolwiek krok w chainie nie obsługuje streamingu (np. parser czeka na pełny JSON), to streaming zostanie „przerwany” i LangChain zbuforuje wynik (-> dostaniesz całość dopiero na końcu). Z tego powodu projektowanie end-to-end streamingu wymaga, żeby każdy krok potrafił operować na chunkach. citeturn0search5turn2search15

---

# Praktyczny przykład — Python (FastAPI, SSE) — token-by-token streaming
Poniżej przykład pokazujący ideę: handler umieszcza tokeny w `asyncio.Queue`, endpoint FastAPI zwraca `StreamingResponse` SSE, a `on_llm_end` wrzuca sentinel `None` żeby generator się zakończył.

```python
# wymagane: pip install langchain langchain_openai fastapi uvicorn
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.callbacks.base import AsyncCallbackHandler

app = FastAPI()

class QueueCallbackHandler(AsyncCallbackHandler):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    async def on_llm_new_token(self, token: str, **kwargs):
        # dostajemy kolejny token (często fragment tekstu)
        await self.queue.put(token)

    async def on_llm_end(self, response, **kwargs):
        # sygnalizujemy zakończenie strumienia
        await self.queue.put(None)

@app.post("/stream")
async def stream_endpoint(req: Request):
    body = await req.json()
    prompt = body.get("prompt", "")
    q: asyncio.Queue = asyncio.Queue()
    handler = QueueCallbackHandler(q)

    # model: streaming=True, przekazujemy callback
    llm = ChatOpenAI(streaming=True, callbacks=[handler], temperature=0.0)

    # odpalenie taska generującego (nie blokuje)
    async def run_model():
        # astream / astream_events można użyć zamiast sync call
        # tu wywołujemy asynchroniczny wariant, żeby model zaczął produkować tokeny
        await llm.astream([HumanMessage(content=prompt)])

    task = asyncio.create_task(run_model())

    async def event_generator():
        while True:
            token = await q.get()
            if token is None:
                break
            # SSE format: "data: <text>\n\n"
            yield f"data: {token}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

Komentarze:
- `ChatOpenAI(streaming=True, callbacks=[handler])` włącza streaming i podłącza handler. citeturn1search0turn2search11  
- `AsyncCallbackHandler` to klasa bazowa dla async handlerów — nadpisujesz `on_llm_new_token` i `on_llm_end`. Używanie async handlera jest zalecane w async frameworks, żeby nie blokować event loop. citeturn4search1turn4search3

---

# Krótki przykład w JavaScript/Node (langchain-js)
W JS mechanika jest podobna: model z `streaming: true`, callback obiekt implementuje `onLLMNewToken`.

```javascript
import express from "express";
import { ChatOpenAI } from "@langchain/openai";

const app = express();
app.use(express.json());

app.post("/stream", async (req, res) => {
  const { prompt } = req.body;
  // handler obiektu callback
  const handler = {
    onLLMNewToken: (run, token, kwargs) => {
      // send token do klienta (tu prosty flush)
      res.write(token);
    },
    onLLMEnd: (run) => {
      res.end();
    }
  };

  const model = new ChatOpenAI({ streaming: true, callbacks: [handler] });
  // uruchamiamy (API może się różnić; można też użyć model.stream()/model.call() zależnie od wersji)
  await model.call([{ role: "user", content: prompt }]);
});

app.listen(3000);
```

Uwaga: w langchain-js eventy są nazywane `onLLMNewToken` / `onLLMEnd` i callbacki mogą być przekazywane jako konstruktorowe lub w czasie wywołania. citeturn3search1turn5search13

---

# Pułapki, wskazówki i dobre praktyki
- **Używaj `AsyncCallbackHandler` w async środowiskach** — sync handler może być wywoływany w executorze i spowolnić event loop. citeturn4search3  
- **Sprawdź, czy Provider obsługuje streaming** — różnice między providerami mogą powodować, że `on_llm_new_token` nie jest wywoływane. Testuj dla konkretnego modelu. citeturn5search2  
- **Jeśli chcesz streamować tylko finalną odpowiedź (nie wszystkie intermediate steps)**: filtruj zdarzenia w callback (np. zbieraj tokeny tylko dla ostatniego `AIMessage` przypisanego do assistant) lub wyłącz streaming w podwywołaniach. W agentach/chainach można też dostosować, które kroki emitują zdarzenia. citeturn1search13turn2search7  
- **Tool-calling**: tool-call chunks mają specjalną strukturę (`tool_call_chunks`) — jeśli agent używa narzędzi, musisz rozważyć ich parsowanie w czasie rzeczywistym. Nie wszyscy providerzy streamują tool-calls. citeturn6search1  
- **Zarządzanie zakończeniem**: w handlerze `on_llm_end` wstaw sentinel do kolejki, żeby generator HTTP/SSE/WS mógł się poprawnie zakończyć. citeturn4search1

---

# Podsumowanie (co powinieneś zrobić, krok po kroku)
1. Sprawdź, czy wybrany provider/model wspiera streaming. citeturn5search2  
2. Zaimplementuj `AsyncCallbackHandler` / callback object i przechwyć `on_llm_new_token` + `on_llm_end`. citeturn4search1turn2search11  
3. Uruchom model z `streaming=True` (albo użyj `.stream()` / `.astream()` na runnable/chain). citeturn1search0turn0search5  
4. W handlerze przepychaj tokeny do kolejki/streamu i serwuj klientowi (SSE / WebSocket / WebTransport / inny).  
5. Testuj end-to-end, zwracając uwagę na to, które kroki łańcucha obsługują streaming — jeśli któryś nie obsługuje, streaming zostanie zbuforowany. citeturn0search5

---

# Źródła i dalsza lektura (fragment)
- LangChain — Streaming (concepts / how-to). citeturn0search5turn0search1  
- LangChain — Callback events (lista zdarzeń: `on_llm_new_token`, `on_llm_end` itd.). citeturn0search7  
- `ChatOpenAI` — parametr `streaming` i metody `stream()` / `astream()`. citeturn1search0turn6search0  
- How to stream tool calls (tool_call_chunks). citeturn6search1  
- Przykłady / dyskusje o różnych providerach i problemach ze streamingiem (issue: Gemini vs OpenAI). citeturn0search6turn5search2

---

Jeśli chcesz, mogę teraz:
- dostarczyć **gotowe, przetestowane repo** (FastAPI + front-end SSE) lub  
- rozbudować przykład o obsługę agentów i tool-calls (pokazać jak filtrować intermediate steps), lub  
- napisać dokładny przykład dla twojego stacka (Streamlit / Flask / Next.js / Express).  

Nie pytam teraz o stack, wykonałem ogólny, techniczny przegląd + przykłady — daj znać którą z powyższych opcji wolisz, a zrobię konkretny, kompletny przykład.