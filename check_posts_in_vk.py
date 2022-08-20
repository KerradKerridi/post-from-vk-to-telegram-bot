import os
import sys
import configparser
import connect_to_vk, send_in_telegram


# Проверяем данные по условиям перед отправкой
def check_posts_vk():
    # Настройки
    config_path = os.path.join(sys.path[0], 'settings.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    DOMAIN = config.get('VK', 'DOMAIN')
    COUNT = config.get('VK', 'COUNT')
    INCLUDE_LINK = config.getboolean('Settings', 'INCLUDE_LINK')

    response = connect_to_vk.get_data(DOMAIN, COUNT)
    response = reversed(response['items'])

    for post in response:
        # Читаем последний известный id из файла
        id = config.get('Settings', 'LAST_ID')

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
            author_name = connect_to_vk.get_users(author_id)
            link_user = f'https://vk.com/id{author_id}'
            text = f'Пост из ВК:\n{text}\n\nАвтор поста: {author_name}\nСсылка: {link_user}'
        else:
            text = f'Пост из ВК:\n{text}\n\nПост опубликован анонимно'

        # Проверяем наличие фото прикрепленных к посту (иных типов данных у меня нет, но там так же возможны видео, опросы и пр.)
        images = []
        links = []
        if 'attachments' in post:
            attach = post['attachments']
            for add in attach:
                if add['type'] == 'photo':
                    img = add['photo']
                    images.append(img)
                else:
                    continue

        if INCLUDE_LINK:
            post_url = "https://vk.com/" + DOMAIN + "?w=wall" + \
                str(post['owner_id']) + '_' + str(post['id'])
            links.insert(0, post_url)
            text = '\n'.join([text] + links)

        if len(images) > 0:
            image_massive_without_text = list(map(lambda img: max(
                img["sizes"], key=lambda size: size["type"])["url"], images))
            image_massive_with_text = send_in_telegram.post_images_with_text(image_massive_without_text, text)

            send_in_telegram.send_posts_in_tg(image_massive_with_text)
        else:
            send_in_telegram.send_message_in_tg(text)

        #Записываем id в файл
        #TODO: Раскоментировать, счетчик постов
        config.set('Settings', 'LAST_ID', str(post['id']))
        with open(config_path, "w") as config_file:
            config.write(config_file)
