# billing.py
from typing import List, Dict
from datetime import datetime
from inventory import (
    read_inventory,
    find_inventory_by_sn,
    find_inventory_by_name_exact,
    search_inventory
)
import inventory as inv_module

# -----------------------------
# LOCAL BILL ITEM STORE
# -----------------------------
bill_items: List[Dict] = []   # [{"name":..., "price":..., "quantity":...}]


# -----------------------------
# QUANTITY CHECKER (NO WALRUS)
# -----------------------------
def quantity_checker(sn: int, requested_quantity: float) -> bool:
    it = find_inventory_by_sn(sn)
    if it is None:
        print("Item not found in inventory.")
        return False
    return it["quantity"] >= requested_quantity


# -----------------------------
# BILL OPERATIONS
# -----------------------------
def bill_add_item(name: str, price: float, quantity: float):
    for it in bill_items:
        if it["name"] == name and abs(it["price"] - price) < 1e-6:
            it["quantity"] += quantity
            return
    bill_items.append({"name": name, "price": price, "quantity": quantity})


def data_passer(sn: int):
    target = find_inventory_by_sn(sn)
    if not target:
        print("Requested SN not found.")
        return
    while True:
        try:
            qty = float(input("Enter the Quantity: ").strip())
        except ValueError:
            print("Invalid quantity, try again.")
            continue

        if quantity_checker(sn, qty):
            bill_add_item(target["name"], target["price"], qty)
            inv_module.quantity_nupdater(sn, qty)
            break
        else:
            print("Not enough stock. Re-enter quantity.")


def sales_single_item_flow():
    product_name = input("Enter product name to search (or '0' to exit): ").strip()
    if product_name == "0" or product_name == "":
        return

    matches = search_inventory(product_name)
    if not matches:
        return

    try:
        symbol_num = int(input("Enter SN from the list: ").strip())
    except ValueError:
        print("Invalid SN.")
        return

    data_passer(symbol_num)


# -----------------------------
# MODIFY BILL AFTER PRINT
# -----------------------------
def add_item_to_bill_flow():
    print("1: Increase quantity of existing bill item")
    print("2: Add new item to bill")

    try:
        choice = int(input("Choice: ").strip())
    except ValueError:
        print("Invalid input.")
        return

    if choice == 1:
        if not bill_items:
            print("Bill empty.")
            return

        for idx, it in enumerate(bill_items, start=1):
            print(f"{idx}. {it['name']} - {it['quantity']}")

        try:
            symbol = int(input("Enter symbol number from bill: ").strip())
        except ValueError:
            print("Invalid number.")
            return

        if symbol < 1 or symbol > len(bill_items):
            print("Invalid selection.")
            return

        try:
            qty = float(input("Enter quantity to add: ").strip())
        except ValueError:
            print("Invalid quantity.")
            return

        idx = symbol - 1
        inv_item = find_inventory_by_name_exact(bill_items[idx]["name"])
        if not inv_item:
            print("Error: inventory entry not found.")
            return

        if quantity_checker(inv_item["SN"], qty):
            bill_items[idx]["quantity"] += qty
            inv_module.quantity_nupdater(inv_item["SN"], qty)
        else:
            print("Not enough stock.")
    elif choice == 2:
        sales_single_item_flow()
    else:
        print("Invalid choice.")


def remove_item_from_bill():
    if not bill_items:
        print("Bill empty.")
        return

    print("Current bill:")
    for idx, it in enumerate(bill_items, start=1):
        print(f"{idx}. {it['name']} - {it['quantity']}")

    try:
        symbol = int(input("Symbol to remove: ").strip())
    except ValueError:
        print("Invalid number.")
        return

    if symbol < 1 or symbol > len(bill_items):
        print("Invalid selection.")
        return

    idx = symbol - 1

    while True:
        try:
            qty = float(input("Enter quantity to remove: ").strip())
            break
        except ValueError:
            print("Invalid quantity.")

    name = bill_items[idx]["name"]
    inv = find_inventory_by_name_exact(name)

    if inv:
        inv_module.quantity_updater(inv["SN"], qty)

    if qty >= bill_items[idx]["quantity"]:
        bill_items.pop(idx)
    else:
        bill_items[idx]["quantity"] -= qty

    print("Bill updated.")
    print_bill()


# -----------------------------
# PRINT BILL + ALLOW ADD/REMOVE
# -----------------------------
def print_bill():
    if not bill_items:
        print("Bill empty.")
        return

    now = datetime.now()
    while True:
        print("-" * 92)
        print(" " * 34 + "ALINA RETAIL STORE")
        print(" " * 33 + "Auckland, NEW ZEALAND")
        print(f"Time: {now.strftime('%H:%M:%S')}")
        print(f"Date: {now.strftime('%Y-%m-%d')}")
        print("-" * 92)

        total = 0
        print("SN\tName\tPrice\tQty\tTotal")
        print("-" * 92)

        for i, it in enumerate(bill_items, start=1):
            amt = it["price"] * it["quantity"]
            print(f"{i}\t{it['name']}\t{it['price']}\t{it['quantity']}\t{amt}")
            total += amt

        print("-" * 92)
        print(f"{'':70}Total: {total}")
        print("-" * 92)

        print("1 - Add item")
        print("2 - Remove item")
        print("0 - Checkout")
        opt = input("Choice: ").strip()

        if opt == "1":
            add_item_to_bill_flow()
        elif opt == "2":
            remove_item_from_bill()
            return
        elif opt == "0":
            break
        else:
            print("Invalid choice.")

    # ------ Checkout ------
    try:
        dis_amt = float(input("Discount amount: ").strip())
    except:
        dis_amt = 0

    if dis_amt > 0:
        total -= dis_amt

    try:
        dis_pr = float(input("Discount %: ").strip())
    except:
        dis_pr = 0

    if dis_pr > 0:
        total -= (total * dis_pr / 100)

    while True:
        try:
            amt = float(input("Amount received: ").strip())
        except:
            print("Invalid.")
            continue

        if amt >= total:
            print(f"Change: {amt - total}")
            print("Thank you! Please visit again!")
            bill_items.clear()
            return
        else:
            print("Insufficient amount.")


# -----------------------------
# HIGH LEVEL SALES ENTRYPOINT
# -----------------------------
def sales():
    while True:
        print("1 - New Item")
        print("2 - Search Item")
        print("0 - Print Bill")
        choice = input("Choice: ").strip()

        if choice == "0":
            print_bill()
            return
        elif choice == "1":
            sales_single_item_flow()
        elif choice == "2":
            sales_single_item_flow()
        else:
            print("Invalid option.")
