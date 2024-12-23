import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from telegram_ans_creator import *

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="")
# Диспетчер
dp = Dispatcher()

api_key = 'tHFH4XKTyk07NEzXehomY5Ru7Vh3wZeI'

open_test_state = -1
mode_weather = ''
ans = []
is_end = False

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Я бот который поможет тебе узнать погоду на твоем маршруте. Пиши /weather чтобы узнать погоду!")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("/start - о боте\n/help - о командах\n/weather - узнать погоду на маршруте\n")

@dp.message(Command("weather"))
async def cmd_weather(message: types.Message):
    global open_test_state
    global mode_weather
    global ans
    global is_end

    open_test_state = -1
    mode_weather = ''
    ans = []
    is_end = False
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Северный (более холодный)",
        callback_data="north"),
        types.InlineKeyboardButton(
            text="Центральный (умеренный)",
            callback_data="center"),
        types.InlineKeyboardButton(
            text="Южный (более теплый)",
            callback_data="south")
    )
    builder.adjust(1)
    await message.answer("К сожалению, в бесплатной версии AccuWeatherAPI доступно получение прогноза погоды только на 5 дней. \n\n Выбери комфортный для тебя режим погоды:", reply_markup=builder.as_markup())

@dp.callback_query(lambda call: call.data in ['south', 'north', 'center'])
async def send_random_value(callback: types.CallbackQuery):
    global open_test_state
    global mode_weather
    await callback.message.answer('Укажите начальный город:')
    mode_weather = callback.data
    open_test_state = 0
    await callback.answer()

@dp.callback_query(lambda call: call.data in ['yes', 'no'])
async def send_random_value(callback: types.CallbackQuery):
    global open_test_state
    global mode_weather
    global is_end
    if callback.data == 'yes':
        await callback.message.answer('Укажите промежуточный город:')
        open_test_state += 1
    else:
        await callback.message.answer('Укажите конечный город:')
        open_test_state += 1
        is_end = True
    await callback.answer()

@dp.message(F.text)
async def extract_data(message: types.Message):
    global open_test_state
    global mode_weather
    global ans
    global is_end

    if open_test_state != -1:
        try:
            ans.append(report_for_city(open_test_state, mode_weather, message.text, api_key))

            print(is_end)

            if is_end:
                for i in ans:
                    await message.answer(i)
                return None

            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(
                text="Хочу",
                callback_data="yes"),
                types.InlineKeyboardButton(
                    text="Нет",
                    callback_data="no")
            )
            await message.answer(
                "Ты хочешь добавить промежуточный город?",
                reply_markup=builder.as_markup())
        except:
            raise
            await message.answer('К сожалению, API Accuweather не отвечает, скорее всего превышен лимит запросов')


# Запуск процесса поллинга новых апдейтов
async def main():
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_weather, Command("weather"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())