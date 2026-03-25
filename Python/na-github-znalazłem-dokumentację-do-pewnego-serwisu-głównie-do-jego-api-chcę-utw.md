# na github znalazłem dokumentację do pewnego serwisu, głównie do jego API. Chcę u

**Data:** 1 lut 2026, 18:51:26 CET

---

**User:**

na github znalazłem dokumentację do pewnego serwisu, głównie do jego API. Chcę utworzyć prostego klienta do tego serwisu w python. Chcę aby ta dokumentacja była dostępna dla narzędzia AI Claude Code. Zastanawiam się jak to ułożyć. Mogę przekopiować repo dokumentacji do repo klienta ale może  jest lepszy sposób?

---

**Gemini:**

Wybór optymalnej strategii zależy od tego, czy dokumentacja jest statyczna, czy często aktualizowana, oraz od limitów tokenów kontekstu (Context Window) modelu, z którego korzystasz wewnątrz Claude Code.

Oto zestawienie najbardziej efektywnych metod integracji zewnętrznej dokumentacji z procesem deweloperskim:

### 1. Model Context Protocol (MCP) – Podejście Natywne

Claude Code jest zaprojektowany do współpracy z serwerami **MCP**. Zamiast kopiować pliki, możesz wykorzystać serwer MCP, który dynamicznie dostarcza dokumentację.

- **mcp-server-fetch:** Jeśli dokumentacja jest dostępna w sieci (np. GitHub Pages, ReadTheDocs), możesz skonfigurować Claude Code, aby pobierał konkretne podstrony w locie.
- **mcp-server-git:** Umożliwia Claude’owi przeszukiwanie i odczytywanie zawartości innych repozytoriów bez konieczności ich fizycznego zagnieżdżania w projekcie.

### 2. Git Submodules z selektywnym filtrowaniem

Jeśli zdecydujesz się na trzymanie plików lokalnie, `git submodule` jest lepszy niż zwykłe kopiowanie, ponieważ zachowuje referencję do konkretnego commitu dokumentacji.

```
git submodule add https://github.com/user/api-docs-repo.git docs/external-api
```

Aby Claude Code nie analizował niepotrzebnych plików (np. obrazków, assetów CSS), skonfiguruj plik `.claudeignore` (jeśli narzędzie go wspiera) lub po prostu ogranicz widoczność plików w sesji.

### 3. Agregacja Kontekstu (Repomix / LLM-Context)

Zamiast dawać Claude’owi dostęp do całego drzewa plików dokumentacji, co może marnować tokeny na zbędną strukturę katalogów, lepiej wygenerować jeden skonsolidowany plik Markdown. Narzędzia takie jak **Repomix** (dawniej `repomix`) potrafią spakować całe repozytorium dokumentacji do jednego, dobrze sformatowanego pliku `.md`.

**Przykład generowania paczki kontekstowej:**

```
npx repomix --include "docs/**/*.md,swagger.yaml,schema.json" --output api_context.md
```

Następnie w Claude Code wskazujesz tylko ten jeden plik: `Claude, refer to api_context.md for API definitions`.

### 4. Symlinki (Local Development)

Jeśli pracujesz lokalnie i masz oba repozytoria sklonowane obok siebie, najprostszym technicznie sposobem jest utworzenie dowiązania symbolicznego (symlink). Claude Code będzie widział dokumentację jako folder wewnątrz Twojego projektu, ale nie będziesz jej commitował do repozytorium klienta.

```
# Linux / macOS
ln -s ../path/to/api-docs-repo ./docs_context

# Windows (PowerShell as Admin)
New-Item -ItemType SymbolicLink -Path ".\docs_context" -Target "..\api-docs-repo"
```

Dodaj `docs_context/` do `.gitignore`, aby uniknąć przypadkowego wypchnięcia linku.

### 5. RAG i wektorowe przeszukiwanie dokumentacji

Przy bardzo obszernych API, przekazywanie całej dokumentacji może przekroczyć limit kontekstu lub obniżyć precyzję (tzw. *lost in the middle*). Claude Code potrafi operować na wynikach wyszukiwania. Jeśli dokumentacja jest hostowana, możesz użyć narzędzi typu `brave-search` lub dedykowanych serwerów MCP do przeszukiwania dokumentacji technicznej, co pozwoli modelowi pobierać tylko te fragmenty, które są aktualnie potrzebne do napisania konkretnej metody klienta.

### Rekomendacja techniczna

Dla prostego klienta Python najlepszym balansem między wygodą a precyzją jest **Metoda 3 (Agregacja)**. Pozwala ona na:

1. Wyczyszczenie dokumentacji z szumu (boilerplate HTML/CSS/JS).
2. Dostarczenie czystego Markdowna, który modele LLM parsują najlepiej.
3. Łatwe odświeżanie kontekstu jednym poleceniem po aktualizacji repozytorium źródłowego.

Czy chcesz, abym przygotował skrypt w Pythonie, który automatycznie pobierze `swagger.json` lub pliki Markdown z GitHub API i przygotuje je jako skonsolidowany kontekst dla Claude Code?