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
            bot.send_message(user_id, localize(user_id, "enter_payment_amount"))
            bot.register_next_step_handler(message, _set_payment_amount, bot, message.text)
        else:
            bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
            general.main_menu(message, bot)
    else:
        bot.send_message(user_id, localize(user_id, "receipt_not_found"))


def _set_payment_amount(message, bot, receipt_id: str):
    general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_payment_customer"), _create_payment, receipt_id)


def _create_payment(message, bot, receipt_id: str, payment_amount: str):
    receipt_object = receipt.load_receipt(receipt_id)
    receipt_object.add_payment(message.chat.id, float(payment_amount))
    bot.send_message(message.chat.id, localize(message.chat.id, "payment_added"))
    general.main_menu(message, bot)
