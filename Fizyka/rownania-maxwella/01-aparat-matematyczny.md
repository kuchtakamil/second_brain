---
tags: [claude-code, elektromagnetyzm, rownania-maxwella, matematyka]
date: 2026-06-29
moduł: 1
artykuł: "1.1-1.9"
---

# Aparat matematyczny: analiza wektorowa od zera do twierdzenia Stokesa

> **Moduł 1 — Aparat matematyczny.** To najdłuższy i najważniejszy rozdział całej serii. Po nim **każdy symbol** z równań Maxwella — $\nabla$, kropka, krzyżyk, całka po powierzchni i po pętli — będzie dla Ciebie konkretną, wyobrażalną ideą, a nie dekoracją.
>
> Zakładam, że znasz pochodną zwykłej funkcji jednej zmiennej ($\mathrm{d}f/\mathrm{d}x$ jako „tempo zmiany") i potrafisz dodawać wektory. Reszta — pochodne cząstkowe, dywergencja, rotacja, strumień, cyrkulacja, twierdzenia całkowe — jest zbudowana tutaj od podstaw. Nie pomijam trudnych miejsc; zamiast tego rozkładam je na intuicję + formalizm + przykład.

Plan rozdziału:

1. [Pola skalarne i wektorowe](#1-pola-skalarne-i-wektorowe)
2. [Pochodne cząstkowe i operator ∇](#2-pochodne-czastkowe-i-operator-nabla)
3. [Gradient](#3-gradient--kierunek-najszybszego-wzrostu)
4. [Dywergencja](#4-dywergencja--ile-pola-wyplywa-z-punktu)
5. [Rotacja](#5-rotacja--ile-pole-wiruje-wokol-punktu)
6. [Strumień przez powierzchnię](#6-strumien--ile-pola-przechodzi-przez-powierzchnie)
7. [Cyrkulacja po pętli](#7-cyrkulacja--ile-pola-krazy-wzdluz-petli)
8. [Twierdzenie Gaussa–Ostrogradskiego](#8-twierdzenie-gaussaostrogradskiego)
9. [Twierdzenie Stokesa](#9-twierdzenie-stokesa)
10. [Jak to wszystko spina równania Maxwella](#10-jak-to-spina-rownania-maxwella)

---

## 1. Pola skalarne i wektorowe

W [[00-po-co-nam-rownania-maxwella|Module 0]] padło, że pole to przestrzeń wypełniona wartościami. Teraz nadajmy temu precyzję.

**Pole skalarne** przypisuje **każdemu punktowi przestrzeni jedną liczbę.** Formalnie to funkcja trzech zmiennych:

$$
f(x, y, z) \in \mathbb{R}.
$$

Przykłady: temperatura w pokoju, ciśnienie w atmosferze, gęstość ładunku $\rho$ (z prawej strony pierwszego równania Maxwella). Pole skalarne wizualizujemy **powierzchniami poziomicowymi** (izopowierzchniami) — zbiorami punktów o tej samej wartości, jak warstwice na mapie.

**Pole wektorowe** przypisuje **każdemu punktowi przestrzeni wektor** (kierunek + długość):

$$
\mathbf{A}(x, y, z) = \big(A_x(x,y,z),\; A_y(x,y,z),\; A_z(x,y,z)\big).
$$

Czyli pole wektorowe to tak naprawdę **trzy pola skalarne naraz** — po jednym dla każdej składowej. Przykłady: prędkość wiatru, prąd wody w rzece, pole elektryczne $\mathbf{E}$, pole magnetyczne $\mathbf{B}$.

### Linie pola

Pole wektorowe wizualizujemy **liniami pola**: to krzywe, które w każdym punkcie są styczne do wektora pola. Reguły czytania linii pola — będą wracać przez całą serię:

- **Kierunek** linii = kierunek pola w danym punkcie.
- **Zagęszczenie** linii = siła pola (gęściej = mocniej).
- Linie pola **nie mogą się przecinać** (w punkcie przecięcia pole miałoby dwa kierunki naraz — sprzeczność).

Dwie jakościowo różne „rzeczy", które linie pola mogą robić, są tak ważne, że mają własne nazwy i własne operatory matematyczne:

- linie mogą **wypływać ze źródeł / wpływać do ujść** → to zmierzy **dywergencja**;
- linie mogą **zakręcać i wirować** → to zmierzy **rotacja**.

Cały Moduł 1 zmierza do precyzyjnego zdefiniowania tych dwóch pojęć i powiązania ich z całkami.

---

## 2. Pochodne cząstkowe i operator ∇ (nabla)

### Pochodna cząstkowa

Pole zależy od trzech zmiennych $(x, y, z)$. Chcemy mówić o „tempie zmiany" — ale w którą stronę? Stąd **pochodna cząstkowa**: pochodna względem jednej zmiennej, przy **pozostałych traktowanych jak stałe**.

Zapis $\partial f / \partial x$ (czytamy „de po de iks") oznacza: jak szybko zmienia się $f$, gdy ruszamy *tylko* wzdłuż osi $x$, zamrażając $y$ i $z$:

$$
\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h,\, y,\, z) - f(x,\, y,\, z)}{h}.
$$

To dokładnie ta sama idea co zwykła pochodna — tylko że poruszamy się po jednej osi spośród trzech. Symbol „$\partial$" (zamiast „$\mathrm{d}$") to przypomnienie: „jest więcej zmiennych, ale tę jedną teraz różniczkuję".

> **Przykład.** Dla $f = x^2 y + z$:
> $\dfrac{\partial f}{\partial x} = 2xy$, $\quad \dfrac{\partial f}{\partial y} = x^2$, $\quad \dfrac{\partial f}{\partial z} = 1.$
> Przy liczeniu $\partial/\partial x$ człon $z$ jest stałą (znika), a $y$ to też stała mnożąca.

Symbol $\partial \mathbf{B} / \partial t$ w równaniach Maxwella to po prostu pochodna cząstkowa po **czasie**: jak szybko zmienia się pole magnetyczne w ustalonym punkcie przestrzeni.

### Nabla jako wektor operatorów

A teraz sztuczka notacyjna, która porządkuje całą resztę. Definiujemy **operator nabla** jako „wektor, którego składowymi są instrukcje różniczkowania":

$$
\nabla = \left( \frac{\partial}{\partial x},\; \frac{\partial}{\partial y},\; \frac{\partial}{\partial z} \right).
$$

Sam w sobie $\nabla$ nic nie liczy — to wektor *czekający*, aż coś na niego podziałamy. Genialne jest to, że **wszystkie trzy podstawowe operacje analizy wektorowej powstają z trzech sposobów „pomnożenia" tego wektora**:

| Działanie | Zapis | Wejście → wyjście | Mierzy |
|---|---|---|---|
| mnożenie przez skalar | $\nabla f$ | skalar → **wektor** | gradient (wzrost) |
| iloczyn skalarny | $\nabla \cdot \mathbf{A}$ | wektor → **skalar** | dywergencję (źródłowość) |
| iloczyn wektorowy | $\nabla \times \mathbf{A}$ | wektor → **wektor** | rotację (wirowość) |

To nie przypadek i nie zbieg okoliczności notacyjny — to dlatego, że gradient, dywergencja i rotacja *naprawdę* zachowują się jak, odpowiednio, mnożenie wektora przez liczbę, iloczyn skalarny i iloczyn wektorowy. Rozłóżmy je po kolei.

---

## 3. Gradient — kierunek najszybszego wzrostu

Bierzemy **pole skalarne** $f$ i działamy na nie operatorem $\nabla$ tak, jakbyśmy mnożyli wektor przez liczbę:

$$
\nabla f = \left( \frac{\partial f}{\partial x},\; \frac{\partial f}{\partial y},\; \frac{\partial f}{\partial z} \right).
$$

Wynik jest **wektorem** (z pola skalarnego zrobiliśmy pole wektorowe).

> **Przykład.** Dla $f = x^2 y + z$ z §2 wszystkie trzy pochodne już policzyliśmy, więc:
> $\nabla f = (2xy,\; x^2,\; 1).$
> W punkcie $(1, 1, 0)$ gradient wynosi $(2, 1, 1)$: pole rośnie najszybciej właśnie w tym kierunku, w tempie $|\nabla f| = \sqrt{6}$ na jednostkę drogi.

### Intuicja: stok wzgórza

Wyobraź sobie, że $f$ to wysokość terenu, a Ty stoisz na zboczu. Gradient $\nabla f$ w Twoim punkcie:

- **wskazuje kierunek najszybszego wzrostu** (prosto „pod górę", najbardziej stromo);
- jego **długość** $|\nabla f|$ mówi, jak strome jest zbocze w tym kierunku.

Dwie konsekwencje, które warto mieć w głowie:

1. Gradient jest **prostopadły do poziomic** (do warstwic mapy). Wzdłuż warstwicy wysokość się nie zmienia, więc najszybszy wzrost musi być w poprzek.
2. Jeśli $\nabla f = \mathbf{0}$, jesteś w punkcie płaskim — szczyt, dolina albo siodło.

### Skąd to wiadomo — pochodna kierunkowa

„Kierunek najszybszego wzrostu" nie jest definicją, tylko konsekwencją — i wynika z jednego wzoru. Gdy przesuniesz się o mały wektor $\mathrm{d}\mathbf{l}$, wartość pola zmieni się o

$$
\mathrm{d}f = \nabla f \cdot \mathrm{d}\mathbf{l} = |\nabla f|\,|\mathrm{d}\mathbf{l}|\cos\theta,
$$

gdzie $\theta$ to kąt między kierunkiem ruchu a gradientem (to tzw. **pochodna kierunkowa**: przy przesunięciu po skosie przyczynki od trzech pochodnych cząstkowych po prostu się sumują). Cała intuicja siedzi teraz w cosinusie:

- $\theta = 0$ → zmiana maksymalna: ruch **wzdłuż** $\nabla f$ daje najszybszy wzrost;
- $\theta = 90°$ → zmiana zerowa: ruch **w poprzek** gradientu nie zmienia $f$ — czyli idziesz po poziomicy (stąd prostopadłość gradientu do poziomic);
- $\theta = 180°$ → najszybszy spadek.

### Po co to w elektromagnetyzmie

Pole elektryczne w statyce daje się zapisać jako gradient pewnego pola skalarnego — **potencjału** $V$:

$$
\mathbf{E} = -\nabla V.
$$

Znak minus mówi: pole elektryczne wskazuje „w dół potencjału" (ładunek dodatni stacza się od wysokiego do niskiego potencjału, jak kulka ze wzgórza). To pojęcie wróci w Module 2. Gradient jest tu narzędziem, które z jednej liczby w każdym punkcie (potencjał) odtwarza pełne pole wektorowe.

---

## 4. Dywergencja — ile pola „wypływa" z punktu

Teraz bierzemy **pole wektorowe** $\mathbf{A}$ i robimy z $\nabla$ **iloczyn skalarny**. Wynik jest **skalarem**:

$$
\nabla \cdot \mathbf{A} = \frac{\partial A_x}{\partial x} + \frac{\partial A_y}{\partial y} + \frac{\partial A_z}{\partial z}.
$$

### Intuicja: kran i odpływ

Wyobraź sobie maleńkie pudełko zanurzone w płynącym polu (np. w wodzie, której prędkość opisuje $\mathbf{A}$). Dywergencja w danym punkcie odpowiada na pytanie:

> **Czy z tego punktu netto coś wypływa, czy do niego wpływa?**

- $\nabla \cdot \mathbf{A} > 0$ → **źródło**. Z punktu wypływa więcej, niż wpływa (jakby był tam kranik dolewający wody). Linie pola „rodzą się" tutaj.
- $\nabla \cdot \mathbf{A} < 0$ → **ujście** (odpływ). Linie pola „giną" tutaj.
- $\nabla \cdot \mathbf{A} = 0$ → ile wpłynęło, tyle wypłynęło. Pole jest **bezźródłowe** w tym punkcie (linie tylko przechodzą na wylot).

Dlaczego suma pochodnych cząstkowych to mierzy? Weź sam człon $\partial A_x / \partial x$ i dwie ścianki pudełka prostopadłe do osi $x$: przez lewą woda **wpływa** z prędkością $A_x(\text{lewa})$, przez prawą **wypływa** z prędkością $A_x(\text{prawa})$. Jeśli $A_x$ rośnie wzdłuż osi $x$ (pochodna dodatnia), to wypływa więcej, niż wpływa — pudełko ma netto wypływ w osi $x$. Człony $\partial A_y/\partial y$ i $\partial A_z/\partial z$ robią ten sam bilans dla pozostałych dwóch par ścianek. Suma trzech członów to całkowity **bilans wypływu na jednostkę objętości** — i to właśnie jest dywergencja.

> **Przykład 1 (czyste źródło).** $\mathbf{A} = (x, y, z)$ — pole rozchodzące się promieniście na zewnątrz z początku układu.
> $\nabla \cdot \mathbf{A} = 1 + 1 + 1 = 3 > 0$ wszędzie. Dodatnia dywergencja = pole faktycznie „wypływa". Tak wygląda pole wokół ładunku dodatniego.
>
> **Przykład 2 (czysty wir).** $\mathbf{A} = (-y, x, 0)$ — pole kręcące się w kółko wokół osi $z$.
> $\nabla \cdot \mathbf{A} = \dfrac{\partial(-y)}{\partial x} + \dfrac{\partial(x)}{\partial y} + 0 = 0$. Mimo że pole „coś robi", nic z żadnego punktu nie wypływa — wir nie ma źródeł.

### Zapowiedź Maxwella

Dwa z czterech równań to równania dla dywergencji:

$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0} \qquad\text{oraz}\qquad \nabla \cdot \mathbf{B} = 0.
$$

Pierwsze: **źródłem pola elektrycznego jest ładunek** ($\rho \neq 0$ → dywergencja niezerowa → linie $\mathbf{E}$ rodzą się na ładunkach). Drugie: **pole magnetyczne nie ma źródeł** (dywergencja zawsze zero → linie $\mathbf{B}$ nigdy się nie zaczynają ani nie kończą → tworzą zamknięte pętle → nie ma monopoli magnetycznych). Teraz te równania już *coś znaczą*.

---

## 5. Rotacja — ile pole „wiruje" wokół punktu

Ostatnia operacja: bierzemy pole wektorowe $\mathbf{A}$ i robimy z $\nabla$ **iloczyn wektorowy**. Wynik jest **wektorem**:

$$
\nabla \times \mathbf{A} = \left(
\frac{\partial A_z}{\partial y} - \frac{\partial A_y}{\partial z},\;\;
\frac{\partial A_x}{\partial z} - \frac{\partial A_z}{\partial x},\;\;
\frac{\partial A_y}{\partial x} - \frac{\partial A_x}{\partial y}
\right).
$$

Wzór wygląda groźnie, ale ma regularną budowę: każda składowa to różnica dwóch „skrzyżowanych" pochodnych. W praktyce wygodnie liczy się go jako wyznacznik symboliczny:

$$
\nabla \times \mathbf{A} =
\begin{vmatrix}
\mathbf{\hat{x}} & \mathbf{\hat{y}} & \mathbf{\hat{z}} \\[2pt]
\dfrac{\partial}{\partial x} & \dfrac{\partial}{\partial y} & \dfrac{\partial}{\partial z} \\[6pt]
A_x & A_y & A_z
\end{vmatrix}.
$$

### Intuicja: młynek w strumieniu

Wyobraź sobie, że wkładasz w pole maleńki **wiatraczek / młynek na osi** i pytasz: *czy zacznie się kręcić?*

- Jeśli pole po jednej stronie młynka jest silniejsze niż po drugiej (albo skręca), łopatki dostają różny napór i wiatraczek rusza. **Rotacja jest niezerowa** — pole lokalnie wiruje.
- Jeśli pole napiera na wszystkie łopatki tak samo, młynek stoi. **Rotacja zero** — pole jest *bezwirowe* (po angielsku *irrotational*).

Wektor $\nabla \times \mathbf{A}$ koduje obie informacje naraz:

- jego **kierunek** = oś, wokół której następuje wirowanie (reguła prawej dłoni: kciuk wzdłuż $\nabla\times\mathbf{A}$, palce pokazują kierunek obrotu);
- jego **długość** = jak intensywne jest to lokalne wirowanie.

> **Przykład 1 (czysty wir).** Znów $\mathbf{A} = (-y, x, 0)$. Licząc składową $z$:
> $\dfrac{\partial A_y}{\partial x} - \dfrac{\partial A_x}{\partial y} = \dfrac{\partial(x)}{\partial x} - \dfrac{\partial(-y)}{\partial y} = 1 - (-1) = 2.$
> Pozostałe składowe zerowe, więc $\nabla \times \mathbf{A} = (0, 0, 2)$. Niezerowa rotacja skierowana wzdłuż osi $z$ — dokładnie oś, wokół której pole się kręci. (Porównaj z §4: to samo pole ma **zerową dywergencję, ale niezerową rotację** — czysty wir.)
>
> **Przykład 2 (czyste źródło).** $\mathbf{A} = (x, y, z)$ ma $\nabla \times \mathbf{A} = \mathbf{0}$. Pole promieniste nigdzie nie zakręca — sama dywergencja, zero rotacji.

Te dwa przykłady to fundament intuicji: **dywergencja i rotacja to dwie niezależne cechy pola.** Pole może mieć jedną, drugą, obie naraz albo żadnej. (Twierdzenie Helmholtza mówi nawet, że te dwie cechy plus zachowanie na brzegu *jednoznacznie* wyznaczają pole — dlatego Maxwell potrzebuje równań i na dywergencję, i na rotację obu pól.)

### Pułapka: rotacja to nie „zakrzywione linie pola"

Kształt linii pola potrafi oszukać — kryterium jest zawsze młynek, nie geometria linii. Dwa kontrprzykłady:

- **Linie proste, rotacja niezerowa.** Pole ścinające $\mathbf{A} = (y, 0, 0)$: wszystko płynie idealnie prosto wzdłuż osi $x$, ale warstwy położone wyżej płyną szybciej (jak rzeka — szybciej na środku niż przy brzegu). Młynek włożony w taki przepływ **kręci się**, bo górna łopatka jest popychana mocniej niż dolna. I rzeczywiście: $\nabla \times \mathbf{A} = (0, 0, -1) \neq \mathbf{0}$.
- **Linie krążą, rotacja zerowa.** Pole wirujące jak $(-y, x, 0)$, ale słabnące z odległością jak $1/r$: $\mathbf{A} = \dfrac{(-y,\; x,\; 0)}{x^2 + y^2}$. Poza samą osią $\nabla \times \mathbf{A} = \mathbf{0}$ — młynek płynie po okręgu z prądem, ale się **nie obraca**. Intuicja: na małej pętelce nieobejmującej osi mocniejsze pole na krótszym łuku wewnętrznym dokładnie znosi słabsze pole na dłuższym łuku zewnętrznym (pole maleje jak $1/r$, długość łuku rośnie jak $r$ — iloczyn stały). To pole to dokładnie kształt pola $\mathbf{B}$ wokół prostego przewodu z prądem — wróci w Module 3.

### Zapowiedź Maxwella

Pozostałe dwa równania to równania dla rotacji:

$$
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t} \qquad\text{oraz}\qquad \nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}.
$$

Czyli: **zmienne pole magnetyczne wytwarza wirujące pole elektryczne** (Faraday) i **prądy oraz zmienne pole elektryczne wytwarzają wirujące pole magnetyczne** (Ampère–Maxwell). Rotacja jest tu językiem, w którym pola „karmią się" nawzajem.

> **Dwie tożsamości, które warto znać (i które są ukryte w Maxwellu):**
> $\nabla \cdot (\nabla \times \mathbf{A}) = 0$ — rotacja nigdy nie ma źródeł (to dlatego $\nabla\cdot\mathbf{B}=0$ jest spójne z tym, że $\mathbf{B}$ bywa rotacją czegoś).
> $\nabla \times (\nabla f) = \mathbf{0}$ — gradient nigdy nie wiruje (to dlatego pole z potencjału, $\mathbf{E}=-\nabla V$, jest bezwirowe w statyce).

---

Do tej pory patrzyliśmy **lokalnie** — co dzieje się w jednym punkcie. Ale równania Maxwella mają też **postać całkową**, mówiącą o całych obszarach i powierzchniach. Potrzebujemy dwóch pojęć całkowych: **strumienia** i **cyrkulacji**. To one są „globalnymi" odpowiednikami dywergencji i rotacji.

---

## 6. Strumień — ile pola przechodzi przez powierzchnię

**Strumień** (ang. *flux*) odpowiada na pytanie: *ile pola wektorowego przepływa przez daną powierzchnię?*

### Budowa pojęcia, krok po kroku

Zacznij od jednorodnego pola $\mathbf{A}$ i płaskiej powierzchni o polu $S$. Strumień zależy nie tylko od wielkości pola i powierzchni, ale i od **kąta**:

- pole **prostopadłe** do powierzchni → przepływa maksymalnie;
- pole **równoległe** do powierzchni (muska ją) → nie przepływa wcale;
- pośrednio → liczy się tylko składowa prostopadła.

Żeby to ująć, każdej powierzchni przypisujemy **wektor normalny** $\mathbf{\hat{n}}$ (jednostkowy, prostopadły do niej). Strumień przez płaski kawałek to:

$$
\Phi = \mathbf{A} \cdot \mathbf{\hat{n}}\, S = |\mathbf{A}|\, S \cos\theta,
$$

gdzie $\theta$ to kąt między polem a normalną. Iloczyn skalarny automatycznie „wyłuskuje" składową prostopadłą — gdy pole jest równoległe do powierzchni ($\theta = 90°$), $\cos\theta = 0$ i strumień znika. Dokładnie tak ma być.

Dla **dowolnej** powierzchni i **niejednorodnego** pola tniemy powierzchnię na maleńkie płatki $\mathrm{d}\mathbf{S} = \mathbf{\hat{n}}\,\mathrm{d}S$, liczymy strumień przez każdy i sumujemy — czyli całkujemy:

$$
\boxed{\;\Phi = \iint_S \mathbf{A} \cdot \mathrm{d}\mathbf{S}\;}
$$

To wszystko, co kryje się pod całką powierzchniową: „posiekaj powierzchnię, w każdym kawałku weź składową pola prostopadłą do niego razy pole kawałka, zsumuj".

### Powierzchnie otwarte i zamknięte

Rozróżnienie kluczowe dla Maxwella:

- **Powierzchnia otwarta** — ma brzeg (jak membrana bębna albo czasza). Ma dwie strony i trzeba *wybrać*, którą stronę uznajemy za „dodatnią" normalną. Ten wybór nie jest kosmetyczny: decyduje o znaku strumienia, a w prawach Faradaya i Ampère'a wiąże się z kierunkiem obiegu brzegu regułą prawej dłoni (wróci w §9).
- **Powierzchnia zamknięta** — otacza objętość, nie ma brzegu (jak powierzchnia kuli czy pudełka). Umawiamy się, że normalna wskazuje **na zewnątrz**. Całkę po powierzchni zamkniętej $S$ zapisujemy jako $\iint_S$, pamiętając, że $S$ otacza objętość i nie ma brzegu (w podręcznikach rysuje się wtedy kółko na znaku całki).

Dla powierzchni zamkniętej strumień ma piękną interpretację: **netto ile pola wypływa z zamkniętego obszaru.** Dodatni strumień = w środku jest źródło; zero = ile wpłynęło, tyle wypłynęło. To brzmi znajomo — bo to ta sama idea co dywergencja, tylko dla całego obszaru zamiast pojedynczego punktu. Ten związek sformalizuje §8.

Prawa Gaussa w postaci całkowej to właśnie zdania o strumieniu przez powierzchnię zamkniętą:

$$
\iint_S \mathbf{E} \cdot \mathrm{d}\mathbf{S} = \frac{Q_{\text{wewn}}}{\varepsilon_0}, \qquad \iint_S \mathbf{B} \cdot \mathrm{d}\mathbf{S} = 0.
$$

„Strumień pola $\mathbf{E}$ przez zamkniętą powierzchnię = ładunek zamknięty w środku (podzielony przez $\varepsilon_0$)" oraz „strumień $\mathbf{B}$ przez dowolną zamkniętą powierzchnię to zawsze zero".

---

## 7. Cyrkulacja — ile pola „krąży" wzdłuż pętli

**Cyrkulacja** odpowiada na pytanie: *jak bardzo pole jest skierowane „wzdłuż" zamkniętej drogi, gdy obejdziemy ją dookoła?*

### Najpierw całka krzywoliniowa

Wyobraź sobie, że idziesz po krzywej $C$ w polu $\mathbf{A}$. W każdym punkcie liczy się tylko **składowa pola wzdłuż Twojego ruchu** (składowa w poprzek nie pomaga ani nie przeszkadza iść). Mnożymy ją przez przebyty kawałek drogi $\mathrm{d}\mathbf{l}$ i sumujemy:

$$
\int_C \mathbf{A} \cdot \mathrm{d}\mathbf{l}.
$$

To **całka krzywoliniowa**. Najbardziej fizyczny przykład: jeśli $\mathbf{A}$ to siła, taka całka to **praca** wykonana wzdłuż drogi. Iloczyn skalarny $\mathbf{A}\cdot\mathrm{d}\mathbf{l}$ znów wyłuskuje tylko część „zgodną z kierunkiem".

### Cyrkulacja = całka po pętli zamkniętej

Gdy droga jest **zamknięta** (wracamy do punktu startu), całkę oznaczamy kółkiem i nazywamy **cyrkulacją**:

$$
\boxed{\;\Gamma = \oint_C \mathbf{A} \cdot \mathrm{d}\mathbf{l}\;}
$$

Interpretacja:

- $\Gamma \neq 0$ → obchodząc pętlę, pole „popycha" nas netto w jedną stronę. Pole **krąży** wzdłuż tej pętli.
- $\Gamma = 0$ → ile pole pomogło na jednej części pętli, tyle zabrało na innej. Brak krążenia.

To znów brzmi znajomo: cyrkulacja po pętli to „globalna" wersja **rotacji** w punkcie. Mały wiatraczek z §5 to nic innego jak cyrkulacja po nieskończenie małej pętli. Ten związek sformalizuje §9.

Prawa Faradaya i Ampère'a w postaci całkowej to zdania o cyrkulacji:

$$
\oint_C \mathbf{E} \cdot \mathrm{d}\mathbf{l} = -\frac{\mathrm{d}\Phi_B}{\mathrm{d}t}, \qquad \oint_C \mathbf{B} \cdot \mathrm{d}\mathbf{l} = \mu_0 I + \mu_0\varepsilon_0\frac{\mathrm{d}\Phi_E}{\mathrm{d}t}.
$$

Faraday: „cyrkulacja pola elektrycznego po pętli = tempo, z jakim maleje strumień magnetyczny przez tę pętlę" — czyli zmienne $\mathbf{B}$ wymusza krążące $\mathbf{E}$. To zasada działania prądnicy.

Ampère analogicznie: niezerowa cyrkulacja $\mathbf{B}$ po pętli zdradza, że przez tę pętlę przebija się prąd $I$ (albo zmienia się strumień pola elektrycznego — to człon dodany przez Maxwella). Krążące pole magnetyczne wokół przewodu z prądem, znane z doświadczenia Ørsteda, to dokładnie ten obraz.

---

## 8. Twierdzenie Gaussa–Ostrogradskiego

Mamy dwie pary pojęć, które „pachną" tym samym:

- **dywergencja** (lokalnie, w punkcie) ↔ **strumień przez zamkniętą powierzchnię** (globalnie, dla obszaru),
- **rotacja** (lokalnie) ↔ **cyrkulacja po pętli** (globalnie).

Dwa wielkie twierdzenia analizy wektorowej zamieniają te „↔" w ścisłe równości. Pierwsze dotyczy pary dywergencja–strumień.

### Treść

**Twierdzenie o dywergencji** (Gaussa–Ostrogradskiego): strumień pola przez **zamkniętą** powierzchnię $S$ równa się całce z dywergencji po **objętości** $V$, którą ta powierzchnia otacza:

$$
\boxed{\;\iint_S \mathbf{A} \cdot \mathrm{d}\mathbf{S} = \iiint_V (\nabla \cdot \mathbf{A})\, \mathrm{d}V\;}
$$

### Dlaczego to prawda — intuicja

Podziel objętość na mnóstwo maleńkich pudełeczek. Strumień wypływający z każdego pudełka to (z definicji dywergencji) $\nabla\cdot\mathbf{A}$ razy jego objętość. Teraz zsumuj po wszystkich pudełkach. **Ściany wewnętrzne się znoszą:** to, co wypływa z jednego pudełka przez wspólną ścianę, wpływa do sąsiada — z przeciwnym znakiem. Zostaje tylko strumień przez **ściany zewnętrzne**, czyli przez powierzchnię $S$. Suma „mikro-źródeł" w środku = całkowity wypływ przez brzeg. To cała treść twierdzenia.

### Po co nam to

To jest **most między dwiema postaciami praw Gaussa**. Weź postać całkową i zastosuj twierdzenie do lewej strony:

$$
\iint_S \mathbf{E}\cdot\mathrm{d}\mathbf{S} = \iiint_V (\nabla\cdot\mathbf{E})\,\mathrm{d}V \quad\text{oraz}\quad \frac{Q_{\text{wewn}}}{\varepsilon_0} = \iiint_V \frac{\rho}{\varepsilon_0}\,\mathrm{d}V.
$$

Skoro obie całki objętościowe są równe **dla dowolnego obszaru $V$**, to ich funkcje podcałkowe muszą być równe w każdym punkcie:

$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}.
$$

I tak z postaci całkowej („o powierzchniach i ładunkach") wyprowadziliśmy postać różniczkową („o punktach"). To nie dwa różne prawa — to **to samo prawo w dwóch językach**, a tłumaczem jest twierdzenie o dywergencji.

---

## 9. Twierdzenie Stokesa

Drugie wielkie twierdzenie dotyczy pary rotacja–cyrkulacja.

### Treść

**Twierdzenie Stokesa:** cyrkulacja pola po zamkniętej pętli $C$ równa się strumieniowi rotacji przez **dowolną** powierzchnię $S$ rozpiętą na tej pętli ($C$ jest brzegiem $S$):

$$
\boxed{\;\oint_C \mathbf{A} \cdot \mathrm{d}\mathbf{l} = \iint_S (\nabla \times \mathbf{A}) \cdot \mathrm{d}\mathbf{S}\;}
$$

(Zwrot obiegu pętli i kierunek normalnej powierzchni wiąże reguła prawej dłoni.)

### Dlaczego to prawda — intuicja

Pokryj powierzchnię siatką maleńkich pętelek. Cyrkulacja po każdej pętelce to (z definicji rotacji) $\nabla\times\mathbf{A}$ rzutowane na tę pętelkę razy jej pole. Zsumuj po wszystkich. **Wewnętrzne krawędzie się znoszą:** każda wewnętrzna krawędź należy do dwóch sąsiednich pętelek, które obiegają ją w przeciwnych kierunkach. Zostaje tylko obieg po **zewnętrznym brzegu** — czyli po $C$. Suma „mikro-wirów" wewnątrz = całkowita cyrkulacja po brzegu. Identyczny mechanizm „znoszenia się wnętrza" jak w twierdzeniu o dywergencji, tylko dla krawędzi zamiast ścian.

### Po co nam to

To **most między dwiema postaciami praw Faradaya i Ampère'a**. Dla Faradaya, startując z postaci całkowej i stosując Stokesa do lewej strony:

$$
\oint_C \mathbf{E}\cdot\mathrm{d}\mathbf{l} = \iint_S (\nabla\times\mathbf{E})\cdot\mathrm{d}\mathbf{S} \quad\text{oraz}\quad -\frac{\mathrm{d}\Phi_B}{\mathrm{d}t} = \iint_S \left(-\frac{\partial \mathbf{B}}{\partial t}\right)\cdot\mathrm{d}\mathbf{S}.
$$

Równość dla **dowolnej** powierzchni $S$ wymusza równość funkcji podcałkowych:

$$
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}.
$$

Znów: jedno prawo, dwa języki, tłumaczem jest twierdzenie Stokesa.

---

## 10. Jak to spina równania Maxwella

Po tym rozdziale możesz spojrzeć na każde równanie i je *przeczytać*. Podsumujmy całą maszynerię w jednej tabeli:

| Równanie (postać różniczkowa) | Operator | Czyta się jako | Most do postaci całkowej |
|---|---|---|---|
| $\nabla \cdot \mathbf{E} = \rho/\varepsilon_0$ | dywergencja | źródłem $\mathbf{E}$ są ładunki | tw. o dywergencji → strumień |
| $\nabla \cdot \mathbf{B} = 0$ | dywergencja | $\mathbf{B}$ nie ma źródeł (brak monopoli) | tw. o dywergencji → strumień |
| $\nabla \times \mathbf{E} = -\partial \mathbf{B}/\partial t$ | rotacja | zmienne $\mathbf{B}$ wytwarza wirowe $\mathbf{E}$ | tw. Stokesa → cyrkulacja |
| $\nabla \times \mathbf{B} = \mu_0\mathbf{J} + \mu_0\varepsilon_0\,\partial\mathbf{E}/\partial t$ | rotacja | prądy i zmienne $\mathbf{E}$ wytwarzają wirowe $\mathbf{B}$ | tw. Stokesa → cyrkulacja |

Spójrz na strukturę: **dwa równania mówią o dywergencji (źródłach) pól, dwa o ich rotacji (wirowości).** To nie przypadek — jak wspomniano przy twierdzeniu Helmholtza, żeby jednoznacznie określić pole wektorowe, trzeba podać i jego dywergencję, i jego rotację. Maxwell robi dokładnie to dla $\mathbf{E}$ i dla $\mathbf{B}$. Cztery równania to nie dowolny zbiór — to *komplet* potrzebny do pełnego opisu dwóch pól.

---

## Co warto zapamiętać z tego rozdziału

- **Pole skalarne** = liczba w każdym punkcie; **pole wektorowe** = strzałka w każdym punkcie (czyli trzy pola skalarne naraz).
- **$\nabla$** to wektor operatorów różniczkowania. Działa na trzy sposoby: $\nabla f$ (gradient, daje wektor), $\nabla\cdot\mathbf{A}$ (dywergencja, daje skalar), $\nabla\times\mathbf{A}$ (rotacja, daje wektor).
- **Gradient** wskazuje kierunek najszybszego wzrostu pola skalarnego — bo $\mathrm{d}f = \nabla f \cdot \mathrm{d}\mathbf{l}$ jest największe wzdłuż $\nabla f$; w EM: $\mathbf{E} = -\nabla V$.
- **Dywergencja** mierzy, ile pola netto wypływa z punktu (źródła i ujścia). Niezerowa tam, gdzie pole się „rodzi".
- **Rotacja** mierzy lokalne wirowanie pola (młynek). Kryterium jest młynek, **nie kształt linii**: proste linie mogą wirować (ścinanie), krążące mogą nie wirować (pole $1/r$). Dywergencja i rotacja to **niezależne** cechy — pole może mieć dowolną kombinację.
- **Strumień** $\iint_S \mathbf{A}\cdot\mathrm{d}\mathbf{S}$ = ile pola przechodzi przez powierzchnię (dla zamkniętej: ile wypływa z obszaru).
- **Cyrkulacja** $\oint_C \mathbf{A}\cdot\mathrm{d}\mathbf{l}$ = jak bardzo pole krąży wzdłuż pętli.
- **Twierdzenie o dywergencji** łączy strumień przez zamkniętą powierzchnię z dywergencją w objętości → spina obie postaci praw Gaussa.
- **Twierdzenie Stokesa** łączy cyrkulację po pętli z rotacją na powierzchni → spina obie postaci praw Faradaya i Ampère'a.
- Postać całkowa i różniczkowa każdego równania Maxwella to **to samo prawo w dwóch językach**; tłumaczami są dwa twierdzenia całkowe.

---

**Poprzedni artykuł:** [[00-po-co-nam-rownania-maxwella|Moduł 0 — Po co nam równania Maxwella]]
**Następny artykuł:** Moduł 2.1 — *Ładunek, prawo Coulomba i gęstość ładunku $\rho$* (pierwszy „fizyczny" składnik: skąd biorą się źródła pola $\mathbf{E}$).
