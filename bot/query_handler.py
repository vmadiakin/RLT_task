import json
from aiogram import types

from aggregation.aggregator import aggregate_salaries


# Функция обработки сообщений от пользователя
async def process_message(message: types.Message) -> None:
    try:
        # Получаем текст сообщения
        data = message.text
        # Преобразуем текст сообщения в словарь JSON
        input_data = json.loads(data)

        # Извлекаем параметры для запроса к БД из словаря
        dt_from = input_data.get('dt_from')
        dt_upto = input_data.get('dt_upto')
        group_type = input_data.get('group_type')

        # Получаем результаты агрегации зарплат
        result = await aggregate_salaries(dt_from, dt_upto, group_type)
        print(result)
        # Отправляем результат пользователю
        await message.answer(f"{result}")
    except Exception as e:
        # В случае ошибки отправляем пользователю сообщение с описанием ошибки
        await message.answer(f"Произошла ошибка: {str(e)}")
