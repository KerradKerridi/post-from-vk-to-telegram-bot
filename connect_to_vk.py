import os
import sys
import vk_api
import configparser

# Настройки
config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
LOGIN = config.get('VK', 'LOGIN')
PASSWORD = config.get('VK', 'PASSWORD')
API_TOKEN = config.get('VK', 'TOKEN', fallback=None)

def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)

vk_session = vk_api.VkApi(LOGIN, PASSWORD, API_TOKEN, auth_handler=auth_handler, captcha_handler=captcha_handler)
# Получаем данные о посте пользователя из vk.com
def get_data(domain_vk, count_vk):
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        return

    vk = vk_session.get_api()
    # Используем метод wall.get из документации по API vk.com
    response_posts = vk.wall.get(domain=domain_vk, count=count_vk)
    return response_posts

# Получаем имя и фамилию пользователя из vk.com
def get_users(user_id):
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        return

    vk = vk_session.get_api()
    response_users = vk.users.get(user_ids=user_id)

    for post in response_users:
        first_name = post['first_name']
        last_name = post['last_name']
        fi_user = first_name + ' ' + last_name
        return fi_user