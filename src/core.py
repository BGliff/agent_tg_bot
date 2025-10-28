import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.exceptions import AiogramError, TelegramBadRequest

from agent.agent import agent_main
from config import BOT_CONFIG


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\n\n"
        f"Я - бот, который может, используя точные встроенные методы, получить данные о погоде, "
        f"рассказать о компании, если ты предоставишь мне ссылку на ее страницу в интернете, "
        f"сложить или умножить два числа.\n\n"
        f"Если это все тебя не интересует, можешь задать мне любой вопрос, "
        f"который можно задать энциклопедии"
    )


@dp.message()
async def query_handler(message: Message) -> None:

    if not isinstance(message.text, str):
        await message.answer("Я могу обрабатывать только текстовые запросы")
        return None
    tmp_message = await message.answer("...")
    answer = await agent_main(message.text)
    try:
        await tmp_message.delete()
    except AiogramError:
        pass
    try:
        await message.answer(answer)
    except TelegramBadRequest:
        await message.answer("Не удалось получить данные")


async def main() -> None:
    bot = Bot(token=BOT_CONFIG.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
