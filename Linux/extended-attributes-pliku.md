# Extended attributes pliku

**Data:** 2025-07-03

---

**User:**

Co to jest extended attributes pliku?

---

**Assistant:**

**Extended attributes (rozszerzone atrybuty pliku)** to mechanizm w systemach plików (głównie Unix/Linux, ale też np. macOS), który pozwala na przypisywanie do plików i katalogów dodatkowych metadanych poza standardowym zestawem atrybutów (takich jak właściciel, uprawnienia, czas modyfikacji).

### Cechy extended attributes:
- Przechowują dane w formie **par klucz-wartość**.
- Klucz jest zwykle **stringiem z prefiksem namespace**, np. `user.comment`.
- Wartość to **ciąg bajtów** (dowolny, może być binarny).
- Mogą być używane przez:
  - **systemy bezpieczeństwa** (np. SELinux używa `security.*`)
  - **użytkowników** (`user.*`)
  - **aplikacje** (np. indeksujące pliki)
  - **system plików** (np. do trzymania znaczników)

### Przykład użycia:
Dodanie atrybutu `user.comment` do pliku:

```bash
setfattr -n user.comment -v "To jest mój plik" mojplik.txt
```

Odczytanie tego atrybutu:

```bash
getfattr -n user.comment mojplik.txt
```

Wyświetlenie wszystkich atrybutów:

```bash
getfattr -d mojplik.txt
```

### Obsługa:
Nie wszystkie systemy plików wspierają extended attributes. Przykładowo:
- **ext3, ext4** – wspierają, ale czasem wymagają opcji montowania
- **XFS, Btrfs** – wspierają natywnie
- **NTFS** (w Windows) – ma własny mechanizm, ale analogiczny
- **FAT32** – nie wspiera

### Zastosowania:
- Znaczniki bezpieczeństwa (np. `security.selinux`)
- Atrybuty używane przez `rsync`, `tar`, `backup` itp.
- Przechowywanie niestandardowych metadanych (np. tagi, hash pliku, informacje o właścicielu logicznym)

Daj znać, jeśli chcesz przykład w kodzie lub chcesz sprawdzić, czy dany system plików wspiera extended attributes.