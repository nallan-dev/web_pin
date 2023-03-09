from copy import deepcopy

import telebot
from telebot.types import CallbackQuery, Message

from conf import settings
from conf.translations import t
from library.clients import switch_data
from library.loggers import get_logger
from library.repository import AppData, get_app_data
from tbot.helpers import KeyboardData

logger = get_logger("TelegramBot")

CHANGE_STATE_URL = f"http://localhost:{settings.WEB_APP_PORT}/"
APP_DATA: AppData = get_app_data()
bot = telebot.TeleBot(APP_DATA.bot_data.telegram_token, threaded=False)


@bot.callback_query_handler(func=lambda _: True)
def callback_query_handler(callback_message: CallbackQuery):
    success_message = "✅"
    is_keyboard_changed_by_request = False
    app_data_before = deepcopy(APP_DATA)
    if KeyboardData.KEY_SEP in callback_message.data:
        # switch pin/schedule & refresh keyboard
        pk_api_name, pk, state = KeyboardData.decode_from_callback_msg(
            callback_message.data
        )
        ret_code = switch_data(pk_api_name, int(pk), int(state), logger)
        if not ret_code:  # ok
            APP_DATA.update()
            is_keyboard_changed_by_request = True
    elif callback_message.data == "refresh":
        APP_DATA.update()  # refresh keyboard only
    # telegram raises error when you send keyboard without changes
    if app_data_before != APP_DATA:
        keyboard_data = KeyboardData.get_from_app_data(APP_DATA)
        if is_keyboard_changed_by_request:
            row_msg = keyboard_data.form_pushed_button_text(
                pk_api_name, pk  # noqa
            )
            success_message = f"{success_message}  {row_msg}"
        bot.edit_message_reply_markup(
            chat_id=callback_message.message.chat.id,
            message_id=callback_message.message.id,
            reply_markup=keyboard_data.form_keyboard(),
        )
    bot.answer_callback_query(
        callback_query_id=callback_message.id,
        text=success_message,
        show_alert=True,
    )


@bot.message_handler(func=lambda _: True)
def message_handler(message: Message):
    APP_DATA.update()
    if message.chat.id not in APP_DATA.bot_data.allowed_clients:
        bot.send_message(message.chat.id, f"ACCESS DENIED - {message.chat.id}")
    keyboard_data = KeyboardData.get_from_app_data(APP_DATA)
    bot.send_message(
        message.chat.id,
        t("Switchers"),
        reply_markup=keyboard_data.form_keyboard(),
    )


def run_bot():
    logger.info("Start bot")
    bot.infinity_polling()


if __name__ == "__main__":
    run_bot()
