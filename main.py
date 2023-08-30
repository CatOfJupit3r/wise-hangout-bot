import json

import telebot
import settings
import commands as commands
from localization.localization import localize, add_user_to_database


def run():
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

    @bot.message_handler(commands=["start"])
    def start(message):
        with open("database/users.json", "r+") as f:
            users = json.load(f)
        user_id = str(message.chat.id)
        if user_id not in users:
            users[user_id] = {
                "current_receipt": None,
                "language": None,
                "nickname": None,
                "last_receipt": None
            }
            with open("database/users.json", "w+") as f:
                json.dump(users, f, indent=4)
            commands.choosing_language(message, bot)
        else:
            commands.main_menu(message, bot)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        user_id = call.message.chat.id
        if call.message:
            data = json.loads(call.data)
            if data[0] == "yes" or data[0] == "no":
                action = data[0]
                callback_function_name = data[1]
                args = data[2:]
                language = None
            elif data[0] == "en" or data[0] == "uk":
                action = None
                callback_function_name = None
                args = None
                language = data[0]
            else:
                settings.logger_errors.error(f"Unknown callback data: {call.data}")
                return
            if action is not None:
                match action:
                    case "yes":
                        bot.delete_message(user_id, call.message.message_id)
                        try:
                            commands.yes_option(call.message, bot, commands.find_callback_function(callback_function_name), *args)
                        except IndexError:
                            commands.yes_option(call.message, bot, commands.find_callback_function(callback_function_name))
                    case "no":
                        bot.delete_message(user_id, call.message.message_id)
                        try:
                            commands.no_option(call.message, bot, commands.find_callback_function(callback_function_name), *args)
                        except IndexError:
                            commands.no_option(call.message, bot, commands.find_callback_function(callback_function_name))
                    case _:
                        settings.logger_errors.error(f"Unknown callback data: {call.data}")
            elif language is not None:
                match call.data:
                    case "en":
                        add_user_to_database(user_id, "en")
                        bot.send_message(user_id, localize(user_id, "welcome_message"))
                        bot.delete_message(user_id, call.message.message_id)
                        commands.choose_nickname(call.message, bot)
                    case "uk":
                        add_user_to_database(user_id, "uk")
                        bot.send_message(user_id, localize(user_id, "welcome_message"))
                        bot.delete_message(user_id, call.message.message_id)
                        commands.choose_nickname(call.message, bot)
                    case _:
                        settings.logger_errors.error(f"Unknown callback data: {call.data}")

    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        user_id = str(message.chat.id)
        if message.text == localize(user_id, "create_receipt"):
            commands.create_receipt(message, bot)
        elif message.text == localize(user_id, "join_receipt"):
            commands.join_receipt(message, bot)
        elif message.text == localize(user_id, "view_debts"):
            commands.view_debts(message, bot)
        elif message.text == localize(user_id, "view_receipt"):
            commands.view_receipt(message, bot)
        elif message.text == localize(user_id, "add_item"):
            commands.add_item(message, bot)
        elif message.text == localize(user_id, "add_payment"):
            commands.add_payment(message, bot)
        elif message.text == localize(user_id, "find_whom_to_pay"):
            commands.find_whom_to_pay(message, bot)
        elif message.text == localize(user_id, "choose_language"):
            commands.choosing_language(message, bot)
        else:  # If user sends something else, then we just send him main menu
            commands.main_menu(message, bot)

    bot.polling(non_stop=True, interval=0, timeout=None)


if __name__ == "__main__":
    run()
