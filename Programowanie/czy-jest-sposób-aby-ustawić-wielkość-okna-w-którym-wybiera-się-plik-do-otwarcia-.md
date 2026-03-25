# czy jest sposób aby ustawić wielkość okna w którym wybiera się plik do otwarcia?

**Data:** 13 gru 2025, 13:33:51 CET

---

**User:**

czy jest sposób aby ustawić wielkość okna w którym wybiera się plik do otwarcia? nie pisz całego kodu od nowa tylko wskaż miejsce gdzie to zrobić

---

**Gemini:**

Niestety, w standardowej bibliotece `tkinter` **nie ma sposobu** na ustawienie wielkości tego konkretnego okna z poziomu kodu.

Funkcja `filedialog.askopenfilename`, która znajduje się w metodzie `load_file`, wywołuje **natywne okno systemowe** (Windowsa, macOS lub Linuxa). Python jedynie wysyła prośbę do systemu operacyjnego "pokaż okno wyboru plików", a system przejmuje nad nim kontrolę.

**Co możesz zrobić?**
System operacyjny zazwyczaj **zapamiętuje ostatni rozmiar** tego okna.

1. Uruchom program.
2. Kliknij "Otwórz".
3. Rozciągnij okno wyboru plików ręcznie myszką do żądanej wielkości.
4. Wybierz plik lub anuluj.
5. Przy następnym uruchomieniu okno powinno otworzyć się w takim rozmiarze, jaki ustawiłeś ręcznie.

Kod odpowiedzialny za to wywołanie znajduje się tutaj (nie ma tu parametru size/geometry do dodania):

```
    def load_file(self):
        # To wywołanie otwiera okno systemowe, którego rozmiaru nie można narzucić w kodzie
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        
        if not filepath: return
        # ... reszta kodu
```