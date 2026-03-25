# Działa dobrze. Teraz rozszerzymy funkcje.  Popraw wyświetlanie tekstu. Zrób więk

**Data:** 13 gru 2025, 00:08:07 CET

---

**User:**

Działa dobrze. Teraz rozszerzymy funkcje. 
Popraw wyświetlanie tekstu. Zrób większe odstępy między wierszami, ale tylko troszkę. Tekst w kolumnie JSON Object Content jest obcinany i zakończony ... Chcę mieć możliwość odczytania całego tekstu. Czy jest możliwe żeby ten tekst był również edytowalny?

---

**Gemini:**

Tak, jest to możliwe. Aby uczynić tekst edytowalnym w sposób bezpieczny (tak, aby nie zepsuć struktury JSON), najlepszym rozwiązaniem w `tkinter` jest otwarcie osobnego okna edycji po dwukrotnym kliknięciu na wiersz. Pozwala to na wygodną edycję sformatowanego JSON-a i walidację poprawności przed zapisaniem zmian.

Poniżej znajduje się zaktualizowany kod. Wprowadzone zmiany:

1. **Edycja (Double-Click):** Dwukrotne kliknięcie na wiersz otwiera okno z pełną treścią obiektu. Możesz go tam edytować i zapisać. Program sprawdzi, czy nowy tekst jest poprawnym JSON-em.
2. **Pełny tekst:** Usunięto obcinanie tekstu (`...`). Dodano poziomy pasek przewijania (scrollbar), aby można było czytać długie wiersze.
3. **Większe odstępy:** Zwiększono `rowheight` w stylu Treeview z 25 na 35 pikseli.

```
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class JsonEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced JSON List Editor v2")
        self.root.geometry("1000x600")

        self.json_data = []
        self.current_filepath = None
        
        self._setup_styles()
        self._create_widgets()
        self._bind_shortcuts()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        # Zwiększono rowheight do 35 (większe odstępy)
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
        
        ttk.Button(btn_frame, text="Load JSON (Ctrl+O)", command=self.load_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Save JSON (Ctrl+S)", command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Selected (Del)", command=self.delete_selected_item).pack(side=tk.LEFT, padx=2)

        # --- Main List Area with Dual Scrollbars ---
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbars
        v_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)

        # Treeview
        self.tree = ttk.Treeview(
            list_frame, 
            columns=("index", "content"), 
            show="headings", 
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )
        
        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        # Layout scrollbars
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.heading("index", text="#")
        self.tree.column("index", width=60, stretch=False, anchor=tk.CENTER)
        self.tree.heading("content", text="JSON Object Content (Double-click to edit)")
        # Minwidth ustawione wysoko, żeby tekst się mieścił
        self.tree.column("content", width=800, minwidth=400, anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind Double Click for Editing
        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Load a file to start.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _bind_shortcuts(self):
        self.root.bind('<Delete>', lambda e: self.delete_selected_item())
        self.root.bind('<Control-o>', lambda e: self.load_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if not filepath: return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list): raise ValueError("JSON root must be a list.")
            self.json_data = data
            self.current_filepath = filepath
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
                
                # Check Key
                k_cond = (key_filter in str_k) if key_filter else True
                # Check Value
                v_cond = (val_filter in str_v) if val_filter else True

                if k_cond and v_cond:
                    match_key = True
                    match_val = True
                    break 
            
            if match_key and match_val:
                # Usunięto obcinanie tekstu
                display_text = json.dumps(obj, ensure_ascii=False)
                self.tree.insert("", tk.END, iid=real_index, values=(real_index, display_text))
                count += 1
        
        msg = f"Showing {count} items."
        if self.current_filepath: msg += f" File: {os.path.basename(self.current_filepath)}"
        self.status_var.set(msg)

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected: return
        
        # Jeśli okno edycji jest otwarte, blokujemy usuwanie (dla bezpieczeństwa)
        # W prostej wersji po prostu usuwamy
        indices = sorted([int(x) for x in selected], reverse=True)
        for idx in indices:
            del self.json_data[idx]
        self.refresh_list()

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id: return
        
        real_index = int(item_id)
        self.open_edit_window(real_index)

    def open_edit_window(self, index):
        """Otwiera okno modalne do edycji pojedynczego obiektu JSON"""
        obj = self.json_data[index]
        
        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Edit Item #{index}")
        edit_win.geometry("600x400")
        
        # Text Area with current JSON formatted nicely
        text_area = tk.Text(edit_win, font=("Consolas", 11), wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pretty print for easier editing
        formatted_json = json.dumps(obj, indent=4, ensure_ascii=False)
        text_area.insert(tk.END, formatted_json)

        def save_changes():
            content = text_area.get("1.0", tk.END).strip()
            try:
                # Validate JSON
                new_obj = json.loads(content)
                if not isinstance(new_obj, dict):
                    raise ValueError("Edited content must be a JSON object (dictionary).")
                
                # Update data
                self.json_data[index] = new_obj
                self.refresh_list()
                edit_win.destroy()
                self.status_var.set(f"Item #{index} updated successfully.")
            except json.JSONDecodeError as e:
                messagebox.showerror("Invalid JSON", f"Syntax Error:\n{e}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        btn_frame = ttk.Frame(edit_win)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Save Changes", command=save_changes).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="Cancel", command=edit_win.destroy).pack(side=tk.RIGHT, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonEditorApp(root)
    root.mainloop()
```