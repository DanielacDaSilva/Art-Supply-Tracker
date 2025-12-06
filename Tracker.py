import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# --- Janela Principal ---
root = tk.Tk()
root.title("Art Supply Tracker")
root.geometry("1000x500")
root.configure(bg="#f2f2f2")

# --- Inventário com mais itens ---
inventory = {
    "Canvas": {
        "Yellow": [{"quantity": 5, "brand": "BrandA"}],
        "Red": [{"quantity": 3, "brand": "BrandB"}],
        "Blue": [{"quantity": 4, "brand": "BrandC"}],
        "Green": [{"quantity": 2, "brand": "BrandD"}],
        "Black": [{"quantity": 6, "brand": "BrandE"}],
        "White": [{"quantity": 7, "brand": "BrandF"}],
        "Orange": [{"quantity": 1, "brand": "BrandG"}],
        "Purple": [{"quantity": 2, "brand": "BrandH"}],
        "Pink": [{"quantity": 3, "brand": "BrandI"}],
        "Brown": [{"quantity": 4, "brand": "BrandJ"}]
    },
    "Glitter": {
        "Gold": [{"quantity": 5, "brand": "BrandK"}],
        "Silver": [{"quantity": 4, "brand": "BrandL"}],
        "Red": [{"quantity": 3, "brand": "BrandM"}],
        "Blue": [{"quantity": 2, "brand": "BrandN"}],
        "Green": [{"quantity": 1, "brand": "BrandO"}],
        "Pink": [{"quantity": 6, "brand": "BrandP"}],
        "Purple": [{"quantity": 2, "brand": "BrandQ"}],
        "Black": [{"quantity": 3, "brand": "BrandR"}],
        "White": [{"quantity": 4, "brand": "BrandS"}],
        "Orange": [{"quantity": 2, "brand": "BrandT"}]
    },
    "Paint": {
        "Red": [{"quantity": 10, "brand": "BrandU"}],
        "Blue": [{"quantity": 8, "brand": "BrandV"}],
        "Yellow": [{"quantity": 6, "brand": "BrandW"}],
        "Green": [{"quantity": 5, "brand": "BrandX"}],
    },
    "Modeling Clay": {
        "Red": [{"quantity": 4, "brand": "BrandBB"}],
        "Blue": [{"quantity": 3, "brand": "BrandCC"}],
        "Yellow": [{"quantity": 6, "brand": "BrandDD"}]
    }
}

# --- Todas as cores possíveis ---
all_colors = ["Yellow", "Red", "Blue", "Green", "Black", "White", "Orange", "Purple", "Pink", "Brown", "Gold", "Silver", "Gray"]

# --- Sizes opcionais ---
all_sizes = ["Small", "Medium", "Large"]

# --- Mapeamento de cores ---
color_map = {
    "Yellow": "#FFFACD",
    "Red": "#FFC0CB",
    "Blue": "#ADD8E6",
    "Green": "#90EE90",
    "Black": "#A9A9A9",
    "White": "#FFFFFF",
    "Orange": "#FFD580",
    "Purple": "#D8BFD8",
    "Pink": "#FFB6C1",
    "Brown": "#DEB887",
    "Gold": "#FFD700",
    "Silver": "#C0C0C0",
    "Gray": "#D3D3D3"
}

# --- Funções ---
def update_fields(item_name, color_name, size_name=""):
    key = f"{color_name}/{size_name}" if size_name else color_name
    if item_name in inventory and key in inventory[item_name]:
        entry_quantity.delete(0, tk.END)
        entry_quantity.insert(0, str(inventory[item_name][key][0]["quantity"]))
        combo_brand['values'] = [b["brand"] for b in inventory[item_name][key]]
        if combo_brand['values']:
            combo_brand.current(0)
    update_table()

def color_selected(event):
    item_name = combo_item.get()
    color_name = combo_color.get()
    size_name = combo_size.get().strip()
    key = f"{color_name}/{size_name}" if size_name else color_name
    if item_name in inventory and key in inventory[item_name]:
        combo_brand['values'] = [b["brand"] for b in inventory[item_name][key]]
        if combo_brand['values']:
            combo_brand.current(0)
        entry_quantity.delete(0, tk.END)
        entry_quantity.insert(0, str(inventory[item_name][key][0]["quantity"]))
    update_table()

def size_selected(event):
    color_selected(None)  # Reutiliza a função color_selected

def brand_selected(event):
    item_name = combo_item.get()
    color_name = combo_color.get()
    size_name = combo_size.get().strip()
    key = f"{color_name}/{size_name}" if size_name else color_name
    brand_name = combo_brand.get()
    for b in inventory[item_name].get(key, []):
        if b["brand"] == brand_name:
            entry_quantity.delete(0, tk.END)
            entry_quantity.insert(0, str(b["quantity"]))
            break
    update_table()

def item_selected(event):
    item_name = combo_item.get()
    combo_color['values'] = all_colors
    combo_color.current(0)
    combo_size['values'] = all_sizes
    combo_size.set("")
    update_fields(item_name, combo_color.get())

def add_update_item():
    item_name = combo_item.get()
    color_name = combo_color.get()
    size_name = combo_size.get().strip()
    key = f"{color_name}/{size_name}" if size_name else color_name
    brand_name = combo_brand.get()
    try:
        quantity = int(entry_quantity.get())
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a number")
        return

    updated = False
    for b in inventory.get(item_name, {}).get(key, []):
        if b["brand"] == brand_name:
            b["quantity"] = quantity
            updated = True
            break

    if not updated:
        if item_name not in inventory:
            inventory[item_name] = {}
        if key not in inventory[item_name]:
            inventory[item_name][key] = []
        inventory[item_name][key].append({"quantity": quantity, "brand": brand_name})

    if color_name not in all_colors:
        all_colors.append(color_name)
        combo_color['values'] = all_colors
        messagebox.showinfo("New Color Added", f"Color '{color_name}' added to the arsenal!")

    update_table()

def remove_item():
    item_name = combo_item.get()
    color_name = combo_color.get()
    size_name = combo_size.get().strip()
    key = f"{color_name}/{size_name}" if size_name else color_name
    brand_name = combo_brand.get()
    if item_name in inventory and key in inventory[item_name]:
        inventory[item_name][key] = [b for b in inventory[item_name][key] if b["brand"] != brand_name]
        if not inventory[item_name][key]:
            del inventory[item_name][key]
        if not inventory[item_name]:
            del inventory[item_name]
    item_selected(None)
    update_table()

def add_new_item():
    def save_new_item():
        new_item = entry_new_item.get().strip()
        new_color = entry_new_color.get().strip()
        new_size = entry_new_size.get().strip()
        key = f"{new_color}/{new_size}" if new_size else new_color
        new_brand = entry_new_brand.get().strip()
        try:
            new_quantity = int(entry_new_quantity.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
            return
        if not new_item or not new_color or not new_brand:
            messagebox.showerror("Error", "Please fill all fields")
            return
        if new_item not in inventory:
            inventory[new_item] = {}
        if key not in inventory[new_item]:
            inventory[new_item][key] = []
        inventory[new_item][key].append({"quantity": new_quantity, "brand": new_brand})

        if new_color not in all_colors:
            all_colors.append(new_color)

        new_window.destroy()
        combo_item['values'] = list(inventory.keys())
        combo_item.set(new_item)
        combo_color['values'] = all_colors
        combo_color.set(new_color)
        combo_size['values'] = all_sizes
        combo_size.set(new_size)
        combo_brand['values'] = [b["brand"] for b in inventory[new_item][key]]
        combo_brand.current(0)
        update_table()

    new_window = tk.Toplevel(root)
    new_window.title("Add New Item")
    new_window.geometry("350x250")
    new_window.configure(bg="#f2f2f2")

    tk.Label(new_window, text="Item Name:", bg="#f2f2f2").pack(pady=2)
    entry_new_item = tk.Entry(new_window)
    entry_new_item.pack(pady=2)

    tk.Label(new_window, text="Color:", bg="#f2f2f2").pack(pady=2)
    entry_new_color = tk.Entry(new_window)
    entry_new_color.pack(pady=2)

    tk.Label(new_window, text="Size (optional):", bg="#f2f2f2").pack(pady=2)
    entry_new_size = tk.Entry(new_window)
    entry_new_size.pack(pady=2)

    tk.Label(new_window, text="Brand:", bg="#f2f2f2").pack(pady=2)
    entry_new_brand = tk.Entry(new_window)
    entry_new_brand.pack(pady=2)

    tk.Label(new_window, text="Quantity:", bg="#f2f2f2").pack(pady=2)
    entry_new_quantity = tk.Entry(new_window)
    entry_new_quantity.pack(pady=2)

    tk.Button(new_window, text="Add Item", command=save_new_item, bg="#4CAF50", fg="white").pack(pady=5)

def update_table():
    for row in tree.get_children():
        tree.delete(row)
    selected_color = combo_color.get()
    selected_size = combo_size.get().strip()
    key = f"{selected_color}/{selected_size}" if selected_size else selected_color
    selected_brand = combo_brand.get()
    for item_name in inventory.keys():
        quantity = 0
        brand = ""
        total = sum([b["quantity"] for blist in inventory[item_name].values() for b in blist])
        if selected_brand and key in inventory[item_name]:
            for b in inventory[item_name][key]:
                if b["brand"] == selected_brand:
                    quantity = b["quantity"]
                    brand = b["brand"]
                    break
        tree.insert("", tk.END, values=(item_name, quantity, brand, total), tags=(selected_color,))
        tree.tag_configure(selected_color, background=color_map.get(selected_color, "#f2f2f2"))

def save_to_csv():
    with open("inventory.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Item", "Color/Size", "Brand", "Quantity"])
        for item_name in inventory:
            for key, brands in inventory[item_name].items():
                for b in brands:
                    writer.writerow([item_name, key, b["brand"], b["quantity"]])
    messagebox.showinfo("Saved", "Inventory saved to inventory.csv")

def load_from_csv():
    if not os.path.exists("inventory.csv"):
        return
    with open("inventory.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = row["Item"]
            key = row.get("Color/Size") or row.get("Color") or row.get("Size")
            brand = row["Brand"]
            quantity = int(row["Quantity"])
            if item not in inventory:
                inventory[item] = {}
            if key not in inventory[item]:
                inventory[item][key] = []
            inventory[item][key].append({"quantity": quantity, "brand": brand})

# --- Layout ---
frame_top = tk.Frame(root, bg="#f2f2f2")
frame_top.pack(pady=10)

tk.Label(frame_top, text="Item:", bg="#f2f2f2").grid(row=0, column=0, padx=5, pady=2)
combo_item = ttk.Combobox(frame_top, values=list(inventory.keys()), state="readonly")
combo_item.grid(row=0, column=1, padx=5, pady=2)
combo_item.bind("<<ComboboxSelected>>", item_selected)
combo_item.current(0)

tk.Label(frame_top, text="Color:", bg="#f2f2f2").grid(row=0, column=2, padx=5, pady=2)
combo_color = ttk.Combobox(frame_top, values=all_colors, state="readonly")
combo_color.grid(row=0, column=3, padx=5, pady=2)
combo_color.bind("<<ComboboxSelected>>", color_selected)
combo_color.current(0)

tk.Label(frame_top, text="Size (optional):", bg="#f2f2f2").grid(row=0, column=4, padx=5, pady=2)
combo_size = ttk.Combobox(frame_top, values=all_sizes, state="readonly")
combo_size.grid(row=0, column=5, padx=5, pady=2)
combo_size.set("")  # Inicialmente vazio
combo_size.bind("<<ComboboxSelected>>", size_selected)

tk.Label(frame_top, text="Brand:", bg="#f2f2f2").grid(row=1, column=2, padx=5, pady=2)
combo_brand = ttk.Combobox(frame_top, state="readonly")
combo_brand.grid(row=1, column=3, padx=5, pady=2)
combo_brand.bind("<<ComboboxSelected>>", brand_selected)

tk.Label(frame_top, text="Quantity:", bg="#f2f2f2").grid(row=1, column=0, padx=5, pady=2)
entry_quantity = tk.Entry(frame_top)
entry_quantity.grid(row=1, column=1, padx=5, pady=2)

# --- Botões ---
frame_buttons = tk.Frame(root, bg="#f2f2f2")
frame_buttons.pack(pady=10)

btn_add = tk.Button(frame_buttons, text="Add/Update", command=add_update_item, bg="#4CAF50", fg="white", width=15)
btn_add.pack(side=tk.LEFT, padx=5)

btn_remove = tk.Button(frame_buttons, text="Remove", command=remove_item, bg="#f44336", fg="white", width=15)
btn_remove.pack(side=tk.LEFT, padx=5)

btn_new = tk.Button(frame_buttons, text="Add New Item", command=add_new_item, bg="#2196F3", fg="white", width=15)
btn_new.pack(side=tk.LEFT, padx=5)

btn_save = tk.Button(frame_buttons, text="Save CSV", command=save_to_csv, bg="#FFA500", fg="white", width=15)
btn_save.pack(side=tk.LEFT, padx=5)

# --- Tabela ---
columns = ("Item", "Quantity", "Brand", "Total")
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.yview)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200, anchor="center")

tree.pack(pady=10, fill=tk.BOTH, expand=True)

# --- Estilo ---
style = ttk.Style()
style.configure("Treeview", rowheight=25, font=('Arial', 12))
style.map('Treeview', background=[('selected', '#6fa1f2')], foreground=[('selected', 'white')])

# --- Inicializar ---
load_from_csv()
item_selected(None)
update_table()
root.mainloop()
