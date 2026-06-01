Polecane pluginy, z którymi pracuję w Obsidian
Po dzisiejszym warsztacie o Obsidianie dostałem kilka wiadomości z pytaniem "a jakich pluginów używasz?". Rozpiszę konkretnie - to są pluginy, z którymi ja faktycznie pracuję w swoim vault'cie.
---
Must-have (używam codziennie):
Dataview → https://obsidian.md/plugins?id=dataview
SQL-like zapytania na frontmatter notatek. Bez tego metadata w YAML to martwe dane. Ja queryuję confidence levels, źródła, ingested status - vault staje się bazą danych. Fundament każdego poważnego workflow.
Omnisearch → https://obsidian.md/plugins?id=omnisearch
Fuzzy search który waży wyniki (tytuł > nagłówek > treść). Łapie literówki, odmiany. Bonus: indeksuje PDF-y z OCR. Native search Obsidiana to przy tym zabawka.
Obsidian Git → https://obsidian.md/plugins?id=obsidian-git
Auto-commit co X minut, auto-pull on open, UI do commit/push bez terminala. Mój vault jest w GitHub repo - plugin daje darmowy version history i sync między urządzeniami. Na mobile trochę kapryśny, ale działa.
Terminal → https://obsidian.md/plugins?id=terminal
Wbudowany terminal w Obsidianie. Odpalam Claude Code prosto z vault'a - working directory już jest tam gdzie trzeba, zero przełączania kontekstu. Edytujesz notatkę Claudem, widzisz zmianę w Obsidianie live.
---
Polecane do doinstalowania:
Templater → https://obsidian.md/plugins?id=templater-obsidian
Szablony z logiką (JS, prompty, daty). Jeden hotkey i masz nową stronę z poprawnym frontmatter, datą, tagami. Odpada ręczne wypełnianie YAML-a przy każdej notatce.
Local Images Plus → https://obsidian.md/plugins?id=obsidian-local-images-plus
Automatycznie ściąga obrazki z linków zewnętrznych do vault'a. Must-have jeśli używasz Web Clippera - bez tego grafiki znikają offline albo po usunięciu źródła.
Iconize → https://obsidian.md/plugins?id=obsidian-icon-folder
Custom ikony na folderach w sidebarze. U mnie raw/ ma 📥, wiki/ ma 📚, persona/ ma 👤. Kosmetyka, ale przy 10+ folderach robi różnicę w nawigacji.
Hover Editor → https://obsidian.md/plugins?id=obsidian-hover-editor
Cmd+hover na wikilink i widzisz treść w popupie bez klikania. Przy grafach wiedzy z dużą liczbą linków eksploracja staje się dużo płynniejsza.
---
Warte obserwacji (jeszcze nie mam, ale mam na oku):
Smart Connections → https://obsidian.md/plugins?id=smart-connections
Semantyczne "Similar notes" przez embeddingi. Ma sens jak masz 200+ stron i keyword search przestaje wystarczać.
Excalidraw → https://obsidian.md/plugins?id=obsidian-excalidraw-plugin
Rysowanie diagramów natywnie w Obsidianie, pliki żyją w vault'cie. Dobre do wizualizacji architektur bezpośrednio w notatkach.
Remotely Save → https://obsidian.md/plugins?id=remotely-save
Sync przez S3, R2, Dropbox, WebDAV z E2E encryption. Alternatywa dla Git albo iCloud - szczególnie jeśli masz WebDAV na własnym serwerze.
---
Czego unikać:
1. Pluginów AI chat w Obsidianie (Copilot, Smart Composer) - Claude Code przez plugin Terminal jest potężniejszy i ma pełny dostęp do vault'a. Natywne AI pluginy mają ograniczony kontekst.
2. Instalowania 20 pluginów naraz - każdy to zależność i potencjalny bug. Testuj 1-2 na raz, odinstaluj co nie działa.
3. Pluginów zastępujących core features - Obsidian szybko rozwija Bases, Properties, Web Clipper. Zanim instalujesz zewnętrzny plugin, sprawdź czy natywnie tego nie dodali.
A wy po warsztacie - co już zainstalowaliście u siebie? Podzielcie się z czym wy działacie! :)