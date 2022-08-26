import os
import sys
import configparser
import time
import telebot

config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
GROUP_FOR_POST = config.get('Settings', 'group_for_posts')
KILL_CHANEL = config.get('Telegram', 'kill_channel')
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
IMPORTANT_LOGS = config.get('Settings', 'important_logs')
GROUP_FOR_LOGS = config.get('Settings', 'group_for_logs')
CHANNEL = config.get('Telegram', 'CHANNEL')

bot = telebot.TeleBot(BOT_TOKEN)

def telegram_bot():

    
    @bot.callback_query_handler(func=lambda call: True)
    def post_for_group(call):
        if call.data == 'post_post_post' and call.message.content_type == 'text':
            try:
                bot.send_message(chat_id=CHANNEL, text=call.message.text)
                bot.delete_message(chat_id=GROUP_FOR_POST, message_id=call.message.message_id)
            except:
                bot.send_message(chat_id=GROUP_FOR_LOGS, text='Не удалось выложить/удалить текстовый пост, что-то пошло не так')
        elif call.data == 'post_post_post' and call.message.content_type == 'photo':
            try:
                bot.send_photo(
                    chat_id=CHANNEL,
                    caption=call.message.caption,
                    photo=call.message.photo[-1].file_id,
                )
                bot.delete_message(chat_id=GROUP_FOR_POST, message_id=call.message.message_id)
            except:
                bot.send_message(chat_id=GROUP_FOR_LOGS, text='Не удалось выложить/удалить пост с фотографией, что-то пошло не так')
        elif call.data == 'decline':
            try:
                bot.delete_message(chat_id=GROUP_FOR_POST, message_id=call.message.message_id)
            except:
                bot.send_message(chat_id=GROUP_FOR_LOGS, text='Не удалось отклонить пост')

if __name__ == '__main__':
    telegram_bot()
    try:
        bot.polling(none_stop=True)
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
    except ConnectionError as e:
        print('Ошибка соединения: ', e)
        bot.send_message(IMPORTANT_LOGS, "Обслуживающий ошибка соединения, потерял связь")
    except Exception as r:
        print("Непредвиденная ошибка: ", r)
        bot.send_message(IMPORTANT_LOGS, "Обслуживающий произошло что-то непредвиденное, хелп")
    finally:
        print("Здесь всё закончилось")
        bot.send_message(IMPORTANT_LOGS, 'Обслуживающий, Я упал, помогите')