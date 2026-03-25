# Wyszukiwanie logów Kibana

**Data:** 2024-11-20

---

**User:**

W kibana w sekcji Discovery, chę wyszukać logi które w treści mają tekst "invalid list of FPP". Jakiego zapytania użyć?

---

**Assistant:**

Aby wyszukać logi zawierające dokładnie tekst **"invalid list of FPP"** w Kibana w sekcji Discovery, możesz skorzystać z następującego zapytania:

```plaintext
message:"invalid list of FPP"
```

### Wyjaśnienie:
1. **message:**  
   Zakładam, że pole w Twoim indeksie, w którym znajdują się logi, to `message`. Jeśli pole nazywa się inaczej, np. `log`, musisz zastąpić `message` nazwą odpowiedniego pola.

2. **Cudzysłowy (""):**  
   Tekst w cudzysłowie oznacza, że Kibana wyszuka dokładnie tę frazę, włącznie z kolejnością słów i spacjami.

### Dodatkowe wskazówki:
- Jeśli nie wiesz, w którym polu przechowywana jest treść logów, możesz po prostu wpisać frazę w polu wyszukiwania (bez `message:`). Kibana przeszuka wtedy wszystkie pola.
- Jeśli chcesz wyszukać tę frazę w logach zawierających dodatkowe informacje, możesz połączyć warunki, np.:
  ```plaintext
  message:"invalid list of FPP" AND status:500
  ```
  Powyższe znajdzie logi z frazą w polu `message` oraz statusem `500`.

Daj znać, jeśli potrzebujesz bardziej złożonych przykładów! 😊