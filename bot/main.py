import os
from aiogram import Bot, Dispatcher, types
import logging
import asyncio
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from query_handler import process_message

# Загрузка переменных среды из файла .env
load_dotenv()

# Создаем объекты бота и диспетчера
bot = Bot(token=os.getenv('token'))
dp = Dispatcher()


# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    # Формируем приветственное сообщение с использованием HTML-разметки
    full_name_url = f"<a href='{message.from_user.url}'>{message.from_user.full_name}</a>"
    await message.answer(f"Hi {full_name_url}!", parse_mode=ParseMode.HTML)


# Обработчик всех остальных сообщений
@dp.message()
async def handle_json(message: types.Message) -> None:
    # Передаем сообщение для обработки в функцию process_message
    await process_message(message)


# Асинхронная функция, запускающая бота
async def main() -> None:
    # Настройка логирования
    logging.basicConfig(level=logging.DEBUG)
    # Запуск бота
    await dp.start_polling(bot)


# Проверка, запущен ли скрипт напрямую, а не импортирован
if __name__ == '__main__':
    try:
        # Запуск основной асинхронной функции
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
