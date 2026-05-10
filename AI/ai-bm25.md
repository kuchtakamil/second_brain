# AI BM25

## Krótkie podsumowanie
BM25 (Best Matching 25) to algorytm wyszukiwania pełnotekstowego (lexical search), oceniający trafność dokumentów. Opiera się na częstotliwości słów (rozwinięcie TF-IDF). Analizuje statystykę wystąpień, nie znaczenie tekstu.

## Kiedy się stosuje
- Tradycyjne silniki wyszukiwania (Elasticsearch, Lucene).
- Wyszukiwanie ścisłych dopasowań (nazwy własne, kody, numery seryjne).
- W systemach RAG jako element wyszukiwania hybrydowego (BM25 + wyszukiwanie wektorowe) dla uodpornienia systemu na literówki oraz wymuszania ścisłych dopasowań.

## Jak działa i czy rozumie synonimy
1. **Zasada działania:** Punktuje dokumenty bazując na częstotliwości wystąpienia słów z zapytania, rzadkości tych słów w całej bazie oraz długości dokumentu.
2. **Brak natywnego rozumienia synonimów i pokrewieństwa:** Sam, "surowy" algorytm BM25 traktuje słowa jako niezależne ciągi znaków. Nie widzi związku ani między synonimami ("samochód" i "auto"), ani wyrazami pokrewnymi ("rzeka" i "rzeczny").
3. **Obsługa synonimów i odmian:** Odbywa się zewnętrznie, przed indeksowaniem:
   - **Lematyzacja/Stemming:** Sprowadzanie słów do formy podstawowej. Odpowiedni analizator językowy (np. w Elasticsearch) sprawi, że słowa "rzeka" i "rzeczny" zostaną zredukowane do wspólnego tokenu i powiązane w wyszukiwaniu.
   - **Słowniki synonimów:** Wymagają manualnej konfiguracji mapowań w silniku (przypisanie, że "auto" = "samochód").
4. **Stosunek do embeddingów i przestrzeni wektorowej:** 
   - **BM25 (Sparse Vectors):** Reprezentacja rzadka. Wektory są wielkości całego korpusu słownikowego. Większość wartości to zera, a nieliczne to wagi TF-IDF obecnych słów. Dopasowanie jest wyłącznie leksykalne (exact match).
   - **Embeddingi (Dense Vectors):** Reprezentacja gęsta. Modele AI konwertują tekst na wektory o stałym, mniejszym wymiarze (np. 1536), gdzie bliskość w przestrzeni wektorowej odpowiada podobieństwu semantycznemu (znaczeniu). Natywnie rozumieją kontekst i synonimy bez słowników.

## Powiązane pliki
- [Baza wektorowa vs LLM](baza-wektorowa-vs-llm.md)
- [Czym jest embedding i bazy wektorowe](wiem-na-czym-polega-embedding-i-wektorowe-bazy-ale-bez-szczegółów-jeśli-chodzi-o.md)
