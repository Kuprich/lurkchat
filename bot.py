import config
import telebot
from telebot import types
from data.repository import DbRepository

bot = telebot.TeleBot(config.TOKEN)
db = DbRepository(config.DB_URL)


@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    bot.send_message(
        message.chat.id, f'Привет, {message.from_user.first_name}, добро пожаловать в анонимный чат! нажми на кнопку найти собеседника', reply_markup=markup)

@bot.message_handler(commands=['stop'])
def stop_command(message):
    room = db.get_room_by_chat_id(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)
    if not room: return
    
    if room.is_busy:
        db.delete_room(room)
        if message.chat.id == room.chat_id_1: 
            bot.send_message(room.chat_id_2, 'Собеседник завершил чат', reply_markup=markup)
            bot.send_message(room.chat_id_1, 'Вы завершили чат', reply_markup=markup)
        else: 
            bot.send_message(room.chat_id_1, 'Собеседник завершил чат', reply_markup=markup)
            bot.send_message(room.chat_id_2, 'Вы завершили чат', reply_markup=markup)
    else:
        stop_search(message)



@bot.message_handler(func=lambda message: message.text == 'Поиск собеседника')
def search_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Остановить поиск')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Ищем...', reply_markup=markup)

    room = db.get_free_room()
    if not room:
        db.create_room(message.chat.id)
    else:
        markup = types.ReplyKeyboardRemove()

        db.add_user_to_room(room.id, message.chat.id)

        bot.send_message(room.chat_id_1, 'Собеседник найден, общение начато:',
                         reply_markup=markup)
        bot.send_message(message.chat.id, 'Собеседник найден, общение начато:',
                         reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Остановить поиск')
def stop_search(message):
    room = db.get_room_by_chat_id(message.chat.id)
    if room:
        db.delete_room(room)
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Поиск остановлен', reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def bot_message(message):
    active_room = db.get_room_by_chat_id(message.chat.id)
    if active_room and active_room.is_busy: 
        markup = types.ReplyKeyboardRemove()
        if message.chat.id == active_room.chat_id_1: 
            bot.send_message(active_room.chat_id_2, message.text, reply_markup=markup)
        else: 
            bot.send_message(active_room.chat_id_1, message.text, reply_markup=markup)
    else: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Поиск собеседника')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Найдите собеседника для общения', reply_markup=markup)

bot.polling(none_stop=True)
