# wiem na czym polega embedding i wektorowe bazy ale bez szczegółów jeśli chodzi o

**Data:** 15 gru 2025, 22:44:08 CET

---

**User:**

wiem na czym polega embedding i wektorowe bazy ale bez szczegółów jeśli chodzi o cachowanie, więc napisz w skrócie.
Później opisz Optymalizacja Kontekstu (Context Management):

---

**Gemini:**

To logiczne podejście. Skoro wiesz, czym są embeddingi, temat cache'owania zamkniemy bardzo szybko.

### Semantic Caching (W skrócie)

W klasycznym cache'owaniu (np. Redis) szukamy **dokładnego dopasowania** (czy string A == string B). W **Semantic Caching**:

1. Zamieniasz nowe pytanie użytkownika na **wektor**.
2. Przeszukujesz bazę wektorową w poszukiwaniu wektorów, które są **blisko** (np. mają wysokie podobieństwo cosinusowe).
3. Jeśli znajdziesz pytanie o bardzo zbliżonym znaczeniu (nawet zapisanym innymi słowami), zwracasz zapisaną odpowiedź.

Dzięki temu system "rozumie", że *"Ile kosztuje ten produkt?"* i *"Jaka jest cena?"* to to samo zapytanie i nie musi ponownie płacić za generowanie odpowiedzi przez LLM.

---

### Optymalizacja Kontekstu (Context Management)

Przejdźmy do głównego tematu. Modele LLM mają ograniczone **okno kontekstowe** (np. 8k, 128k tokenów). Im więcej historii rozmowy przesyłasz w każdym zapytaniu:

- 💰 Tym więcej płacisz (płacisz za input tokens).
- 🐢 Tym wolniej model odpowiada (latency).
- 😵 Tym łatwiej model "gubi się" w nadmiarze informacji (problem *Lost in the Middle*).

Optymalizacja kontekstu to sztuka decydowania, co włożyć do "plecaka" 🎒 wysyłanego modelowi, aby wiedział co się dzieje, ale nie był przeciążony.

Oto trzy główne podejścia do zarządzania tą pamięcią. Które z nich chciałbyś przeanalizować szczegółowo?

1. **Windowing (Przesuwne okno):** Proste techniki przycinania historii (np. trzymanie tylko ostatnich $k$ par pytań/odpowiedzi). Jakie ma to wady przy dłuższych wątkach?
2. **Summarization (Podsumowanie progresywne):** Wykorzystanie mniejszego, szybszego modelu LLM do tworzenia bieżącego streszczenia starej rozmowy, które jest doklejane do promptu.
3. **Selekcja wektorowa historii:** Wybieranie z historii tylko tych wiadomości, które są semantycznie związane z *bieżącym* pytaniem (trochę jak RAG, ale na własnej rozmowie).