import json

from . import general
from localization.localization import localize
import components.receipt as receipt
import settings


def add_payment(message, bot):
    settings.logger_general.info(f"User {message.chat.id} chose to add a payment to a receipt")
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
            settings.logger_general.error(f"User {message.chat.id} is not in receipt {message.text}")
            bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
            general.main_menu(message, bot)
    else:
        settings.logger_general.error(f"Receipt {message.text} not found")
        bot.send_message(user_id, localize(user_id, "receipt_not_found"))


def _create_payment(message, bot, receipt_id: str):
    try:
        settings.logger_general.info(f"User {message.chat.id} entered payment amount {message.text} to receipt {receipt_id}")
        receipt_object = receipt.load_receipt(receipt_id)
        receipt_object.add_payment(message.chat.id, float(message.text))
        settings.logger_general.info(f"User {message.chat.id} added payment {message.text} to receipt {receipt_id} successfully!")
        bot.send_message(message.chat.id, localize(message.chat.id, "payment_added"))
        general.main_menu(message, bot)
    except ValueError:
        settings.logger_errors.error(f"User {message.chat.id} entered payment amount {message.text}, which is not a number")
        bot.send_message(message.chat.id, localize(message.chat.id, "payment_not_number"))
        general.main_menu(message, bot)
