Buduję aplikację z Claude Code. Pierwszy widok wygląda super. Generuję drugi - inne odstępy, inne radiusy, inny odcień szarości. Trzeci jeszcze inny.

Aplikacja wygląda jak Frankenstein.

Agent nie ma punktu odniesienia. Za każdym razem strzela na ślepo, dobiera kolory i typografię na bazie tego, co akurat ma w kontekście.

Najprostsze rozwiązanie - jeden plik DESIGN.md w katalogu projektu.

Markdown, w którym opisujesz:

→ Paletę kolorów z konkretnymi hex

→ Typografię - rodziny fontów, rozmiary, line-height

→ Spacing - skala 4px / 8px

→ Radiusy, cienie, bordery

→ Tone of voice w copy

→ Zasady dla komponentów - przyciski, karty, formularze

Claude Code i Cursor czytają ten plik przy każdej zmianie i trzymają się jednego języka wizualnego w całej aplikacji. Spójność spada z "modlę się żeby było OK" do "po prostu jest".



Wczoraj trafiłem na getdesign.md - kolekcja gotowych plików DESIGN.md inspirowanych 70+ markami:

→ Tech: Claude, Cursor, Linear, Notion, Vercel, Stripe, Figma

→ Automotive: BMW, Ferrari, Tesla, Lamborghini

→ Retail: Apple, Nike, Shopify, Starbucks, Airbnb

→ Fintech: Coinbase, Binance, Revolut, Wise

→ Media: Spotify, WIRED, The Verge

Pobierasz md, wrzucasz do projektu, agent buduje UI w wybranym stylu.

Tylko jedna rada - nie kopiuj 1:1.

Stylu Apple czy Linear w swojej aplikacji nie potrzebujesz. Potrzebujesz czegoś, co pasuje do Twojego produktu i Twoich użytkowników.

Lepsze użycie: weź 2-3 marki, wyciągnij z nich konkretne zasady (radius z Linear, spacing z Apple, typografia z WIRED) i zbuduj na tej bazie własny DESIGN.md.

Wtedy masz inspirację, a nie kopię.