import json
import traceback

import settings
from . import general
from localization.localization import localize
import components.receipt as receipt


def find_whom_to_pay(message, bot):
    settings.logger_general.info(f"User {message.chat.id} chose to find whom to pay")
    general.check_for_receipt_id(message, bot, send_whom_to_pay)


def send_whom_to_pay(message, bot):
    try:
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
                    bot.send_message(user_id, localize(user_id, "whom_to_pay") + "\n" + str(receipt_object.find_whom_to_pay(user_id)))
                settings.logger_general.info(f"User {user_id} requested whom to pay in receipt {receipt_id} successfully!")
            else:
                settings.logger_general.error(f"User {user_id} is not in receipt {receipt_id}")
                bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
        else:
            settings.logger_general.error(f"Receipt {receipt_id} not found")
            bot.send_message(user_id, localize(user_id, "receipt_not_found"))
        general.main_menu(message, bot)
    except Exception as e:
        settings.logger_errors.error(f"Error while finding whom to pay in receipt {message.text}: {e}")
        settings.logger_errors.error(traceback.format_exc())
        bot.send_message(message.chat.id, localize(message.chat.id, "error_while_finding_whom_to_pay"))
        general.main_menu(message, bot)
