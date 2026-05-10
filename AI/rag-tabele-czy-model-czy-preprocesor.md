# RAG a dane stabelaryzowane: Model vs Preprocesor

## Krótkie podsumowanie
Gdy budujesz system RAG (Retrieval-Augmented Generation), który musi radzić sobie z danymi stabelaryzowanymi (np. raporty finansowe, zestawienia księgowe, rozbudowane cenniki), stajesz przed wyborem: użyć zaawansowanego modelu LLM zdolnego "czytać" tabele, czy też zastosować specjalny preprocesor. W praktyce inżynierii AI, **zdecydowanie zaleca się użycie dobrego preprocesora tabel**, który przekonwertuje je na format ustrukturyzowany (np. Markdown, HTML) przed fazą embeddingu i przekazaniem do głównego modelu w procesie generacyjnym.

## Dlaczego to ma znaczenie?
Tabele to struktury dwuwymiarowe, rządzace się skomplikowanymi relacjami (nagłówki wierszy, nagłówki kolumn, połączone komórki). Podstawowe metody ekstrakcji tekstu z PDF (np. PyPDF2) zazwyczaj zlewają zawartość komórek w jeden liniowy ciąg tekstu, całkowicie niszcząc relacje pomiędzy danymi. Gdy LLM otrzymuje taki potok tekstu "na wejściu" (w kontekście RAG), nie potrafi z niego wywnioskować np. jakiego miesiąca i działu dotyczy dana wartość finansowa.

## Jakie mamy opcje i jak one działają?

### Opcja 1: Poleganie na samym LLM (Multimodalność / Vision)
W tym scenariuszu rezygnujemy z dogłębnego strukturyzowania. Strona z tabelą jest konwertowana do obrazu i podczas odpowiedzi przesyłana jako plik wizualny do modeli VLM (Vision-Language Models), takich jak GPT-4o czy Claude 3.5 Sonnet, aby "spojrzały" i znalazły odpowiedź.
*   **Plusy**: Relatywnie najmniej pracy programistycznej na początku (szybki setup). Model "odczytuje" dane wizualnie, co sprawdza się przy wykresach.
*   **Minusy**: Niezwykle **drogi koszt** wywołań API (przetwarzanie obrazów o dużej rozdzielczości zużywa masę tokenów),  bardzo duże opóźnienia (**latency**) w zwracaniu odpowiedzi. Ponadto zjawisko halucynacji w złożonych raportach finansowych jest nagminne, zwłaszcza gdy tabela ma małą czcionkę. W procesie RAG trudno jest też wektoryzować (wyszukać wektorowo) obraz tak precyzyjnie jak poszczególny węzeł tekstowy.

### Opcja 2: Użycie preprocesora układu (Zalecane)
Podejście to kładzie nacisk na bardzo dobre przetworzenie pliku źródłowego, aby dostarczyć maszynie czytelny plik tekstowy z zachowaniem logiki dwuwymiarowej.
Wykorzystuje się parsery Document Understanding (np. LlamaParse, Unstructured.io, Microsoft Document Intelligence, AWS Textract). Narzędzie takie potrafi zidentyfikować tabelę i przekuć ją w odpowiednik napisany w formacie Markdown, HTML, lub JSON.

*   **Plusy**:
    *   **Zgodność wejściowa z LLM**: Format Markdown pozwala LLM-owi bardzo precyzyjnie rozumieć powiązania pomiędzy nagłówkiem a poszczególną wartością.
    *   **Lepszy Retrieval**: Tabele przekonwertowane na formy tekstowe (oraz otagowane metadanymi) ładnie układają się w bazie wektorowej, znacząco podnosząc jakość dopasowań. Koszty operacyjne oraz "latency" podczas samego działania na froncie czatu są bardzo niskie względem opcji Vision.
*   **Minusy**: Architektura staje się bardziej skomplikowana. Rozwiązania komercyjne pod pre-processing zaawansowany (np. płatny pakiet LlamaParse) dodają stały wydatek operacyjny na czas samego indeksowania danych.

## Podsumowując: Architektury z użyciem RAG
Budując rozwiązanie docelowe na tabelach i raportach finansowych, najlepszą strategią jest:
1. Zastosowanie dobrego **preprocesora zdolnego do wyodrębniania spójnego Markdown z tabel** z dokumentów ustrukturyzowanych (także opartych o skany).
2. Dodatkowe zastosowanie wzorców takich jak **Table Summarization** – zaraz po rozpakowaniu tabel z PDF-a, w tle prosisz relatywnie mały i szybki LLM (np. LLama 3.1 8B): "*Opisz w kilku zdaniach jakie dane przedstawia ta tabela*".
3. To wygenerowane **podsumowanie** (krótki tekst) następnie zrzucasz do embeddera i indeksujesz w przestrzeni wektorowej. Jeśli w zapytaniu użytkownika system znajdzie to podsumowanie w pierwszej trójce podobieństw (*Top-K retrieval*), to jako zawartość kontekstu podpinasz do promptu oryginalną (surową, wielką) tabelę ze źródła Markdown (metoda znana pod pojęciem *Parent Document Retriever*).
To rozwiązanie optymalizuje zarówno koszty wyszukiwania jak i niweluje problem poszatkowanych, nielogicznych tokenów w bazie.

## Powiązane pliki
- [Baza wektorowa vs LLM](baza-wektorowa-vs-llm.md)
- [Pytania rekrutacyjne RAG](pytania-rekrutacyjne-rag.md)
- [Kontrowersje wokół RAG](kontrowersje-wokół-rag.md)
