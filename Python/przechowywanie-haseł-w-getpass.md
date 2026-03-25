# Przechowywanie haseł w getpass

**Data:** 2025-09-11

---

**User:**

gdzie i w jakiej formie przechowywane są hasła w getpass w python?

---

**Assistant:**

Moduł **`getpass`** w Pythonie nie przechowuje haseł w żadnej trwałej formie.  

### Jak to działa:
- Funkcja `getpass.getpass()` służy tylko do **bezpiecznego pobrania hasła od użytkownika z terminala** (bez jego wyświetlania na ekranie).
- W praktyce:
  - na Uniksach/Linuxie używa funkcji systemowych do wyłączenia echa na terminalu (`termios` / `tty`),
  - na Windowsie korzysta z `msvcrt.getwch()` do odczytu znaków bez ich wyświetlania.
- Hasło zwracane jest jako **zwykły obiekt typu `str`** w Pythonie i istnieje tylko w pamięci RAM twojego procesu.
- Nie jest nigdzie zapisywane, buforowane ani szyfrowane przez `getpass`.  

### Ważne skutki:
- Po wywołaniu `pwd = getpass.getpass()` hasło znajdziesz tylko w zmiennej `pwd`.  
- To oznacza, że jeśli chcesz je wykorzystać do logowania, szyfrowania czy przechowywania, sam musisz zadbać o bezpieczeństwo (np. szyfrowanie, czyszczenie zmiennej po użyciu).
- W RAM-ie zostaje ono do momentu, aż obiekt zostanie zwolniony przez garbage collector.  

Czy chcesz, żebym pokazał Ci przykładowy kod, który pokazuje jak `getpass` działa "pod spodem" (np. na Linuxie)?