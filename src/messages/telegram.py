import logging

from pathlib import Path

import settings
import telegram

from logging.config import fileConfig

cfg = Path("/src/logs/logging_config.ini")
if cfg.exists():
    fileConfig(cfg)
logger = logging.getLogger()


async def send_message(message: str):
    bot = telegram.Bot(settings.TELEGRAM_TOKEN)
    await bot.send_message(
        chat_id=settings.TELEGRAM_CHAT_ID,
        text=message
    )
