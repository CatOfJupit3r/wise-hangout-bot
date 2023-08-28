import components.purchase as purchase
import time
import json
import settings

"""
This module contains class Receipt
Receipt represents a go to a restaurant or a cafe
"""


def load_receipt(name) -> "Receipt":
    """
    Loads receipt from json file
    :param name: str
    :return: Receipt object
    """
    with open("database/receipts.json", "r+") as f:
        receipts = json.load(f)
    receipt = receipts[name]
    receipt_object = Receipt(name, push_to_database=False)
    receipt_object.date = receipt["date"]
    receipt_object._users = receipt["users"]
    for item in receipt["items"]:
        item_object = purchase.Purchase(item["name"], item["price_for_one"], item["quantity"], item["customer"],
                                        item["purchase_date"])
        receipt_object.add_item(item_object)
    return receipt_object


class Receipt:
    """
    This class represents a receipt
    """

    def __init__(self, name: str, *, push_to_database=True):
        """
        Constructor for Receipt class
        :param name: str
        """
        self.id = settings.generate_id()
        self.name = name
        self.date = time.strftime("%d/%m/%Y %H:%M:%S")
        self._items: list[purchase.Purchase] = []
        self.total: int = 0
        self._users = []
        if push_to_database:
            self.__save_to_database()

    def __save_to_database(self):
        """
        Adds receipt to json file
        :return: None
        """
        with open("database/receipts.json", "r+") as f:
            receipts = json.load(f)
        items_to_save = []
        for item in self.items:
            if item.customer not in self.users:
                self.users.append(item.customer)
            items_to_save.append({
                "name": item.name,
                "price_for_one": item.price_for_one,
                "quantity": item.quantity,
                "customer": item.customer,
                "purchase_date": item.purchase_date,
            })
        receipts[self.id] = {
            "name": self.name,
            "date": self.date,
            "items": items_to_save,
            "users": self.users
        }
        with open("database/receipts.json", "w+") as f:
            json.dump(receipts, f, indent=4)

    def add_item(self, item):
        """
        Adds item to the receipt
        :param item: Item object
        :return: None
        """
        self._items.append(item)
        if item.customer not in self.users:
            self.users.append(item.customer)
        self.total += item.price_for_one * item.quantity
        self.__save_to_database()

    @property
    def items(self):
        return self._items

    @property
    def users(self):
        return self._users

    def calculate_each_user_debt(self):
        """
        Tries to come up with a solution to the debt problem
        Each 
        :return: dict
        """
        divided_total = self.total / len(self.users)
        debt = {}
        for item in self.items:
            if item.customer not in debt:
                debt[item.customer] = 0
            debt[item.customer] += item.price_for_one * item.quantity
        for user in debt:
            debt[user] = divided_total - debt[user]
        return debt

    def get_receipt_info(self):
        """
        Returns receipt info
        :return: str
        """
        return f"{self.name}\n{self.date}\n{self.total}\n"
