import os
import sys
import telebot
import configparser
from telebot.types import InputMediaPhoto


# Считываем настройки
config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
CHANNEL = config.get('Telegram', 'CHANNEL')
PREVIEW_LINK = config.getboolean('Settings', 'PREVIEW_LINK')

# Инициализируем телеграмм бота
bot = telebot.TeleBot(BOT_TOKEN)

#Функция отправки поста с вложенными фото
def send_posts_in_tg(img):
    global bot
    global CHANNEL
    pass
    bot.send_media_group(chat_id=CHANNEL, media=img)


#Отправка только текстовых постов
def send_message_in_tg(text):
    global bot
    global CHANNEL
    global PREVIEW_LINK
    # функция отправки текста
    if len(text) > 4096:
        # В телеграмме есть ограничения на длину одного сообщения в 4091 символ, разбиваем длинные сообщения на части
        for msg in split(text):
            bot.send_message(CHANNEL, msg, disable_web_page_preview=not PREVIEW_LINK, parse_mode='MarkdownV2')
    else:
        bot.send_message(CHANNEL, text, disable_web_page_preview=not PREVIEW_LINK)

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


#Преобразование фото к объектам MediaPhoto. Ограничение по тексту прикрепляемому к фото 1024 символа.
def post_images_with_text(img, text):
    img_new = []
    if len(img) == 1 and len(text) < 1024:
        img_new = [InputMediaPhoto(img[0], caption=text)]
    elif len(img) > 1 and len(text) < 1024:
        for i in range(1, len(img)):
            if i + 1 < len(img):
                img_new.append(InputMediaPhoto(img[i]))
            else:
                img_new.append(InputMediaPhoto(img[i], caption=text))
    else:
        pass
    return img_new

