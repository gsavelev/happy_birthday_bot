import os

from dotenv import load_dotenv
from telebot import TeleBot

from ss.parser import Parser


# load .env
dotenv_path = os.path.join(os.path.dirname(__file__), 'creds/.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError('Did not find the environment file')

TOKEN = os.getenv('PG_TOKEN')
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['ping'])
def ping(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, '<b>PONG</b>\n' +
                         f'Chat id: {message.chat.id}', parse_mode='HTML')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    # TODO just for test
    p = Parser()
    birthday_guys = p.parse()
    for guy in birthday_guys:
        name = guy[0]
        tg = guy[1]
        bot.send_message(message.chat.id, f'{name} - {tg}')


if __name__ == '__main__':
    bot.infinity_polling()
