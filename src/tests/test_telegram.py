# -*- coding: utf-8 -*-
import os
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from messages.telegram import send_message


class SendMessageTest(unittest.IsolatedAsyncioTestCase):
    async def test_send_message_sends_text(self):
        os.environ['TELEGRAM_TOKEN'] = 'TEST_TOKEN'
        os.environ['TELEGRAM_CHAT_ID'] = '123456'

        fake_bot = MagicMock()
        fake_bot.send_message = AsyncMock()

        with patch('messages.telegram.logger') as logger_mock:
            await send_message('hola', bot=fake_bot)

            fake_bot.send_message.assert_awaited_once_with(
                chat_id='123456',
                text='hola',
            )
            logger_mock.info.assert_called_once_with('Message has been sent')

    async def test_send_message_no_chat_id_error(self):
        os.environ['TELEGRAM_TOKEN'] = 'TEST_TOKEN'
        os.environ.pop('TELEGRAM_CHAT_ID', None)

        fake_bot = MagicMock()
        fake_bot.send_message = AsyncMock()

        with self.assertRaises(RuntimeError) as ctx:
            await send_message('hola', bot=fake_bot)

        self.assertIn('TELEGRAM_CHAT_ID is not set', str(ctx.exception))
        fake_bot.send_message.assert_not_called()

    async def test_send_message_no_token_error(self):
        os.environ.pop('TELEGRAM_TOKEN', None)
        os.environ['TELEGRAM_CHAT_ID'] = '123456'

        fake_bot = MagicMock()
        fake_bot.send_message = AsyncMock()

        with self.assertRaises(RuntimeError) as ctx:
            await send_message('hola', bot=fake_bot)

        self.assertIn('TELEGRAM_TOKEN is not set', str(ctx.exception))
        fake_bot.send_message.assert_not_called()

    async def test_send_message_creates_bot_if_missing(self):
        os.environ['TELEGRAM_TOKEN'] = 'TEST_TOKEN'
        os.environ['TELEGRAM_CHAT_ID'] = '123456'

        fake_bot = MagicMock()
        fake_bot.send_message = AsyncMock()

        with patch('messages.telegram.get_bot', return_value=fake_bot) as get_bot_mock:
            await send_message('hola')

            get_bot_mock.assert_called_once_with('TEST_TOKEN')
            fake_bot.send_message.assert_awaited_once_with(
                chat_id='123456',
                text='hola',
            )
