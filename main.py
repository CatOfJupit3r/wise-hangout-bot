import json

import telebot
import settings
import commands as commands
from localization.localization import localize, add_user_to_database


def run():
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

    @bot.message_handler(commands=["start"])
    def start(message):
        settings.logger_general.info(f"User {message.chat.id} started the bot")
        with open("database/users.json", "r+") as f:
            users = json.load(f)
        user_id = str(message.chat.id)
        if user_id not in users:
            users[user_id] = {
                "current_receipt": None,
                "language": None,
                "nickname": None,
            }
            with open("database/users.json", "w+") as f:
                json.dump(users, f, indent=4)
            commands.choosing_language(message, bot)
        else:
            commands.main_menu(message, bot)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        user_id = str(call.message.chat.id)
        if call.message:
            if call.data == "en" or call.data == "uk":
                action = None
                callback_function_name = None
                language = call.data
            else:
                data = json.loads(call.data)
                action = data[0]
                callback_function_name = data[1]
                language = None
            if action is not None:
                match action:
                    case "yes":
                        settings.logger_general.info(f"User {user_id} chose \"Yes\" option")
                        bot.delete_message(user_id, call.message.message_id)
                        commands.yes_option(call.message, bot, commands.find_callback_function(callback_function_name))
                    case "no":
                        settings.logger_general.info(f"User {user_id} chose \"No\" option")
                        bot.delete_message(user_id, call.message.message_id)
                        commands.no_option(call.message, bot, commands.find_callback_function(callback_function_name))
                    case _:
                        settings.logger_errors.error(f"Unknown callback data: {call.data}")
            elif language is not None:
                match call.data:
                    case "en":
                        settings.logger_general.info(f"User {user_id} chose English language")
                        add_user_to_database(user_id, "en")
                        bot.send_message(user_id, localize(user_id, "welcome_message"))
                        bot.delete_message(user_id, call.message.message_id)
                        commands.choose_nickname(call.message, bot)
                    case "uk":
                        settings.logger_general.info(f"User {user_id} chose Ukrainian language")
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
        elif message.text == localize(user_id, "leave_receipt"):
            commands.leave_receipt(message, bot)
        elif message.text == localize(user_id, "delete_my_data"):
            commands.delete_user(message, bot)
        elif message.text == localize(user_id, "choose_language"):
            settings.logger_general.info(f"User {message.chat.id} chose to change language")
            commands.choosing_language(message, bot)
        else:  # If user sends something else, then we just send him main menu
            settings.logger_general.info(f"User {message.chat.id} sent unknown message: {message.text}")
            commands.main_menu(message, bot)
    while(True):
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            continue


if __name__ == "__main__":
    run()
