import CollectionStructure.Product as Product
from FileHelperModule.GetSerialNumber import GetSerialNumber
import FileCRUDModules.FileWrite as FileWrite

def new_item():
    while True:
        product_name = ""
        price = 0.0
        quantity = 0.0
        quantitytype = ""

        print("Please Enter 0 if you want to end adding inventory \n")
        print("??\tFor Easy Searching Suggested Format: CategoryName-ProductName\t??\n")
        print("??\t For Eg: Noodles-WaiWai \t??")
        product_name = input("Enter the name of the product: \n > ")
        if product_name == "0":
            break

        price = float(input("Enter the MRP of the product: \n > "))
        print()
        quantity = float(input("Enter the Quantity of the product: \n > "))
        print()
        quantitytype = input("Enter the Quantity Type ")
        print("??\t For Eg: Kg , Pcs , ml , ltr \t??")
        serial = GetSerialNumber("inventory.txt")
        Product.Inventory.append((serial, product_name, price, quantity, quantitytype))

    FileWrite.FileWriter("inventory.txt", Product.Inventory)