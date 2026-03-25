import os
import datetime
import urllib.parse
from collections import defaultdict

# Konfiguracja
# Ścieżka bazowa to ten sam katalog, w którym znajduje się skrypt
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = SCRIPT_DIR
TARGET_FOLDERS = ['Python', 'AI', 'Linux', 'Java']

# Plik wyjściowy będzie w katalogu głównym (BASE_DIR)
OUTPUT_FILE = os.path.join(BASE_DIR, 'index.md')

def generate_index():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# Indeks materiałów\n\n")

        for top_folder in TARGET_FOLDERS:
            # Szukamy folderów w katalogu ze skryptem (second_brain)
            top_folder_path = os.path.join(SCRIPT_DIR, top_folder)
            
            f.write(f"## {top_folder}\n\n")
            
            # Sprawdzenie czy folder faktycznie istnieje
            if not os.path.isdir(top_folder_path):
                f.write("*Katalog nie istnieje*\n\n")
                continue
                
            # Grupowanie plików po podkatalogach. 
            # Klucz: relatywna ścieżka od top_folder_path
            # Wartość: lista krotek (item, mtime, item_path)
            groups = defaultdict(list)
            has_any_files = False
            
            for root, dirs, files in os.walk(top_folder_path):
                # Ignorowanie ukrytych folderów (np. .obsidian, .git)
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                rel_dir = os.path.relpath(root, top_folder_path)
                if rel_dir == '.':
                    rel_dir = '' # Katalog główny kategorii (bez podrozdziału)
                    
                for item in files:
                    # Pomijamy ukryte pliki
                    if item.startswith('.'):
                        continue
                        
                    # Akceptujemy tylko pliki .md
                    if not item.lower().endswith('.md'):
                        continue
                        
                    has_any_files = True
                    item_path = os.path.join(root, item)
                    mtime = os.path.getmtime(item_path)
                    groups[rel_dir].append((item, mtime, item_path))
            
            if not has_any_files:
                f.write("*Brak plików w tej kategorii*\n\n")
                continue
                
            # Sortujemy podkatalogi alfabetycznie (główny folder '' będzie na samym początku)
            sorted_dirs = sorted(groups.keys())
            
            for d in sorted_dirs:
                files_with_mtime = groups[d]
                
                # Sortowanie plików wewnątrz podkatalogu: malejąco po dacie modyfikacji
                files_with_mtime.sort(key=lambda x: x[1], reverse=True)
                
                if not files_with_mtime:
                    continue
                    
                # Jeśli to podkatalog, formatujemy nagłówek (podrozdział)
                if d != '':
                    # Obliczanie odpowiedniego stopnia nagłówka
                    # np. "FastAPI" (głębokość 1) -> "### FastAPI"
                    depth = d.count(os.sep) + 1
                    header_prefix = "#" * (2 + depth)
                    
                    # Podmiana ewentualnych ukośników na ładniejsze przy wyświetlaniu
                    display_dir = d.replace(os.sep, ' / ')
                    f.write(f"{header_prefix} {display_dir}\n\n")
                    
                # Listowanie plików
                for item, mtime, item_path in files_with_mtime:
                    # Usunięcie z nazwy rozszerzenia .md do wyświetlania
                    display_name = os.path.splitext(item)[0] if item.endswith('.md') else item
                    
                    # Relatywna ścieżka do index.md i formatowanie URL
                    rel_to_base = os.path.relpath(item_path, BASE_DIR)
                    safe_path = urllib.parse.quote(rel_to_base, safe='/')
                    
                    # Tworzenie standardowego linku Markdown
                    f.write(f"- [{display_name}]({safe_path})\n")
                    
                f.write("\n")

if __name__ == "__main__":
    generate_index()
    print(f"Pomyślnie wygenerowano plik {OUTPUT_FILE} w katalogu {BASE_DIR}")
