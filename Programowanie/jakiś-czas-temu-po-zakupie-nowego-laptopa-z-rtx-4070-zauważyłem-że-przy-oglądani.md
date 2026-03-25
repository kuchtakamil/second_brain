# Jakiś czas temu po zakupie nowego laptopa z RTX 4070 zauważyłem że przy oglądani

**Data:** 26 cze 2025, 23:16:02 CET

---

**User:**

Jakiś czas temu po zakupie nowego laptopa z RTX 4070 zauważyłem że przy oglądaniu youtube na chrome i ruszaniu myszką ekran mruga, staje się biały na ułamki sekund. Znalazłem wtedy w internecie jakąś instrukcję która mówiła żeby coś wyłączyć albo włączyć w ustawieniach chrome. Chyba chodziło o jakieś wspieranie sprzętowe. Poszukaj co to było

---

**Gemini:**

Prawdopodobnie chodziło o jedną z dwóch funkcji: akcelerację sprzętową lub MPO (Multi-plane Overlay). Obie są związane z tym, jak przeglądarka wykorzystuje procesor graficzny (GPU) do renderowania treści.

### Rozwiązanie 1: Wyłączenie Akceleracji Sprzętowej (Najbardziej prawdopodobne)

Jest to najczęstsza przyczyna problemów z renderowaniem w przeglądarkach. Akceleracja sprzętowa polega na przekazywaniu zadań związanych z wyświetlaniem grafiki z procesora (CPU) na wyspecjalizowany procesor graficzny (GPU). Czasami, z powodu błędów w sterownikach lub w implementacji przeglądarki, powoduje to artefakty, takie jak migotanie.

**Jak wyłączyć:**

1. Otwórz Google Chrome.
2. Wklej w pasku adresu `chrome://settings/system` i naciśnij Enter.
3. Znajdź opcję **"Użyj akceleracji sprzętowej, gdy jest dostępna"** (Use hardware acceleration when available).
4. Wyłącz tę opcję.
5. Uruchom ponownie przeglądarkę.

### Rozwiązanie 2: Wyłączenie MPO (Multi-plane Overlay) (Bardziej zaawansowane i bardzo częste w przypadku kart NVIDIA)

MPO to funkcja systemu Windows (od Windows 8.1), która pozwala na bardziej efektywne renderowanie i kompozycję okien na pulpicie. Zamiast składać cały obraz pulpitu w jeden bufor, MPO pozwala GPU na operowanie na wielu "płaszczyznach" (overlays) jednocześnie (np. jedna płaszczyzna dla wideo, druga dla interfejsu przeglądarki, trzecia dla kursora myszy).

Problem polega na tym, że sterowniki NVIDIA (szczególnie w połączeniu z nowymi architekturami, jak w serii RTX 30xx i 40xx) miały liczne problemy ze stabilnością MPO w aplikacjach opartych na Chromium (Chrome, Edge). Objawia się to właśnie losowym migotaniem, czarnymi lub białymi ekranami, zwłaszcza gdy na dynamicznej treści (jak wideo) pojawia się inny element (jak kursor myszy).

Wyłączenie MPO na poziomie systemu operacyjnego często definitywnie rozwiązuje ten problem, nie wpływając negatywnie na wydajność w grach, a jedynie zmieniając sposób, w jaki pulpit Windows komponuje okna.

**Jak wyłączyć MPO (wymaga edycji rejestru):**

> **Ostrzeżenie:** Edycja rejestru systemowego może być ryzykowna. Zalecane jest wykonanie kopii zapasowej rejestru przed wprowadzeniem zmian.

1. Otwórz Notatnik.
2. Wklej do niego poniższą treść:

   ```
   Windows Registry Editor Version 5.00

   [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Dwm]
   "OverlayTestMode"=dword:00000005
   ```
3. Zapisz plik z rozszerzeniem `.reg` (np. `Disable_MPO.reg`). Upewnij się, że w oknie zapisu w polu "Zapisz jako typ" wybrałeś "Wszystkie pliki (`*.*`)".
4. Kliknij prawym przyciskiem myszy na zapisany plik `.reg` i wybierz "Scal" (Merge).
5. Potwierdź chęć dodania informacji do rejestru.
6. Uruchom ponownie komputer, aby zmiany weszły w życie.

Aby przywrócić domyślne ustawienie MPO, możesz usunąć stworzony wpis, używając pliku `.reg` z poniższą zawartością lub usuwając klucz `OverlayTestMode` ręcznie za pomocą edytora rejestru (`regedit.exe`):

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\Dwm]
"OverlayTestMode"=-
```

### Rozwiązanie 3: Zmiana Backendu Graficznego ANGLE

Chrome używa warstwy pośredniczącej o nazwie ANGLE (Almost Native Graphics Layer Engine) do tłumaczenia wywołań API graficznego (zazwyczaj WebGL, opartego na OpenGL ES) na natywne API systemu operacyjnego, takie jak Direct3D w Windows. Czasami zmiana backendu, którego używa ANGLE, może rozwiązać problemy ze sterownikami.

**Jak zmienić backend ANGLE:**

1. Otwórz Google Chrome.
2. Wklej w pasku adresu `chrome://flags/#use-angle` i naciśnij Enter.
3. Znajdziesz opcję **"Choose ANGLE graphics backend"**.
4. Możesz eksperymentalnie zmienić wartość z `Default` na `D3D11`, `D3D9` lub `OpenGL`.
5. Po każdej zmianie uruchom ponownie przeglądarkę i sprawdź, czy problem ustąpił. Dla kart NVIDIA, `D3D11` lub `OpenGL` są zazwyczaj dobrymi alternatywami do przetestowania.

Z dużym prawdopodobieństwem problemem, który pamiętasz, było wyłączenie akceleracji sprzętowej (Rozwiązanie 1). Jednakże, w przypadku nowej karty RTX 4070, faktycznym źródłem problemu jest najprawdopodobniej MPO (Rozwiązanie 2) i jego wyłączenie jest technicznie lepszym i bardziej trwałym rozwiązaniem.