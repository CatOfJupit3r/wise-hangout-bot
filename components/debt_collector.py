"""
"""
import json


def add_debts(receipt_id: int | str, debts_of_receipt: dict) -> None:
    """
    Adds debts to each user into database
    :param receipt_id: id of receipt. If value is integer, it will be converted to string
    :param debts_of_receipt: debt dictionary, which is given by receipt object
    :return:
    """
    if type(receipt_id) == int:
        receipt_id = str(receipt_id)
    with open("database/users.json", "r+") as f:
        users = json.load(f)
    for user in debts_of_receipt:
        if user in users:
            users[user]["receipts"][receipt_id] = debts_of_receipt[user]


def get_debts(user_id: int | str) -> dict:
    """
    Returns dictionary of what user owes in each receipt
    :param user_id: id of user. If value is integer, it will be converted to string
    :return: dict
    """
    if type(user_id) == int:
        user_id = str(user_id)
    with open("database/users.json", "r+") as f:
        users = json.load(f)
    return users[user_id]["receipts"]
