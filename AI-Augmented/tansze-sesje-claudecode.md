W Claude Code trzymam się jednej zasady: nie każdy task musi lecieć na Opusie. To najprostszy sposób, żeby utrzymać limity bez tracenia jakości tam, gdzie jest naprawdę potrzebna.

W definicji każdego skill albo agenta (frontmatter w pliku) możesz dać model: haiku albo model: sonnet. Subagent leci wtedy na konkretnym modelu zamiast dziedziczyć po głównej sesji. Jak to dzielę u siebie:

Haiku - mechaniczne taski, gdzie nie ma czego sądzić. Parsowanie outputu, czyszczenie list, formatowanie, ekstrakcja danych z dokumentu, prosta klasyfikacja. Wszystko gdzie dobry pattern matching wystarcza i model nie musi nic kombinować.

Sonnet - research, eksploracja kodu w średnich repo, synteza materiałów, przegląd dokumentacji, code review. Tu już potrzebujesz inteligencji, ale nie najgrubszej.

Opus - planowanie projektu, decyzje z trade-offami, architektura, debugowanie nietypowych błędów. Praca, gdzie jakość naprawdę się liczy i błąd dużo kosztuje. Tu zostaję na Opusie i nie kombinuję.

Globalnie wszystkie subagenty ustawisz zmienną CLAUDE_CODE_SUBAGENT_MODEL - przydatne, jeśli jeszcze nie chce Ci się oznaczać każdego agenta osobno. Per-agent daje większą kontrolę, globalne jest do szybkiego przetestowania.

Dokumentacja modeli: https://code.claude.com/docs/en/model-config

1M context - używać, ale z głową

Sonnet z 1M tokenów to świetna sprawa w długich sesjach research, gdzie chcesz mieć cały projekt, dokumentację i historię chatu w jednym miejscu. Nie odpuszczam tego.

Ale obserwuję jedno: jakość zauważalnie spada, kiedy raw kontekst rośnie ponad 200-400k tokenów. Model zaczyna gubić wątki, mieszać szczegóły, halucynować rzeczy, których wcześniej w sesji nie było. Plus każdy turn na takim kontekście kosztuje swoje.

Moja praktyka: pracuję w 1M, ale ręcznie kompaktuję sesję przy ~200-400k komendą /compact. Tracę raw historię, zachowuję syntezę tego, co zrobiliśmy. Model wraca do peak performance, koszty maleją, sesja może lecieć dalej.

Jeśli zapomnisz manualnej kompakcji, jest też auto-compact - domyślnie odpala się ~95% kontekstu, możesz go obniżyć w .claude/settings.json przez CLAUDE_AUTOCOMPACT_PCT_OVERRIDE (np. 80). Górny limit i tak jest twardy w okolicach 83%.

Co z tego wynika praktycznie

Przejrzyj swoje skille i agenty - zaznacz, który "potrzebuje Opusa", a który spokojnie pójdzie na Haiku albo Sonneta

Dodaj model: haiku w frontmatterze tych prostych - zobaczysz różnicę w zużyciu tokenów na plus.

W długich sesjach pilnuj okolic 200-400k i kompaktuj manualnie zanim model zacznie gubić wątki

Źródła:

Konfiguracja modeli i subagentów: https://code.claude.com/docs/en/model-config

Subagenty: https://code.claude.com/docs/en/sub-agents

Env vars (auto-compact, CLAUDE_CODE_SUBAGENT_MODEL): https://code.claude.com/docs/en/env-vars