import os
import sys
import telebot
import configparser
from telebot.types import InputMediaPhoto
from telebot import types

# Считываем настройки
config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
CHANNEL = config.get('Telegram', 'CHANNEL')
PREVIEW_LINK = config.getboolean('Settings', 'PREVIEW_LINK')
GROUP_FOR_POST = config.get('Settings', 'group_for_posts')
IMPORTANT_LOGS = config.get('Settings', 'important_logs')

# Инициализируем телеграмм бота
bot = telebot.TeleBot(BOT_TOKEN)

#Функция отправки поста с вложенным фото
def send_posts_in_tg(img, text):
    global bot
    global GROUP_FOR_POST
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Опубликовать", callback_data='post_post_post')
    item2 = types.InlineKeyboardButton("Отклонить", callback_data='decline')
    markup.add(item1, item2)
    try:
        bot.send_photo(chat_id=GROUP_FOR_POST, photo=img, reply_markup=markup, caption=text)
    except:
        bot.send_message(chat_id=IMPORTANT_LOGS, text='Не удалось вытащить пост с вк')


#Отправка только текстовых постов
def send_message_in_tg(text):
    global bot
    global GROUP_FOR_POST
    global PREVIEW_LINK
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Опубликовать", callback_data='post_post_post')
    item2 = types.InlineKeyboardButton("Отклонить", callback_data='decline')
    markup.add(item1, item2)
    # функция отправки текста
    if len(text) > 4096:
        # В телеграмме есть ограничения на длину одного сообщения в 4091 символ, разбиваем длинные сообщения на части
        for msg in split(text):
            bot.send_message(GROUP_FOR_POST, msg, disable_web_page_preview=not PREVIEW_LINK, parse_mode='MarkdownV2', reply_markup=markup)
    else:
        bot.send_message(GROUP_FOR_POST, text, disable_web_page_preview=not PREVIEW_LINK, reply_markup=markup)

def split(text):
    message_breakers = [':', ' ', '\n']
    max_message_length = 4091

    if len(text) >= max_message_length:
        last_index = max(
            map(lambda separator: text.rfind(separator, 0, max_message_length), message_breakers))
        good_part = text[:last_index]
        bad_part = text[last_index + 1:]
        return [good_part] + split(bad_part)
    else:
        return [text]

def resend_in_group_for_post_text(text, type):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Опубликовать", callback_data='post_post_post')
    item2 = types.InlineKeyboardButton("Отклонить", callback_data='decline')
    markup.add(item1, item2)
    try:
        bot.send_message(
            # TODO: GROUP_FOR_POST
            chat_id=GROUP_FOR_POST,
            text=f'Пост из ТГ:\n{text}\n\nПост опубликован анонимно',
            reply_markup=markup
        )
    except:
        bot.send_message(IMPORTANT_LOGS,
                         f'ALARM, Не удалось выгрузить пост\n\nИсточник: {type}\n')

def send_logs(text):
    global bot
    global IMPORTANT_LOGS
    global PREVIEW_LINK
    # функция отправки текста
    bot.send_message(IMPORTANT_LOGS, text, disable_web_page_preview=not PREVIEW_LINK, reply_markup=markup)
        