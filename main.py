import json

REORDER_POINT = 5

class Item:
    def __init__(self, sku, name, quantity, category, price):
        self._name = name
        self._category = category
        self._quantity = quantity
        self._price = price

        if len(str(sku)) != 8:
            raise TypeError("Item sku must be 8 characters long")
        self._sku = sku


    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, quantity):
        if type(quantity) != int:
            raise TypeError("Item quantity must be an integer")
        if quantity < 0:
            raise ValueError("Item quantity cannot be negative")
        self._quantity = quantity

    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, price):
        if type(price) != float:
            raise TypeError("Item price must be float")
        if price <= 0:
            raise ValueError("Item price must be greater than 0")
        self._price = price

    @property
    def category(self):
        return self._category
    @category.setter
    def category(self, category):
        if type(category) != str:
            raise TypeError("Item category must be string")
        self._category = category

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if type(name) != str:
            raise TypeError("Item name must be string")
        self._name = name


class Inventory:
    def __init__(self, company_name:str):
        self.company_name = company_name
        self.items_inventory = {}

    def add_item(self, item_properties:dict):
        if item_properties["sku"] not in self.items_inventory:
            try:
               self.items_inventory[item_properties["sku"]] = Item(sku=item_properties["sku"], category=item_properties["category"],
                                                                   price=item_properties["price"], quantity=item_properties["quantity"],
                                                                   name=item_properties["name"])
            except TypeError as e:
                print(e)
        else:
            print(f"Item already exists in Inventory: {item_properties['sku']}")

    def remove_item(self, item_sku):
        try:
            self.items_inventory.pop(item_sku)
        except KeyError as e:
            print(f"Item ({item_sku}) not found")
            print("Item doesn't exist in inventory", end="\n\n")
            print(e)

    def update_item(self, sku, item_property_to_update:str, new_value):
        match item_property_to_update:
            case "quantity":
                try:
                    new_value = int(new_value)
                    self.items_inventory[sku].quantity = new_value
                except TypeError as e:
                    print(e)
                except ValueError as e:
                    print(e)
                except KeyError as e:
                    print(f"Item ({sku}) not found")
                    print("Item doesn't exist in inventory", end="\n\n")
                    print(e)

            case "price":
                try:
                    new_value = float(new_value)
                    self.items_inventory[sku].price = new_value
                except TypeError as e:
                    print(e)
                except ValueError as e:
                    print(e)
                except KeyError as e:
                    print(f"Item ({sku}) not found")
                    print("Item doesn't exist in inventory", end="\n\n")
                    print(e)

            case "category":
                try:
                    self.items_inventory[sku].category = new_value
                except TypeError as e:
                    print(e)
                except KeyError as e:
                    print(f"Item ({sku}) not found")
                    print("Item doesn't exist in inventory", end="\n\n")
                    print(e)

            case "name":
                try:
                    self.items_inventory[sku].name = new_value
                except TypeError as e:
                    print(e)
                except KeyError as e:
                    print(f"Item ({sku}) not found")
                    print("Item doesn't exist in inventory", end="\n\n")
                    print(e)

            case _:
                raise NameError("Item property not found")

    def get_item(self, sku):
        try:
            print(f"Item Name: {self.items_inventory[sku].name}")
            print(f"Item Quantity: {self.items_inventory[sku].quantity}")
            print(f"Item Price: {self.items_inventory[sku].price}")
            print(f"Item Category: {self.items_inventory[sku].category}")
        except KeyError:
            print(f"Item ({sku}) not found")
            print("Item doesn't exist in inventory", end="\n\n")
            return None

    def list_inventory(self):
        print(f"   SKU  :      Name        Quantity    Price        Category")
        for sku in self.items_inventory:
            print(f"{sku}: {self.items_inventory[sku].name:^15}, {self.items_inventory[sku].quantity:^8},"
                  f"{self.items_inventory[sku].price:^11}, {self.items_inventory[sku].category:^15}")

    def export_items(self, sku, quantity):
        new_quantity = self.items_inventory[sku].quantity - quantity
        if new_quantity < 0:
            print(f"Insufficient quantity of item ({sku}) in stock: {self.items_inventory[sku].quantity}")
            print(f"Items not exported: {sku}")
        else:
            self.items_inventory[sku].quantity = new_quantity
            print(f"Items successfully exported: {sku}")

    def need_restock(self):
        if self.items_inventory:
            for sku, values in self.items_inventory.items():
                if values.quantity <= REORDER_POINT:
                    print(f"Item ({sku}) is short in stock: {values.quantity}")
                elif values.quantity == 0:
                    print(f"Item ({sku}) is empty in stock: {values.quantity}")
        else:
            return

    def restock(self, sku, quantity):
        self.items_inventory[sku].quantity += quantity
        print(f"Item restocked: {sku}")

    def load_inventory(self):
        try:
            with open(self.company_name + "_inventory.json", "r") as inventory_file:
                inventory_json = json.load(inventory_file)
        except FileNotFoundError:
            print(f"Inventory does not exist for {self.company_name}", end="\n\n")
            return

        for sku, item in inventory_json.items():
            self.items_inventory[sku] = Item(sku=sku, name=item["name"], quantity=item["quantity"],
                                             price=item["price"], category=item["category"])

    def save_inventory(self):
        items_dict = {}
        for sku, item in self.items_inventory.items():
            items_dict[sku] = {"name": item.name, "quantity": item.quantity,
                               "price": item.price, "category": item.category}

        with open(self.company_name + "_inventory.json", "w") as inventory_file:
            json.dump(items_dict, inventory_file, indent=4)


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

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