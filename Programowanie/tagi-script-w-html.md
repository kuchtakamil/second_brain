# Tagi script w HTML

**Data:** 2024-12-01

---

**User:**

W html linki do skryptów js umieszcza się w tagu head. Czy umieszczenie tagu script src=... poza head wywołuje negatywne konsekwencje?

---

**Assistant:**

Umieszczenie tagu `<script src="..."></script>` poza `<head>` (np. na końcu sekcji `<body>`) nie powoduje negatywnych konsekwencji — wręcz przeciwnie, w wielu przypadkach jest to preferowana praktyka.

Oto szczegóły:

### **Umieszczenie w `<head>`**
- Kiedy `<script>` znajduje się w `<head>`, przeglądarka musi załadować i wykonać skrypt zanim przejdzie do renderowania reszty dokumentu. 
- Może to opóźnić ładowanie i renderowanie strony, co negatywnie wpływa na wydajność użytkownika (np. widoczne opóźnienie w wyświetleniu treści strony).

### **Umieszczenie na końcu `<body>`**
- Skrypty umieszczone na końcu `<body>` ładują się dopiero po załadowaniu całego HTML i renderowaniu treści strony.
- Dzięki temu użytkownik szybciej widzi gotową treść strony, nawet jeśli skrypt jeszcze nie został załadowany.
- To podejście jest szczególnie korzystne w przypadku ciężkich skryptów lub kiedy nie są one krytyczne dla początkowego widoku strony.

### **Atrybuty async i defer**
Jeśli skrypty muszą być w `<head>`, można użyć atrybutów:
1. **`async`**: Skrypt ładuje się asynchronicznie i wykonuje zaraz po załadowaniu, niezależnie od renderowania dokumentu.
2. **`defer`**: Skrypt ładuje się asynchronicznie, ale wykonuje się dopiero po załadowaniu całego dokumentu.

Przykład:
```html
<head>
  <script src="script.js" defer></script>
</head>
```

### **Podsumowanie**
- **Bez negatywnych konsekwencji**: Umieszczenie skryptów na końcu `<body>` to dobra praktyka poprawiająca wydajność.
- **Unikaj blokowania renderowania**: Jeśli musisz umieścić skrypty w `<head>`, używaj `async` lub `defer`.
- **Wyjątki**: Jeśli skrypt musi być wykonany przed renderowaniem (np. narzędzia analityczne lub konfiguracja strony), to może być konieczne umieszczenie go w `<head>`.

Wybór miejsca zależy od potrzeb Twojej strony i priorytetu ładowania danego skryptu.