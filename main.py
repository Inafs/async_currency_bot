import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from commands import set_commands
from pars import get_kurs
from config_reader import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()

currencies = {'USD':'Доллару','EUR':'Евро','GBP':'фунту стерлингов','AMD':'армянский драм','BGN':'Болгарский лев','BRL':'бразильский реал','VND':'Донг','GEL':'Лари','ILS':'Шекель','KZT':'Тенге'}

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Доллар", callback_data="value_USD"),
            types.InlineKeyboardButton(text="Евро", callback_data="value_EUR")
        ],
        [
            types.InlineKeyboardButton(text="Фунт стерлингов", callback_data="value_GBP"),
            types.InlineKeyboardButton(text="Армянский драм", callback_data="value_AMD")
        ],
        [
            types.InlineKeyboardButton(text="Болгарский Лев", callback_data="value_BGN"),
            types.InlineKeyboardButton(text="Бразильский реал", callback_data="value_BRL")
        ],
        [
            types.InlineKeyboardButton(text="Донг", callback_data="value_VND"),
            types.InlineKeyboardButton(text="Лари", callback_data="value_GEL")
        ],
        [
            types.InlineKeyboardButton(text="Шекель", callback_data="value_ILS"),
            types.InlineKeyboardButton(text="Тенге", callback_data="value_KZT")
        ]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_kurs(message: types.Message, new_value: str):
    await message.edit_text(
        f"Укажите число: {new_value}",
        reply_markup=get_keyboard()
    )


@dp.message(commands=['start'])
async def cmd_start(message: types.Message):
    await set_commands(bot)
    await message.answer("Приветствую в боте актуальных курсов валют! Нажмите /currency чтобы просмотреть валюты.")

@dp.message(commands=["currency"])
async def cmd_currency(message: types.Message):
    await message.answer("Выберите валюту", reply_markup=get_keyboard())


@dp.callback_query(Text(text_startswith="value_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]

    await callback.message.edit_text(f"Курс рубля к {currencies[action]}: {get_kurs(action)}")

    await callback.answer()




async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())