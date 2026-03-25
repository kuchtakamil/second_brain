# Suma kontrolna pliku

**Data:** 2025-03-09

---

**User:**

Używając dowolnej biblioteki w Python chcę policzyć wartość sumy kontrolnej dla plików video w Windows. Czy na wartość sumy kontrolnej ma wpływ lokalizacja pliku oraz jego nazwa?

---

**Assistant:**

Świetnie! Odpowiadając na Twoje pytanie:

### ✅ Czy lokalizacja i nazwa pliku wpływa na sumę kontrolną?
**Nie**, lokalizacja pliku (np. `C:\videos\file.mp4` vs `D:\archive\file.mp4`) **ani jego nazwa pliku** **nie wpływa na sumę kontrolną**, o ile liczysz ją na podstawie **zawartości pliku**. Suma kontrolna (np. MD5, SHA256 itd.) jest wyliczana na podstawie **bitów znajdujących się w środku pliku**, a nie metadanych systemu plików czy nazwy.

---

### 🔢 Jak policzyć sumę kontrolną w Pythonie?

Możesz skorzystać z wbudowanej biblioteki `hashlib`, np. dla `SHA256` lub `MD5`. Oto przykład:

```python
import hashlib

def calculate_checksum(file_path, algorithm='sha256', chunk_size=8192):
    hash_func = getattr(hashlib, algorithm)()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_func.update(chunk)
    return hash_func.hexdigest()

# Przykład użycia
file_path = r'C:\path\to\your\video.mp4'
checksum = calculate_checksum(file_path, algorithm='sha256')  # lub 'md5', 'sha1', itd.
print(f"Suma kontrolna: {checksum}")
```

---

### 💡 Dodatkowe uwagi:
- Jeśli dwa pliki mają **identyczną zawartość binarną**, ich suma kontrolna będzie taka sama, nawet jeśli mają różne nazwy, znajdują się w różnych folderach, czy mają różne daty utworzenia.
- Jeśli chcesz porównywać pliki pod kątem identyczności — **suma kontrolna to świetne narzędzie**.

---

Chcesz, żebym dorzucił też przykład porównywania wielu plików w folderze lub stworzenia katalogu z sumami kontrolnymi?