# Niezmieniane EOL w Git

**Data:** 2023-06-16

---

**User:**

Mam repozytorium z plikami z różnymi końcami linii CRLF i LF. Jak mam ustawić gita żeby przy edycji pliku nie zmieniał znaków końca linii?

---

**Assistant:**

Aby Git nie zmieniał automatycznie znaków końca linii przy edycji plików, możesz ustawić odpowiednie atrybuty konfiguracyjne dla repozytorium. W przypadku systemów Unix/Linux, gdzie standardowo używany jest znak nowej linii (LF), możesz ustawić atrybut `core.eol` na wartość `lf`. Natomiast dla systemów Windows, gdzie standardowo używany jest zestaw znaków powrotu karetki i nowej linii (CRLF), możesz ustawić atrybut `core.eol` na wartość `crlf`.

Aby to zrobić, wykonaj następujące kroki:

1. Otwórz terminal lub konsolę w katalogu głównym repozytorium.

2. Wykonaj poniższą komendę, aby ustawić atrybut dla znaków końca linii dla plików na LF:
   ```
   git config core.eol lf
   ```

   Jeśli preferujesz CRLF jako znaki końca linii, wykonaj zamiast tego tę komendę:
   ```
   git config core.eol crlf
   ```

3. Dodaj następujący atrybut, aby Git nie konwertował automatycznie znaków końca linii:
   ```
   git config core.autocrlf false
   ```

Po wykonaniu tych kroków Git nie będzie zmieniał automatycznie znaków końca linii przy edycji plików. Pamiętaj jednak, że istniejące pliki w repozytorium, które mają różne znaki końca linii, mogą wymagać ręcznej konwersji, jeśli chcesz zachować spójność.