import components.purchase as purchase
import components.receipt as receipt
import settings
import telebot
import components.debt_collector as debt_collector
from localization.localization import localize, add_user_to_database


# debt_collector.add_debts("evening", receipt.load_receipt("evening").calculate_each_user_debt())
# print(debt_collector.get_debts("john"))


def run():
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

    def _choosing_language(message):
        markup = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton(text="🇬🇧 English", callback_data="en")
        btn2 = telebot.types.InlineKeyboardButton(text="🇺🇦 Державна", callback_data="uk")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "Choose language:", reply_markup=markup)

    def _main_menu(message):
        markup = telebot.types.ReplyKeyboardMarkup()
        btn1 = telebot.types.KeyboardButton(text=localize(message.chat.id, "create_receipt"))
        btn2 = telebot.types.KeyboardButton(text=localize(message.chat.id, "view_debts"))
        btn3 = telebot.types.KeyboardButton(text=localize(message.chat.id, "view_receipt"))
        btn_language = telebot.types.KeyboardButton(text=localize(message.chat.id, "choose_language"))
        markup.add(btn1, btn2, btn3, btn_language)
        bot.send_message(message.chat.id, localize(message.chat.id, "main_menu"), reply_markup=markup)

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

    @bot.message_handler(commands=["create_receipt"])
    def _create_receipt(message):
        pass

    def _view_receipt(message):
        pass

    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        user_id = message.chat.id
        if message.text == localize(user_id, "create_receipt"):
            bot.send_message(user_id, localize(user_id, "enter_receipt_id"))
            bot.register_next_step_handler(message, _create_receipt)
        elif message.text == localize(user_id, "view_debts"):
            ...
        elif message.text == localize(user_id, "view_receipt"):
            try:
                bot.send_message(user_id, localize(user_id, "enter_receipt_id"))
                bot.register_next_step_handler(message, _view_receipt)
            except Exception as e:
                bot.send_message(user_id, localize(user_id, "receipt_not_found"))
        elif message.text == localize(user_id, "choose_language"):
            _choosing_language(message)
        else:
            _main_menu(message)

    bot.polling(none_stop=True, interval=0)
    pass


if __name__ == "__main__":
    run()
