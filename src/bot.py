import telegram
from src.config import TELE_GROUP_ID


class Bot:
    def __init__(self, token):
        self.bot = telegram.Bot(token=token)

    def send(self, text):
        self.bot.sendMessage(chat_id=TELE_GROUP_ID, text=text, timeout=50)
