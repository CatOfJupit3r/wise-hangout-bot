import json
import traceback

import settings
from . import general
from localization.localization import localize
import components.receipt as receipt


def create_receipt(message, bot):
    settings.logger_general.info(f"User {message.chat.id} chose to create a new receipt")
    general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_receipt_name"), _set_receipt_name)


def _set_receipt_name(message, bot):
    try:
        new_receipt = receipt.Receipt(message.text)
        general.update_current_receipt_id(message.chat.id, new_receipt.id)
        with open("database/receipts.json", "r+") as f:
            receipts = json.load(f)
        if message.chat.id not in receipts[new_receipt.id]["users"]:
            receipts[new_receipt.id]["users"][message.chat.id] = 0
        with open("database/receipts.json", "w+") as f:
            json.dump(receipts, f, indent=4)
        bot.send_message(message.chat.id, localize(message.chat.id, "receipt_created"))
        bot.send_message(message.chat.id, localize(message.chat.id, "receipt_id").format(f"`{new_receipt.id}`"), parse_mode='MarkdownV2')
        general.main_menu(message, bot)
    except Exception as e:
        settings.logger_errors.error(f"Error while creating receipt {message.text} of user {message.chat.id}: {e}")
        settings.logger_errors.error(traceback.format_exc())
        bot.send_message(message.chat.id, localize(message.chat.id, "receipt_creation_error"))
        general.main_menu(message, bot)
