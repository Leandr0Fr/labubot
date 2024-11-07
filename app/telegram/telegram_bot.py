import telebot
from requests.exceptions import ReadTimeout

from ..constants.constants import TELEGRAM_ID, TELEGRAM_KEY

bot = telebot.TeleBot(TELEGRAM_KEY)


def send_ofert(url_job: str, color: str) -> None:
    try:
        bot.send_message(
            TELEGRAM_ID,
            f"""Aquí tienes una oferta interesante {color} 
            {url_job}""",
        )
    except ReadTimeout:
        send_ofert(url_job, color)


def send_keyword(keyword: str) -> None:
    try:
        bot.send_message(TELEGRAM_ID, f"Ofertas de {keyword}")
    except ReadTimeout:
        send_keyword(keyword)
