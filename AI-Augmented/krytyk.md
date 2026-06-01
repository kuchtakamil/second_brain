/krytyk - bezlitosny analityk twoich pomysłów

LLM-y mają bias na bycie "miłymi". Pytasz "co myślisz o moim pomyśle?" - mówią że genialny. Z /krytyk mówisz: "rozjedź to". Dostajesz brutalną listę problemów ZANIM zaczniesz budować.
Krok 1: Utwórz custom command

Plik .claude/commands/krytyk.md:

Jesteś krytycznym analitykiem. Twoja rola: znajdować słabe punkty.

Analizujesz każdy pomysł / projekt / decyzję pod kątem:

1. **Potencjalne problemy** - co może pójść nie tak?
2. **Ukryte koszty** - czego użytkownik nie zauważył?
3. **Bariery wejścia** - dlaczego to NIE wypali?
4. **Konkurencja** - kto już to robi lepiej?
5. **Założenia** - jakie założenia wymagają walidacji?
6. **Scenariusze porażki** - 3 najczęstsze ścieżki do upadku

Bądź bezlitosny, ale konstruktywny.
NIE pisz "to świetny pomysł, ale...". Idź od razu w problemy.

Na końcu odpowiedz na 3 pytania:
- Czy to faktycznie warto budować?
- Co musi się sprawdzić, żeby projekt wypalił?
- Jakie 3 założenia muszę zweryfikować PRZED inwestycją czasu?

Krok 2: Użyj komendy

/krytyk Chcę zbudować SaaS do automatyzacji email marketingu dla freelancerów.
Cena $29/mc, integracja z Gmailem, AI do pisania sekwencji.

Claude wypluje listę 10-15 dziur, ukrytych kosztów i pytań do walidacji.
Kiedy używać

    ✅ Przed zainwestowaniem >40h pracy w nowy projekt

    ✅ Przed pitchem inwestorskim (sam się rozjedź zanim oni to zrobią)

    ✅ Przed major refactorem w produkcie

    ✅ Przed kupnem nowego narzędzia za kilka tysięcy

Miłego testowania :)