import json

import telebot
from localization.localization import localize
import settings


def update_current_receipt_id(user_id: str, receipt_id: str):
    with open("database/users.json", "r+") as f:
        users = json.load(f)
    users[str(user_id)]["current_receipt"] = receipt_id
    with open("database/users.json", "w+") as f:
        json.dump(users, f, indent=4)


def send_message_and_wait(bot: telebot.TeleBot, message, text_to_send: str, next_step_handler: callable, *args):
    bot.send_message(message.chat.id, text_to_send)
    settings.logger_general.info(f"User {message.chat.id} has been sent message {text_to_send}. Waiting for response...")
    bot.register_next_step_handler(message, next_step_handler, bot, *args)


def main_menu(message, bot):
    button_labels = [
        "join_receipt",
        "find_whom_to_pay",
        "view_receipt",
        "create_receipt",
        "add_item",
        "add_payment",
        "view_debts",
        "leave_receipt",
        "delete_my_data",
        "choose_language"
    ]
    keyboard_buttons = [
        telebot.types.KeyboardButton(text=localize(message.chat.id, label))
        for label in button_labels
    ]
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*keyboard_buttons)
    bot.send_message(message.chat.id, localize(message.chat.id, "main_menu"), reply_markup=markup)


def choosing_language(message, bot: telebot.TeleBot):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton(text="🇬🇧 English", callback_data="en")
    btn2 = telebot.types.InlineKeyboardButton(text="🇺🇦 Державна", callback_data="uk")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Choose language/Оберіть мову:", reply_markup=markup)


def choose_nickname(message, bot: telebot.TeleBot):
    send_message_and_wait(bot, message, localize(message.chat.id, "enter_nickname"), _set_nickname)


def _set_nickname(message, bot: telebot.TeleBot):
    with open("database/users.json", "r+") as f:
        users = json.load(f)
    users[str(message.chat.id)]["nickname"] = message.text
    with open("database/users.json", "w+") as f:
        json.dump(users, f, indent=4)
    settings.logger_general.info(f"User {message.chat.id} set nickname {message.text}")
    main_menu(message, bot)


def check_for_receipt_id(message, bot: telebot.TeleBot, callback_function):
    user_id = str(message.chat.id)
    with open("database/users.json", "r+") as f:
        users = json.load(f)
    if users[user_id]["current_receipt"] is not None:
        settings.logger_general.info(f"User {user_id} has current receipt {users[user_id]['current_receipt']}. Asking to use it...")
        yes_or_no_choice(message, bot, callback_function)
    else:
        settings.logger_general.info(f"User {user_id} has no current receipt. Asking to enter receipt id...")
        send_message_and_wait(bot, message, localize(message.chat.id, "enter_receipt_id"), callback_function)


def yes_or_no_choice(message, bot, callback_function):
    btn1 = telebot.types.InlineKeyboardButton(
        text=localize(message.chat.id, "yes"),
        callback_data=json.dumps(("yes", callback_function.__name__))
    )
    btn2 = telebot.types.InlineKeyboardButton(
        text=localize(message.chat.id, "no"),
        callback_data=json.dumps(("no", callback_function.__name__))
    )
    markup = telebot.types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, localize(message.chat.id, "use_last_receipt"), reply_markup=markup.add(btn1, btn2))


def find_callback_function(callback_function_name):
    for module_name in ["view_receipt", "add_item", "add_payment", "find_whom_to_pay", "leave_receipt"]:
        module = __import__(f"commands.{module_name}", fromlist=[callback_function_name])
        if hasattr(module, callback_function_name):
            return getattr(module, callback_function_name)
    raise AttributeError(f"Callback function {callback_function_name} not found")


def yes_option(message, bot, callback_function):
    with open("database/users.json", "r+") as f:
        users = json.load(f)
    message.text = str(users[str(message.chat.id)]["current_receipt"])
    callback_function(message, bot)


def no_option(message, bot, callback_function):
    send_message_and_wait(bot, message, localize(message.chat.id, "enter_receipt_id"), callback_function)
