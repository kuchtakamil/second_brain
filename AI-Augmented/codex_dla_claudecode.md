Codex Plugin dla Claude Code - oficjalny plugin

OpenAI wypuściło oficjalny plugin podpinający swojego agenta Codex pod Claude Code. Po instalacji w trakcie sesji Claude możesz wpisać /codex:review i dostać równoległą recenzję od OpenAI - na tym samym kodzie, w tym samym terminalu. Albo /codex:rescue żeby zdelegować zadanie do Codexa, który robi je w tle.

To rzadki przypadek, że konkurent shipuje swój produkt jako rozszerzenie produktu drugiej firmy. I to działa - bo żaden model nie ma monopolu na bycie najlepszym we wszystkim.

🔗 Repo: github.com/openai/codex-plugin-cc
Wymagania

    Claude Code

    Node.js 18.18+ (nodejs.org)

    Konto ChatGPT (Free wystarczy na start)

Instalacja

W aktywnej sesji Claude Code wpisujesz po kolei:

/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup

/codex:setup sprawdza czy Codex CLI jest zainstalowany. Jak nie, instaluje sam (npm install -g @openai/codex). W razie potrzeby dorzuć:

!codex login

(prefix ! w Claude Code uruchamia komendę w terminalu, dzięki czemu output trafia do kontekstu sesji - przydatne przy interaktywnym logowaniu).
Komendy slashowe które dostajesz

    /codex:review - standardowa recenzja kodu na bieżącej zmianie albo branchu

    /codex:adversarial-review - recenzja "zaczepna", podważa decyzje projektowe i założenia

    /codex:rescue - delegujesz zadanie do Codexa (debug, próba fixa, refactor)

    /codex:status - sprawdzasz progress odpalonych jobów Codexa

    /codex:result - wyświetla finalny output z zakończonych jobów

    /codex:cancel - zatrzymuje aktywne zadanie w tle

    /codex:setup - weryfikacja instalacji i autentykacji

Najważniejsze flagi

    --base <ref> - porównanie do konkretnego brancha (np. --base main)

    --background - odpal asynchronicznie (nie blokuje sesji)

    --wait - czekaj na zakończenie

    --resume / --fresh - kontynuuj poprzednią pracę albo zacznij od zera

    --model <name> - wybierasz model (np. gpt-5.4-mini, spark)

    --effort - poziom reasoning effort

Konfiguracja

Per-projekt: .codex/config.toml w katalogu głównym projektu

model = "gpt-5.4-mini"
model_reasoning_effort = "high"

User-level (globalnie): ~/.codex/config.toml. Ustawienia projektowe nadpisują globalne.
Kiedy realnie tego używasz

    Code review przed PR - Claude pisze kod, Codex robi second opinion zanim coś wypchniesz. Często łapie rzeczy, których Claude nie zauważył (i odwrotnie)

    Adversarial review przy decyzjach architektonicznych - przed major refactorem albo wyborem stacka. /codex:adversarial-review zmusza model do trybu "rozjedź to" - dostajesz argumenty przeciw, zanim wsiądziesz głęboko

    Delegacja długich zadań w tle - /codex:rescue --background na trudny bug, w tym czasie pracujesz dalej z Claude'em na innym tasku. /codex:status co jakiś czas żeby zobaczyć progress

    Drugie zdanie na PR z code review - czasem Claude i Codex widzą zupełnie inne problemy. Łączysz oba i masz pełniejszy obraz

Pro tip - zapisz protokół w CLAUDE.md

W CLAUDE.md projektu dorzuć regułę:

## Code review protocol

Przed każdym commitem zmiany:
1. Pokaż mi diff
2. Wywołaj /codex:review --base main
3. Pokaż wynik recenzji Codexa
4. Zaproponuj fix dla każdej zasadnej uwagi
5. Dopiero po akceptacji - commit

Claude od teraz domyślnie deleguje review do Codexa zanim zabierze się za commit. Łapiesz problemy zanim trafią do gita.
Inne ciekawe pluginy:

    fcakyon/claude-codex-settings - gotowy zestaw skills, hooks, agents pod Claude Code + Codex: github.com/fcakyon/claude-codex-settings

    m-ghalib/gemini-plugin-cc - to samo co plugin Codexa, ale dla Gemini CLI: github.com/m-ghalib/gemini-plugin-cc

Idź dalej (źródła)

    Oficjalne ogłoszenie OpenAI Developer Community: community.openai.com/t/introducing-codex-plugin-for-claude-code/1378186

    Repo z pełną dokumentacją: github.com/openai/codex-plugin-cc

    Mark Chen - "When Rivals Collaborate": medium.com/@markchen69/when-rivals-collaborate

    Nick Babich - "Codex plugin for Claude Code, why and how": uxplanet.org/codex-plugin-for-claude-code