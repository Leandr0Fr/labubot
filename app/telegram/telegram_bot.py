import telebot

from ..constants.constants import TELEGRAM_ID, TELEGRAM_KEY


def send_offers(offers) -> None:
    bot = telebot.TeleBot(TELEGRAM_KEY)
    try:
        bot.send_message(
            TELEGRAM_ID,
            offers,
        )
    except Exception:
        send_offers(offers)


def send_keyword(keyword: str) -> None:
    bot = telebot.TeleBot(TELEGRAM_KEY)
    try:
        bot.send_message(TELEGRAM_ID, f"Ofertas de {keyword}")
    except Exception:
        send_keyword(keyword)
