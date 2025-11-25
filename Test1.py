import os
import hashlib
from datetime import datetime

# --------------------------- File Paths --------------------------- #
INVENTORY_FILE = "inventory.txt"
TEMP_FILE = "temp.txt"
USER_FILE = "user.txt"

# --------------------------- Globals --------------------------- #
bill_items = []  # list of dicts: {name, price, quantity}


# ==================================================================
#                       USER LOGIN SYSTEM
# ==================================================================

def hash_value(text):
    return hashlib.sha256(text.encode()).hexdigest()


def ensure_user_file():
    if not os.path.exists(USER_FILE):
        open(USER_FILE, "w").close()


def register_user():
    ensure_user_file()
    print("\n=== Register New User ===")
    username = input("Enter new username: ").strip()
    password = input("Enter new password: ").strip()

    h_user = hash_value(username)
    h_pass = hash_value(password)

    # Check if username already exists
    with open(USER_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            stored_user, _ = line.strip().split()
            if stored_user == h_user:
                print("Username already exists!")
                return False

    with open(USER_FILE, "a") as f:
        f.write(f"{h_user} {h_pass}\n")

    print("User registered successfully!\n")
    return True


def login_user():
    ensure_user_file()
    print("\n=== Login ===")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    h_user = hash_value(username)
    h_pass = hash_value(password)

    with open(USER_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            stored_user, stored_pass = line.strip().split()
            if stored_user == h_user and stored_pass == h_pass:
                print("\nLogin successful!\n")
                return True

    print("Invalid username or password.\n")
    return False


def login_menu():
    while True:
        print("=== Login Menu ===")
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        ch = input("Choice: ").strip()

        if ch == "1":
            if login_user():
                return True
        elif ch == "2":
            register_user()
        elif ch == "0":
            return False
        else:
            print("Invalid choice.\n")


# ==================================================================
#                        INVENTORY FUNCTIONS
# ==================================================================

def ensure_inventory_file():
    if not os.path.exists(INVENTORY_FILE):
        open(INVENTORY_FILE, "w").close()


def read_inventory():
    ensure_inventory_file()
    items = []
    with open(INVENTORY_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split("\t")
            if len(parts) < 4: continue
            try:
                items.append({
                    "SN": int(parts[0]),
                    "name": parts[1],
                    "price": float(parts[2]),
                    "quantity": float(parts[3])
                })
            except:
                continue
    return items


def append_inventory_entry(name, price, quantity):
    items = read_inventory()
    last_sn = items[-1]["SN"] if items else 0
    sn = last_sn + 1

    with open(INVENTORY_FILE, "a") as f:
        f.write(f"{sn}\t{name}\t{price:.2f}\t{quantity:.2f}\n")

    print("\n++++++ New Item Added ++++++\n")
    return sn


def rewrite_inventory(updated_items):
    with open(TEMP_FILE, "w") as tf:
        for it in updated_items:
            tf.write(f"{it['SN']}\t{it['name']}\t{it['price']:.2f}\t{it['quantity']:.2f}\n")
    os.replace(TEMP_FILE, INVENTORY_FILE)


def find_inventory_by_sn(sn):
    for it in read_inventory():
        if it["SN"] == sn:
            return it
    return None


def search_inventory(partial_name):
    items = read_inventory()
    matches = []
    for it in items:
        if partial_name.lower() in it["name"].lower():
            print(f"SN:{it['SN']}   {it['name']}   Price:{it['price']}   Qty:{it['quantity']}")
            matches.append(it)
    if not matches:
        print("No matching items found.")
    return matches


def new_item():
    print("Enter new items (type '0' to stop)")
    while True:
        name = input("Enter product name: ").strip()
        if name == "0": break
        try:
            price = float(input("Enter price: ").strip())
            qty = float(input("Enter quantity: ").strip())
        except:
            print("Invalid numeric input.")
            continue
        append_inventory_entry(name, price, qty)


def quantity_updater(sn, qty):
    items = read_inventory()
    for it in items:
        if it["SN"] == sn:
            it["quantity"] += qty
            rewrite_inventory(items)
            print("\nQuantity Increased.\n")
            return


def quantity_nupdater(sn, qty):
    items = read_inventory()
    for it in items:
        if it["SN"] == sn:
            it["quantity"] -= qty
            if it["quantity"] < 0: it["quantity"] = 0
            rewrite_inventory(items)
            return


def inventory_menu():
    while True:
        print("\nInventory Menu")
        print("1 - Previously Bought")
        print("2 - New Item")
        print("0 - Back")
        choice = input("Choice: ").strip()

        if choice == "0":
            return
        elif choice == "1":
            prev_item_flow()
        elif choice == "2":
            new_item()
        else:
            print("Invalid choice.")


def prev_item_flow():
    name = input("Search item: ").strip()
    matches = search_inventory(name)
    if not matches: return

    try:
        sn = int(input("Enter SN from list: ").strip())
        mrp = float(input("Enter MRP: ").strip())
    except:
        print("Invalid input.")
        return

    target = find_inventory_by_sn(sn)
    if target and abs(target["price"] - mrp) < 1e-6:
        qty = float(input("Enter quantity: ").strip())
        quantity_updater(sn, qty)
    else:
        qty = float(input("Enter quantity: ").strip())
        new_name = f"{name}_{mrp}"
        append_inventory_entry(new_name, mrp, qty)


# ==================================================================
#                        BILLING / SALES
# ==================================================================

def quantity_checker(sn, req_qty):
    it = find_inventory_by_sn(sn)
    if not it:
        print("Item not found.")
        return False
    return it["quantity"] >= req_qty


def bill_add_item(name, price, qty):
    for it in bill_items:
        if it["name"] == name and abs(it["price"] - price) < 1e-6:
            it["quantity"] += qty
            return
    bill_items.append({"name": name, "price": price, "quantity": qty})


def data_passer(sn):
    target = find_inventory_by_sn(sn)
    if not target:
        print("SN not found.")
        return

    while True:
        try:
            qty = float(input("Enter quantity: ").strip())
        except:
            print("Invalid quantity.")
            continue

        if quantity_checker(sn, qty):
            bill_add_item(target["name"], target["price"], qty)
            quantity_nupdater(sn, qty)
            break
        else:
            print("Not enough stock.")


def remove_item_from_bill():
    if not bill_items:
        print("Bill empty.")
        return

    print("Current bill items:")
    for i, it in enumerate(bill_items, start=1):
        print(f"{i}. {it['name']} Qty:{it['quantity']}")

    try:
        idx = int(input("Select item to remove: ").strip()) - 1
        qty = float(input("Quantity to remove: ").strip())
    except:
        print("Invalid input.")
        return

    if idx < 0 or idx >= len(bill_items):
        print("Invalid index.")
        return

    item = bill_items[idx]
    inv = find_inventory_by_sn(find_inventory_by_name(item["name"]))

    quantity_updater(inv, qty)

    if qty >= item["quantity"]:
        bill_items.pop(idx)
    else:
        item["quantity"] -= qty

    print("Bill updated.")


def sales_single_item_flow():
    name = input("Search product: ").strip()
    if name == "0": return
    matches = search_inventory(name)
    if not matches: return

    try:
        sn = int(input("Enter SN: ").strip())
    except:
        print("Invalid SN.")
        return

    data_passer(sn)


def sales():
    while True:
        name = input("Enter product (0 to finish): ").strip()
        if name == "0": break
        matches = search_inventory(name)
        if not matches: continue

        try:
            sn = int(input("Enter SN: ").strip())
        except:
            print("Invalid SN.")
            continue

        data_passer(sn)

    print_bill()


# ==================================================================
#                           PRINT BILL
# ==================================================================

def print_bill():
    if not bill_items:
        print("Bill empty.")
        return

    now = datetime.now()

    print("\n" + "-" * 92)
    print(" " * 34 + "ALINA RETAIL STORE")
    print(" " * 33 + "Auckland, NEW ZEALAND")
    print(f"Time: {now.strftime('%H:%M:%S')}")
    print(f"Date: {now.strftime('%Y-%m-%d')}")
    print("-" * 92)
    print("SN\tName\tPrice\tQty\tTotal")
    print("-" * 92)

    total = 0
    for i, it in enumerate(bill_items, start=1):
        amt = it["price"] * it["quantity"]
        total += amt
        print(f"{i}\t{it['name']}\t{it['price']}\t{it['quantity']}\t{amt:.2f}")

    print("-" * 92)
    print(f"Amount: {total:.2f}")

    dis_amt = float(input("Discount Amount (0 if none): "))
    if dis_amt > 0: total -= dis_amt

    dis_perc = float(input("Discount % (0 if none): "))
    if dis_perc > 0: total -= total * (dis_perc / 100)

    while True:
        amt_received = float(input("Amount Received: "))
        if amt_received >= total:
            print(f"Change: {amt_received - total:.2f}")
            print("Thank you! Visit again.")
            bill_items.clear()
            return
        else:
            print("Insufficient amount.")


# ==================================================================
#                            MAIN MENU
# ==================================================================

def main():
    ensure_inventory_file()

    # LOGIN FIRST
    if not login_menu():
        print("Goodbye.")
        return

    while True:
        print("\n=== Retail Billing System ===")
        print("1. Sales")
        print("2. Inventory")
        print("0. Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            sales()
        elif choice == "2":
            inventory_menu()
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
