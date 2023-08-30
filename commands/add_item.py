import json

from . import general
from localization.localization import localize
import components.receipt as receipt
import components.purchase as purchase


def add_item(message, bot):
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
            bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
            general.main_menu(message, bot)
    else:
        bot.send_message(user_id, localize(user_id, "receipt_not_found"))


def _set_item_name(message, bot, receipt_id: str):
    general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_item_price"), _set_item_price, receipt_id, message.text)


def _set_item_price(message, receipt_id: str, bot, item_name: str):
    general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_item_quantity"), _set_item_quantity, receipt_id, item_name, message.text)


def _set_item_quantity(message, receipt_id: str, bot, item_name: str, item_price: str):
    general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_item_customer"), _create_purchase, receipt_id, item_name, item_price, message.text)


def _create_purchase(message, receipt_id: str, bot, item_name: str, item_price: str):
    new_item = purchase.Purchase(item_name, float(item_price), int(message.text))
    receipt_object = receipt.load_receipt(receipt_id)
    receipt_object.add_item(new_item)
    bot.send_message(message.chat.id, localize(message.chat.id, "item_added"))
    general.main_menu(message, bot)

