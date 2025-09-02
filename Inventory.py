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

if __name__ == "__main__":
    inventory = Inventory("sauna")
    inventory.load_inventory()