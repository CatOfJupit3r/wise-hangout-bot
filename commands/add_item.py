import json

import settings
from . import general
from localization.localization import localize
import components.receipt as receipt
import components.purchase as purchase


def add_item(message, bot):
    settings.logger_general.info(f"User {message.chat.id} chose to add an item")
    general.check_for_receipt_id(message, bot, add_item_to_receipt)


def add_item_to_receipt(message, bot):
    general.update_current_receipt_id(message.chat.id, message.text)
    user_id = str(message.chat.id)
    with open("database/receipts.json", "r+") as f:
        receipts = json.load(f)
    if message.text in receipts:
        if user_id in receipts[message.text]["users"]:
            general.send_message_and_wait(bot, message, localize(user_id, "enter_item_name"), _set_item_name, message.text)
        else:
            settings.logger_general.error(f"User {message.chat.id} is not in receipt {message.text}")
            bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
            general.main_menu(message, bot)
    else:
        settings.logger_general.error(f"Receipt {message.text} not found")
        bot.send_message(user_id, localize(user_id, "receipt_not_found"))


def _set_item_name(message, bot, receipt_id: str):
    settings.logger_general.info(f"User {message.chat.id} entered item name {message.text} to receipt {receipt_id}")
    general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_item_price"), _set_item_price, receipt_id, message.text)


def _set_item_price(message, bot, receipt_id: str, item_name: str):
    try:
        settings.logger_general.info(f"User {message.chat.id} entered item price {message.text} to receipt {receipt_id}")
        float(message.text)
        general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_item_quantity"), _create_purchase, receipt_id, item_name, message.text)
    except ValueError:
        settings.logger_errors.error(f"User {message.chat.id} entered item price {message.text}, which is not a number")
        bot.send_message(message.chat.id, localize(message.chat.id, "price_not_number"))
        general.main_menu(message, bot)


def _create_purchase(message, bot, receipt_id: str, item_name: str, item_price: str):
    try:
        settings.logger_general.info(f"User {message.chat.id} entered item quantity {message.text} to receipt {receipt_id}")
        int(message.text)
        new_item = purchase.Purchase(item_name, float(item_price), int(message.text))
        settings.logger_general.info(f"User {message.chat.id} created purchase {new_item} to receipt {receipt_id}")
        receipt_object = receipt.load_receipt(receipt_id)
        receipt_object.add_item(new_item)
        settings.logger_general.info(f"User {message.chat.id} added purchase {new_item} to receipt {receipt_id} successfully!")
        bot.send_message(message.chat.id, localize(message.chat.id, "item_added"))
        general.main_menu(message, bot)
    except ValueError:
        settings.logger_errors.error(f"User {message.chat.id} entered item quantity {message.text}, which is not a number")
        bot.send_message(message.chat.id, localize(message.chat.id, "quantity_not_number"))
        general.main_menu(message, bot)

