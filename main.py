# ...existing code...
import CoreModules.Billing as Billing
import CoreModules.Inventory as Inventory

def main():
    choice: int = 0
    while choice != 3:
        print("\t\t======\t\tWelcome To Retail Billing System\t\t======\n")
        print("(1) Enter 1 for Billing")
        print("(2) Enter 2 for Inventory")
        print("(3) Quit")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("\t\tPlease enter a valid number.\n")
            continue

        if choice == 1:
            Billing.Billing()
        elif choice == 2:
            Inventory.Inventory()
        elif choice == 3:
            print("\t\tClosing The Main Function.....\n")
            return
        else:
            print("\t\tPlease Enter The Valid Choice \n")

if __name__ == "__main__":
    main()
# ...existing code...