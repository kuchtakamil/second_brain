# LLM Guardrails

## Podsumowanie (Co to jest?)
**LLM Guardrails** (zabezpieczenia modeli językowych) to mechanizmy, filtry, lub warstwy kontrolne umieszczone między aplikacją opartą o duży model językowy (LLM) a jej użytkownikiem lub samym modelem bazowym. Służą one do monitorowania i walidacji zarówno danych wejściowych (promptów), jak i danych wyjściowych (odpowiedzi modelu), w celu zagwarantowania, że zachowanie sztucznej inteligencji jest bezpieczne, spójne, etyczne i zgodne z założeniami biznesowymi.

## Dlaczego się stosuje? (Zastosowanie i Znaczenie)
Modele takie jak GPT-4 czy Claude zostały wytrenowane na ogromnych, zróżnicowanych zestawach danych i potrafią generować każdy rodzaj tekstu. Są niesamowicie elastyczne, ale też **nieprzewidywalne** i podatne na obejście reguł (tzw. Jailbreak). Guardrails chronią aplikacje produkcyjne przed następującymi zagrożeniami:

1. **Ochrona przed Prompt Injection i Jailbreak:** Uniemożliwienie użytkownikom wstrzykiwania złośliwych instrukcji, które próbują zmusić model do zignorowania instrukcji systemowych.
2. **Redukcja Halucynacji:** Blokowanie modelu przed wymyślaniem fałszywych informacji, szczególnie w systemach RAG (Retrieval-Augmented Generation), polegając mocno na upewnieniu się, że odpowiedź jest oparta tylko na podanym kontekście.
3. **Filtrowanie Toksyczności i Ochrona Danych (PII):** Zapobieganie generowaniu szkodliwych, agresywnych czy nielegalnych treści, a także dbanie o to, by prywatne dane użytkownika (adresy, numery PESEL) nie zostały przesłane do zewnętrznego API dostawcy modelu.
4. **Wymuszanie Formatu i Działania Biznesowego (Off-topic):** Kontrolowanie, czy model nie odbiega od głównego tematu (np. chat bot sklepu wędkarskiego odmawiający pomocy w pisaniu kodu w Pythonie) oraz czy prawidłowo zwraca zażądany typ danych (np. struktura JSON).

## Jak to działa i Przykłady Technologii

Architektura ta najczęściej opiera się na umieszczaniu *walidatorów* na jednym lub obu końcach interakcji z modelem głównym. Czasami jako "Systemów Kontrolnych" (Judges) używa się innych, mniejszych i wyspecjalizowanych LLM, których jedynym zadaniem jest ocena i klasyfikacja promptów pod względem bezpieczeństwa (np. model wykrywający szkodliwe zamiary w 50 milisekund).

### Rynkowe Przykłady Technologii
- **NeMo Guardrails (NVIDIA):** Framework open-source oparty na tzw. *Colang* (język modelowania dialogu), pozwalający na łatwe skryptowanie dokładnych, twardych ścieżek zachowań modelu tak, by uniknąć jakichkolwiek ucieczek tematycznych.
- **Guardrails AI:** Świetne narzędzie do nakładania walidacji na formaty, błędy składniowe czy nawet do weryfikacji semantycznej odpowiedzi (zapewnia automatyczny *Retry* do poprawy odpowiedzi w razie błędu struktury uby modelu).
- **Llama Guard (Meta):** Specjalistyczny LLM (z rodziny Llama) dostrojony wyłącznie do bycia "ochroniarzem". Sprawdza tekst pod kątem taksonomii zagrożeń (Violence & Hate, Sexual Content, itp.).

### Przykładowy pseudo-kod w ujęciu aplikacyjnym (Logika Guardrails)

```python
from my_guardrail_framework import validate_input, validate_output

def chat_with_assistant(user_prompt: str) -> str:
    # 1. INPUT GUARDRAIL - Walidacja przed uderzeniem do głównego LLMa
    is_safe_prompt = validate_input(user_prompt, checks=["no_prompt_injection", "no_pii"])
    if not is_safe_prompt:
        return "Przepraszam, ale Twoja wiadomość narusza zasady bezpieczeństwa."
        
    # 2. Strzał do głównego i potencjalnie drogiego modelu np. GPT-4o
    raw_response = get_llm_response(user_prompt)
    
    # 3. OUTPUT GUARDRAIL - Walidacja po wygenerowaniu odpowiedzi
    is_safe_response = validate_output(raw_response, checks=["no_hallucination_from_context", "valid_json"])
    if not is_safe_response:
        # Wymuszenie re-generacji (Retry)
        raw_response = get_llm_response(f"Błąd reguł: Popraw odpowiedź: {raw_response}")
        
    return raw_response
```

## Powiązane pliki (Zobacz również)
- [[bezpieczenstwo-danych-kontrola-dostepu-governance-ai]]
- [[komunikacja-z-llm-w-langchain]]
- [[langchain-structured-output-jinja2]]
