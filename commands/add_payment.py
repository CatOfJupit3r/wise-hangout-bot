import json

from . import general
from localization.localization import localize
import components.receipt as receipt


def add_payment(message, bot):
    general.check_for_receipt_id(message, bot, add_payment_to_receipt)


def add_payment_to_receipt(message, bot):
    general.update_current_receipt_id(message.chat.id, message.text)
    user_id = str(message.chat.id)
    with open("database/receipts.json", "r+") as f:
        receipts = json.load(f)
    if message.text in receipts:
        if user_id in receipts[message.text]["users"]:
            general.send_message_and_wait(bot, message, localize(user_id, "enter_payment_amount"), _create_payment, message.text)
        else:
            bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
            general.main_menu(message, bot)
    else:
        bot.send_message(user_id, localize(user_id, "receipt_not_found"))


def _create_payment(message, bot, receipt_id: str):
    try:
        receipt_object = receipt.load_receipt(receipt_id)
        receipt_object.add_payment(message.chat.id, float(message.text))
        bot.send_message(message.chat.id, localize(message.chat.id, "payment_added"))
        general.main_menu(message, bot)
    except ValueError:
        bot.send_message(message.chat.id, localize(message.chat.id, "payment_not_number"))
        general.main_menu(message, bot)
