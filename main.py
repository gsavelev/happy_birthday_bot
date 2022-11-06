import os

from dotenv import load_dotenv
from telebot import TeleBot


# load .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError("Did not find the environment file")

TOKEN = os.getenv("TOKEN")

bot = TeleBot(TOKEN)

if __name__ == "__main__":
    bot.infinity_polling()
