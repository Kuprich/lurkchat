import config
import logging
from aiogram import Bot, Dispatcher
from aiogram import types
from data.repository import DbRepository
from aiogram.filters.command import Command
from aiogram import F
import asyncio

logging.basicConfig(level=logging.INFO)

bot = Bot(config.TOKEN)
dp = Dispatcher()
db = DbRepository(config.DB_URL)

search_companion_markup = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text='Поиск собеседника')]],
    resize_keyboard=True
)
stop_search_markup = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text='Остановить поиск')]],
    resize_keyboard=True
)
empty_markup = types.ReplyKeyboardRemove()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    room = db.get_room_by_chat_id(message.chat.id)
    if not room: 
        await message.answer(f"Привет, {message.from_user.first_name},\nДобро пожаловать в анонимный чат! нажми на кнопку найти собеседника",
                         reply_markup=search_companion_markup)
    elif room.is_busy: 
        await message.answer(f"Имеется активный чат.",reply_markup=empty_markup)
    else: 
        await message.answer(f"Идет поиск содеседника.",reply_markup=empty_markup)


@dp.message(Command('stop'))
async def cmd_stop(message: types.Message):
    room = db.get_room_by_chat_id(message.chat.id)

    if not room:
        return

    if room.is_busy:
        db.delete_room(room)
        chat_id = room.chat_id_1 if message.chat.id != room.chat_id_1 else room.chat_id_2

        await bot.send_message(chat_id, 'Собеседник завершил чат', reply_markup=search_companion_markup)
        await message.answer('Вы завершили чат', reply_markup=search_companion_markup)

    else:
        await stop_search(message)


@dp.message(F.text == 'Поиск собеседника')
async def search(message: types.Message):
    await message.answer('Ищем...', reply_markup=stop_search_markup)

    room = db.get_free_room()
    if not room:
        db.create_room(message.chat.id)
    else:
        db.add_user_to_room(room.id, message.chat.id)

        await bot.send_message(room.chat_id_1, 'Собеседник найден, общение начато:', reply_markup=empty_markup)
        await message.answer('Собеседник найден, общение начато:', reply_markup=empty_markup)



@dp.message(F.text == 'Остановить поиск')
async def stop_search(message: types.Message):
    room = db.get_room_by_chat_id(message.chat.id)
    if room:
        db.delete_room(room)
    await message.answer('Поиск остановлен', reply_markup=empty_markup)


@dp.message(F.text)
async def bot_message(message: types.Message):
    active_room = db.get_room_by_chat_id(message.chat.id)
    if active_room and active_room.is_busy:
        if message.chat.id == active_room.chat_id_1:
            await bot.send_message(active_room.chat_id_2, message.text, reply_markup=empty_markup)
        else:
            await bot.send_message(active_room.chat_id_1, message.text, reply_markup=empty_markup)
    else:
        await message.answer('Найдите собеседника для общения', reply_markup=search_companion_markup)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
