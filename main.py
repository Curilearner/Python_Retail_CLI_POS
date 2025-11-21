import CoreFunctions.Billing
import CoreFunctions.Inventory

def main():
    choice:int = 0
    while choice!=3:
        print("\t\t======\t\tWelcome To Retail Billing System\t\t======\n")
        print("(1) Enter 1 for Billing")
        print("(2) Enter 2 for Inventory")
        print("(3) Quit")
        choice = int(input("Enter your choice: "))
        match choice:
        case 1:
            Billing.Billing()
        case 2:
            Inventory.Inventory()
        case 3:
            print("\t\tClosing The Main Function.....\n")
            return
        case _:
            print("\t\tPlease Enter The Valid Choice \n")
    
    


if __name__ == "__main__":
    main()