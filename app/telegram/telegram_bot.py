import telebot

from ..constants.constants import TELEGRAM_ID, TELEGRAM_KEY


def send_ofert(url_job: str, color: str) -> None:
    bot = telebot.TeleBot(TELEGRAM_KEY)
    bot.send_message(
        TELEGRAM_ID,
        f"""Aquí tienes una oferta interesante {color}
{url_job}""",
    )
