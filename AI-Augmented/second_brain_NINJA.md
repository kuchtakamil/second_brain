# Second Brain z Obsidian + Claude Code - Szablon

Gotowy projekt vault'a Obsidian skonfigurowanego pod pracę z Claude Code w stylu LLM Wiki Karpathy'ego. Klonujesz repo, otwierasz jako vault, mówisz do Claude'a "skonfiguruj vault" - przeprowadzi Cię przez bootstrap pod Twój kontekst. Dorzucasz pierwsze źródło do `raw/` i mówisz "zingestuj" - Claude robi syntezę i zapisuje w `wiki/`.

🔗 **Repo z szablonem:** [github.com/AI-Ninjas-Dojo/obsidian-ai-vault](https://github.com/AI-Ninjas-Dojo/obsidian-ai-vault)

**Materiał bonusowy z webinaru:** Notion - AI Ninjas Materiał bonusowy Obsidian

---

## Konfiguracja

### 1. Obsidian

- **Pobierz:** [obsidian.md/download](https://obsidian.md/download) (Mac/Windows/Linux/iOS/Android, darmowy)
- **Vault** = folder z plikami `.md`. Zero magii.

### 2. Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```
*(Wymaga Node.js 18+ z [nodejs.org](https://nodejs.org))*

### 3. Sklonuj szablon vault'a

```bash
git clone https://github.com/AI-Ninjas-Dojo/obsidian-ai-vault.git
cd obsidian-ai-vault
```

Otwórz folder jako vault w Obsidian (Open folder as vault).

### 4. Bootstrap z Claude Code

W folderze vault'a uruchom:

```bash
claude
```

Powiedz: `"skonfiguruj vault"`

Claude otworzy `bootstrap.md` i przeprowadzi Cię przez pytania:
- Kim jesteś (dla Persony)
- Jaki temat ma vault (research / praca / hobby)
- Twój styl pisania
- Poziom techniczny

### 5. Pierwszy ingest

Wrzuć źródło (artykuł, transkrypcja, PDF, dowolny `.md` / `.txt`) do folderu `raw/` i możesz napisać krótko:

> *"zingestuj nowe źródła"*

**Claude:**
- Skanuje źródła w `raw/`
- Ocenia jakość (quality gate)
- Pyta co cię w nim interesuje
- Aktualizuje `wiki/` kaskadowo - dodaje, łączy, supersession (nowe info zastępuje stare z historią)

---

## Obsidian Skills od Kepano (CEO Obsidian)

Oficjalne *agent skills*, które uczą Claude'a poprawnej pracy z formatami Obsidian. 

**5 skills:**
1. `obsidian-markdown` - wikilinki, embeds, callouts, properties
2. `obsidian-bases` - views, filtry, formuły
3. `json-canvas` - pliki `.canvas`, nodes, edges
4. `obsidian-cli` - interakcja z vault przez CLI
5. `defuddle` - ekstrakcja czystego markdown ze stron www

🔗 **Repo:** [github.com/kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)

**Instalacja w vault z Claude Code:**

```bash
npx skills add git@github.com:kepano/obsidian-skills.git
```
*Albo ręcznie - skopiuj zawartość repo do folderu `.claude/` w vault'cie.*

---

## Kluczowe koncepty z warsztatu

- **LLM Wiki (Karpathy):** Obsidian to IDE. LLM to programista. Wiki to codebase. AI nie wyszukuje - AI buduje i utrzymuje bazę wiedzy.
- **3 warstwy:**
  - `raw/` - źródła (niemodyfikowalne, archiwum)
  - `wiki/` - synteza (Claude utrzymuje, kaskadowe aktualizacje)
  - `CLAUDE.md` - schema, reguły, persona
- **Ingest:** wrzuć źródło → "zingestuj" → Claude skanuje, ocenia jakość, pyta co Cię interesuje, aktualizuje wiki kaskadowo.
- **Supersession:** nowe info nie kasuje starego - jawnie zastępuje z historią. Widzisz co się zmieniło i dlaczego.
- **Persona:** `persona/` z opisem kim jesteś. Claude pisze w Twoim stylu i na Twoim poziomie technicznym.
- **Less is more:** zacznij od 4 folderów (`persona/`, `raw/`, `wiki/`, `_audit/`). Dodawaj złożoność gdy boli, nie wcześniej.

---

## Idź dalej (źródła)

- **Andrej Karpathy - LLM Wiki (gist):** [gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- **rohitg00 - LLM Wiki v2 (lifecycle extensions):** [gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)
- **Stefan Imhoff - Agentic Note-Taking:** [stefanimhoff.de/agentic-note-taking-obsidian-claude-code](https://stefanimhoff.de/agentic-note-taking-obsidian-claude-code)
- **Eleanor Konik - Claude + Obsidian + MCP:** [eleanorkonik.com/p/how-claude-obsidian-mcp-solved-my](https://www.eleanorkonik.com/p/how-claude-obsidian-mcp-solved-my)
- **Kyle Gao - CLAUDE.md w vault'cie:** [kyleygao.com/blog/2025/using-claude-code-with-obsidian](https://kyleygao.com/blog/2025/using-claude-code-with-obsidian)

---

## Szybki start

1. **Sklonuj / pobierz** ten szablon do folderu na dysku
2. **Otwórz** folder jako vault w Obsidian
3. **Otwórz** `bootstrap.md` i odpowiedz na pytania o siebie i temat vault'a
4. **Uruchom Claude Code** w folderze vault'a: `cd twoj-vault && claude`
5. **Powiedz:** "skonfiguruj vault" - Claude uzupełni pliki na podstawie Twoich odpowiedzi
6. **Wrzuć pierwsze źródło** do `raw/` i powiedz: "zingestuj"

---

## Jak to działa

```text
Ty wrzucasz źródło            Claude robi resztę
      |                               |
      ▼                               ▼
  raw/ (1:1)  ────────────>  wiki/ (synteza)
                                      |
                           ┌──────────┼──────────┐
                           ▼          ▼          ▼
                         index       log    cross-refs
```

**Twoja robota:** dodawanie źródeł + pytania. **Robota Claude'a:** synteza, cross-references, utrzymanie spójności, quality gate.


Przygotowałem gotowy szablon vault'a oparty na Karpathy LLM Wiki z rozszerzeniami z praktyki:

https://github.com/AI-Ninjas-Dojo/obsidian-ai-vault

Jak użyć:

1. Sklonuj lub pobierz ZIP: `git clone <https://github.com/AI-Ninjas-Dojo/obsidian-ai-vault.gi`
2. Otwórz folder jako vault w Obsidian
3. Otwórz `bootstrap.md` i odpowiedz na pytania o siebie i temat vault'a
4. Uruchom Claude Code w folderze: `cd obsidian-ai-vault && claude`
5. Powiedz: "skonfiguruj vault"
6. Wrzuć pierwsze źródło do `raw/` i powiedz: "zingestuj"

Co dostajesz w szablonie:

- [CLAUDE.md](http://claude.md/) ze schematem (instrukcja dla Claude'a jak pracować z vault'em)
- Struktura 3-warstwowa: raw/ (źródła) → wiki/ (synteza) → _audit/ (health-check)
- Persona - Claude pisze w twoim stylu, nie jak "assistant"
- Quality gate - Claude filtruje badziewie na wejściu
- Ingestion tracking - wiesz co już przetworzone
- Supersession - nowa info jawnie zastępuje starą (z historią)
- Bootstrap - krok po kroku konfiguracja vault'a pod ciebie

**TLDR; Po prostu pobierz projekt i powiedz Claude Code, by przeprowadził cię przez pierwszą konfigurację 🥷**

## Obsidian Skills od Kepano (CEO Obsidian)

Oficjalne agent skills uczące Claude'a jak poprawnie pracować z formatami Obsidian:

https://github.com/kepano/obsidian-skills

5 skills:

- obsidian-markdown - wikilinki, embeds, callouts, properties
- obsidian-bases - views, filtry, formuły
- json-canvas - pliki .canvas, nodes, edges
- obsidian-cli - interakcja z vault przez CLI
- defuddle - ekstrakcja czystego markdown ze stron www

Instalacja (w vault z Claude Code):

```
npx skills add git@github.com:kepano/obsidian-skills.git
```

Albo ręcznie: skopiuj zawartość repo do `/.claude` w vault'cie.

## Polecane pluginy Obsidian

- **Dataview** - queryowanie vault'a jak bazy danych. Frontmatter staje się queryowalny.
- **Web Clipper** - clipowanie stron z przeglądarki do `raw/`. Uwaga: domyślny folder to `Clippings/`, zmień na `raw/` w ustawieniach rozszerzenia (per-template).
- **Templater** - szablony nowych notatek z frontmatter.
- **Obsidian Git** - wersjonowanie vault'a w Git. Automatyczny backup.

## Narzędzia do integracji

## Kluczowe koncepty z warsztatu

**LLM Wiki (Karpathy):** Obsidian to IDE. LLM to programista. Wiki to codebase. AI nie wyszukuje - AI buduje i utrzymuje bazę wiedzy.

**3 warstwy:** raw/ (źródła, niemodyfikowalne) → wiki/ (synteza, Claude utrzymuje) → [CLAUDE.md](http://claude.md/) (schema, reguły)

**Ingest:** wrzuć źródło do raw/, powiedz "zingestuj". Claude skanuje, ocenia jakość, pyta co cię interesuje, aktualizuje wiki kaskadowo.

**Supersession:** nowe info nie kasuje starego - jawnie zastępuje z historią. Widzisz co się zmieniło i dlaczego.

**Persona:** folder persona/ z opisem kim jesteś. Claude pisze w twoim stylu i na twoim poziomie technicznym.

**Less is more:** zacznij od 4 folderów (persona/, raw/, wiki/, _audit/). Dodawaj złożoność gdy boli, nie wcześniej.

## Źródła i inspiracje

- Andrej Karpathy - LLM Wiki (gist): https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- rohitg00 - LLM Wiki v2 (lifecycle extensions): https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
- Stefan Imhoff - Agentic Note-Taking: https://www.stefanimhoff.de/agentic-note-taking-obsidian-claude-code/
- Eleanor Konik - Claude + Obsidian + MCP: https://www.eleanorkonik.com/p/how-claude-obsidian-mcp-solved-my
- Kyle Gao - [CLAUDE.md](http://claude.md/) w vault'cie: https://kyleygao.com/blog/2025/using-claude-code-with-obsidian/