import os
import telegram

from settings.logging import get_logger

logger = get_logger(__name__)

async def send_message(message: str):
    bot = telegram.Bot(os.getenv("TELEGRAM_TOKEN"))
    await bot.send_message(
        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        text=message
    )

    logger.info("Message has been sent")