# Zakładając, że będę chciał stworzyć z infografik ebooka w PDF, to w jakiej rozdz

**Data:** 27 sty 2026, 11:29:02 CET

---

**User:**

Zakładając, że będę chciał stworzyć z infografik ebooka w PDF, to w jakiej rozdzielczości powinienem generować infografiki?
2752x1536 px zajmuje około 5,6MB
5504x3072 px zajmuje około 16MB

---

**Gemini:**

Zdecydowanie rekomenduję wybór **Option A ($2752 \times 1536 \text{ px}$)** jako standardu produkcyjnego, z ewentualnym użyciem Option B tylko w specyficznych przypadkach.

Oto techniczna analiza dlaczego ta rozdzielczość jest "złotym środkiem" (Sweet Spot) dla Twojego projektu, biorąc pod uwagę standardy urządzeń i format PDF.

### 1. Matematyka pikseli (Dlaczego 2752 px wystarczy?)

Musimy odnieść rozdzielczość grafiki do ekranu, na którym będzie wyświetlana.

- **iPad Pro 12.9" (największy popularny tablet):** Ma rozdzielczość dłuższego boku **$2732 \text{ px}$**.
- **Twój obrazek (Option A):** Ma **$2752 \text{ px}$**.

**Wniosek:** Grafika $2752 \times 1536$ pokrywa piksel w piksel (1:1) największy ekran tabletu dostępny na rynku w jakości Retina. Generowanie grafiki $5504 \text{ px}$ (Option B) jest w tym momencie "marnowaniem zasobów" (overkill), ponieważ żaden standardowy czytnik ani tablet nie wyświetli tych dodatkowych detali bez pomniejszania obrazu.

### 2. Waga pliku końcowego (Rozmiar ma znaczenie)

To kluczowy aspekt przy dystrybucji ebooka.

- Jeśli Twój ebook ma 50 stron.
- Używając grafik 16 MB: $50 \times 16 \text{ MB} = \textbf{800 MB}$ (przed kompresją). To potwór, którego ciężko pobrać na telefonie.
- Używając grafik 5,6 MB: $50 \times 5,6 \text{ MB} = \textbf{280 MB}$.

Oczywiście, program do składu (Figma/InDesign) skompresuje te zdjęcia przy eksporcie do PDF, ale **praca na lżejszych plikach jest znacznie płynniejsza**. Figma przy 50 grafikach po 16 MB może zacząć zacinać przeglądarkę.

### 3. Aspekt hybrydowy (Wektory + Raster)

Pamiętaj o swojej strategii: **wymieniasz tekst na wektorowy**.
To zmienia reguły gry. Największym problemem niskiej rozdzielczości jest nieczytelny tekst. Ty ten problem eliminujesz, nakładając ostry tekst w postprodukcji. Tło (ilustracja) może być nieco miękkie, a oko ludzkie i tak odbierze całą stronę jako "ostrą jak żyleta", ponieważ krawędzie liter (na których skupia się wzrok) będą wektorowe.

### Moja rekomendacja: Strategia "Smart"

1. **Generuj w rozdzielczości $2752 \times 1536 \text{ px}$.** To wystarczy do wyświetlania na każdym ekranie i do druku w formacie zbliżonym do A4 (przy ~240 DPI, co jest akceptowalne dla digital druku).
2. **Użyj formatu PNG.** Przy generowaniu nie używaj JPG, aby uniknąć artefaktów kompresji przed edycją.
3. **Upscaling (Plan B).** Jeśli uznasz, że jakaś konkretna grafika ma mnóstwo drobnych detali (np. mapa, skomplikowany schemat) i wygląda niewyraźnie:
   - Nie generuj jej od nowa w $5504 \text{ px}$ (co zużywa więcej tokenów/czasu GPU).
   - Użyj **AI Upscalera** (np. *Magnific AI*, *Upscayl* lub wbudowanego w Photoshop *Super Zoom*). Te narzędzia zrobią z Twojego $2752 \text{ px}$ obrazek $5504 \text{ px}$ o lepszej ostrości niż natywny render.

**Podsumowując:**
Zostań przy **$2752 \times 1536$**. To idealny balans między jakością Retina a wydajnością pracy. Wersja $5504$ to wchodzenie w rejony druku plakatowego, niepotrzebne w ebooku.