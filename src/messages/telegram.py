import logging
import settings
import telegram

from logging.config import fileConfig

fileConfig('logs/logging_config.ini')
logger = logging.getLogger()


def send_message(message: str):
    bot = telegram.Bot(settings.TELEGRAM_TOKEN)
    # Make a photo to send it
    with open('./last_sighting.jpg', 'rb') as photo:
        bot.send_photo(
            chat_id=settings.TELEGRAM_CHAT_ID,
            photo=photo,
            caption=message,
            filename='last_sighting.jpg'
        )
