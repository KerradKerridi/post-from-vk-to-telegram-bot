import os
import sys
import configparser
import time
import connect_to_vk, send_in_telegram


config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
BSK_LOVA = config.get('VK', 'bsk_lova')
SEE_YOU = config.get('VK', 'see_you')
last_id_for_bsk_lova = config.get('Settings', 'last_id_for_bsk_lova')
last_id_for_see_you = config.get('Settings', 'last_id_for_see_you')
COUNT = config.get('VK', 'COUNT')
INCLUDE_LINK = config.getboolean('Settings', 'INCLUDE_LINK')


# Проверяем данные по условиям перед отправкой
def check_posts_vk():
    response_from_lova_bsk = connect_to_vk.get_data(BSK_LOVA, COUNT)
    response_from_lova_bsk = reversed(response_from_lova_bsk['items'])
    something_function(response_from_lova_bsk, 'lova_bsk')
    time.sleep(1)
    response_from_see_you = connect_to_vk.get_data(SEE_YOU, COUNT)
    response_from_see_you = reversed(response_from_see_you['items'])
    something_function(response_from_see_you, 'see_you')

def something_function(response, type):
    for post in response:
        # Читаем последний известный id из файла
        if type == 'lova_bsk':
            id = last_id_for_bsk_lova
        else:
            id = last_id_for_see_you
        # Сравниваем id, пропускаем уже опубликованные
        if int(post['id']) <= int(id):
            continue

        # Текст
        text = post['text']

        # Автор
        try:
            author_id = post['signer_id']
        except KeyError:
            author_id = ''

        if author_id != '':
            continue
        else:
            pass

        # Проверяем наличие фото прикрепленных к посту (иных типов данных у меня нет, но там так же возможны видео, опросы и пр.)
        images = []
        if 'attachments' in post:
            attach = post['attachments']
            for add in attach:
                if add['type'] == 'photo':
                    img = add['photo']
                    images.append(img)
                else:
                    continue

        if not images:
            send_in_telegram.resend_in_group_for_post_text(text, type)
        else:
            pass


        #Записываем id в файл
        #TODO: Раскоментировать, счетчик постов
        if type == 'lova_bsk':
            config.set('Settings', 'last_id_for_bsk_lova', str(post['id']))
        else:
            config.set('Settings', 'last_id_for_see_you', str(post['id']))
        with open(config_path, "w") as config_file:
            config.write(config_file)
            

