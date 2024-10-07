from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram import F
from app import bot
from app import db

from assets.markup_templates import search_companion_markup, stop_search_markup, empty_markup


router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    room = db.get_room_by_chat_id(message.chat.id)
    if not room:
        await message.answer(f"Привет, {message.from_user.first_name}. Добро пожаловать в анонимный чат! нажми на кнопку найти собеседника",
                             reply_markup=search_companion_markup)
        return

    answer_text = "Имеется активный чат." if room.is_busy else "Идет поиск содеседника."
    await message.answer(answer_text, reply_markup=empty_markup)
    
    
@router.message(Command('menu'))
async def cmd_menu(message: types.Message):
    room = db.get_room_by_chat_id(message.chat.id)
    if not room:
        await message.answer(f"Привет, {message.from_user.first_name}. Добро пожаловать в анонимный чат! нажми на кнопку найти собеседника",
                             reply_markup=search_companion_markup)
        return

    answer_text = "Имеется активный чат." if room.is_busy else "Идет поиск содеседника."
    await message.answer(answer_text, reply_markup=empty_markup)


@router.message(Command('stop'))
async def cmd_stop(message: types.Message):
    room = db.get_room_by_chat_id(message.chat.id)

    if not room:
        return

    if room and room.is_busy:
        db.delete_room(room)
        chat_id = room.chat_id_1 if message.chat.id != room.chat_id_1 else room.chat_id_2

        await bot.send_message(chat_id, 'Собеседник завершил чат', reply_markup=search_companion_markup)
        await message.answer('Вы завершили чат', reply_markup=search_companion_markup)

    else:
        await stop_search(message)


@router.message(F.text == 'Поиск собеседника')
async def search(message: types.Message):
    await message.answer('Ищем...', reply_markup=stop_search_markup)

    room = db.get_free_room()
    if not room:
        db.create_room(message.chat.id)
    else:
        db.add_user_to_room(room.id, message.chat.id)

        await bot.send_message(room.chat_id_1, 'Собеседник найден, общение начато:', reply_markup=empty_markup)
        await message.answer('Собеседник найден, общение начато:', reply_markup=empty_markup)


@router.message(F.text == 'Остановить поиск')
async def stop_search(message: types.Message):
    room = db.get_room_by_chat_id(message.chat.id)
    if room:
        db.delete_room(room)
    await message.answer('Поиск остановлен', reply_markup=empty_markup)


@router.message(F.text)
async def bot_message(message: types.Message):
    room = db.get_room_by_chat_id(message.chat.id)
    if room and room.is_busy:
        chat_id = room.chat_id_2 if message.chat.id == room.chat_id_1 else room.chat_id_1
        await bot.send_message(chat_id, message.text, reply_markup=empty_markup)
    else:
        await message.answer('Найдите собеседника для общения', reply_markup=search_companion_markup)
