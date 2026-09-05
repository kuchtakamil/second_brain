---
tags: [claude-code, plan, elektromagnetyzm]
date: 2026-06-28
---

# Plan serii: Droga do zrozumienia równań Maxwella

**Założenia:** czytelnik dorosły, zna podstawy fizyki (mechanika, pojęcie pola, ładunku, prądu na poziomie ogólnym). Pomijamy banały. Skupiamy się na budowaniu intuicji + aparatu matematycznego, tak by cztery równania na końcu były oczywiste, a nie magiczne. Każdy punkt = osobny artykuł (zasada: wiele małych notatek).

Istniejąca notatka [[równania-maxwella-wyjaśnione]] to **cel/punkt docelowy** serii — reszta artykułów do niej prowadzi.

---

## Prompt dla modelu piszącego artykuły

> Poniższa instrukcja obowiązuje przy pisaniu **każdego** kolejnego artykułu serii. Przekaż ją (lub wskaż ten plik) modelowi wykonującemu zadanie.

Piszesz kolejny artykuł serii „Droga do zrozumienia równań Maxwella" według tego planu. Zanim napiszesz cokolwiek, przeczytaj ten plan **oraz dotychczasowe artykuły** w `Fizyka/rownania-maxwella/` — nowy tekst ma być ich spójną kontynuacją: te same oznaczenia, ten sam ton, ten sam poziom.

**Treść — kompleksowo i wyczerpująco:**

- Omów **wszystkie** zagadnienia z punktu planu i wyczerp temat: po lekturze czytelnik nie powinien musieć doczytywać nigdzie indziej niczego, co jest potrzebne do dalszych modułów.
- **Nie pomijaj trudnych miejsc** — to najczęstszy błąd podręczników. Każde trudne miejsce rozłóż na trójkę: *intuicja → formalizm → policzony przykład* (z konkretnymi liczbami, doprowadzony do końca).
- Każdy nowy symbol definiuj przy pierwszym użyciu. Żadne twierdzenie nie może być tylko *ogłoszone* — zawsze dodaj uzasadnienie, choćby intuicyjne („dlaczego to prawda").
- Jawnie prostuj **typowe pułapki i nieporozumienia** związane z tematem (sekcje typu „Pułapka: …").

**Forma — intuicyjnie i zrozumiale:**

- Czytelnik: dorosły, zna podstawy fizyki, nie jest matematykiem. Najpierw obraz/analogia fizyczna (woda, teren, przepływ), potem wzór — nigdy odwrotnie.
- Pisz po polsku, drugą osobą („wyobraź sobie…"), bez banałów i bez akademickiej sztywności; angielskie terminy podawaj w nawiasie przy pierwszym wystąpieniu.
- Struktura artykułu: frontmatter → wstęp z kontekstem serii → plan rozdziału (lista linków) → ponumerowane sekcje → po każdym pojęciu, gdzie to ma sens, sekcja „Zapowiedź Maxwella" (po co to w równaniach) → „Co warto zapamiętać z tego rozdziału" (lista) → linki *Poprzedni/Następny artykuł*.
- Zawsze pokazuj **związki**: odwołuj się wstecz do pojęć z poprzednich artykułów (wikilinkami `[[...]]`) i zapowiadaj, gdzie pojęcie wróci.

**Konwencje techniczne:**

- Plik: `Fizyka/rownania-maxwella/NN-krotki-slug.md` (numeracja ciągła). Frontmatter jak w istniejących artykułach: `tags: [claude-code, elektromagnetyzm, rownania-maxwella, ...]`, `date`, `moduł`, `artykuł` (zakres punktów planu, np. `"3.1-3.4"`). Jeden moduł = jeden plik.
- Matematyka **wyłącznie** w `$...$` / `$$...$$` (nigdy `\(...\)` ani `\[...\]`). Nie używaj makr, których Obsidian nie renderuje (np. `\oiint` — zamiast tego `\iint`/`\oint` z dopiskiem słownym, że powierzchnia/pętla jest zamknięta). Wektory: `\mathbf{E}`, `\mathbf{B}`.
- Po napisaniu sprawdź: czy każdy symbol, który pojawi się w docelowych czterech równaniach, został już wyjaśniony lub ma jasno wskazane miejsce w serii, gdzie zostanie wyjaśniony.

---

## Moduł 0 — Mapa i motywacja

**0.1. Po co nam równania Maxwella i co właściwie opisują**
Czym jest pole jako byt fizyczny (a nie tylko wykres). Zapowiedź: 4 równania, 2 pola (E, B), jeden wniosek — światło. Krótka mapa zależności całej serii.

---

## Moduł 1 — Aparat matematyczny (analiza wektorowa)

To jest serce przygotowania. Bez tego równania to symbole.

**1.1. Pola skalarne i wektorowe**
Temperatura w pokoju vs. wiatr. Wizualizacja pola wektorowego (strzałki, linie pola).

**1.2. Pochodne cząstkowe i operator ∇ (nabla)**
∂/∂x jako „zmiana w jednym kierunku”. Nabla jako wektor operatorów.

**1.3. Gradient — kierunek najszybszego wzrostu**
∇f. Intuicja: stok wzgórza. Po co w elektromagnetyzmie (potencjał → pole).

**1.4. Dywergencja — „źródłowość” pola**
∇·A. Intuicja: kran i odpływ, strumień netto z punktu. Dlaczego dodatnia dywergencja = źródło.

**1.5. Rotacja — „wirowość” pola**
∇×A. Intuicja: młynek/wirek w strumieniu. Pole wirowe vs. bezźródłowe.

**1.6. Strumień pola przez powierzchnię (flux)**
Ile pola „przepływa” przez powierzchnię. Powierzchnie otwarte vs. zamknięte. Klucz do postaci całkowej praw Gaussa.

**1.7. Cyrkulacja i całka krzywoliniowa po pętli**
∮ wokół zamkniętej pętli. Klucz do postaci całkowej Faradaya i Ampère'a.

**1.8. Twierdzenie Gaussa-Ostrogradskiego (o dywergencji)**
Łączy strumień przez zamkniętą powierzchnię z dywergencją w objętości. Most: postać całkowa ↔ różniczkowa praw Gaussa.

**1.9. Twierdzenie Stokesa**
Łączy cyrkulację po pętli z rotacją na powierzchni. Most całkowa ↔ różniczkowa dla Faradaya i Ampère'a.

**1.10. Drugie pochodne: laplasjan i tożsamości operatora ∇**
∇² = ∇·∇ (laplasjan, dla pola skalarnego i wektorowego), tożsamości ∇·(∇×A) = 0 i ∇×(∇f) = 0 oraz kluczowa ∇×(∇×A) = ∇(∇·A) − ∇²A. **Twardy wymóg dla 6.2** — bez podwójnej rotacji nie da się wyprowadzić równania falowego. (Dwie pierwsze tożsamości są już zasygnalizowane w [[01-aparat-matematyczny]] — do rozwinięcia tam lub jako krótki osobny artykuł przed Modułem 6.)

> Po Module 1 czytelnik rozumie *każdy symbol* w równaniach. Reszta to fizyka.

---

## Moduł 2 — Elektryczność

**2.1. Ładunek, prawo Coulomba, gęstość ładunku ρ**
Krótko (zna podstawy) — nacisk na ρ jako pole skalarne i na ε₀ jako stałą natury.

**2.2. Pole elektryczne E**
Definicja przez siłę na ładunku próbnym. Linie pola, superpozycja. Powiązanie z gradientem potencjału.

**2.3. (opcjonalnie) Potencjał elektryczny**
Dlaczego pole elektrostatyczne jest „bezwirowe” (∇×E = 0 w statyce) — przygotowuje kontrast z Faradayem.

---

## Moduł 3 — Magnetyzm

**3.1. Pole magnetyczne B i siła Lorentza**
B definiowane przez działanie na poruszający się ładunek. Czemu B jest „inne” niż E.

**3.2. Prąd elektryczny i gęstość prądu J**
J jako pole wektorowe. Prąd jako źródło pola magnetycznego (zapowiedź Ampère'a). Stała μ₀.

**3.3. Brak monopoli magnetycznych**
Dlaczego linie B są zawsze zamknięte — przygotowuje ∇·B = 0.

**3.4. Zasada zachowania ładunku i równanie ciągłości**
∇·J = −∂ρ/∂t: ładunek nie znika — może tylko odpłynąć, a lokalny ubytek ρ musi być widoczny jako wypływ J. Pierwsze fizyczne zastosowanie dywergencji z 1.4. **Kluczowy składnik 5.4**: prawo Ampère'a bez poprawki Maxwella łamie ciągłość ładunku — to stąd bierze się prąd przesunięcia.

---

## Moduł 4 — Sprzężenie pól (indukcja)

**4.1. Strumień magnetyczny i indukcja elektromagnetyczna**
Eksperyment Faradaya: zmienne B → napięcie. Reguła Lenza i znak minus.

**4.2. Prawo Faradaya jako most do równań**
Od „zmiana strumienia” do ∇×E = −∂B/∂t.

---

## Moduł 5 — Cztery równania, jedno po drugim

(Każde: intuicja → postać całkowa → postać różniczkowa → przykład.)

**5.1. Prawo Gaussa dla elektryczności** — ∇·E = ρ/ε₀
**5.2. Prawo Gaussa dla magnetyzmu** — ∇·B = 0
**5.3. Prawo Faradaya** — ∇×E = −∂B/∂t
**5.4. Prawo Ampère'a + prąd przesunięcia (poprawka Maxwella)** — ∇×B = μ₀J + μ₀ε₀ ∂E/∂t
Osobny nacisk na *dlaczego* Maxwell dodał człon ∂E/∂t (niespójność, ciągłość ładunku, kondensator).

---

## Moduł 6 — Synteza i konsekwencje

**6.1. Postać całkowa vs. różniczkowa — to samo dwoma językami**
Spięcie Modułu 1 (tw. Gaussa i Stokesa) z czterema równaniami.

**6.2. Wyprowadzenie równania falowego i fale elektromagnetyczne**
Jak z czterech równań w próżni wypada fala. c = 1/√(μ₀ε₀).

**6.3. Wniosek: światło to fala elektromagnetyczna**
Domknięcie serii — widmo EM, radio, optyka.

**6.4. (opcjonalnie) Energia pola i wektor Poyntinga**
Gęstość energii pól E i B, przepływ energii S = (1/μ₀) E×B. Odpowiada na pytanie „gdzie fizycznie siedzi energia" i domyka obraz fali EM jako fali *niosącej* energię (światło słoneczne grzeje).

**6.5. (opcjonalnie) Epilog: co dalej**
Zajawki bez pełnego wykładu, jako mapa dalszej nauki: równania Maxwella w materii (pola D i H, polaryzacja, magnetyzacja), potencjały i cechowanie, oraz najgłębszy wniosek — B jako relatywistyczny efekt E (magnetyzm = elektryczność + szczególna teoria względności).

---

## Kolejność czytania

0 → 1 (cały, fundament) → 2 → 3 → 4 → 5 → 6.
Moduły 2 i 3 są niezależne (można zamienić). Moduł 1 jest twardym wymaganiem dla 5 i 6; punkt 1.10 (laplasjan) — dla 6.2.

**Łącznie:** ~28 punktów planu (Moduł 1 to ~10 z nich — celowo, bo to najczęstsza luka). W praktyce seria powstaje jako **jeden plik na moduł**, czyli ~7 artykułów.

---

## Stan realizacji

- [x] Moduł 0 → [[00-po-co-nam-rownania-maxwella]]
- [x] Moduł 1 (1.1–1.9) → [[01-aparat-matematyczny]] — **1.10 do dopisania** (tam lub osobno przed Modułem 6)
- [x] Moduł 2 → [[02-elektrycznosc]]
- [ ] Moduł 3 (3.1–3.4)
- [ ] Moduł 4 (4.1–4.2)
- [ ] Moduł 5 (5.1–5.4)
- [ ] Moduł 6 (6.1–6.3 + opcjonalne 6.4–6.5)