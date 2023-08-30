import json

from localization.localization import localize
from . import general
import components.receipt as receipt


def view_debts(message, bot):
    user_id = str(message.chat.id)
    with open("database/receipts.json", "r+") as f:
        receipts = json.load(f)
    for receipt_id in receipts:
        receipt_object = receipt.load_receipt(receipt_id)
        if user_id in receipt_object.users and receipt_object.get_debt_info(user_id) != 0:
            bot.send_message(user_id, str(receipt_object.get_debt_info(user_id)))
    else:
        bot.send_message(user_id, localize(user_id, "no_debts"))

    general.main_menu(message, bot)
