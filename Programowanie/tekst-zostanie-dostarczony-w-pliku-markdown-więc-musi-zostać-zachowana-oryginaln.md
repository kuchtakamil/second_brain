# Tekst zostanie dostarczony w pliku markdown więc musi zostać zachowana oryginaln

**Data:** 18 gru 2025, 13:00:13 CET

---

**User:**

Tekst zostanie dostarczony w pliku markdown więc musi zostać zachowana oryginalna struktura rozdziałów czyli wszystkie ### muszą być zachowane a tytuły mają pozostać bez zmian.
Dodatkowo do każdego pliku będzie dołączona informacja do którego dużego rozdziału tekst należy np. "rozdzia_6_bezpieczenstwo_operacyjne_model_zagrozen_dla_api". Może to pomoże utrzymać kontekst dla skracanego tekstu.

---

**Gemini:**

Aby uwzględnić rygorystyczne zachowanie struktury dokumentu oraz wykorzystanie dostarczonego kontekstu rozdziału nadrzędnego, zaktualizowałem prompt. Skupia się on teraz na edycji „in-place”, czyli modyfikowaniu treści pod konkretnymi nagłówkami bez naruszania ich hierarchii.

### Zaktualizowany System Prompt / Instructions

```
**Role:** Senior Technical Editor & Documentation Architect.

**Objective:** Process the provided Markdown text to increase its information density. You are performing a "Technical Extraction" – removing all literary filler while retaining 100% of the substantive technical content.

**Contextual Awareness:**
The provided text is a fragment of a larger section titled: "{{CHAPTER_CONTEXT}}". Use this information to maintain technical consistency and resolve ambiguous terms, but do not repeat this title in the output unless it appears in the source text.

**STRICT STRUCTURAL CONSTRAINTS:**
1. **Preserve Headings:** You MUST keep all original Markdown headings (e.g., `###`, `####`) exactly as they are in the source text.
2. **Title Integrity:** Do not change, translate, or summarize any heading titles. They must remain 1:1 with the source.
3. **Structure Retention:** The sequence of sections must remain identical to the original.

**CONTENT EXTRACTION RULES:**
- **RETAIN:** Every technical fact, parameter, code block, architectural decision, trade-off, API specification, and logical flow.
- **ELIMINATE:** Anecdotes, metaphors, "we will discuss" statements, rhetorical questions, motivational filler, and wordy transitions.
- **STYLE:** Convert descriptive paragraphs into concise technical statements or bullet points where appropriate, provided it doesn't lose nuance.

**Execution Directive:** Act as a filter that blocks "noise" but lets "signal" (data) pass through. The resulting document should look like the original Markdown file in terms of headers, but the text under those headers should be dense, factual, and devoid of any "bookish" narrative.
```

---

### Szablon wiadomości użytkownika (User Message)

Wysyłając fragment do AI, użyj poniższego formatu, aby precyzyjnie przekazać dane:

> **Main Chapter Context:** `rozdzia_6_bezpieczenstwo_operacyjne_model_zagrozen_dla_api`
>
> **Input Markdown Text:** > [Tutaj wklej treść pliku .md]
>
> **Action:** Apply the Technical Extraction protocol. Keep all `###` headers and their titles exactly as provided. Clean the content under each header from any non-technical filler.

---

### Dlaczego ta wersja jest lepsza dla Twojego przypadku?

1. **Zmienna `{{CHAPTER_CONTEXT}}`**: Pozwala modelowi zrozumieć, że jeśli w tekście pojawia się np. słowo "klucz", to w kontekście bezpieczeństwa API prawdopodobnie chodzi o klucz kryptograficzny/API, a nie klucz do bazy danych.
2. **Rygor strukturalny**: Instrukcja "STRICT STRUCTURAL CONSTRAINTS" blokuje skłonność AI do "uładzania" struktury lub łączenia rozdziałów, co jest częstym błędem przy zwykłym poleceniu `summarize`.
3. **Edycja segmentowa**: Model traktuje każdy blok tekstu pod nagłówkiem jako niezależną jednostkę do "wyczyszczenia", co gwarantuje, że nie pominie żadnego podrozdziału.
4. **Zachowanie Markdown**: Dzięki jawnemu wskazaniu symboli `###`, AI nie zamieni ich na pogrubienie czy listy, co ułatwi Ci późniejsze scalanie plików.