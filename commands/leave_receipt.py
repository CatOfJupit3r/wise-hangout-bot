import json

from . import general
from localization.localization import localize
import settings
import traceback


def leave_receipt(message, bot):
    settings.logger_general.info(f"User {message.chat.id} chose to leave a receipt")
    general.check_for_receipt_id(message, bot, _remove_user_from_receipt)


def _remove_user_from_receipt(message, bot):
    try:
        general.update_current_receipt_id(message.chat.id, message.text)
        receipt_id = message.text
        user_id = str(message.chat.id)
        with open("database/receipts.json", "r+") as f:
            receipts = json.load(f)
        if receipt_id in receipts:
            if user_id in receipts[receipt_id]["users"]:
                receipts[receipt_id]["users"].pop(user_id)
                with open("database/receipts.json", "w+") as f:
                    json.dump(receipts, f, indent=4)
                settings.logger_general.info(f"User {user_id} removed from receipt {receipt_id}")
                bot.send_message(user_id, localize(user_id, "user_removed_from_receipt"))
            else:
                settings.logger_general.error(f"User {user_id} never been in receipt {receipt_id}")
                bot.send_message(user_id, localize(user_id, "user_never_been_in_receipt"))
        else:
            settings.logger_general.error(f"Receipt {receipt_id} not found")
            bot.send_message(user_id, localize(user_id, "receipt_not_found"))
        general.main_menu(message, bot)
    except Exception as e:
        settings.logger_errors.error(f"Error while removing user {message.chat.id} from receipt {message.text}: {e}")
        settings.logger_errors.error(traceback.format_exc())
        bot.send_message(message.chat.id, localize(message.chat.id, "error_while_removing_user_from_receipt"))
        general.main_menu(message, bot)
