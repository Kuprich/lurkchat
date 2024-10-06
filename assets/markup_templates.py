from aiogram import types

search_companion_markup = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text='Поиск собеседника')]],
    resize_keyboard=True
)

stop_search_markup = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text='Остановить поиск')]],
    resize_keyboard=True
)

empty_markup = types.ReplyKeyboardRemove()