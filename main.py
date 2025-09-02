from Inventory import Inventory

def main():
    menu = ("\n"
            f"[0] Load Inventory\n"
            f"[1] Add Item\n"
            f"[2] Remove Item\n"
            f"[3] Update Item\n"
            f"[4] Export Items\n"
            f"[5] Get Item\n"
            f"[6] List Inventory\n"
            f"[7] Restock\n"
            f"[8] Exit Inventory\n")

    print("Welcome to Inventory")
    company_name = input("Enter company name: ")
    inventory = Inventory(company_name)
    print("Inventory created!")

    while True:
        print(menu)
        choice = input("Enter your choice: ")
        match choice:
            case "0":
                inventory.load_inventory()
                inventory.need_restock()

            case "1":
                sku = input("Enter SKU: ")
                name = input("Enter item name: ")
                while True:
                    quantity = input("Enter quantity: ")
                    if quantity.isdigit() and int(quantity) >= 0:
                        break
                while True:
                    price = input("Enter price: ")
                    if is_float(price):
                        if float(price) >= 0:
                            break
                category = input("Enter category: ")
                inventory.add_item({"sku": sku, "name": name, "quantity": int(quantity),
                                    "category": category, "price": float(price)})
                inventory.need_restock()

            case "2":
                sku = input("Enter SKU of item to remove: ")
                inventory.remove_item(sku)
                inventory.need_restock()

            case "3":
                sku = input("Enter SKU of item to update: ")
                property_to_update = input("Enter property to update: ")
                value = input("Enter the new value to assign: ")
                inventory.update_item(sku, property_to_update, value)
                inventory.need_restock()

            case "4":
                sku = input("Enter SKU of item to export: ")
                quant = input("Enter quantity to export: ")
                while True:
                    if quant.isdigit():
                        if int(quant) >= 0:
                            break
                    quant = input("Enter quantity to export: ")
                try:
                    inventory.export_items(sku, int(quant))
                except KeyError as e:
                    print(f"Item not found in inventory")
                    print(e)
                inventory.need_restock()

            case "5":
                sku = input("Enter SKU of item to get: ")
                inventory.get_item(sku)
                inventory.need_restock()

            case "6":
                inventory.list_inventory()
                inventory.need_restock()

            case "7":
                sku = input("Enter SKU of item to restock: ")
                quantity = input("Enter quantity to restock: ")
                while True:
                    if quantity.isdigit():
                        if int(quantity) >= 0:
                            break
                    quantity = input("Enter quantity to restock: ")
                inventory.restock(sku, int(quantity))
                inventory.need_restock()

            case "8":
                inventory.save_inventory()
                break

    print("Thank you for using this program!")

if __name__ == "__main__":
    main()


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False