import CollectionStructure.Product

def Inventory():
    while True:
        print("\n" + "="*50)
        print("INVENTORY MANAGEMENT")
        print("="*50)
        print("Enter 1 - If item is previously bought")
        print("Enter 2 - If item is newly bought") 
        print("Enter 0 - Exit to main menu")
        print("-" * 50)
        
        try:
            option_inventory = int(input("Enter your choice: "))
        except ValueError:
            print("Please Enter a Valid Number")
            continue
        
        if option_inventory == 0:
            print("Returning to main menu...")
            return
        
        if option_inventory == 1:
            prev_item()
        elif option_inventory == 2:
            new_item()
        else:
            print("Please Enter a Valid Number")