# Java Code Improvement

**Data:** 2023-10-30

---

**User:**

Java, czy ten kod jest poprawny i czy można go ulepszyć?

ScanArgs  args = new ScanArgs();
int count = params.getCount();
if (count != 0L) {
  scanParams.limit(count);
}

---

**Assistant:**

Ten kod jest prawie poprawny, ale może być ulepszony. Oto poprawiona wersja:

```java
ScanArgs args = new ScanArgs();
long count = params.getCount(); // zmiana z int na long, aby pasowała do typu count
if (count != 0) { // sprawdzanie czy count jest różny od 0, bez potrzeby dodawania L na końcu
  args.limit(count); // zmiana scanParams na args, aby pasowało do nazwy zmiennej
}
```

W poprawionej wersji zmieniono nazwę zmiennej `scanParams` na `args`, aby pasowała do nazwy obiektu `ScanArgs`. Zmieniono także typ zmiennej `count` z `int` na `long`, aby dopasować ją do typu zwracanego przez `params.getCount()`. W warunku if usunięto literę "L" na końcu liczby, ponieważ typ `count` został zmieniony na `long`, co nie wymaga już dodatkowego oznaczenia literą "L".

---

**User:**

params.getCount() zwraca int, nie long

---

**Assistant:**

Jeśli `params.getCount()` zwraca `int`, a nie `long`, to nie ma potrzeby zmieniania typu zmiennej `count`. Poprawiony kod wyglądałby następująco:

```java
ScanArgs args = new ScanArgs();
int count = params.getCount();
if (count != 0) {
  args.limit(count);
}
```

W poprawionej wersji zmieniono nazwę zmiennej `scanParams` na `args`, aby pasowała do nazwy obiektu `ScanArgs`. Następnie warunek `count != 0L` został zmieniony na `count != 0`, aby porównywać bez konieczności dodawania literki "L" na końcu liczby.