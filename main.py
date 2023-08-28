import json


import components.receipt as receipt
import settings
import telebot
from localization.localization import localize, add_user_to_database


def run():
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

    @bot.message_handler(commands=["start"])
    def start(message):
        _choosing_language(message)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        user_id = call.message.chat.id
        if call.message:
            match call.data:
                case "en":
                    add_user_to_database(user_id, "en")
                    bot.send_message(user_id, localize(user_id, "welcome_message"))
                    bot.delete_message(user_id, call.message.message_id)
                    _main_menu(call.message)
                case "uk":
                    add_user_to_database(user_id, "uk")
                    bot.send_message(user_id, localize(user_id, "welcome_message"))
                    bot.delete_message(user_id, call.message.message_id)
                    _main_menu(call.message)
                case "yes_use_last_receipt":
                    bot.delete_message(user_id, call.message.message_id)
                    _view_receipt_with_id(call.message)
                case "no_use_last_receipt":
                    bot.delete_message(user_id, call.message.message_id)
                    bot.send_message(user_id, localize(user_id, "enter_receipt_id"))
                    bot.register_next_step_handler(call.message, _set_current_id_view)
                case _:
                    settings.logger_errors.error(f"Unknown callback data: {call.data}")

    def _choosing_language(message):
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton(text="🇬🇧 English", callback_data="en")
        btn2 = telebot.types.InlineKeyboardButton(text="🇺🇦 Державна", callback_data="uk")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "Choose language:", reply_markup=markup)

    def _main_menu(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton(text=localize(message.chat.id, "create_receipt"))
        btn2 = telebot.types.KeyboardButton(text=localize(message.chat.id, "view_debts"))
        btn3 = telebot.types.KeyboardButton(text=localize(message.chat.id, "view_receipt"))
        btn4 = telebot.types.KeyboardButton(text=localize(message.chat.id, "add_item"))
        btn5 = telebot.types.KeyboardButton(text=localize(message.chat.id, "join_receipt"))
        btn_language = telebot.types.KeyboardButton(text=localize(message.chat.id, "choose_language"))
        markup.add(btn1, btn2, btn3, btn4, btn5, btn_language)
        bot.send_message(message.chat.id, localize(message.chat.id, "main_menu"), reply_markup=markup)

    # CREATING NEW RECEIPT

    def _create_receipt(message):
        bot.send_message(message.chat.id, localize(message.chat.id, "enter_receipt_id"))
        bot.register_next_step_handler(message, _set_receipt_name)

    def _set_receipt_name(message):
        with open("database/users.json", "r+") as f:
            users = json.load(f)
        # creates new receipt with name from user and sets it as current receipt. Hacky :>
        users[str(message.chat.id)]["current_receipt"] = receipt.Receipt(message.text).id
        with open("database/users.json", "w+") as f:
            json.dump(users, f, indent=4)
        bot.send_message(message.chat.id, localize(message.chat.id, "receipt_created"))
        _main_menu(message)

    # VIEWING RECEIPT

    def _view_receipt(message):
        with open("database/users.json", "r+") as f:
            users = json.load(f)
        user_id = str(message.chat.id)
        if user_id in users:
            if users[user_id]["current_receipt"] is not None:
                btn1 = telebot.types.InlineKeyboardButton(text=localize(user_id, "yes"), callback_data="yes_use_last_receipt")
                btn2 = telebot.types.InlineKeyboardButton(text=localize(user_id, "no"), callback_data="no_use_last_receipt")
                markup = telebot.types.InlineKeyboardMarkup()
                bot.send_message(user_id, localize(user_id, "use_last_receipt"), reply_markup=markup.add(btn1, btn2))
            else:
                bot.send_message(user_id, localize(user_id, "enter_receipt_id"))
                bot.register_next_step_handler(message, _set_current_id_view)

    def _set_current_id_view(message):
        with open("database/users.json", "r+") as f:
            users = json.load(f)
        users[str(message.chat.id)]["current_receipt"] = message.text
        with open("database/users.json", "w+") as f:
            json.dump(users, f, indent=4)
        _view_receipt_with_id(message)

    def _view_receipt_with_id(message):
        user_id = message.chat.id
        with open("database/users.json", "r+") as f:
            users = json.load(f)
        if users[str(user_id)]["current_receipt"] is not None:
            receipt_id = users[str(user_id)]["current_receipt"]
            receipt_object = receipt.load_receipt(receipt_id)
            if receipt_object is not None:
                # if user_id not in receipt_object.users and user_id != settings.OWNER_ID:
                #     bot.send_message(user_id, localize(user_id, "user_not_in_receipt"))
                #     _main_menu(message)
                #     return
                bot.send_message(user_id, receipt_object.get_receipt_info())
                for item in receipt_object.items:
                    bot.send_message(user_id, item.get_item_info())
            else:
                bot.send_message(user_id, localize(user_id, "receipt_not_found"))
        else:
            bot.send_message(user_id, localize(user_id, "receipt_not_found"))
        _main_menu(message)

    # ADD USER TO RECEIPT

    def _set_current_id(message):
        with open("database/users.json", "r+") as f:
            users = json.load(f)
        users[str(message.chat.id)]["current_receipt"] = message.text
        with open("database/users.json", "w+") as f:
            json.dump(users, f, indent=4)
        _add_user_to_receipt(message, message.text)

    def _add_user_to_receipt(message, receipt_id: str):
        user_id = message.chat.id
        with open("database/receipts.json", "r+") as f:
            receipts = json.load(f)
        if receipt_id in receipts:
            if user_id not in receipts[receipt_id]["users"]:
                receipts[receipt_id]["users"].append(user_id)
                with open("database/receipts.json", "w+") as f:
                    json.dump(receipts, f, indent=4)
                bot.send_message(user_id, localize(user_id, "user_added_to_receipt"))
            else:
                bot.send_message(user_id, localize(user_id, "user_already_in_receipt"))
        else:
            raise ValueError(f"Receipt {receipt_id} not found in database")
        _main_menu(message)

    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        user_id = message.chat.id
        if message.text == localize(user_id, "create_receipt"):
            _create_receipt(message)
        elif message.text == localize(user_id, "join_receipt"):
            bot.send_message(user_id, localize(user_id, "enter_receipt_id"))
            bot.register_next_step_handler(message, _set_current_id)
        elif message.text == localize(user_id, "view_debts"):
            ...
        elif message.text == localize(user_id, "view_receipt"):
            _view_receipt(message)
        elif message.text == localize(user_id, "add_item"):
            ...
        elif message.text == localize(user_id, "choose_language"):
            _choosing_language(message)
        else: # If user sends something else, then we just send him main menu
            _main_menu(message)

    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    run()

