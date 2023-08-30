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
        item_object = purchase.Purchase(item["name"], item["price_for_one"], item["quantity"])
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
        self.need_to_be_paid: int = 0
        self._users = {} # {user_id: how much he paid}
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
            items_to_save.append({
                "name": item.name,
                "price_for_one": item.price_for_one,
                "quantity": item.quantity,
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
        self.need_to_be_paid += item.price_for_one * item.quantity
        self.__save_to_database()

    @property
    def items(self):
        return self._items

    @property
    def users(self):
        return self._users

    def add_user(self, user_id):
        """
        Adds user to the receipt
        :param user_id: int
        :return: None
        """
        self._users[user_id] = 0
        self.__save_to_database()

    def add_payment(self, user_id, amount):
        """
        Adds payment to the receipt
        :param user_id: int
        :param amount: int
        :return: None
        """
        self._users[user_id] = amount
        self.__save_to_database()

    def get_debt_info(self, user_id=None) -> int | dict[str, int]:
        """
        Returns debt info.
        :param user_id: if set to None, returns all debts
        :return:
        """
        how_many_users = len(self.users.keys())
        if user_id is None:
            debt = self.need_to_be_paid / how_many_users
            result = {}
            for user in self.users:
                result[user] = debt - self.users[user]
        else:
            result = self.need_to_be_paid / how_many_users - self.users[user_id]
        return result

    def find_whom_to_pay(self, user_id) -> int:
        """
        Returns id of user to pay
        :param user_id: int
        :return: int
        """
        debt_info = self.get_debt_info()
        if user_id in debt_info:
            return user_id
        else:
            for user in debt_info:
                if debt_info[user] < 0:
                    return user

    def get_receipt_info(self):
        """
        Returns receipt info
        :return: str
        """
        return f"{self.name}\n{self.date}\n{self.need_to_be_paid}\n"
