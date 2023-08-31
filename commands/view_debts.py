import json
import traceback

import settings
from localization.localization import localize
from . import general
import components.receipt as receipt


def view_debts(message, bot):
    settings.logger_general.info(f"User {message.chat.id} chose to view his debts")
    try:
        user_id = str(message.chat.id)
        with open("database/receipts.json", "r+") as f:
            receipts = json.load(f)
        has_debts = False
        debts: str = ""
        for receipt_id in receipts:
            receipt_object = receipt.load_receipt(receipt_id)
            if user_id in receipt_object.users:
                has_debts = True
                debts += str(receipt_object.name + " — " + str(receipt_object.get_debt_info(user_id)) + "\n")
        if has_debts is False:
            settings.logger_general.info(f"User {user_id} has no debts")
            bot.send_message(user_id, localize(user_id, "no_debts"))
        else:
            settings.logger_general.info(f"User {user_id} has debts")
            bot.send_message(user_id, debts)
        general.main_menu(message, bot)
    except Exception as e:
        settings.logger_errors.error(f"Error while viewing debts of user {message.chat.id}: {e}")
        settings.logger_errors.error(traceback.format_exc())
        bot.send_message(message.chat.id, localize(message.chat.id, "error_while_viewing_debts"))
        general.main_menu(message, bot)
