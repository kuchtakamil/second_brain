# Czy możesz dodać funkcje aby móc zaznaczyć w jakiś sposób wybrane wiersze np. kl

**Data:** 13 gru 2025, 00:24:05 CET

---

**User:**

Czy możesz dodać funkcje aby móc zaznaczyć w jakiś sposób wybrane wiersze np. klawiszem x, a potem przechodzę na inny wiersz i po przyciśnięciu klawisza v te wcześniej zaznaczone wiersze zostaną przeniesione poniżej tego obecnego wiersza.

---

**Gemini:**

Oto zaktualizowany kod, który implementuje funkcję **Wytnij i Wklej (Przenieś)**.

### Jak to działa?

1. **Zaznaczanie (Klawisz `x`):** Zaznaczasz jeden lub więcej wierszy i wciskasz `x`. Wiersze te zmienią kolor tła na **żółty**, co oznacza, że są gotowe do przeniesienia.
2. **Przenoszenie (Klawisz `v`):** Klikasz na inny wiersz (docelowy) i wciskasz `v`. Wcześniej zaznaczone (żółte) wiersze zostaną usunięte ze swoich starych pozycji i wstawione **poniżej** wiersza, na którym stoisz.

### Kod programu (wersja 2.3)

```
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class JsonEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced JSON List Editor v2.3 - Move Feature")
        self.root.geometry("1000x600")

        self.json_data = []
        self.current_filepath = None
        
        # Przechowuje indeksy wierszy zaznaczonych do przeniesienia (schowek)
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
        # --- Top Control Panel ---
        control_frame = ttk.LabelFrame(self.root, text="Filter & Actions", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Filter Key:").grid(row=0, column=0, padx=5)
        self.entry_key_filter = ttk.Entry(control_frame, width=20)
        self.entry_key_filter.grid(row=0, column=1, padx=5)
        self.entry_key_filter.bind('<KeyRelease>', self.apply_filters)

        ttk.Label(control_frame, text="Filter Value:").grid(row=0, column=2, padx=5)
        self.entry_val_filter = ttk.Entry(control_frame, width=30)
        self.entry_val_filter.grid(row=0, column=3, padx=5)
        self.entry_val_filter.bind('<KeyRelease>', self.apply_filters)

        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=0, column=4, padx=20, sticky=tk.E)
        
        ttk.Button(btn_frame, text="Load (Ctrl+O)", command=self.load_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Save (Ctrl+S)", command=self.save_file).pack(side=tk.LEFT, padx=2)
        # Informacja o skrótach w interfejsie
        ttk.Label(btn_frame, text=" |  [x] = Cut, [v] = Paste Below").pack(side=tk.LEFT, padx=10)

        # --- Main List Area ---
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
            xscrollcommand=h_scroll.set
        )
        
        # Konfiguracja tagu dla zaznaczonych do przeniesienia (żółte tło)
        self.tree.tag_configure('marked_for_move', background='#fffacd') 

        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        self.tree.heading("index", text="#")
        self.tree.column("index", width=60, stretch=False, anchor=tk.CENTER)
        
        self.tree.heading("content", text="JSON Object Content")
        self.tree.column("content", width=3000, stretch=False, anchor=tk.W)

        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        self.status_var.set("Ready.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _bind_shortcuts(self):
        self.root.bind('<Delete>', lambda e: self.delete_selected_item())
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        # Nowe skróty do przenoszenia
        self.root.bind('x', self.mark_for_move)
        self.root.bind('v', self.move_items_here)

    def mark_for_move(self, event):
        """Zaznacza wybrane wiersze do przeniesienia (koloruje na żółto)."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        # Czyścimy poprzednie zaznaczenie (opcjonalnie, można też dodawać)
        self.marked_indices.clear()
        
        for item in selected_items:
            real_index = int(item)
            self.marked_indices.add(real_index)
        
        self.refresh_list()
        self.status_var.set(f"Marked {len(self.marked_indices)} items for moving. Select destination and press 'v'.")

    def move_items_here(self, event):
        """Przenosi zaznaczone (żółte) wiersze poniżej aktualnie zaznaczonego wiersza."""
        if not self.marked_indices:
            self.status_var.set("No items marked. Select items and press 'x' first.")
            return

        # Pobierz element docelowy (target) - ten na którym stoi kursor
        target_item = self.tree.focus()
        if not target_item:
            self.status_var.set("No destination row selected.")
            return

        target_index = int(target_item)

        # Nie można przenieść, jeśli cel jest jednym z zaznaczonych elementów
        if target_index in self.marked_indices:
            self.status_var.set("Cannot move items into themselves.")
            return

        # --- Logika przenoszenia ---
        
        # 1. Pobierz obiekty do przeniesienia
        items_to_move = []
        sorted_indices_to_move = sorted(list(self.marked_indices))
        for idx in sorted_indices_to_move:
            items_to_move.append(self.json_data[idx])

        # 2. Usuń je ze starych miejsc (od tyłu, żeby nie psuć indeksów)
        for idx in sorted(list(self.marked_indices), reverse=True):
            del self.json_data[idx]

        # 3. Oblicz nowy indeks wstawienia
        # Ponieważ usunęliśmy elementy, indeksy "powyżej" celu mogły się zmienić.
        # Musimy odjąć od target_index liczbę elementów usuniętych, które znajdowały się PRZED nim.
        items_removed_before_target = sum(1 for idx in self.marked_indices if idx < target_index)
        new_target_index = target_index - items_removed_before_target
        
        # Wstawiamy PO elemencie docelowym, więc +1
        insert_pos = new_target_index + 1

        # 4. Wstaw elementy w nowe miejsce
        # Wstawiamy je w odwrotnej kolejności (jeśli używamy insert na tej samej pozycji) 
        # lub w normalnej inkrementując pozycję. Użyjmy slice assignment dla czytelności.
        
        self.json_data[insert_pos:insert_pos] = items_to_move

        # 5. Sprzątanie
        self.marked_indices.clear()
        self.refresh_list()
        
        # Opcjonalnie: zaznacz nowo przeniesione elementy w nowym miejscu
        # (Wymagałoby obliczenia ich nowych ID, dla uproszczenia pomijamy)
        self.status_var.set("Items moved successfully.")

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
            self.status_var.set(f"Saved to {os.path.basename(filepath)}")
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
                
                # Sprawdź, czy ten indeks jest oznaczony do przeniesienia
                # Jeśli tak, dodaj tag 'marked_for_move'
                row_tags = ('marked_for_move',) if real_index in self.marked_indices else ()

                self.tree.insert("", tk.END, iid=real_index, values=(real_index, display_text), tags=row_tags)
                count += 1
        
        msg = f"Showing {count} items."
        if self.current_filepath: msg += f" File: {os.path.basename(self.current_filepath)}"
        self.status_var.set(msg)

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected: return
        
        if messagebox.askyesno("Confirm", f"Delete {len(selected)} items?"):
            indices = sorted([int(x) for x in selected], reverse=True)
            for idx in indices:
                # Jeśli usuwamy coś, co było zaznaczone do przenoszenia, usuń to też z setu marked
                if idx in self.marked_indices:
                    self.marked_indices.remove(idx)
                del self.json_data[idx]
            
            # Musimy wyczyścić marked_indices całkowicie, bo indeksy się przesunęły
            # i stare zaznaczenia będą wskazywać na złe obiekty.
            if self.marked_indices:
                self.marked_indices.clear()
                self.status_var.set("Deleted items. Move selection cleared due to index shift.")
            
            self.refresh_list()

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id: return
        self.open_edit_window(int(item_id))

    def open_edit_window(self, index):
        obj = self.json_data[index]
        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Edit Item #{index}")
        edit_win.geometry("600x400")
        
        text_area = tk.Text(edit_win, font=("Consolas", 11), wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, json.dumps(obj, indent=4, ensure_ascii=False))

        def save_changes():
            content = text_area.get("1.0", tk.END).strip()
            try:
                new_obj = json.loads(content)
                if not isinstance(new_obj, dict): raise ValueError("Must be a dict.")
                self.json_data[index] = new_obj
                self.refresh_list()
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(edit_win, text="Save", command=save_changes).pack(side=tk.RIGHT, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonEditorApp(root)
    root.mainloop()
```