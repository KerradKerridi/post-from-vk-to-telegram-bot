import os
import sys
import configparser
import time

import vk_api
import connect_to_vk
import check_post_in_other_vk
from datetime import datetime
import telebot

# Настройки
config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
LOGIN = config.get('VK', 'LOGIN')
PASSWORD = config.get('VK', 'PASSWORD')
API_TOKEN = config.get('VK', 'TOKEN', fallback=None)
KILL = config.get('VK', 'kill')
COUNT_FOR_KILL = config.get('VK', 'count_for_kill')
INCLUDE_LINK_FOR_KILL = config.get('Settings', 'include_link_for_kill')
vk_session = vk_api.VkApi(LOGIN, PASSWORD, API_TOKEN, auth_handler=connect_to_vk.auth_handler, captcha_handler=connect_to_vk.captcha_handler)
DOMAIN = config.get('VK', 'DOMAIN')
KILL_CHANEL = config.get('Telegram', 'kill_channel')
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
PREVIEW_LINK = config.getboolean('Settings', 'PREVIEW_LINK')
IMPORTANT_LOGS = config.get('Settings', 'important_logs')
GROUP_FOR_LOGS = config.get('Settings', 'group_for_logs')

# Инициализируем телеграмм бота
bot = telebot.TeleBot(BOT_TOKEN)

def get_data_from_vk(domain_vk, count_vk):
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        return

    vk = vk_session.get_api()
    # Используем метод wall.get из документации по API vk.com
    response_posts = vk.wall.get(domain=domain_vk, count=count_vk)
    return response_posts

# Проверяем данные по условиям перед отправкой
def check_posts_enemy_vk():
    response = connect_to_vk.get_data(KILL, COUNT_FOR_KILL)
    response = reversed(response['items'])
    text_massive = []
    links_massive = []
    date_for_enemy_post = []
    for post in response:
        # Текст
        text = post['text']
        text_massive.append(text)
        date = datetime.fromtimestamp(post['date'])
        date_for_enemy_post.append(date)
        links = []
        if INCLUDE_LINK_FOR_KILL:
            post_url = "https://vk.com/" + KILL + "?w=wall" + \
                str(post['owner_id']) + '_' + str(post['id'])
            links.insert(0, post_url)
        links_massive.append(links)

    matching(text_massive, links_massive, date_for_enemy_post)

    
def matching(text, links, date_for_enemy_post):
    my_posts, links_from_my_post, date_for_my_post = check_posts_vk_in_my_publ()
    match = []
    for i in my_posts:
        for j in text:
            if i == j and j:
                match.append(j)
                break
    for i in range(0, len(match)):
        index = text.index(match[i])
        index_my = my_posts.index(match[i])
        f = f'Текст поста: {match[i]}\nСсылка на пост в его канале:{links[index]}\nВремя публикации в его канале: {date_for_enemy_post[index]}\n' \
            f'Ссылка на пост в моем канале: {links_from_my_post[index_my]}\nВремя публикации в моем канале:{date_for_my_post[index_my]}'
        send_message_in_tg_for_kill(f)


def check_posts_vk_in_my_publ():
    response = connect_to_vk.get_data(DOMAIN, COUNT_FOR_KILL)
    response = reversed(response['items'])
    text_massive = []
    links = []
    date_for_my_post = []
    for post in response:
        # Текст
        text = post['text']
        date = datetime.fromtimestamp(post['date'])
        date_for_my_post.append(date)
        text_massive.append(text)
        post_url = "https://vk.com/" + DOMAIN + "?w=wall" + \
            str(post['owner_id']) + '_' + str(post['id'])
        links.append(post_url)
    return text_massive, links, date_for_my_post

def send_message_in_tg_for_kill(text):
    global bot
    global KILL_CHANEL
    global PREVIEW_LINK
    # функция отправки текста
    if len(text) > 4096:
        # В телеграмме есть ограничения на длину одного сообщения в 4091 символ, разбиваем длинные сообщения на части
        for msg in split(text):
            bot.send_message(KILL_CHANEL, msg, disable_web_page_preview=not PREVIEW_LINK, parse_mode='MarkdownV2')
    else:
        bot.send_message(KILL_CHANEL, text, disable_web_page_preview=not PREVIEW_LINK)


if __name__ == '__main__':
    check_posts_enemy_vk()
    check_post_in_other_vk.check_posts_vk()

