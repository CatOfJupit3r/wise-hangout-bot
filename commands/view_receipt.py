import json
import traceback

import settings
from . import general
from localization.localization import localize
import components.receipt as receipt


def view_receipt(message, bot):
    settings.logger_general.info(f"User {message.chat.id} chose to view a receipt")
    general.check_for_receipt_id(message, bot, view_receipt_with_id)


def view_receipt_with_id(message, bot):
    try:
        general.update_current_receipt_id(message.chat.id, message.text)
        user_id = str(message.chat.id)
        with open("database/users.json", "r+") as f:
            users = json.load(f)
        if users[str(user_id)]["current_receipt"] is not None:
            receipt_id = users[str(user_id)]["current_receipt"]
            receipt_object = receipt.load_receipt(receipt_id)
            if receipt_object is not None:
                if user_id == settings.OWNER_ID or user_id in receipt_object.users:
                    result = ""
                    result += str(receipt_object.get_receipt_info(user_id) + "\n")
                    result += localize(user_id, "items") + "\n"
                    has_items = False
                    for item in receipt_object.items:
                        has_items = True
                        result += str(item.get_item_info(user_id) + "\n")
                    if not has_items:
                        result += localize(user_id, "no_items") + "\n"
                    debts = receipt_object.users
                    if debts is not None:
                        result += localize(user_id, "payed") + "\n" + "\n"
                        for debt in debts:
                            if isinstance(debts[debt], list):
                                result += str(users[debt]["nickname"] + " — " + str(abs(debts[debt][0])) + "\n")
                            else:
                                result += str(users[debt]["nickname"] + " — " + str(abs(debts[debt])) + "\n")
                    settings.logger_general.info(f"User {user_id} viewed receipt {receipt_id} successfully!")
                    bot.send_message(user_id, result)
                else:
                    settings.logger_general.error(f"User {user_id} is not in receipt {receipt_id}")
                    bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
            else:
                settings.logger_general.error(f"Receipt {receipt_id} not found")
                bot.send_message(user_id, localize(user_id, "receipt_not_found"))
        else:
            settings.logger_general.error(f"User {user_id} has no current receipt")
            bot.send_message(user_id, localize(user_id, "receipt_not_found"))
        general.main_menu(message, bot)
    except Exception as e:
        settings.logger_errors.error(f"Error while viewing receipt of user {message.chat.id}: {e}")
        settings.logger_errors.error(traceback.format_exc())
        bot.send_message(message.chat.id, localize(message.chat.id, "error_while_viewing_receipt"))
        general.main_menu(message, bot)
