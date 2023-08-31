import json

from . import general
from localization.localization import localize
import settings
import traceback


def join_receipt(message, bot):
    settings.logger_general.info(f"User {message.chat.id} chose to join a receipt")
    general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_receipt_id"), _add_user_to_receipt)


def _add_user_to_receipt(message, bot):
    try:
        general.update_current_receipt_id(message.chat.id, message.text)
        receipt_id = message.text
        user_id = str(message.chat.id)
        with open("database/receipts.json", "r+") as f:
            receipts = json.load(f)
        if receipt_id in receipts:
            if user_id not in receipts[receipt_id]["users"]:
                receipts[receipt_id]["users"][user_id] = 0
                with open("database/receipts.json", "w+") as f:
                    json.dump(receipts, f, indent=4)
                settings.logger_general.info(f"User {user_id} added to receipt {receipt_id}")
                bot.send_message(user_id, localize(user_id, "user_added_to_receipt"))
            else:
                settings.logger_general.error(f"User {user_id} is already in receipt {receipt_id}")
                bot.send_message(user_id, localize(user_id, "user_already_in_receipt"))
        else:
            settings.logger_general.error(f"Receipt {receipt_id} not found")
            bot.send_message(user_id, localize(user_id, "receipt_not_found"))
        general.main_menu(message, bot)
    except Exception as e:
        settings.logger_errors.error(f"Error while adding user {message.chat.id} to receipt {message.text}: {e}")
        settings.logger_errors.error(traceback.format_exc())
        bot.send_message(message.chat.id, localize(message.chat.id, "error_while_adding_user_to_receipt"))
        general.main_menu(message, bot)
