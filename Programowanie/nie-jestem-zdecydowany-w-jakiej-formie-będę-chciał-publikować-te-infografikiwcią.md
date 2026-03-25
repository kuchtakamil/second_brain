# Nie jestem zdecydowany w jakiej formie będę chciał publikować te infografiki.Wci

**Data:** 15 sty 2026, 20:28:12 CET

---

**User:**

Nie jestem zdecydowany w jakiej formie będę chciał publikować te infografiki.Wciąż biorę pod uwagę ebooka. Zaproponuj w jakiej rozdzielczości wygenerować te infografiki, tak aby ta rozdzielczość była jak najbardziej uniwersalna.

---

**Gemini:**

Wybór uniwersalnej rozdzielczości wymaga zbalansowania trzech czynników: czytelności typografii na ekranach o wysokiej gęstości pikseli (Retina/OLED), wagi pliku (performance w aplikacjach/webie) oraz standardów druku (DPI).

### 1. Rekomendowany "Master Resolution": Standard A4 300 DPI

Najbardziej uniwersalnym formatem dla infografik edukacyjnych jest format **A4** w orientacji pionowej, renderowany w **300 DPI**. Pozwala on na bezstratny druk oraz doskonałą ostrość na tabletach klasy Premium (iPad Pro).

- **Piksele:** $2480 \times 3508$ px
- **Proporcje (Aspect Ratio):** $1:\sqrt{2}$ (ok. 1:1.41)
- **Zastosowanie:** E-booki High-End, druk fizyczny, materiały do pobrania (printable).

Jeśli Twoje infografiki mają być konsumowane głównie na smartfonach, rozważ proporcje **9:16** (Full HD w pionie) lub **2:3**:

- **Piksele:** $2160 \times 3840$ px (4K Vertical) – zapewnia to "future-proofing" na nadchodzące lata.

---

### 2. Porównanie rozdzielczości pod kątem zastosowań

| Format | Rozdzielczość (px) | DPI | Przeznaczenie |
| --- | --- | --- | --- |
| **Print-Ready** | $2480 \times 3508$ | 300 | Druk, profesjonalne PDFy, tablety 12.9" |
| **Web/Mobile Standard** | $1240 \times 1754$ | 150 | Czytniki E-ink (Kindle), przeglądarki web |
| **Social Media / App** | $1080 \times 1350$ | 72-96 | Instagram (4:5), szybki podgląd w aplikacji |
| **Ultra-HD Master** | $3508 \times 4961$ | 600 | Archiwizacja, wielkoformatowe plakaty |

---

### 3. Techniczne aspekty eksportu

Przy generowaniu plików z myślą o produkcie cyfrowym, sama rozdzielczość to nie wszystko. Należy zwrócić uwagę na:

- **Przestrzeń barwna:** Eksportuj w **sRGB**. Przestrzeń CMYK (drukarska) na urządzeniach mobilnych często wygląda blado i nieatrakcyjnie.
- **Format pliku:**
  - **WebP:** Najlepszy stosunek jakości do wagi dla aplikacji i stron webowych (wspiera przezroczystość).
  - **PNG-24:** Wyłącznie dla grafik z małą liczbą kolorów i ostrymi krawędziami (tekst).
  - **PDF (Vector-based):** Jeśli tworzysz infografiki w Illustratorze/Figmie, zachowaj tekst jako wektory. PDF wektorowy będzie ważył 500 KB, a zachowa idealną ostrość przy dowolnym powiększeniu.

---

### 4. Optymalizacja pod E-booki (PDF/EPUB)

Standardowy PDF z grafikami $2480 \times 3508$ px może być bardzo ciężki (np. 100 stron = 500 MB). Aby produkt był użyteczny:

1. **Downsampling:** Dla standardowego e-booka (nie-premium) celuj w **150-200 DPI** ($1414 \times 2000$ px). Jest to wystarczające dla większości ekranów laptopów.
2. **OCR & Metadata:** Upewnij się, że tekst na infografikach jest przeszukiwalny. W PDF-ie warstwa tekstowa (invisible text layer) pod grafiką drastycznie podnosi wartość użytkową produktu.

---

### 5. Skrypt do masowej zmiany rozmiaru (Python/Pillow)

Jeśli masz grafiki w wysokiej rozdzielczości (Master) i chcesz wygenerować wersje "lekkie" do aplikacji lub podglądu, możesz użyć poniższego skryptu w celu zachowania proporcji i wysokiej jakości resamplingu (Lanczos):

```
from PIL import Image
import os

def resize_infographics(input_dir, output_dir, target_width):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            with Image.open(os.path.join(input_dir, filename)) as img:
                # Calculate height maintaining aspect ratio
                w_percent = (target_width / float(img.size[0]))
                target_height = int((float(img.size[1]) * float(w_percent)))
                
                # Use Lanczos for high-quality downsampling
                resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                
                # Save as optimized WebP
                base_name = os.path.splitext(filename)[0]
                resized_img.save(os.path.join(output_dir, f"{base_name}.webp"), "WEBP", quality=85)

# Example: Generate 150 DPI equivalents (approx 1240px width for A4)
resize_infographics('./master_files', './web_optimized', 1240)
```

**Moja rekomendacja:** Generuj pliki źródłowe (Master) w **300 DPI ($2480 \times 3508$ px)**. Pozwoli Ci to w przyszłości na dowolną konwersję – zarówno do druku fizycznych kart, jak i do lekkiej aplikacji mobilnej, bez utraty danych obrazu.

Czy chciałbyś, abym przeanalizował różnice w wyświetlaniu takich grafik na konkretnych urządzeniach, np. Kindle vs. iPad?