# Chciałbym móc zaznaczyć kilka wierszy klawiszem x, dowolnych wierszy np. wiersze

**Data:** 13 gru 2025, 00:28:43 CET

---

**User:**

Chciałbym móc zaznaczyć kilka wierszy klawiszem x, dowolnych wierszy np. wiersze numer 6, 72, 85 i 332 a potem wszystkie wkleić klawiszem v.
Widzę że przez przypadek skasowałeś funkcję kasowania - delete. Przywróć ją proszę.

---

**Gemini:**

Zrozumiałem. Poprzednia wersja przy klawiszu `x` czyściła listę zaznaczonych elementów, zamiast do niej dopisywać. W tej wersji to naprawimy.

Oto wprowadzone zmiany:

1. **Kumulatywne zaznaczanie (`x`):** Teraz wciśnięcie `x` działa jak **przełącznik (toggle)**. Jeśli wiersz nie jest zaznaczony na żółto -> zaznacza go. Jeśli już jest -> odznacza go. Dzięki temu możesz skakać po liście i zaznaczać dowolne wiersze (np. 6, 72, 85).
2. **Przywrócone usuwanie (`Delete`):** Sprawdziłem wiązania klawiszy. Funkcja usuwania działa na **niebieskim zaznaczeniu** (tym systemowym), a nie na żółtym (tym do przenoszenia). To pozwala na niezależne zaznaczanie do przeniesienia i niezależne usuwanie.
3. **Inteligentne przenoszenie (`v`):** Algorytm przenoszenia został poprawiony, aby poprawnie obliczać nową pozycję, nawet gdy przenosisz wiersze z góry na dół i odwrotnie.

### Kompletny kod (wersja 2.4)

```
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class JsonEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Editor v2.4 - Multi-Select Move & Fixes")
        self.root.geometry("1000x600")

        self.json_data = []
        self.current_filepath = None
        
        # Zbiór indeksów zaznaczonych "na żółto" do przeniesienia
        self.marked_indices = set()

        self._setup_styles()
        self._create_widgets()
        self._bind_shortcuts()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", rowheight=35, font=('Consolas', 10))
        style.configure("TLabel", font=('Segoe UI', 10))
        style.configure("TButton", font=('Segoe UI', 9))

    def _create_widgets(self):
        # --- Panel sterowania ---
        control_frame = ttk.LabelFrame(self.root, text="Panel sterowania", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Filtr Klucz:").grid(row=0, column=0, padx=5)
        self.entry_key_filter = ttk.Entry(control_frame, width=20)
        self.entry_key_filter.grid(row=0, column=1, padx=5)
        self.entry_key_filter.bind('<KeyRelease>', self.apply_filters)

        ttk.Label(control_frame, text="Filtr Wartość:").grid(row=0, column=2, padx=5)
        self.entry_val_filter = ttk.Entry(control_frame, width=30)
        self.entry_val_filter.grid(row=0, column=3, padx=5)
        self.entry_val_filter.bind('<KeyRelease>', self.apply_filters)

        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=0, column=4, padx=20, sticky=tk.E)
        
        ttk.Button(btn_frame, text="Otwórz (Ctrl+O)", command=self.load_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Zapisz (Ctrl+S)", command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Usuń (Delete)", command=self.delete_selected_item).pack(side=tk.LEFT, padx=2)

        # Instrukcja skrótów
        info_label = ttk.Label(btn_frame, text=" | [x] Zaznacz/Odznacz do przenieś. | [v] Wklej pod spodem", foreground="blue")
        info_label.pack(side=tk.LEFT, padx=10)

        # --- Lista główna ---
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        v_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            list_frame, 
            columns=("index", "content"), 
            show="headings", 
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
            selectmode="extended" # Pozwala na zaznaczanie wielu wierszy shiftem/ctrl
        )
        
        # Styl dla wierszy zaznaczonych do przeniesienia (żółty)
        self.tree.tag_configure('marked_for_move', background='#fffacd') 

        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        self.tree.heading("index", text="#")
        self.tree.column("index", width=60, stretch=False, anchor=tk.CENTER)
        
        self.tree.heading("content", text="Treść obiektu JSON (Dwuklik edytuje)")
        self.tree.column("content", width=3000, stretch=False, anchor=tk.W)

        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Pasek statusu ---
        self.status_var = tk.StringVar()
        self.status_var.set("Gotowy.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _bind_shortcuts(self):
        # Delete działa globalnie na oknie
        self.root.bind('<Delete>', lambda e: self.delete_selected_item())
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        
        # 'x' i 'v' działają, gdy focus jest na liście (żeby nie pisać 'x' w filtrze)
        self.tree.bind('x', self.toggle_mark_for_move)
        self.tree.bind('v', self.move_items_here)

    def toggle_mark_for_move(self, event):
        """Dodaje lub usuwa zaznaczone wiersze ze zbioru 'do przeniesienia'."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        changed_count = 0
        for item in selected_items:
            real_index = int(item)
            
            if real_index in self.marked_indices:
                self.marked_indices.remove(real_index)
            else:
                self.marked_indices.add(real_index)
            changed_count += 1
        
        self.refresh_list()
        
        # Po wciśnięciu 'x' zdejmijmy systemowe zaznaczenie (niebieskie), żeby lepiej widzieć żółte
        # (Opcjonalne - jeśli wolisz, usuń poniższą linię)
        self.tree.selection_remove(self.tree.selection())

        self.status_var.set(f"Zaktualizowano zaznaczenie. Łącznie w schowku: {len(self.marked_indices)}. Wybierz cel i wciśnij 'v'.")

    def move_items_here(self, event):
        """Przenosi żółte wiersze pod aktualny wiersz."""
        if not self.marked_indices:
            self.status_var.set("Schowek pusty. Zaznacz wiersze klawiszem 'x'.")
            return

        target_item = self.tree.focus()
        if not target_item:
            self.status_var.set("Nie wybrano wiersza docelowego. Kliknij wiersz, pod który chcesz wkleić.")
            return

        target_index = int(target_item)

        if target_index in self.marked_indices:
            self.status_var.set("Nie możesz wkleić elementów wewnątrz nich samych.")
            return

        # 1. Pobierz obiekty do przeniesienia (zachowując ich pierwotną kolejność względem siebie)
        # Sortujemy indeksy rosnąco, żeby pobrać dane w dobrej kolejności
        indices_list = sorted(list(self.marked_indices))
        items_to_move = [self.json_data[i] for i in indices_list]

        # 2. Oblicz, ile elementów usuwamy powyżej celu (to przesunie indeks celu w górę)
        items_removed_before_target = sum(1 for idx in self.marked_indices if idx < target_index)
        
        # 3. Usuń elementy z listy głównej (od tyłu, żeby nie psuć indeksów podczas usuwania)
        for idx in sorted(indices_list, reverse=True):
            del self.json_data[idx]

        # 4. Oblicz nowy indeks wstawienia
        # Skorygowany cel to: stary_cel - liczba_usuniętych_nad_nim
        current_target_pos = target_index - items_removed_before_target
        
        # Wstawiamy POD celem, więc +1
        insert_pos = current_target_pos + 1

        # 5. Wstaw
        self.json_data[insert_pos:insert_pos] = items_to_move

        # 6. Czyść i odśwież
        count = len(self.marked_indices)
        self.marked_indices.clear()
        self.refresh_list()
        
        # Spróbujmy od razu zaznaczyć (na niebiesko) nowo przeniesione elementy w nowym miejscu
        new_selection = []
        for i in range(count):
            new_idx = insert_pos + i
            if new_idx < len(self.json_data): # safety check
                new_selection.append(str(new_idx))
        
        if new_selection:
            self.tree.selection_set(new_selection)
            self.tree.focus(new_selection[0])
            self.tree.see(new_selection[0])

        self.status_var.set(f"Przeniesiono {count} elementów.")

    def delete_selected_item(self):
        """Usuwa aktualnie zaznaczone (niebieskie) wiersze."""
        selected = self.tree.selection()
        if not selected: 
            self.status_var.set("Nic nie zaznaczono do usunięcia.")
            return
        
        if messagebox.askyesno("Potwierdź", f"Czy na pewno usunąć {len(selected)} elementów?"):
            indices = sorted([int(x) for x in selected], reverse=True)
            
            for idx in indices:
                # Jeśli usuwamy element, który był w schowku (żółty), usuń go też ze zbioru
                if idx in self.marked_indices:
                    self.marked_indices.remove(idx)
                
                # Usuń z danych
                del self.json_data[idx]
            
            # Ponieważ indeksy się zmieniły, stare zaznaczenia "żółte" mogą wskazywać na złe rzeczy.
            # Najbezpieczniej jest wyczyścić schowek przy usuwaniu, lub trzeba by przeliczać indeksy.
            # Tutaj: czyścimy schowek dla bezpieczeństwa.
            if self.marked_indices:
                self.marked_indices.clear()
                messagebox.showinfo("Info", "Zaznaczenie 'do przeniesienia' zostało wyczyszczone z powodu usunięcia wierszy.")

            self.refresh_list()
            self.status_var.set(f"Usunięto {len(indices)} elementów.")

    def apply_filters(self, event=None):
        self.refresh_list()

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if not filepath: return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list): raise ValueError("JSON root must be a list.")
            self.json_data = data
            self.current_filepath = filepath
            self.marked_indices.clear()
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_file(self):
        if not self.json_data: return
        filepath = filedialog.asksaveasfilename(defaultextension=".json", initialfile=os.path.basename(self.current_filepath) if self.current_filepath else "output.json")
        if not filepath: return
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.json_data, f, indent=4, ensure_ascii=False)
            self.current_filepath = filepath
            self.status_var.set(f"Zapisano do {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        key_filter = self.entry_key_filter.get().lower()
        val_filter = self.entry_val_filter.get().lower()

        count = 0
        for real_index, obj in enumerate(self.json_data):
            if not isinstance(obj, dict): continue
            
            match_key = False
            match_val = False
            
            for k, v in obj.items():
                str_k = str(k).lower()
                str_v = str(v).lower()
                k_cond = (key_filter in str_k) if key_filter else True
                v_cond = (val_filter in str_v) if val_filter else True

                if k_cond and v_cond:
                    match_key = True
                    match_val = True
                    break 
            
            if match_key and match_val:
                display_text = json.dumps(obj, ensure_ascii=False)
                
                # Dodaj tag, jeśli indeks jest w schowku
                row_tags = ('marked_for_move',) if real_index in self.marked_indices else ()

                self.tree.insert("", tk.END, iid=real_index, values=(real_index, display_text), tags=row_tags)
                count += 1
        
        msg = f"Wyświetlono {count} elementów."
        if self.current_filepath: msg += f" Plik: {os.path.basename(self.current_filepath)}"
        self.status_var.set(msg)

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id: return
        self.open_edit_window(int(item_id))

    def open_edit_window(self, index):
        obj = self.json_data[index]
        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Edycja elementu #{index}")
        edit_win.geometry("600x400")
        
        text_area = tk.Text(edit_win, font=("Consolas", 11), wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, json.dumps(obj, indent=4, ensure_ascii=False))

        def save_changes():
            content = text_area.get("1.0", tk.END).strip()
            try:
                new_obj = json.loads(content)
                if not isinstance(new_obj, dict): raise ValueError("Musi być obiektem (słownikiem).")
                self.json_data[index] = new_obj
                self.refresh_list()
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Błąd", str(e))

        ttk.Button(edit_win, text="Zapisz", command=save_changes).pack(side=tk.RIGHT, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonEditorApp(root)
    root.mainloop()
```