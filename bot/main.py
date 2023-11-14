import os
from aiogram import Bot, Dispatcher, types
import logging
import asyncio

from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('token'))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    full_name_url = f"<a href='{message.from_user.url}'>{message.from_user.full_name}</a>"
    await message.answer(f"Hi {full_name_url}!", parse_mode=ParseMode.HTML)


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
