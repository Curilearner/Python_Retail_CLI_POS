
import os
import time
from datetime import datetime

INVENTORY_FILE = "inventory.txt"
TEMP_FILE = "temp.txt"
MAX_ITEMS = 200

# In-memory current bill items (list of dicts)
bill_items = []  # each item: {"name":..., "price":..., "quantity":...}


# ----------------- File & Inventory helpers ----------------- #

def ensure_inventory_file():
    if not os.path.exists(INVENTORY_FILE):
        open(INVENTORY_FILE, "w").close()


def read_inventory():
    """Return list of inventory entries as dicts with keys SN(int), name(str), price(float), quantity(float)."""
    ensure_inventory_file()
    items = []
    with open(INVENTORY_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                # Try robust parsing (in case name contains spaces without tabs)
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


def append_inventory_entry(name, price, quantity):
    """Append a new inventory entry; assign SN = lastSN + 1 (or 1)."""
    ensure_inventory_file()
    items = read_inventory()
    last_sn = items[-1]["SN"] if items else 0
    sn = last_sn + 1
    with open(INVENTORY_FILE, "a") as f:
        f.write(f"{sn}\t{name}\t{price:.2f}\t{quantity:.2f}\n")
    print("\n\t++++++ New Item Successfully added ++++++\t\n")
    return sn


def rewrite_inventory(updated_items):
    """Overwrite inventory file with updated_items list (each item dict must contain SN,name,price,quantity)."""
    with open(TEMP_FILE, "w") as tf:
        for it in updated_items:
            tf.write(f"{it['SN']}\t{it['name']}\t{it['price']:.2f}\t{it['quantity']:.2f}\n")
    # atomic-ish replace
    os.replace(TEMP_FILE, INVENTORY_FILE)


def find_inventory_by_sn(sn):
    items = read_inventory()
    for it in items:
        if it["SN"] == sn:
            return it
    return None


def find_inventory_by_name_exact(name):
    items = read_inventory()
    for it in items:
        if it["name"] == name:
            return it
    return None


# ----------------- Inventory operations ----------------- #

def new_item():
    print("Enter new items (type single word name). Enter 0 as name to stop.")
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


def search_inventory(partial_name):
    """Print matching inventory lines and return matching items list (for convenience)."""
    items = read_inventory()
    matches = []
    for it in items:
        if partial_name.lower() in it["name"].lower():
            print(f"SN:{it['SN']}\t{it['name']}\tPrice:{it['price']:.2f}\tQty:{it['quantity']:.2f}")
            matches.append(it)
    if not matches:
        print("No matching items found.")
    return matches


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
        # same MRP -> update quantity
        try:
            quantity = float(input("Enter the Quantity to update: ").strip())
        except ValueError:
            print("Invalid quantity.")
            return
        quantity_updater(symbol, quantity)
    else:
        # new MRP -> create new item with MRP appended to name (mimics original behavior)
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
            new_item()
        else:
            print("Invalid choice. Try again.")


def quantity_updater(symbol, quantity):
    """Increase quantity for SN == symbol by quantity."""
    items = read_inventory()
    updated = False
    for it in items:
        if it["SN"] == symbol:
            it["quantity"] += quantity
            updated = True
            break
    if updated:
        rewrite_inventory(items)
        print("\n===++++++===Quantity Successfully Increased===++++++===\n")
    else:
        print("Symbol not found; no update performed.")


def quantity_nupdater(symbol, quantity):
    """Decrease quantity when selling. Equivalent to C's Quantity_nupdater."""
    items = read_inventory()
    updated = False
    for it in items:
        if it["SN"] == symbol:
            it["quantity"] -= quantity
            if it["quantity"] < 0:
                it["quantity"] = 0
            updated = True
            break
    if updated:
        rewrite_inventory(items)
    else:
        print("Symbol not found; cannot decrease quantity.")


def price_updater(symbol, new_price):
    items = read_inventory()
    updated = False
    for it in items:
        if it["SN"] == symbol:
            it["price"] = new_price
            updated = True
            break
    if updated:
        rewrite_inventory(items)
        print("\n===++++++=== Price Successfully Updated ===++++++===\n")
    else:
        print("Symbol not found; no price update.")


# ----------------- Sales / Billing ----------------- #

def quantity_checker(sn, requested_quantity):
    """Return True if enough quantity available, False otherwise"""
    it = find_inventory_by_sn(sn)
    if it is None:
        print("Item not found in inventory.")
        return False
    return it["quantity"] >= requested_quantity


def bill_add_item(name, price, quantity):
    # if same name exists in bill, increase quantity
    for it in bill_items:
        if it["name"] == name and abs(it["price"] - price) < 1e-6:
            it["quantity"] += quantity
            return
    bill_items.append({"name": name, "price": price, "quantity": quantity})


def data_passer(num):
    items = read_inventory()
    # in original code num matched line number; here treat num as SN
    target = find_inventory_by_sn(num)
    if not target:
        print("Requested SN not found.")
        return
    while True:
        try:
            qty = float(input("Enter the Quantity: ").strip())
        except ValueError:
            print("Invalid quantity, try again.")
            continue
        if quantity_checker(num, qty):
            bill_add_item(target["name"], target["price"], qty)
            quantity_nupdater(num, qty)
            break
        else:
            print("Unable to provide such Quantity. Please re-enter.")


def remove_item_from_bill():
    if not bill_items:
        print("Bill is empty.")
        return
    print("Current bill items:")
    for idx, it in enumerate(bill_items, start=1):
        print(f"{idx}. {it['name']} - {it['quantity']:.2f}")
    try:
        symbol = int(input("Enter the symbol number of the bill item to remove: ").strip())
    except ValueError:
        print("Invalid input.")
        return
    if symbol < 1 or symbol > len(bill_items):
        print("Invalid symbol number.")
        return
    index_to_remove = symbol - 1
    while True:
        try:
            qty = float(input("Enter the Quantity to remove: ").strip())
        except ValueError:
            print("Invalid quantity.")
            continue
        if qty > bill_items[index_to_remove]["quantity"]:
            print("Cannot remove more than in bill. Try again.")
            continue
        break
    # find actual inventory SN for that item
    name = bill_items[index_to_remove]["name"]
    inv = find_inventory_by_name_exact(name)
    if inv:
        quantity_updater(inv["SN"], qty)  # return items to inventory
    else:
        print("Warning: could not find inventory entry to return quantity to.")
    if abs(qty - bill_items[index_to_remove]["quantity"]) < 1e-6:
        # remove the item entirely
        bill_items.pop(index_to_remove)
    else:
        bill_items[index_to_remove]["quantity"] -= qty
    print("Item updated in bill.")
    print_bill()  # reprint


def add_item_to_bill_flow():
    print("1: Increase quantity of existing bill item")
    print("2: Add new item to current bill")
    try:
        choice = int(input("Choice: ").strip())
    except ValueError:
        print("Invalid choice.")
        return
    if choice == 1:
        if not bill_items:
            print("Bill empty.")
            return
        for idx, it in enumerate(bill_items, start=1):
            print(f"{idx}. {it['name']} - {it['quantity']:.2f}")
        try:
            symbol = int(input("Enter the symbol number of the item from the Bill: ").strip())
        except ValueError:
            print("Invalid input.")
            return
        if symbol < 1 or symbol > len(bill_items):
            print("Invalid symbol number.")
            return
        try:
            Quantity = float(input("Enter the Quantity to add to the Bill: ").strip())
        except ValueError:
            print("Invalid quantity.")
            return
        index_to_add = symbol - 1
        # find real SN by name
        inv = find_inventory_by_name_exact(bill_items[index_to_add]["name"])
        if not inv:
            print("Item not found in inventory.")
            return
        if quantity_checker(inv["SN"], Quantity):
            bill_items[index_to_add]["quantity"] += Quantity
            quantity_nupdater(inv["SN"], Quantity)
        else:
            print("Not enough stock to add.")
    elif choice == 2:
        # call sales flow to add new item (will append to bill and update inventory)
        sales_single_item_flow()
    else:
        print("Invalid choice.")


def print_bill():
    if not bill_items:
        print("Bill empty.")
        return
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    print("-" * 92)
    print(" " * 34 + "ALINA RETAIL STORE")
    print(" " * 33 + "Auckland, NEW ZEALAND")
    print(f"Transaction Time: {time_str}")
    print(f"Transaction Date: {date_str}")
    print("-" * 92)
    print("SN\tParticulars\tPrice\tQuantity\tTotal")
    print("-" * 92)
    total = 0.0
    for i, it in enumerate(bill_items, start=1):
        amount = it["price"] * it["quantity"]
        print(f"{i}\t{it['name']}\t{it['price']:.2f}\t{it['quantity']:.2f}\t{amount:.2f}")
        total += amount
    print("-" * 92)
    print(f"{'':70}Amount: {total:.2f}")
    print("-" * 92)

    # allow add/remove items before checkout
    while True:
        print("Enter 1 to add item, 2 to remove item, 0 to continue to checkout.")
        try:
            meow = int(input("Choice: ").strip())
        except ValueError:
            print("Invalid choice.")
            continue
        if meow == 2:
            remove_item_from_bill()
            return
        elif meow == 1:
            add_item_to_bill_flow()
            return
        elif meow == 0:
            break
        else:
            print("Invalid option. Try again.")

    # Discount amount
    try:
        dis_amt = float(input("Enter the Discount amount (0 if none): ").strip())
    except ValueError:
        dis_amt = 0.0
    if 0 < dis_amt <= total:
        total -= dis_amt
        print(f"New Amount after Discount amount: {total:.2f}")

    # Discount percentage
    try:
        dis_perc = float(input("Enter the Discount percentage (0 if none): ").strip())
    except ValueError:
        dis_perc = 0.0
    if 0 < dis_perc <= 100:
        discount_amount = 0.01 * dis_perc * total
        total -= discount_amount
        print(f"New Amount after Discount Percentage: {total:.2f}")

    # Amount received
    while True:
        try:
            amt_receive = float(input("Amount received: ").strip())
        except ValueError:
            print("Invalid amount. Try again.")
            continue
        if amt_receive >= total:
            change = amt_receive - total
            if change > 0:
                print(f"Change : {change:.2f}")
            print("==============================THANK YOU FOR WEARING MASK :-) ==================================")
            print("**********************************PLEASE VISIT AGAIN*******************************************")
            bill_items.clear()
            return
        else:
            print("Unable To receive less amount. Please enter sufficient amount.")


# ----------------- Sales input loop ----------------- #

def sales_single_item_flow():
    # search, pick SN, then pass data
    product_name = input("Enter the product name to search (or '0' to exit): ").strip()
    if product_name == "0" or not product_name:
        return
    matches = search_inventory(product_name)
    if not matches:
        return
    try:
        symbol_num = int(input("Please Enter the SN from the list: ").strip())
    except ValueError:
        print("Invalid SN.")
        return
    data_passer(symbol_num)


def sales():
    while True:
        product_name = input("Enter the product name to search (or '0' to finish sales and print bill): ").strip()
        if product_name == "0":
            break
        matches = search_inventory(product_name)
        if not matches:
            continue
        try:
            symbol_num = int(input("Please Enter the SN from the list: ").strip())
        except ValueError:
            print("Invalid SN.")
            continue
        data_passer(symbol_num)
    print_bill()


# ----------------- Utility ----------------- #

def clear_items():
    bill_items.clear()


# ----------------- Main menu ----------------- #

def main():
    ensure_inventory_file()
    while True:
        print("\t\t======\t\tWelcome To Retail Billing System\t\t======")
        print("Enter 1 for Sales && 2 for Inventory && 0 to Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            sales()
        elif choice == "2":
            inventory_menu()
        elif choice == "0":
            print("Exiting. Goodbye.")
            break
        else:
            print("Please Enter the correct option")


if __name__ == "__main__":
    main()
