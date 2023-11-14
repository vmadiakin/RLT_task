import json
from aiogram import types


async def aggregate_salaries(dt_from, dt_upto, group_type) -> None:
    pass


async def process_message(message: types.Message) -> None:
    try:
        data = message.text
        input_data = json.loads(data)

        dt_from = input_data.get('dt_from')
        dt_upto = input_data.get('dt_upto')
        group_type = input_data.get('group_type')

        result = await aggregate_salaries(dt_from, dt_upto, group_type)
        await message.answer(f"{result}")
    except Exception as e:

        await message.answer(f"Произошла ошибка: {str(e)}")
