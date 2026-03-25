# działa.  Dodaj poziomy, działający scrollbar.

**Data:** 13 gru 2025, 00:15:35 CET

---

**User:**

działa. 
Dodaj poziomy, działający scrollbar.

---

**Gemini:**

Aby poziomy pasek przewijania (horizontal scrollbar) działał w `tkinter.Treeview`, muszą zostać spełnione dwa warunki, które często są pomijane:

1. Kolumny muszą mieć **zablokowane rozciąganie** (`stretch=False`). Jeśli rozciąganie jest włączone (domyślnie jest), `Treeview` spróbuje upchnąć tekst w widocznym oknie, zamiast aktywować pasek przewijania.
2. Suma szerokości kolumn musi być fizycznie **większa** niż szerokość okna programu.

Poniżej znajduje się finalny kod. Zmieniłem sposób układania elementów w sekcji listy na `grid` (jest stabilniejszy dla pasków przewijania) i ustawiłem kolumnę z treścią na sztywną szerokość **3000 pikseli**, co wymusi pojawienie się suwaka.

### Kompletny kod (wersja 2.2)

```
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class JsonEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced JSON List Editor v2.2")
        self.root.geometry("1000x600")

        self.json_data = []
        self.current_filepath = None
        
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
        
        ttk.Button(btn_frame, text="Load JSON (Ctrl+O)", command=self.load_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Save JSON (Ctrl+S)", command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Selected (Del)", command=self.delete_selected_item).pack(side=tk.LEFT, padx=2)

        # --- Main List Area (Using Grid for better scrollbar control) ---
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Configure grid weights so the treeview expands but scrollbars stay slim
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

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
        
        # Link scrollbars
        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        # Layout Elements in Grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        # --- Column Configuration ---
        self.tree.heading("index", text="#")
        self.tree.column("index", width=60, stretch=False, anchor=tk.CENTER)
        
        self.tree.heading("content", text="JSON Object Content (Double-click to edit)")
        # CRITICAL CHANGE: width set to 3000 and stretch=False ensures horizontal scroll works
        self.tree.column("content", width=3000, stretch=False, anchor=tk.W)

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
                self.tree.insert("", tk.END, iid=real_index, values=(real_index, display_text))
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
                del self.json_data[idx]
            self.refresh_list()
            self.status_var.set(f"Deleted {len(indices)} items.")

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id: return
        
        real_index = int(item_id)
        self.open_edit_window(real_index)

    def open_edit_window(self, index):
        obj = self.json_data[index]
        
        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Edit Item #{index}")
        edit_win.geometry("600x400")
        
        text_area = tk.Text(edit_win, font=("Consolas", 11), wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        formatted_json = json.dumps(obj, indent=4, ensure_ascii=False)
        text_area.insert(tk.END, formatted_json)

        def save_changes():
            content = text_area.get("1.0", tk.END).strip()
            try:
                new_obj = json.loads(content)
                if not isinstance(new_obj, dict):
                    raise ValueError("Edited content must be a JSON object (dictionary).")
                
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