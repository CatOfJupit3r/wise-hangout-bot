import json

from . import general
from localization.localization import localize
import components.receipt as receipt


def create_receipt(message, bot):
    general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_receipt_name"), _set_receipt_name)


def _set_receipt_name(message, bot):
    new_receipt = receipt.Receipt(message.text)
    general.update_current_receipt_id(message.chat.id, new_receipt.id)
    with open("database/receipts.json", "r+") as f:
        receipts = json.load(f)
    if message.chat.id not in receipts[new_receipt.id]["users"]:
        receipts[new_receipt.id]["users"][message.chat.id] = 0
    with open("database/receipts.json", "w+") as f:
        json.dump(receipts, f, indent=4)
    bot.send_message(message.chat.id, localize(message.chat.id, "receipt_created"))
    general.main_menu(message, bot)
