# inventory.py
import os
from typing import List, Dict, Optional
from config import INVENTORY_FILE, TEMP_FILE

def ensure_inventory_file():
    if not os.path.exists(INVENTORY_FILE):
        open(INVENTORY_FILE, "w").close()

def read_inventory() -> List[Dict]:
    ensure_inventory_file()
    items = []
    with open(INVENTORY_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            try:
                sn = int(parts[0])
                name = parts[1]
                price = float(parts[2])
                qty = float(parts[3])
            except ValueError:
                continue
            items.append({"SN": sn, "name": name, "price": price, "quantity": qty})
    return items

def rewrite_inventory(updated_items: List[Dict]):
    with open(TEMP_FILE, "w") as tf:
        for it in updated_items:
            tf.write(f"{it['SN']}\t{it['name']}\t{it['price']:.2f}\t{it['quantity']:.2f}\n")
    os.replace(TEMP_FILE, INVENTORY_FILE)

def append_inventory_entry(name: str, price: float, quantity: float) -> int:
    items = read_inventory()
    last_sn = items[-1]["SN"] if items else 0
    sn = last_sn + 1
    with open(INVENTORY_FILE, "a") as f:
        f.write(f"{sn}\t{name}\t{price:.2f}\t{quantity:.2f}\n")
    print("\n++++++ New Item Successfully added ++++++\n")
    return sn

def find_inventory_by_sn(sn: int) -> Optional[Dict]:
    for it in read_inventory():
        if it["SN"] == sn:
            return it
    return None

def find_inventory_by_name_exact(name: str) -> Optional[Dict]:
    for it in read_inventory():
        if it["name"] == name:
            return it
    return None

def search_inventory(partial_name: str) -> List[Dict]:
    items = read_inventory()
    matches = []
    for it in items:
        if partial_name.lower() in it["name"].lower():
            print(f"SN:{it['SN']}\t{it['name']}\tPrice:{it['price']:.2f}\tQty:{it['quantity']:.2f}")
            matches.append(it)
    if not matches:
        print("No matching items found.")
    return matches

def quantity_updater(sn: int, quantity: float):
    items = read_inventory()
    updated = False
    for it in items:
        if it["SN"] == sn:
            it["quantity"] += quantity
            updated = True
            break
    if updated:
        rewrite_inventory(items)
        print("\n===++++++===Quantity Successfully Increased===++++++===\n")
    else:
        print("Symbol not found; no update performed.")

def quantity_nupdater(sn: int, quantity: float):
    items = read_inventory()
    updated = False
    for it in items:
        if it["SN"] == sn:
            it["quantity"] -= quantity
            if it["quantity"] < 0:
                it["quantity"] = 0.0
            updated = True
            break
    if updated:
        rewrite_inventory(items)
    else:
        print("Symbol not found; cannot decrease quantity.")

def price_updater(sn: int, new_price: float):
    items = read_inventory()
    updated = False
    for it in items:
        if it["SN"] == sn:
            it["price"] = new_price
            updated = True
            break
    if updated:
        rewrite_inventory(items)
        print("\n===++++++=== Price Successfully Updated ===++++++===\n")
    else:
        print("Symbol not found; no price update.")

# Convenience flows used by menus:
def new_item_flow():
    print("Enter new items (type single word name). Enter 0 as name to stop.")
    print("Suggestion: CategoryName_ProductName (For Easy Searching)")
    while True:
        product_name = input("Enter product name (or '0' to finish): ").strip()
        if product_name == "0":
            break
        try:
            price = float(input("Enter the MRP of the product: ").strip())
            quantity = float(input("Enter the Quantity of the product: ").strip())
        except ValueError:
            print("Invalid numeric input. Try again.")
            continue
        append_inventory_entry(product_name, price, quantity)

def prev_item_flow():
    item_name = input("Enter the name of the item to search: ").strip()
    if not item_name:
        return
    matches = search_inventory(item_name)
    try:
        symbol = int(input("Enter the S.N. from the list or 0 if not on the list: ").strip())
    except ValueError:
        print("Invalid SN.")
        return
    if symbol == 0:
        return
    try:
        mrp = float(input("Enter the MRP of the product: ").strip())
    except ValueError:
        print("Invalid MRP.")
        return

    target = find_inventory_by_sn(symbol)
    if target and abs(target["price"] - mrp) < 1e-6:
        try:
            quantity = float(input("Enter the Quantity to update: ").strip())
        except ValueError:
            print("Invalid quantity.")
            return
        quantity_updater(symbol, quantity)
    else:
        try:
            quantity = float(input("Enter the Quantity of MARKED ITEM: ").strip())
        except ValueError:
            print("Invalid quantity.")
            return
        new_name = (target["name"] + f"_{mrp:.2f}") if target else f"{item_name}_{mrp:.2f}"
        append_inventory_entry(new_name, mrp, quantity)

def inventory_menu():
    while True:
        print("\nInventory Menu")
        print("1 - Item previously bought")
        print("2 - Newly bought item")
        print("0 - Back")
        choice = input("Choice: ").strip()
        if choice == "0":
            return
        elif choice == "1":
            prev_item_flow()
        elif choice == "2":
            new_item_flow()
        else:
            print("Invalid choice. Try again.")
