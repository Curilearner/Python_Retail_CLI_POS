#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h>
#include <unistd.h>

#define MAX_ITEMS 200
#define NAME_LENGTH 100

typedef struct {
    int SN;
    char name[NAME_LENGTH];
    float price;
    float quantity;
} Item;

//static Struct Declaration
static Item items[MAX_ITEMS];
static int itemCount = 0;
static Item inven[MAX_ITEMS];
static int invenCount = 0;


//function prototype

int MRP_checker(float MRP,int symbol);
void new_item();
void write_product(char product_name[], float price, float quantity);
void prev_item();
void inventory();
void sales();
void search_inventory(char *partial_name);
void Data_passer(int num);
void bill_function(char name[], float price, float quantity);
void Print_bill(Item items[], int itemCount);
void add_debt(char customer_name[], int Temp_debt);
int Quantity_checker(int num, float Quantity);
void Quantity_updater(int , float);
void Quantity_nupdater(int,float);
void renameoffile();
void rename_coffile();
void price_updater(int, float);
void remove_item(Item items[], int itemCount);
void add_item(Item items[], int itemCount);
int symbol_returner(char str[]);
void clear_items();

void clear_items() {

    for (int i = 0; i < MAX_ITEMS; i++) 
    {
        items[i].name[0] = '\0';
        items[i].price = 0;
        items[i].quantity = 0;
    }
}

void new_item() {
     
    while(1)
    {
        char product_names[100] = "";
        float price = 0;
        float Quantity = 0;

        printf("Please Enter 0 if you want to end adding inventory\n");
        printf("Enter the name of the product\n");
        scanf("%s", product_names);
        if (strcmp(product_names, "0") == 0) 
        {
            break;
        }
        printf("Enter the MRP of the product\n");
        scanf("%f", &price);
        printf("\n");
        printf("Enter the Quantity of the product\n");
        scanf("%f", &Quantity);
        printf("\n");
        getchar(); 
        write_product(product_names, price, Quantity);

    }
}

void write_product(char product_name[], float price,float quantity) {
    if (invenCount >= MAX_ITEMS) {
        printf("Error: Maximum item limit reached.\n");
        return;
    }

    strcpy(inven[invenCount].name, product_name);
    inven[invenCount].price = price;
    inven[invenCount].quantity = quantity;
    inven[invenCount].SN = invenCount + 1;
    invenCount++;

    FILE *fptr;
    fptr = fopen("inventory.txt", "a");
    if (fptr == NULL) {
        printf("Unable to open the File\n");
        exit(1);
    }
    fprintf(fptr, "%d\t%s\t%.2f\t%.2f\n", inven[invenCount-1].SN, inven[invenCount - 1].name, inven[invenCount - 1].price, inven[invenCount - 1].quantity);
    fclose(fptr);
    printf("\n\t++++++ New Item Successfully added ++++++\t\n\n");
}

int MRP_Checker(float MRP,int symbol)
{
     FILE *read;
    read = fopen("inventory.txt", "r");
    if (read == NULL) {
        printf("Unable to open the inventory file\n");
        exit(1);
    }

    int in = 1;
    while (fscanf(read, "%d\t%s\t%.2f\t%.2f\n", &inven[in-1].SN, inven[in- 1].name, &inven[in- 1].price, &inven[in - 1].quantity) != EOF) {
        if (symbol == in)
        {
         if(MRP == inven[in-1].price)
         {
             fclose(read);
             return 1;
         }
        }
        
        in++;
    }
    return 0;
}
void string_returner(int symbol, float MRP)
{
           FILE *fptr;
           fptr = fopen("inventory.txt", "r");
           int in = 1;
           float Quantity;
           printf("Enter the Quantity of MARKED ITEM\n");
           scanf("%f", &Quantity);

           while (fscanf(fptr, "%d\t%s\t%.2f\t%.2f\n", &inven[in - 1].SN, inven[in - 1].name, &inven[in - 1].price, &inven[in - 1].quantity) != EOF)
           {
               if (inven[in - 1].SN == symbol)
               {
                   char str2[MAX_ITEMS];
                   sprintf(str2, "%.2f", MRP);
                   strcat(inven[in - 1].name, str2);
                   write_product(inven[in - 1].name, MRP, Quantity);
                   break;
               }
               in++;
           }
           fclose(fptr);
} 
     

void renameoffile()
{
    rename("inventory.txt", "inventory_backup.txt");
    rename("temp.txt", "inventory.txt");
    remove("inventory_backup.txt");
}

void Quantity_nupdater(int symbol, float quantity) {
   FILE *original_file, *temp_file;

    original_file = fopen("inventory.txt", "r");
    if (original_file == NULL) {
        perror("Error opening inventory.txt");
        exit(1);
    }

    temp_file = fopen("temp.txt", "w");
    if (temp_file == NULL) {
        perror("Error opening temp.txt");
        fclose(original_file);
        exit(1);
    }

   Item newItem;
    while (fscanf(original_file, "%d\t%s\t%f\t%f\n", &newItem.SN, newItem.name, &newItem.price, &newItem.quantity) == 4) {
        if (symbol == newItem.SN) {
            newItem.quantity = newItem.quantity - quantity;
        }
        fprintf(temp_file, "%d\t%s\t%f\t%f\n", newItem.SN, newItem.name, newItem.price, newItem.quantity);
    }

    fclose(original_file);
    fclose(temp_file);
    renameoffile();
   
}
void price_updater(int symbol, float price) {
   FILE *original_file, *temp_file;

    original_file = fopen("inventory.txt", "r");
    if (original_file == NULL) {
        perror("Error opening inventory.txt");
        exit(1);
    }

    temp_file = fopen("temp.txt", "w");
    if (temp_file == NULL) {
        perror("Error opening temp.txt");
        fclose(original_file);
        exit(1);
    }

   Item newItem;
    while (fscanf(original_file, "%d\t%s\t%f\t%f\n", &newItem.SN, newItem.name, &newItem.price, &newItem.quantity) == 4) {
        if (symbol == newItem.SN) {
            newItem.price = price;
        }
        fprintf(temp_file, "%d\t%s\t%.2f\t%.2f\n", newItem.SN, newItem.name, newItem.price, newItem.quantity);
    }

    fclose(original_file);
    fclose(temp_file);
    printf("\n===++++++=== Price Sucessfully Increased ===++++++===\n");
    renameoffile();
    
   
}
void Quantity_updater(int symbol, float quantity) {
   FILE *original_file, *temp_file;

    original_file = fopen("inventory.txt", "r");
    if (original_file == NULL) {
        perror("Error opening inventory.txt");
        exit(1);
    }

    temp_file = fopen("temp.txt", "w");
    if (temp_file == NULL) {
        perror("Error opening temp.txt");
        fclose(original_file);
        exit(1);
    }

    Item newItem;
    while (fscanf(original_file, "%d\t%s\t%f\t%f\n", &newItem.SN, newItem.name, &newItem.price, &newItem.quantity) == 4) {
        if (symbol == newItem.SN) {
            newItem.quantity += quantity;
        }
        fprintf(temp_file, "%d\t%s\t%.2f\t%.2f\n", newItem.SN, newItem.name, newItem.price, newItem.quantity);
    }

    fclose(original_file);
    fclose(temp_file);
    printf("\n===++++++===Quantity Sucessfully Increased===++++++===\n");
    renameoffile();
    
   
}
void prev_item() {
    char item_name[100];
    int symbol;
    float MRP;
    printf("Enter the name of the item\n");
    scanf("%s", item_name);
    getchar();
    search_inventory(item_name);
    printf("Enter the S.N. from the List or 0 if not on the list\n");
    scanf("%d", &symbol);
    if(symbol == 0)
    {
        return;
    }
    printf("Enter the MRP of the product\n");
    scanf("%f", &MRP);
    int test = MRP_Checker(MRP,symbol);
     if(test==1)
    {
        float quantity;
        printf("Enter the Quantity to update\n");
        scanf("%f", &quantity);
        Quantity_updater(symbol, quantity);
    }
    else
    {
        string_returner(symbol, MRP);
    }
}

void inventory() {
    int option_inventory;
    while (1) {
        printf("Enter 1\n");
        printf("If item is previously bought\n");
        printf("Enter 2\n");
        printf("If item is newly bought\n");
        scanf("%d", &option_inventory);
        getchar();
        if(option_inventory==0)
        {
            return;
        }

        switch (option_inventory) {
            case 1:
                prev_item();
                break;

            case 2:
                new_item();
                break;

            default:
                printf("...............................\n");
                printf("..Please Enter the valid Input..\n");
                printf("...........Try Again..............\n");
                printf("...............................\n");
                break;
        }
    }
}


int main() {
    int n;
    while (1) {
        printf("\t\t======\t\tWelcome To Retail Billing System\t\t======\n");
        printf("Enter 1 for Sales && 2 for Inventory \n");
        scanf("%d", &n);
        getchar(); // To consume the newline character left by scanf

        switch (n) {
            case 1:
                sales();
                break;

            case 2:
                inventory();
                break;

            default:
                printf("Please Enter the correct option\n");
                break;
        }
    }
    return 0;
}

void sales()
{
    while (1)
    {
        char product_name[100];
        printf("Enter the product name to search (or '0' to exit):\n");
        scanf("%s", product_name);
        if (strcmp(product_name, "0") == 0) {
            break;
        }
        search_inventory(product_name);
        int Symbol_num = 0;
        printf("Please Enter the SN from the list \n");
        scanf("%d", &Symbol_num);
        getchar(); 
        Data_passer(Symbol_num);
    }
    Print_bill(items, itemCount);
}

void Data_passer(int num) {
    FILE *read;
    read = fopen("inventory.txt", "r");
    if (read == NULL) {
        printf("Unable to open the inventory file\n");
        exit(1);
    }

    int in = 1;
    while (fscanf(read, "%d\t%s\t%f\t%f\n", &inven[in-1].SN, inven[in- 1].name, &inven[in- 1].price, &inven[in - 1].quantity) != EOF) {
        float Quantity;
        if (num == in) {
            m: Quantity = 0;
            printf("Enter the Quantity\n"); 
            scanf("%f", &Quantity);
            int z = Quantity_checker(num, Quantity);
            if (z == 0) {
                bill_function(inven[in- 1].name, inven[in - 1].price, Quantity);
                fclose(read);
                Quantity_nupdater(num, Quantity);
            } 
            else
            {
                printf("Unable to provide such Quantity\n");
                printf("Please re-enter the Quantity\n");
                goto m;
            }
            break;
        }
        in++;
    }
    fclose(read);
}

int Quantity_checker(int num, float Quantity) {
    FILE *read;
    read = fopen("inventory.txt", "r");
    if (read == NULL) {
        printf("Unable to open the inventory file\n");
        exit(1);
    }
    int i = 0;
    while (fscanf(read, "%d\t%s\t%f\t%f\n", &inven[i].SN, inven[i].name, &inven[i].price, &inven[i].quantity) != EOF) {
        if (num == i + 1) { // Adjusted condition to match the SN
            if (inven[i].quantity >= Quantity) {
                fclose(read);
                return 0;
            } else {
                printf("Quantity sold exceeds the Quantity in Inventory\n");
                fclose(read);
                return 1;
            }
        }
        i++;
    }
    fclose(read);
    return 1;
}

void bill_function(char name[], float price, float quantity) {
    if (itemCount >= MAX_ITEMS) {
        printf("Error: Maximum item limit reached.\n");
        return;
    }

    strcpy(items[itemCount].name, name);
    items[itemCount].price = price;
    items[itemCount].quantity = quantity;
    itemCount++;
}

void search_inventory(char *partial_name) {
    FILE *fptr;
    fptr = fopen("inventory.txt", "r");
    if (fptr == NULL) {
        printf("Unable to open the inventory file\n");
        return;
    }

    invenCount = 0;
    while (fscanf(fptr, "%d\t%s\t%f\t%f\n", &inven[invenCount].SN, inven[invenCount].name, &inven[invenCount].price, &inven[invenCount].quantity) != EOF) {
        if (strstr(inven[invenCount].name, partial_name)!= NULL ) {
            printf("SN:%d\t%s\tPrice:%.2f\tQty:%.2f\n", inven[invenCount].SN, inven[invenCount].name, inven[invenCount].price,inven[invenCount].quantity); // Adjusted to print correct SN
        }
        invenCount++;
    }
    fclose(fptr);
}
void remove_item(Item items[], int itemCount) 
{
    int symbol = 0;
    float Quantity;
    printf("Enter the symbol number of the item to remove: ");
    scanf("%d", &symbol);
    int indexToRemove = symbol - 1;
    if (symbol < 1 || symbol > invenCount) 
    {
        printf("Invalid symbol number. No item added.\n");
        return;
    }
        m:
        Quantity = 0;
            printf("Enter the Quantity to remove: ");
             scanf("%f", &Quantity);
            if(Quantity > items[indexToRemove].quantity)
            {
                printf("INVALID.... ERROR 404\n");
                printf("Please Re-enter the Quantity\n");
                goto m;
            }
           
            
            
    
    int Actualindex = symbol_returner(items[indexToRemove].name);
    Quantity_updater(Actualindex, Quantity);
    if(Quantity == items[indexToRemove].quantity)
    {
        
       for (int i = indexToRemove; i < itemCount - 1; i++) {
        strcpy(items[i].name, items[i + 1].name);
        items[i].price = items[i + 1].price;
        items[i].quantity = items[i + 1].quantity;
       }
        // Clear the last item in the array
    items[itemCount - 1].name[0] = '\0';
    items[itemCount - 1].price = 0;
    items[itemCount - 1].quantity = 0;

    // Decrease item count
    itemCount--;

    printf("Item removed successfully.\n");
    
    }
    else
    {
        items[indexToRemove].quantity = items[indexToRemove].quantity - Quantity;
        Quantity_updater(Actualindex, Quantity);
    }
    
    Print_bill(items, itemCount);
}
int symbol_returner(char str[])
{
    Item Messi;
    FILE *fptr;
    fptr = fopen("inventory.txt", "r");
    while(fscanf(fptr, "%d\t%s\t%f\t%f\n", &Messi.SN, Messi.name, &Messi.price, &Messi.quantity) != EOF)
    {
      if(strcmp(Messi.name ,str )== 0)
      {
          fclose(fptr);
          return Messi.SN;
      }
    }
    fclose(fptr);
    printf("Sorry unable to Find the string\n");
    return 0;
}
void add_item(Item items[], int itemCount)
 {
    int choice = 0;
    printf("Enter 1 to increase Quantity && 2 to add new item in Current Bill\n");
    scanf("%d", &choice);
    if(choice==1)
    {
    char product_name[100];
    int symbol = 0;
    float Quantity;

    
    printf("Enter the symbol number of the item from the Bill: \n");
    scanf("%d", &symbol);

    if (symbol < 1 || symbol > invenCount) {
        printf("Invalid symbol number. No item added.\n");
        return;
    }

    printf("Enter the Quantity to add to the Bill: \n");
    scanf("%f", &Quantity);
    int indexToAdd = symbol - 1;
    int realsn = symbol_returner(items[indexToAdd].name);
    int z = Quantity_checker(realsn, Quantity);
    if (z == 0)
    {
        items[indexToAdd].quantity = items[indexToAdd].quantity + Quantity;
        Quantity_nupdater(realsn, Quantity);
    }
    }

     else if(choice == 2)
    {
        sales();
        return;
    }
    else
    {
        printf("\n You didn't entered the valid option \n");
        return;
    }

    Print_bill(items, itemCount);
}

void Print_bill(Item items[], int itemCount) {
    
    time_t current_time;
    time(&current_time);
    struct tm *local_time = localtime(&current_time);
    char time_str[100],Date_str[100];
    strftime(time_str , sizeof(time_str),"%H:%M:%S", local_time);
    strftime(Date_str , sizeof(Date_str),"%Y-%m-%d", local_time);
    float Total = 0;
    printf("--------------------------------------------------------------------------------------------\n");
    printf("                                  RETAIL STORE                                          \n");
    printf("                                 BHAKTAPUR, NEPAL                                             \n");
    printf("Transaction Time: %s\n", time_str);
    printf("Transaction Date: %s\n", Date_str);
    printf("--------------------------------------------------------------------------------------------\n");
    printf("SN\t\tParticulars\t\tPrince\t\tQuantity\t\tTotal\n");
    printf("--------------------------------------------------------------------------------------------\n");
    printf("\n");
    for (int i = 0; i < itemCount; i++) {
        float amount = items[i].price * items[i].quantity;
        printf("%d\t\t%s\t\t%.2f\t\t%.2f\t\t%.2f\n", i + 1, items[i].name, items[i].price, items[i].quantity, amount);
        Total += amount;
    }
    printf("--------------------------------------------------------------------------------------------\n");
    printf("                                                                            Amount:%.2f\n", Total);
    printf("--------------------------------------------------------------------------------------------\n");
    float Dis_percen , Dis_amt;
    int meow = 0 , option = 0;
    s:
    printf("Enter the 1 to add item && Enter 2 to remove item from the bill && ZERO to continue\n");
    scanf("%d", &meow);
    if(meow == 2)
    {
        remove_item(items , itemCount);
        return;
    }
    if(meow == 1)
    {
        add_item(items , itemCount);
        return;
    }

    if(meow < 0 && meow > 2)
    {
        printf("Please re-enter the Quantity\n\n");
        goto s;
    }
    
    printf("Enter the Discount amount\n");
    scanf("%f", &Dis_amt);

    if (Dis_amt > 0 && Dis_amt <= Total)
    {
        Total = Total - Dis_amt;
        printf("--------------------------------------------------------------------------------------------\n");
        printf("                                                 New Amount after Discount amount:%.2f\n", Total);
        printf("--------------------------------------------------------------------------------------------\n");
        
    }
    printf("Enter the Discount percentage\n");
    scanf("%f", &Dis_percen);

    if (Dis_percen > 0 && Dis_percen <= 100) {
        float discount_amount = 0.01 * Dis_percen * Total;
        Total -= discount_amount;
        printf("--------------------------------------------------------------------------------------------\n");
        printf("                                           New Amount after Discount Percentage :%.2f\n", Total);
        printf("--------------------------------------------------------------------------------------------\n");
    }
    
   
    float Amt_receive=0;
    m:
    printf("Amount received: \n");
    scanf("%f", &Amt_receive);

    if (Amt_receive > Total) {
        float change = Amt_receive - Total;
        printf("----------------------------------------------------------------------------------------------\n");
        printf("                                                                        Change :%.2f\n", change);
        printf("-----------------------------------------------------------------------------------------------\n");
        printf("==============================THANK YOU FOR WEARING MASK :-) ==================================\n\n ");
        printf("**********************************PLEASE VISIT AGAIN*******************************************\n\n");
        clear_items();
        return;
    } else if (Amt_receive == Total) 
    {
        printf("==============================THANK YOU FOR WEARING MASK :-) ==================================\n\n ");
        printf("**********************************PLEASE VISIT AGAIN*******************************************\n\n");
        clear_items();
        return;
    }
    else {

        printf("Unable To receive less amount\n");
        goto m;
    }
}
