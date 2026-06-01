# Grafemy, punkty kodowe i bajty w Pythonie (Unicode)

W kontekście kodowania znaków zasada brzmi: **grafem ≠ punkt kodowy ≠ bajt**.
Zrozumienie tej różnicy jest kluczowe przy przetwarzaniu tekstu, zwłaszcza wielojęzycznego lub bogatego w emoji.

## Podsumowanie pojęć

*   **Bajt (Byte):** Podstawowa jednostka pamięci (8 bitów).
*   **Punkt kodowy (Code point):** Pojedyncza wartość liczbowa w standardzie Unicode przypisana do jakiegoś elementu (np. litery, znaku interpunkcyjnego, modyfikatora).
*   **Grafem (Grapheme):** Pojedynczy "widzialny" znak z perspektywy użytkownika. Jeden grafem może składać się z wielu punktów kodowych (np. litera + osobny znak akcentu, lub połączone emoji).

---

## Jak to wygląda w Pythonie?

W Pythonie 3 ciągi znaków są domyślnie **Unicode-aware** (działają na poziomie punktów kodowych), co rozwiązuje wiele problemów znanych z języków działających na bajtach, ale nadal nie jest rozwiązaniem **grapheme-aware**.

### 1. Podejście Unicode-unaware (Bajty)
Jeśli używasz typu `bytes`, Python traktuje dane jako czysty strumień bajtów.
*   **Kiedy używać:** Tylko gdy pracujesz na czystym ASCII lub z binarnymi danymi (np. odczyt z gniazda sieciowego przed zdekodowaniem).
*   **Funkcje:** Wbudowane metody dla `bytes`. `len(b'tekst')` zwraca dokładną liczbę bajtów.

### 2. Podejście Unicode-aware (Punkty kodowe) - Standard Pythona
Wbudowany typ `str` w Pythonie to ciąg punktów kodowych.
*   **Kiedy używać:** W 95% przypadków jest to wystarczające.
*   **Funkcje:** Wbudowane funkcje dla stringów, takie jak `len(tekst)`, `tekst.replace()`, operacje na indeksach (`tekst[0:5]`) czy wbudowana biblioteka `re`.
*   **Haczyk:** `len("é")` może zwrócić `2`, jeśli ciąg składa się ze zwykłego `"e"` (U+0065) i osobnego znaku modyfikującego `"´"` (U+0301). Choć dla użytkownika to jeden znak, dla Pythona to dwa punkty kodowe.

### 3. Podejście Grapheme-aware (Grafemy) - Maksymalna precyzja
Python **nie posiada** wbudowanych narzędzi (w standardowej bibliotece), które w pełni operują na grafemach. Jeśli przetwarzasz dane pod kątem wizualnym (np. chcesz uciąć tweet do dokładnie 140 wyświetlanych znaków, albo odwrócić string bez niszczenia emoji), natywne funkcje mogą "rozerwać" znak na pół, produkując krzaki.

*   **Kiedy używać:** Gdy maksymalna precyzja i poprawne traktowanie skomplikowanych znaków Unicode (emoji, języki arabskie, hindi, skomplikowane akcenty) ma znaczenie.
*   **Jakich funkcji/bibliotek używać:** Należy skorzystać z bibliotek zewnętrznych, np. `grapheme` lub `regex`.

## Przykłady w kodzie i rozwiązanie (Grapheme-aware)

```python
# --- Przykład problemu z punktami kodowymi ---
text_composed = "e\u0301"  # 'e' + akcent łączony (U+0301)
emoji_family = "👨‍👩‍👧‍👦"  # Rodzina: składa się z kilku złączonych emoji

# Funkcje wbudowane w Pythona (Unicode-aware, ale NIE Grapheme-aware)
print(len(text_composed))  # Wynik: 2 (dwa punkty kodowe)
print(len(emoji_family))   # Wynik: 7 (mężczyzna + zw + kobieta + zw + dziewczynka + zw + chłopiec)

# --- Rozwiązanie z biblioteką `grapheme` ---
# pip install grapheme
import grapheme

print(grapheme.length(text_composed))  # Wynik: 1 (jeden widzialny znak)
print(grapheme.length(emoji_family))   # Wynik: 1 (jedno połączone emoji)

# Bezpieczne cięcie stringów bez rozrywania grafemów
sub_str = list(grapheme.graphemes(emoji_family + text_composed))[0:2]
print("".join(sub_str)) # Oczekiwany poprawny wynik: 👨‍👩‍👧‍👦é
```

### Wyrażenia regularne a grafemy
Wbudowany moduł `re` nie rozumie grafemów. Jeśli chcesz np. dopasować dokładnie "trzy dowolne znaki widzialne", `re` może zawieść.
Aby tego uniknąć, użyj zewnętrznej biblioteki `regex` (stanowi drop-in replacement dla `re`), która obsługuje sekwencję `\X` oznaczającą *Grapheme Cluster* (zgrupowanie grafemu).

```python
# pip install regex
import regex

# \X dopasowuje pojedynczy grafem
matches = regex.findall(r'\X', "a👨‍👩‍👧‍👦b")
print(matches) # Wynik: ['a', '👨‍👩‍👧‍👦', 'b']
```

## Podsumowanie (Jakich funkcji używać?)
1. **Domyślnie:** Używaj standardowych funkcji typu `str` i metody `len()`. Typ `str` prawidłowo obsługuje punkty kodowe Unicode (nie ma problemu z polskimi znakami, o ile nie są w postaci zdekomponowanej).
2. **Zaawansowane przetwarzanie widocznego tekstu:** Jeżeli Twoja aplikacja zlicza "widzialne" znaki lub musi poprawnie dzielić długi tekst bez psucia emoji (np. generowanie fragmentów postów, odwracanie stringów), zignoruj wbudowane operatory na listach/stringach i skorzystaj z pakietu `grapheme` oraz biblioteki `regex`.
