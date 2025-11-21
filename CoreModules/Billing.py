def Billing():
    while true:
        productname = ""
        print("===\t\tEnter the product name to search (or '0' to exit):\t\t===\n")
        productname = input("> ")

         if productname.strip() == '0': 
            print("Exiting Billing...")
            break
            
