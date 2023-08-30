import json

from . import general
from localization.localization import localize


def join_receipt(bot, message):
    general.send_message_and_wait(bot, message, localize(message.chat.id, "enter_receipt_id"), _add_user_to_receipt)


def _add_user_to_receipt(bot, message, receipt_id: str):
    general.update_current_receipt_id(message.chat.id, receipt_id)
    user_id = str(message.chat.id)
    with open("database/receipts.json", "r+") as f:
        receipts = json.load(f)
    if receipt_id in receipts:
        if user_id not in receipts[receipt_id]["users"]:
            receipts[receipt_id]["users"][user_id] = 0
            with open("database/receipts.json", "w+") as f:
                json.dump(receipts, f, indent=4)
            bot.send_message(user_id, localize(user_id, "user_added_to_receipt"))
        else:
            bot.send_message(user_id, localize(user_id, "user_already_in_receipt"))
    else:
        bot.send_message(user_id, localize(user_id, "receipt_not_found"))
    general.main_menu(message, bot)