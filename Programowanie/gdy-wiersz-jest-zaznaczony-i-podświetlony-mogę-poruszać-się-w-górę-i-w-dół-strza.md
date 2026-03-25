# Gdy wiersz jest zaznaczony i podświetlony mogę poruszać się w górę i w dół strza

**Data:** 13 gru 2025, 13:24:23 CET

---

**User:**

Gdy wiersz jest zaznaczony i podświetlony mogę poruszać się w górę i w dół strzałkami na klawiaturze. Gdy nacinsnę x podświetlenie znika i strzałki nie działają. Chcę aby po x podświetlony został kolejny wiersz, chyba że dalej nie ma następnego wiersza.

---

**Gemini:**

Rozumiem problem. Działo się tak, ponieważ w poprzedniej wersji metoda `refresh_list()` (wywoływana po naciśnięciu 'x') czyściła całą listę i budowała ją od nowa, przez co program "zapominał", gdzie był kursor (focus).

Aby to naprawić, musimy:

1. Aktualizować wygląd wiersza (kolor żółty) **bez** przeładowywania całej listy.
2. Ręcznie przesunąć zaznaczenie (selection) i focus na **następny element** w drzewie.

Oto poprawiona metoda `toggle_mark_for_move` oraz kompletny kod wersji **2.5**.

### Co zmieniono w kodzie?

W funkcji `toggle_mark_for_move`:

- Zamiast `self.refresh_list()`, używam `self.tree.item(id, tags=...)`. To zmienia kolor wiersza w ułamku sekundy bez resetowania widoku.
- Używam `self.tree.next(last_selected)`, aby znaleźć identyfikator kolejnego wiersza.
- Następnie ustawiam na nim `selection_set` (podświetlenie) i `focus` (dla klawiatury).

### Kompletny kod (wersja 2.5)

```
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class JsonEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Editor v2.5 - Smooth Selection")
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
        # Parametr rowheight odpowiada za wysokość wiersza (odstępy)
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

        info_label = ttk.Label(btn_frame, text=" | [x] Oznacz/Przejdź dalej | [v] Wklej", foreground="blue")
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
            selectmode="extended"
        )
        
        # Styl dla wierszy oznaczonych do przeniesienia (żółty)
        self.tree.tag_configure('marked_for_move', background='#fffacd') 

        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        self.tree.heading("index", text="#")
        self.tree.column("index", width=60, stretch=False, anchor=tk.CENTER)
        
        self.tree.heading("content", text="Treść obiektu JSON")
        # Parametr width odpowiada za długość scrollbara poziomego (obszar wirtualny)
        self.tree.column("content", width=3000, stretch=False, anchor=tk.W)

        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Pasek statusu ---
        self.status_var = tk.StringVar()
        self.status_var.set("Gotowy.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _bind_shortcuts(self):
        self.root.bind('<Delete>', lambda e: self.delete_selected_item())
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        
        # Skróty dla Treeview
        self.tree.bind('x', self.toggle_mark_for_move)
        self.tree.bind('v', self.move_items_here)

    def toggle_mark_for_move(self, event):
        """Oznacza wiersze na żółto i automatycznie przechodzi do następnego."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        # 1. Zaktualizuj status (żółty kolor) dla zaznaczonych elementów
        for item_id in selected_items:
            real_index = int(item_id)
            
            # Logika toggle
            if real_index in self.marked_indices:
                self.marked_indices.remove(real_index)
            else:
                self.marked_indices.add(real_index)
            
            # Bezpośrednia aktualizacja tagu w drzewie (bez refresh_list!)
            # Dzięki temu nie tracimy focusu ani pozycji scrolla
            tags = ('marked_for_move',) if real_index in self.marked_indices else ()
            self.tree.item(item_id, tags=tags)

        self.status_var.set(f"Schowek: {len(self.marked_indices)} elem.")

        # 2. Przesuń zaznaczenie na kolejny element
        # Bierzemy ostatni z aktualnie zaznaczonych (w przypadku multiselect)
        last_selected = selected_items[-1]
        next_item = self.tree.next(last_selected)

        if next_item:
            self.tree.selection_set(next_item) # Zaznacz (niebieski)
            self.tree.focus(next_item)         # Ustaw focus (dla klawiatury)
            self.tree.see(next_item)           # Przewiń, jeśli poza ekranem
        else:
            # Jeśli to był ostatni element, po prostu zdejmij zaznaczenie z obecnego,
            # żeby widać było, że został "odznaczony" na żółto
            self.tree.selection_remove(selected_items)

    def move_items_here(self, event):
        """Wkleja żółte elementy pod aktualnie wybrany wiersz."""
        if not self.marked_indices:
            self.status_var.set("Schowek pusty. Użyj 'x' aby dodać elementy.")
            return

        target_item = self.tree.focus()
        if not target_item:
            self.status_var.set("Brak celu. Zaznacz wiersz.")
            return

        target_index = int(target_item)

        if target_index in self.marked_indices:
            self.status_var.set("Nie można wkleić wewnątrz przenoszonego bloku.")
            return

        # Pobieranie i usuwanie (standardowa logika)
        indices_list = sorted(list(self.marked_indices))
        items_to_move = [self.json_data[i] for i in indices_list]

        items_removed_before_target = sum(1 for idx in self.marked_indices if idx < target_index)
        
        for idx in sorted(indices_list, reverse=True):
            del self.json_data[idx]

        current_target_pos = target_index - items_removed_before_target
        insert_pos = current_target_pos + 1

        self.json_data[insert_pos:insert_pos] = items_to_move

        count = len(self.marked_indices)
        self.marked_indices.clear()
        
        # Tutaj musimy odświeżyć całą listę, bo kolejność się zmieniła
        self.refresh_list()
        
        # Próba przywrócenia focusu na przeniesione elementy (opcjonalne)
        if count > 0 and insert_pos < len(self.json_data):
            # Nowy ID pierwszego wklejonego elementu (w uproszczeniu, bo ID=index)
            # Uwaga: przy filtrowaniu ID mogą nie być ciągłe, ale refresh_list resetuje ID do indeksów
            new_selection_id = str(insert_pos)
            if self.tree.exists(new_selection_id):
                self.tree.selection_set(new_selection_id)
                self.tree.focus(new_selection_id)
                self.tree.see(new_selection_id)

        self.status_var.set(f"Przeniesiono {count} elementów.")

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected: return
        
        if messagebox.askyesno("Potwierdź", f"Usunąć {len(selected)} elementów?"):
            indices = sorted([int(x) for x in selected], reverse=True)
            for idx in indices:
                if idx in self.marked_indices:
                    self.marked_indices.remove(idx)
                del self.json_data[idx]
            
            if self.marked_indices:
                self.marked_indices.clear()
            
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
        # Ta funkcja jest "ciężka", używamy jej tylko przy filtrach, load, delete i paste
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
                row_tags = ('marked_for_move',) if real_index in self.marked_indices else ()
                self.tree.insert("", tk.END, iid=real_index, values=(real_index, display_text), tags=row_tags)
                count += 1
        
        msg = f"Widoczne: {count}."
        if self.current_filepath: msg += f" Plik: {os.path.basename(self.current_filepath)}"
        self.status_var.set(msg)

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id: return
        self.open_edit_window(int(item_id))

    def open_edit_window(self, index):
        obj = self.json_data[index]
        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Edycja #{index}")
        edit_win.geometry("600x400")
        
        text_area = tk.Text(edit_win, font=("Consolas", 11), wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, json.dumps(obj, indent=4, ensure_ascii=False))

        def save_changes():
            content = text_area.get("1.0", tk.END).strip()
            try:
                new_obj = json.loads(content)
                if not isinstance(new_obj, dict): raise ValueError("Wymagany słownik (dict).")
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