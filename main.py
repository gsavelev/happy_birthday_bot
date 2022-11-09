import os
import time

import schedule
from dotenv import load_dotenv
from telebot import TeleBot

from ss.parser import Parser
from wishes.wish_maker import WishMaker


# load .env
dotenv_path = os.path.join(os.path.dirname(__file__), 'creds/.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError('Did not find the environment file')

TOKEN = os.getenv('TOKEN')
bot = TeleBot(TOKEN)


def job():
    parser = Parser()
    birthday_guys = parser.parse()
    wish_maker = WishMaker()
    wish = wish_maker.make_wish(birthday_guys)
    target_chat_id = os.getenv('TARGET_CHAT')
    if wish:
        bot.send_message(target_chat_id, wish)


@bot.message_handler(commands=['ping'])
def ping(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, '<b>PONG</b>\n' +
                         f'Chat id: {message.chat.id}', parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start(message):
    if len(schedule.jobs) == 0:
        if message.chat.type == 'private':
            if message.chat.id == int(os.getenv('ADMIN')):
                greeting = '🫡'
                report = 'Включил поздравлялку'
                bot.send_message(message.chat.id, greeting)
                time.sleep(1)
                bot.send_message(message.chat.id, report)
                schedule.every().day.at('10:00').do(job)
                while True:
                    schedule.run_pending()
                    if not schedule.jobs:
                        break
                    time.sleep(1)
            else:
                msg = 'Сори, я подчиняюсь только админу!\nСпроси во флуде, кто админ.'
                bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['stop'])
def stop(message):
    if len(schedule.jobs) > 0:  # any work exists
        if message.chat.type == 'private':
            if message.chat.id == int(os.getenv('ADMIN')):
                greeting = '🫡'
                report = 'Выключил поздравлялку'
                bot.send_message(message.chat.id, greeting)
                time.sleep(1)
                bot.send_message(message.chat.id, report)
                schedule.cancel_job(schedule.jobs[0])
            else:
                msg = 'Сори, я подчиняюсь только админу!\nСпроси во флуде, кто админ.'
                bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['help'])
def help(message):
    if message.chat.type == 'private'\
            and message.chat.id == int(os.getenv('ADMIN')):
        guide = 'Чтобы завести поздравлялку скомандуй /start'
        bot.send_message(message.chat.id, guide)


if __name__ == '__main__':
    bot.infinity_polling()
