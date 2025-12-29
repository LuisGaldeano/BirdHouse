# -*- coding: utf-8 -*-
import os
from typing import Optional

from telegram import Bot
from settings.logging import get_logger

logger = get_logger(__name__)

def get_telegram_config() -> tuple[str, str]:
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not token:
        raise RuntimeError('TELEGRAM_TOKEN is not set')
    if not chat_id:
        raise RuntimeError('TELEGRAM_CHAT_ID is not set')

    return token, chat_id


def get_bot(token: str) -> Bot:
    return Bot(token=token)

async def send_message(message: str, bot: Optional[Bot] = None) -> None:
    token, chat_id = get_telegram_config()
    bot = bot or get_bot(token)

    await bot.send_message(chat_id=chat_id, text=message)

    logger.info('Message has been sent')


async def send_image(image_path: str, caption: str | None = None, bot: Optional[Bot] = None) -> None:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    token, chat_id = get_telegram_config()
    bot = bot or get_bot(token)

    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
        )

    logger.info('Image has been sent')
