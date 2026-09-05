---
tags: [claude-code, elektromagnetyzm, rownania-maxwella, elektryczność]
date: 2026-06-30
moduł: 2
artykuł: "2.1-2.3"
---

# Elektryczność: ładunek, pole $\mathbf{E}$ i potencjał

> **Moduł 2 — Elektryczność.** W [[01-aparat-matematyczny|Module 1]] zbudowaliśmy narzędzia (gradient, dywergencja, strumień, cyrkulacja). Teraz pierwszy raz wkładamy do nich **fizykę**. Celem rozdziału jest pełne zrozumienie *prawej i lewej strony* pierwszego równania Maxwella:
> $$ \nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}. $$
> Co to jest $\rho$ (źródło), co to jest $\mathbf{E}$ (pole) i skąd bierze się stała $\varepsilon_0$ — oraz dlaczego w elektrostatyce $\nabla \times \mathbf{E} = \mathbf{0}$, co pozwoli wprowadzić potencjał.
>
> Zakładam, że wiesz, czym z grubsza jest ładunek i że „plusy odpychają się, a plus i minus przyciągają". Nie tłumaczę tego od zera — buduję na tym precyzyjny aparat.

Plan rozdziału:

1. [Ładunek, prawo Coulomba i stała $\varepsilon_0$](#1-ladunek-prawo-coulomba-i-stala-varepsilon_0)
2. [Gęstość ładunku $\rho$ — od punktów do pola skalarnego](#2-gestosc-ladunku-rho--od-punktow-do-pola-skalarnego)
3. [Pole elektryczne $\mathbf{E}$](#3-pole-elektryczne-mathbfe)
4. [Strumień $\mathbf{E}$ i zapowiedź prawa Gaussa](#4-strumien-mathbfe-i-zapowiedz-prawa-gaussa)
5. [Potencjał elektryczny i dlaczego $\nabla \times \mathbf{E} = \mathbf{0}$ w statyce](#5-potencjal-elektryczny-i-dlaczego-nabla-times-mathbfe--mathbf0-w-statyce)
6. [Co warto zapamiętać](#co-warto-zapamietac-z-tego-rozdzialu)

---

## 1. Ładunek, prawo Coulomba i stała $\varepsilon_0$

### Ładunek elektryczny

Ładunek to **fundamentalna właściwość materii** — taka jak masa, tyle że związana z oddziaływaniem elektromagnetycznym, a nie grawitacyjnym. Trzy fakty, które warto mieć jako twarde tło:

- **Dwa znaki.** Dodatni i ujemny. Jednoimienne się odpychają, różnoimienne przyciągają. (Masa ma tylko jeden „znak" — dlatego grawitacja tylko przyciąga. Elektryczność ma dwa, dlatego potrafi i przyciągać, i odpychać.)
- **Kwantyzacja.** Ładunek występuje w wielokrotnościach ładunku elementarnego $e = 1{,}602 \times 10^{-19}\ \text{C}$ (kulomb). Elektron ma $-e$, proton $+e$.
- **Zachowanie.** Całkowity ładunek w izolowanym układzie jest stały. Ładunku nie da się stworzyć ani zniszczyć — można go tylko przemieszczać. (To prawo zachowania okaże się w Module 5 ukryte wprost w równaniach Maxwella.)

### Prawo Coulomba

Siła między dwoma punktowymi ładunkami $q_1$ i $q_2$ odległymi o $r$:

$$
\mathbf{F} = \frac{1}{4\pi\varepsilon_0}\,\frac{q_1 q_2}{r^2}\,\hat{\mathbf{r}},
$$

gdzie $\hat{\mathbf{r}}$ to wektor jednostkowy wzdłuż linii łączącej ładunki. Przeczytaj tę formułę strukturalnie — każdy element coś znaczy:

- **$\propto q_1 q_2$** — siła rośnie z każdym z ładunków. Iloczyn dodatni (ładunki jednoimienne) → $\mathbf{F}$ wzdłuż $+\hat{\mathbf{r}}$ → odpychanie. Iloczyn ujemny → przyciąganie. Znak sam się załatwia.
- **$\propto 1/r^2$** — odwrotność kwadratu odległości. Identyczna struktura jak w grawitacji Newtona. To nie przypadek — wynika z tego, że żyjemy w 3 wymiarach (o tym w §4).
- **$\hat{\mathbf{r}}$** — siła działa wzdłuż prostej łączącej ładunki (oddziaływanie centralne).

### Stała $\varepsilon_0$

Czynnik $\dfrac{1}{4\pi\varepsilon_0}$ to po prostu **stała proporcjonalności** dopasowująca jednostki. Wielkość $\varepsilon_0$ nazywa się **przenikalnością elektryczną próżni**:

$$
\varepsilon_0 \approx 8{,}854 \times 10^{-12}\ \frac{\text{C}^2}{\text{N}\cdot\text{m}^2}, \qquad \frac{1}{4\pi\varepsilon_0} \approx 8{,}99 \times 10^{9}\ \frac{\text{N}\cdot\text{m}^2}{\text{C}^2}.
$$

Intuicja fizyczna $\varepsilon_0$: mówi, **jak silnie dany ładunek „produkuje" pole w próżni**. Pojawia się w mianowniku, więc im większe $\varepsilon_0$, tym *słabsze* pole na dany ładunek. Czynnik $4\pi$ wygląda na dziwactwo, ale jest celowy — to „pole powierzchni kuli jednostkowej", które (jak zobaczymy w §4) skraca się i sprawia, że prawo Gaussa wychodzi czyste, bez $4\pi$.

> **Dlaczego akurat $1/r^2$, a nie $1/r^3$?** Bo pole rozchodzi się w trzech wymiarach. Wyobraź sobie ładunek otoczony kulą o promieniu $r$. To, co ładunek „wysyła", rozkłada się równo na powierzchnię tej kuli, a powierzchnia rośnie jak $4\pi r^2$. Im dalej, tym bardziej „rozcieńczone" na coraz większej sferze — stąd spadek dokładnie jak $1/r^2$. Ta sama geometria stoi za grawitacją, natężeniem dźwięku i jasnością gwiazd. Zapamiętaj ten obraz — wróci jako prawo Gaussa.

---

## 2. Gęstość ładunku $\rho$ — od punktów do pola skalarnego

Prawo Coulomba dotyczy ładunków punktowych. Ale realny ładunek bywa „rozmazany" w objętości (naładowana kula, chmura elektronów, plazma). Żeby opisać to ciągłym aparatem z Modułu 1, wprowadzamy **gęstość ładunku objętościową**:

$$
\rho(\mathbf{r}) = \frac{\mathrm{d}Q}{\mathrm{d}V} \qquad \left[\frac{\text{C}}{\text{m}^3}\right].
$$

To jest **pole skalarne** — dokładnie ten obiekt, który zdefiniowaliśmy w [[01-aparat-matematyczny|§1 Modułu 1]]: każdemu punktowi przestrzeni przypisuje jedną liczbę (ile ładunku na metr sześcienny tam siedzi). I to jest właśnie $\rho$ z prawej strony pierwszego równania Maxwella.

Całkowity ładunek w obszarze $V$ odzyskujemy całkowaniem po objętości:

$$
Q = \iiint_V \rho\, \mathrm{d}V.
$$

> **Notacja na marginesie.** Gdy ładunek siedzi na powierzchni, używa się gęstości powierzchniowej $\sigma$ $[\text{C}/\text{m}^2]$, a gdy wzdłuż drutu — liniowej $\lambda$ $[\text{C}/\text{m}]$. To warianty tej samej idei; w równaniach Maxwella występuje objętościowa $\rho$.

Kluczowe przejście myślowe: **Coulomb operuje punktami, Maxwell operuje polami.** $\rho$ jest mostem — pozwala przełożyć „zbiór ładunków punktowych" na „gładkie pole skalarne", na którym działają dywergencja i całki z Modułu 1.

---

## 3. Pole elektryczne $\mathbf{E}$

### Definicja przez ładunek próbny

Zamiast mówić „ładunek $q_1$ działa siłą na ładunek $q_2$ na odległość", wprowadzamy pośrednika: ładunek **wypełnia przestrzeń wokół siebie polem**, a pole działa lokalnie na inne ładunki (ta zmiana myślenia padła już w [[00-po-co-nam-rownania-maxwella|Module 0]]).

Definicja operacyjna: wstaw w dane miejsce maleńki **ładunek próbny** $q$, zmierz siłę $\mathbf{F}$, jaka na niego działa, i podziel:

$$
\mathbf{E} = \lim_{q \to 0} \frac{\mathbf{F}}{q} \qquad \left[\frac{\text{N}}{\text{C}} = \frac{\text{V}}{\text{m}}\right].
$$

Granica $q \to 0$ jest istotna fizycznie: chcemy *zmierzyć* pole, a nie *zaburzyć* go — zbyt duży ładunek próbny sam rozpchnąłby źródła. Pole $\mathbf{E}$ jest **polem wektorowym**: w każdym punkcie strzałka mówiąca, w którą stronę i jak mocno popchnęłoby to dodatni ładunek.

### Pole ładunku punktowego

Łącząc definicję z prawem Coulomba, pole pojedynczego ładunku $Q$ to:

$$
\mathbf{E} = \frac{1}{4\pi\varepsilon_0}\,\frac{Q}{r^2}\,\hat{\mathbf{r}}.
$$

Dla $Q > 0$ strzałki wskazują **na zewnątrz** (pole „wypływa" z ładunku), dla $Q < 0$ — **do wewnątrz**. To jest dokładnie obraz „czystego źródła" $\mathbf{A} = (x,y,z)$ z [[01-aparat-matematyczny|§4 Modułu 1]], gdzie liczyliśmy dodatnią dywergencję. Linie pola elektrycznego:

- **zaczynają się na ładunkach dodatnich, kończą na ujemnych** (lub uciekają/przychodzą z nieskończoności);
- ich zagęszczenie obrazuje siłę pola.

To „rodzenie się linii na ładunkach" to wizualna treść tego, że $\nabla \cdot \mathbf{E} \neq 0$ tam, gdzie jest ładunek.

### Zasada superpozycji

Pole wielu ładunków to **suma wektorowa** pól od każdego z osobna:

$$
\mathbf{E} = \sum_i \mathbf{E}_i.
$$

To wynika z liniowości — i jest potężne, bo pozwala policzyć pole dowolnego rozkładu. Dla ciągłego rozkładu opisanego gęstością $\rho$ suma staje się całką:

$$
\mathbf{E}(\mathbf{r}) = \frac{1}{4\pi\varepsilon_0} \iiint \frac{\rho(\mathbf{r}')}{|\mathbf{r} - \mathbf{r}'|^2}\,\hat{\mathbf{r}}_{\,\mathbf{r}-\mathbf{r}'}\, \mathrm{d}V'.
$$

Wygląda groźnie, ale czyta się prosto: „posiekaj źródło na kawałeczki $\rho\,\mathrm{d}V'$, każdy traktuj jak ładunek punktowy, policz jego coulombowskie pole i wszystko zsumuj". To jest dosłowne połączenie §1 (Coulomb), §2 ($\rho$) i superpozycji.

> Liczenie pola tą całką bywa koszmarne. Właśnie dlatego dalej tak cenne okaże się **prawo Gaussa** — gdy rozkład ma symetrię, pozwala wyznaczyć $\mathbf{E}$ niemal bez całkowania.

---

## 4. Strumień $\mathbf{E}$ i zapowiedź prawa Gaussa

Tu spina się Moduł 1 z fizyką. Policzmy **strumień** pola $\mathbf{E}$ (pojęcie z [[01-aparat-matematyczny|§6 Modułu 1]]) przez **kulę** o promieniu $r$ otaczającą ładunek punktowy $Q$ umieszczony w jej środku.

Na powierzchni kuli pole ma wszędzie tę samą wartość $E = \dfrac{1}{4\pi\varepsilon_0}\dfrac{Q}{r^2}$ i jest wszędzie **prostopadłe** do powierzchni (równoległe do normalnej $\hat{\mathbf{n}}$). Strumień to więc po prostu wartość pola razy pole powierzchni kuli $4\pi r^2$:

$$
\Phi = \iint_S \mathbf{E}\cdot \mathrm{d}\mathbf{S} = E \cdot 4\pi r^2 = \frac{1}{4\pi\varepsilon_0}\frac{Q}{r^2}\cdot 4\pi r^2 = \frac{Q}{\varepsilon_0}.
$$

Zatrzymaj się na tym wyniku — jest piękny i nieprzypadkowy:

- **$r$ się skróciło.** Strumień **nie zależy od promienia** kuli. Bo pole słabnie jak $1/r^2$, a powierzchnia rośnie jak $r^2$ — i jedno dokładnie kasuje drugie. To geometryczna konsekwencja trójwymiarowości, ta sama, o której mówiłem przy „dlaczego $1/r^2$" w §1.
- **$4\pi$ zniknęło.** Teraz widać, po co był ten dziwny czynnik $4\pi$ w prawie Coulomba: po to, żeby tutaj się skrócił z powierzchnią kuli i zostawił czystą formułę.
- Można pokazać (rachunek pomijam), że wynik jest taki sam dla **dowolnej** zamkniętej powierzchni otaczającej $Q$, nie tylko kuli, oraz że ładunek **na zewnątrz** powierzchni daje zerowy wkład (tyle linii wchodzi, ile wychodzi).

Sumując po wszystkich ładunkach wewnątrz (superpozycja), dostajemy **prawo Gaussa w postaci całkowej**:

$$
\boxed{\;\iint_S \mathbf{E}\cdot \mathrm{d}\mathbf{S} = \frac{Q_{\text{wewn}}}{\varepsilon_0}\;}
$$

„Strumień pola elektrycznego przez dowolną zamkniętą powierzchnię = ładunek zamknięty w środku, podzielony przez $\varepsilon_0$." A teraz domknięcie całej linii rozumowania: zastosuj do lewej strony **twierdzenie o dywergencji** z [[01-aparat-matematyczny|§8 Modułu 1]], a $Q_{\text{wewn}}$ zapisz jako całkę z $\rho$ (z §2):

$$
\iiint_V (\nabla\cdot\mathbf{E})\,\mathrm{d}V = \iiint_V \frac{\rho}{\varepsilon_0}\,\mathrm{d}V.
$$

Równość zachodzi dla **dowolnego** obszaru $V$, więc funkcje podcałkowe muszą być równe w każdym punkcie:

$$
\boxed{\;\nabla\cdot\mathbf{E} = \frac{\rho}{\varepsilon_0}\;}
$$

**To jest pierwsze równanie Maxwella — i właśnie je wyprowadziliśmy od zera.** Z prawa Coulomba (§1) + pojęcia strumienia (Moduł 1) + twierdzenia o dywergencji (Moduł 1). Czyta się jednoznacznie: *źródłem pola elektrycznego są ładunki; tam gdzie $\rho > 0$, linie $\mathbf{E}$ się rodzą; tam gdzie $\rho < 0$, giną.*

---

## 5. Potencjał elektryczny i dlaczego $\nabla \times \mathbf{E} = \mathbf{0}$ w statyce

Mamy dywergencję $\mathbf{E}$. Ale (jak podkreślaliśmy w [[01-aparat-matematyczny|§5 i §10 Modułu 1]]) pole jest w pełni określone dopiero, gdy znamy też jego **rotację**. Jaka jest rotacja pola elektrostatycznego?

### Pole elektrostatyczne jest zachowawcze

Policzmy **cyrkulację** $\mathbf{E}$ po dowolnej zamkniętej pętli (pojęcie z [[01-aparat-matematyczny|§7 Modułu 1]]). Cyrkulacja siły $\mathbf{F} = q\mathbf{E}$ po pętli to praca wykonana przy obejściu pętli i powrocie do startu. Doświadczenie (i struktura pola coulombowskiego) mówią: **przy powrocie do punktu wyjścia praca wynosi zero**. Nie da się zbudować „elektrostatycznego perpetuum mobile", w którym ładunek krąży w kółko, zyskując energię. Zatem:

$$
\oint_C \mathbf{E}\cdot\mathrm{d}\mathbf{l} = 0 \quad \text{(dla pól statycznych)}.
$$

Teraz zastosuj **twierdzenie Stokesa** z [[01-aparat-matematyczny|§9 Modułu 1]]: skoro cyrkulacja po *każdej* pętli jest zerowa, to rotacja musi znikać w każdym punkcie:

$$
\boxed{\;\nabla \times \mathbf{E} = \mathbf{0} \quad \text{(elektrostatyka)}\;}
$$

Pole elektrostatyczne jest **bezwirowe**. Zapamiętaj zastrzeżenie „w statyce" — w [[01-aparat-matematyczny|Module 4]] zobaczymy, że zmienne w czasie pole magnetyczne *psuje* to zero (prawo Faradaya: $\nabla\times\mathbf{E} = -\partial\mathbf{B}/\partial t$). Bezwirowość to cecha elektryczności *bez zmian w czasie*.

### Potencjał jako konsekwencja

Tu wraca tożsamość z [[01-aparat-matematyczny|§5 Modułu 1]]: **gradient nigdy nie wiruje**, $\nabla\times(\nabla f) = \mathbf{0}$. Działa to też w drugą stronę — jeśli pole jest bezwirowe, to *musi* być gradientem pewnego pola skalarnego. To pole skalarne nazywamy (z umownym minusem) **potencjałem elektrycznym** $V$:

$$
\boxed{\;\mathbf{E} = -\nabla V\;} \qquad [V] = \text{wolt} = \text{V}.
$$

Dlaczego to wygodne? Bo zamiast trzech funkcji $(E_x, E_y, E_z)$ z więzami wystarczy **jedna funkcja skalarna** $V$ — a pełne pole odzyskujemy gradientem (operacją z [[01-aparat-matematyczny|§3 Modułu 1]]). Znak minus jest konwencją: pole wskazuje „w dół potencjału", więc dodatni ładunek samorzutnie stacza się od wysokiego $V$ do niskiego, jak kulka ze wzgórza.

Potencjał ładunku punktowego (przyjmując $V=0$ w nieskończoności):

$$
V = \frac{1}{4\pi\varepsilon_0}\frac{Q}{r}.
$$

Zwróć uwagę: $V \propto 1/r$, podczas gdy $E \propto 1/r^2$ — bo gradient (różniczkowanie po $r$) „dokłada" jedną potęgę $r$ w mianowniku. To spójne: $\mathbf{E} = -\nabla V$.

### Powierzchnie ekwipotencjalne

Zbiory punktów o stałym $V$ to **powierzchnie ekwipotencjalne**. Z [[01-aparat-matematyczny|§3 Modułu 1]] wiemy, że gradient jest prostopadły do poziomic — więc **linie pola $\mathbf{E}$ są zawsze prostopadłe do powierzchni ekwipotencjalnych**. Dla ładunku punktowego ekwipotencjały to koncentryczne sfery, a linie pola — promienie. Mapa pola elektrycznego to dokładnie „mapa topograficzna" potencjału: linie pola biegną prostopadle do warstwic, w stronę malejącego $V$.

---

## Co warto zapamiętać z tego rozdziału

- **Ładunek**: dwa znaki, skwantowany ($e = 1{,}602\times10^{-19}$ C), zachowany. Prawo Coulomba $\mathbf{F} = \frac{1}{4\pi\varepsilon_0}\frac{q_1q_2}{r^2}\hat{\mathbf{r}}$ — odwrotność kwadratu wynika z geometrii 3D.
- **$\varepsilon_0$** (przenikalność elektryczna próżni) to stała sprzęgająca ładunek z polem; czynnik $4\pi$ jest tak dobrany, by skrócić się z powierzchnią kuli w prawie Gaussa.
- **$\rho$** to gęstość ładunku — **pole skalarne** $[\text{C}/\text{m}^3]$, most między „punktami" Coulomba a „polami" Maxwella; $Q = \iiint_V \rho\,\mathrm{d}V$.
- **$\mathbf{E}$** to **pole wektorowe**, $\mathbf{E} = \lim_{q\to0}\mathbf{F}/q$. Pole ładunku punktowego: $\frac{1}{4\pi\varepsilon_0}\frac{Q}{r^2}\hat{\mathbf{r}}$. Linie zaczynają się na „+", kończą na „−". Obowiązuje superpozycja.
- **Strumień $\mathbf{E}$ przez kulę = $Q/\varepsilon_0$, niezależnie od promienia** (bo $1/r^2$ kasuje się z $4\pi r^2$) → prawo Gaussa $\iint_S \mathbf{E}\cdot\mathrm{d}\mathbf{S} = Q_{\text{wewn}}/\varepsilon_0$ → przez tw. o dywergencji → **pierwsze równanie Maxwella** $\nabla\cdot\mathbf{E} = \rho/\varepsilon_0$.
- W **elektrostatyce** $\oint_C \mathbf{E}\cdot\mathrm{d}\mathbf{l} = 0$ → przez tw. Stokesa → $\nabla\times\mathbf{E} = \mathbf{0}$ (pole bezwirowe). To zero psuje się dopiero przy zmiennym $\mathbf{B}$ (Faraday).
- Bezwirowość pozwala wprowadzić **potencjał** $V$: $\mathbf{E} = -\nabla V$. Jedna funkcja skalarna zamiast trzech składowych. Linie pola $\perp$ powierzchnie ekwipotencjalne.

---

**Poprzedni artykuł:** [[01-aparat-matematyczny|Moduł 1 — Aparat matematyczny]]
**Następny artykuł:** Moduł 3 — *Magnetyzm: pole $\mathbf{B}$, siła Lorentza, prąd $\mathbf{J}$ i brak monopoli* (drugie pole i jego źródła — z istotną różnicą: $\nabla\cdot\mathbf{B}=0$).
