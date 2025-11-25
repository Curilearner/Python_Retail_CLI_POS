# main.py
from auth import login_menu
from inventory import inventory_menu, search_inventory
from billing import sales, sales_single_item_flow, print_bill, bill_items
import billing

def main():
    # Login first
    if not login_menu():
        print("Goodbye.")
        return

    while True:
        print("\t\t======\t\tWelcome To Retail Billing System\t\t======")
        print("Enter 1 for Sales && 2 for Inventory && 0 to Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            # Sales: user can add multiple items then print bill (which allows add/remove)
            # We'll call sales() which ends with print_bill()
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
