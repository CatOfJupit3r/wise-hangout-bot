import json

from . import general
from localization.localization import localize
import settings
import traceback


def delete_user(message, bot):
    settings.logger_general.info(f"User {message.chat.id} chose to delete his data")
    general.send_message_and_wait(bot, message, localize(message.chat.id, "you_sure"), _remove_user)


def _remove_user(message, bot):
    if message.text == localize(message.chat.id, "yes"):
        try:
            user_id = str(message.chat.id)
            with open("database/users.json", "r+") as f:
                users = json.load(f)
            if user_id in users:
                users.pop(user_id)
                with open("database/users.json", "w+") as f:
                    json.dump(users, f, indent=4)
                settings.logger_general.info(f"User {user_id} removed from database")
                with open("database/receipts.json", "r+") as f:
                    receipts = json.load(f)
                for receipt_id in receipts:
                    if user_id in receipts[receipt_id]["users"]:
                        if receipts[receipt_id]["users"].get("deleted_user") is None:
                            receipts[receipt_id]["users"]["deleted_user"] = [0, 0]
                        receipts[receipt_id]["users"]["deleted_user"][0] += receipts[receipt_id]["users"][user_id]
                        receipts[receipt_id]["users"]["deleted_user"][1] += 1
                        receipts[receipt_id]["users"].pop(user_id)
                with open("database/receipts.json", "w+") as f:
                    json.dump(receipts, f, indent=4)
                bot.send_message(user_id, localize(user_id, "user_removed"))
            else:
                settings.logger_general.error(f"User {user_id} not found in database")
                bot.send_message(user_id, localize(user_id, "user_not_found"))
            general.main_menu(message, bot)
        except Exception as e:
            settings.logger_errors.error(f"Error while removing user {message.chat.id} from database: {e}")
            settings.logger_errors.error(traceback.format_exc())
            bot.send_message(message.chat.id, localize(message.chat.id, "error_while_removing_user"))
            general.main_menu(message, bot)
    elif message.text == localize(message.chat.id, "no"):
        general.main_menu(message, bot)
    else:
        settings.logger_errors.error(f"Unknown message: {message.text}")
        bot.send_message(message.chat.id, localize(message.chat.id, "invalid_input"))
        general.main_menu(message, bot)
