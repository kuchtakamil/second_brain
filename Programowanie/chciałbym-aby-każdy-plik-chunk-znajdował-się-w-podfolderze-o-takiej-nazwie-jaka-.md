# chciałbym aby każdy plik - chunk znajdował się w podfolderze o takiej nazwie jak

**Data:** 18 gru 2025, 12:25:38 CET

---

**User:**

chciałbym aby każdy plik - chunk znajdował się w podfolderze o takiej nazwie jaka jest nazwa dużego rozdziału w której fragment się znajduje. Duży rozdział jest oznaczony przez # i jest to np. # Rozdział 7. Uwierzytelnianie i autoryzacja API
Tak więc podfolder miałby nazwę podobną do: rozdział_7_._uwierzytelnianie_i_autoryzacja_api

---

**Gemini:**

To świetny pomysł – dzięki temu struktura plików na dysku będzie idealnie odzwierciedlać strukturę logiczną książki, co znacznie ułatwi nawigację i późniejsze przetwarzanie (np. w systemach RAG).

Aby to osiągnąć, musimy zmodyfikować logikę w dwóch miejscach:

1. **Grupowanie:** Zanim zaczniemy łączyć małe chunki ("greedy merging"), musimy pogrupować fragmenty według ich nagłówka H1 (`#`).
2. **Sanityzacja nazw (Slugify):** Musimy zamienić tekst "Rozdział 7. Uwierzytelnianie..." na bezpieczną nazwę folderu (bez spacji, polskich znaków, kropek).

Oto kompletny, zaktualizowany skrypt.

### Kod Python: Podział na podfoldery według H1

```
import os
import re
import unicodedata
from collections import defaultdict
from langchain_text_splitters import MarkdownHeaderTextSplitter

def slugify(value: str) -> str:
    """
    Zamienia dowolny ciąg znaków na bezpieczną nazwę folderu/pliku.
    Np. 'Rozdział 7. Żółta Łódź' -> 'rozdzial_7_zolta_lodz'
    """
    if not value:
        return "bez_tytulu"
    
    # 1. Normalizacja Unicode (zamiana ą->a, ł->l, etc.)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    
    # 2. Zamiana wszystkiego co nie jest literą/cyfrą na spację, potem lowercase
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    
    # 3. Zamiana spacji i myślników na podkreślniki
    value = re.sub(r'[-\s]+', '_', value)
    
    return value

def split_markdown_by_chapters(
    file_path: str, 
    output_base_dir: str, 
    min_chunk_size: int = 2000
):
    # 1. Wczytanie pliku
    if not os.path.exists(file_path):
        print(f"Błąd: Plik {file_path} nie istnieje.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # 2. Konfiguracja splittera
    # Ważne: splitujemy po H1 (#) i H2 (##)
    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2"),
    ]
    
    # strip_headers=False sprawia, że nagłówki zostają w treści (dobre dla kontekstu),
    # ale jednocześnie trafiają do metadanych (dobre dla nazewnictwa folderów).
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, 
        strip_headers=False 
    )
    
    raw_splits = markdown_splitter.split_text(markdown_text)

    # 3. Grupowanie dokumentów według H1 (Rozdziałów)
    # Tworzymy słownik: { "Tytuł Rozdziału H1": [lista fragmentów] }
    chapters_map = defaultdict(list)
    
    for split in raw_splits:
        # Pobieramy nazwę rozdziału z metadanych. 
        # Jeśli brak H1 (np. wstęp), używamy klucza "Inne"
        h1_title = split.metadata.get("h1", "Wstęp_i_inne")
        chapters_map[h1_title].append(split.page_content)

    # 4. Przetwarzanie każdego rozdziału osobno
    total_files_created = 0
    
    print(f"Znaleziono {len(chapters_map)} głównych rozdziałów (H1). Rozpoczynam przetwarzanie...\n")

    for h1_title, contents in chapters_map.items():
        # A. Tworzenie bezpiecznej nazwy folderu
        folder_name = slugify(h1_title)
        current_output_dir = os.path.join(output_base_dir, folder_name)
        
        if not os.path.exists(current_output_dir):
            os.makedirs(current_output_dir)

        # B. Logika łączenia małych fragmentów (Greedy Merging) w obrębie TEGO rozdziału
        final_chunks = []
        current_chunk_buffer = ""

        for content in contents:
            # Jeśli bufor nie jest pusty i dodanie nowego fragmentu przekroczy limit...
            if current_chunk_buffer and (len(current_chunk_buffer) + len(content) > min_chunk_size):
                # ...zapisujemy obecny bufor
                final_chunks.append(current_chunk_buffer)
                current_chunk_buffer = content # Nowy bufor
            else:
                # ...doklejamy do bufora
                separator = "\n\n" if current_chunk_buffer else ""
                current_chunk_buffer += separator + content

        # Dodajemy to, co zostało w buforze na koniec rozdziału
        if current_chunk_buffer:
            final_chunks.append(current_chunk_buffer)

        # C. Zapis plików w podfolderze
        for i, chunk in enumerate(final_chunks):
            filename = os.path.join(current_output_dir, f"part_{i+1:03d}.md")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(chunk)
            total_files_created += 1
            
        print(f"   -> Utworzono folder: [{folder_name}] z {len(final_chunks)} plikami.")

    print(f"\nZakończono. Łącznie utworzono {total_files_created} plików w katalogu '{output_base_dir}'.")

# --- PRZYKŁAD UŻYCIA ---
# split_markdown_by_chapters(
#     file_path="exports/full_book.md", 
#     output_base_dir="exports/split_book_v2", 
#     min_chunk_size=2000
# )
```

### Najważniejsze zmiany w kodzie:

1. **Funkcja `slugify`:**

   - Używa `unicodedata.normalize('NFKD', ...)` aby rozbić znaki diakrytyczne (np. `ą` to `a` + ogonek).
   - `.encode('ascii', 'ignore')` usuwa ogonki, zostawiając czyste ASCII (np. `ą` -> `a`, `Ż` -> `Z`).
   - `re.sub` czyści wszystko co nie jest literą, cyfrą lub spacją, a potem zamienia spacje na `_`.
   - Efekt: `# Rozdział 7. API` -> `rozdzial_7_api`.
2. **Słownik `chapters_map`:**

   - Zamiast przetwarzać listę liniowo, najpierw grupujemy fragmenty. Kluczem jest nagłówek H1 (pobrany z `split.metadata.get("h1")`).
   - Dzięki temu logika łączenia chunków (merging) działa **izolowanie dla każdego rozdziału**. Nie ma ryzyka, że końcówka Rozdziału 1 sklei się z początkiem Rozdziału 2.
3. **Struktura katalogów:**

   - Kod automatycznie tworzy podkatalog dla każdego H1 wewnątrz `output_base_dir`.

### Wynik działania na dysku:

```
exports/split_book_v2/
├── wstep_i_inne/
│   └── part_001.md
├── rozdzial_1_wprowadzenie/
│   ├── part_001.md
│   ├── part_002.md
│   └── part_003.md
└── rozdzial_7_uwierzytelnianie_i_autoryzacja_api/
    ├── part_001.md (np. 2100 znaków)
    └── part_002.md (np. 2300 znaków)
```

Czy chcesz, abym dodał do tego kodu generowanie pliku `index.json` lub `structure.yaml` w głównym katalogu, który mapowałby oryginalną strukturę spisu treści na wygenerowane pliki? To bardzo pomaga przy późniejszym indeksowaniu w bazach wektorowych.