# Główne Komponenty Ekosystemu LangChain (Transkrypt)

## Podsumowanie
Poniższe zestawienie stanowi transkrypt zrzutu ekranu prezentującego komponenty ekosystemu LangChain (i pokrewnych narzędzi) wykorzystywanych do budowy aplikacji LLM, w tym systemów RAG (Retrieval-Augmented Generation) czy aplikacji agentowych. LangChain oferuje bogaty zbiór abstrakcji i integracji ułatwiających m.in. pobieranie i wektoryzację danych, łączenie z zewnętrznymi bazami i dostarczanie interfejsów (narzędzi) dla modeli językowych.

## Główne Kategorie i Przykłady Integracji

Zgodnie ze zrzutem ekranu, ten fragment ekosystemu dzieli się na kilka kluczowych obszarów integracji:

*   **Narzędzia (Tools)**: Umożliwiają agentom LLM interakcję ze światem zewnętrznym i wykonywanie zaprogramowanych akcji.
    *   *Przykłady:* `SerpAPI`, `Bearly Code Interpreter`, `Github Tool`, ...
*   **Retrievery**: Odpowiadają za pobieranie najbardziej dopasowanych dokumentów w odpowiedzi na zapytanie użytkownika.
    *   *Przykłady:* `ElasticsearchRetriever`, `WikipediaRetriever`, ...
*   **Embeddingi (Embeddings)**: Modele pozwalające na zamianę treści tekstowej (oraz np. audio/wideo) na gęste reprezentacje wektorowe (liczbowe), celem osadzania ich w przestrzeniach wielowymiarowych.
    *   *Przykłady:* `OpenAIEmbeddings`, `OllamaEmbeddings`, `HuggingFaceEmbeddings`, ...
*   **Vector Stores (Bazy wektorowe)**: Wyspecjalizowane wektorowe bazy danych do przechowywania wygenerowanych reprezentacji i efektywnego przeszukiwania ich pod kątem bliskości zapytania (tzw. *similarity search*).
    *   *Przykłady:* `PGVector`, `Chroma`, `Qdrant`, ...
*   **Key-value stores (Magazyny klucz-wartość)**: Magazyny klucz-wartość stosowane często do przechowywania stanu zapamiętanych sesji, wiadomości chatu (cache), do deduplikacji zapytań itp.
    *   *Przykłady:* `RedisStore`, `CassandraByteStore`, `AstraDBByteStore`, ...

## Jak to działa w praktyce? (Przykład kodu)

Poniższy fragment kodu z transkryptu prezentuje typowy proces użycia komponentów LangChain. Przygotowane fragmenty dokumentów są przepuszczane przez model embeddujący, a gotowe wektory w ramach procesu *DB Integration* lądują w bazie (np. rozszerzeniu bazy PostgreSQL - PGVector). Następnie wykonane zostaje wyszukiwanie semantyczne bliskoznacznych treści.

```python
from langchain_community.retrievers import ArxivRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

# Retriever
retriever = ArxivRetriever(load_max_docs=3, get_full_documents=True)
docs = retriever.invoke("large language models")

# Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
)

raw_texts = [doc.page_content for doc in docs]
metadatas = [doc.metadata for doc in docs]

chunked_docs = text_splitter.create_documents(
    texts=raw_texts,
    metadatas=metadatas,
)

# Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# DB Integration
vectorstore = PGVector.from_documents(
    documents=chunked_docs,
    embedding=embeddings,
    collection_name="arxiv_collection",
    connection="postgresql+psycopg://user:password@localhost:5432/arxiv_db",
)

query = "What are the key challenges with LLMs?"
print("Semantic search results:")

results = vectorstore.similarity_search(query=query, k=5)

for i, r in enumerate(results, 1):
    print(f"[{i}]. {r.page_content[:200]}...\n")
```

## Powiązane tematy

*   [Komunikacja z LLM w LangChain](komunikacja-z-llm-w-langchain.md)
*   [Wzorce wieloagentowe Langchain](langchain-multi-agent-patterns.md)
*   [Baza wektorowa vs LLM](baza-wektorowa-vs-llm.md)
*   [Indeksowanie w bazach Qdrant](indeksowanie-w-bazach-qdrant.md)
*   [Pytania rekrutacyjne RAG](pytania-rekrutacyjne-rag.md)
