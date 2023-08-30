import json

import settings
from . import general
from localization.localization import localize
import components.receipt as receipt


def view_receipt(message, bot):
    general.check_for_receipt_id(message, bot, view_receipt_with_id)


def view_receipt_with_id(message, bot):
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
                for item in receipt_object.items:
                    result += str(item.get_item_info(user_id) + "\n")
                debts = receipt_object.users
                if debts is not None:
                    result += localize(user_id, "payed") + "\n"
                    for debt in debts:
                        result += str(users[debt]["nickname"] + " — " + str(abs(debts[debt])) + "\n")
                bot.send_message(user_id, result)
            else:
                bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
        else:
            bot.send_message(user_id, localize(user_id, "receipt_not_found"))
    else:
        bot.send_message(user_id, localize(user_id, "receipt_not_found"))
    general.main_menu(message, bot)
