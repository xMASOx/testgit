import telebot  # библиотека telebot
from config import token  # импорт токена

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(func=lambda message: True)
def check_and_ban(message):
    if "https://" in message.text or "http://" in message.text:
        user_id = message.from_user.id
        username = message.from_user.username
        
        bot.reply_to(message, f"Пользователь @{username} забанен за отправку ссылки.")
        bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id)
    else:
        bot.reply_to(message, message.text)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:  # Проверка, что команда вызвана в ответ на сообщение
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
        
        if user_status in ['administrator', 'creator']:
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

bot.infinity_polling(none_stop=True)