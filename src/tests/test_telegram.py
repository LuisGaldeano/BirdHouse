import os
import unittest
from unittest.mock import AsyncMock, MagicMock, patch


class SendMessageTest(unittest.IsolatedAsyncioTestCase):
    async def test_send_message_envia_texto_con_chat_id(self):
        os.environ["TELEGRAM_TOKEN"] = "TEST_TOKEN"
        os.environ["TELEGRAM_CHAT_ID"] = "123456"

        from messages.telegram import send_message  # ajusta si tu path es otro

        fake_bot = MagicMock()
        fake_bot.send_message = AsyncMock()

        with patch("messages.telegram.logger") as logger_mock:
            await send_message("hola", bot=fake_bot)

            fake_bot.send_message.assert_awaited_once_with(
                chat_id="123456",
                text="hola",
            )
            logger_mock.info.assert_called_once_with("Message has been sent")

    async def test_send_message_sin_chat_id_lanza_runtimeerror(self):
        os.environ["TELEGRAM_TOKEN"] = "TEST_TOKEN"
        os.environ.pop("TELEGRAM_CHAT_ID", None)

        from messages.telegram import send_message

        fake_bot = MagicMock()
        fake_bot.send_message = AsyncMock()

        with self.assertRaises(RuntimeError) as ctx:
            await send_message("hola", bot=fake_bot)

        self.assertIn("TELEGRAM_CHAT_ID is not set", str(ctx.exception))
        fake_bot.send_message.assert_not_called()

    async def test_send_message_sin_token_lanza_runtimeerror(self):
        os.environ.pop("TELEGRAM_TOKEN", None)
        os.environ["TELEGRAM_CHAT_ID"] = "123456"

        from messages.telegram import send_message

        fake_bot = MagicMock()
        fake_bot.send_message = AsyncMock()

        with self.assertRaises(RuntimeError) as ctx:
            await send_message("hola", bot=fake_bot)

        self.assertIn("TELEGRAM_TOKEN is not set", str(ctx.exception))
        fake_bot.send_message.assert_not_called()

    async def test_send_message_si_no_se_inyecta_bot_crea_bot_con_token(self):
        os.environ["TELEGRAM_TOKEN"] = "TEST_TOKEN"
        os.environ["TELEGRAM_CHAT_ID"] = "123456"

        from messages.telegram import send_message

        fake_bot = MagicMock()
        fake_bot.send_message = AsyncMock()

        with patch("messages.telegram.get_bot", return_value=fake_bot) as get_bot_mock:
            await send_message("hola")  # sin bot inyectado

            get_bot_mock.assert_called_once_with("TEST_TOKEN")
            fake_bot.send_message.assert_awaited_once_with(
                chat_id="123456",
                text="hola",
            )
