import json

from . import general
from localization.localization import localize
import components.receipt as receipt


def find_whom_to_pay(message, bot):
    general.check_for_receipt_id(message, bot, send_whom_to_pay)


def send_whom_to_pay(message, bot):
    receipt_id = message.text
    user_id = str(message.chat.id)
    general.update_current_receipt_id(message.chat.id, receipt_id)
    with open("database/receipts.json", "r+") as f:
        receipts = json.load(f)
    people = ""
    if receipt_id in receipts:
        if user_id in receipts[receipt_id]["users"]:
            receipt_object = receipt.load_receipt(receipt_id)
            people += str(receipt_object.find_whom_to_pay(user_id))
            if people.strip() == "":
                bot.send_message(user_id, localize(user_id, "no_one"))
            else:
                bot.send_message(user_id, str(receipt_object.find_whom_to_pay(user_id)))
        else:
            bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
    else:
        bot.send_message(user_id, localize(user_id, "receipt_not_found"))
    general.main_menu(bot, message)
