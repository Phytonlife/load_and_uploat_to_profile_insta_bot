import telebot
from telebot import types
import subprocess

# Вставьте ваш токен здесь
TOKEN = '7297162378:AAGsQWJAV_Pn1FpDbBmA4_b5hfBV-9fgfsg'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения временных данных пользователей
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_data[message.chat.id] = {
        'instagram_profile': None,
        'instagram_password': None,
        'target_profile': None
    }
    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    user = user_data.get(chat_id, {})
    if not user.get('instagram_profile'):
        btn1 = types.KeyboardButton("Ввести профиль Instagram")
        markup.add(btn1)
    if not user.get('instagram_password'):
        btn2 = types.KeyboardButton("Ввести пароль Instagram")
        markup.add(btn2)
    if not user.get('target_profile'):
        btn3 = types.KeyboardButton("Ввести профиль таргет пользователя")
        markup.add(btn3)
    if all([user.get('instagram_profile'), user.get('instagram_password'), user.get('target_profile')]):
        btn4 = types.KeyboardButton("Пуск")
        markup.add(btn4)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if message.text == "Ввести профиль Instagram":
        msg = bot.send_message(chat_id, "Введите ваш профиль Instagram:")
        bot.register_next_step_handler(msg, process_instagram_profile)
    elif message.text == "Ввести пароль Instagram":
        msg = bot.send_message(chat_id, "Введите ваш пароль Instagram:")
        bot.register_next_step_handler(msg, process_instagram_password)
    elif message.text == "Ввести профиль таргет пользователя":
        msg = bot.send_message(chat_id, "Введите профиль таргет пользователя:")
        bot.register_next_step_handler(msg, process_target_profile)
    elif message.text == "Пуск":
        user = user_data[chat_id]
        start_bestbot2(user['target_profile'], user['instagram_profile'], user['instagram_password'])
        bot.send_message(chat_id, "Все данные введены. Начинаем процесс...")
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите одну из опций.")

def process_instagram_profile(message):
    chat_id = message.chat.id
    user_data[chat_id]['instagram_profile'] = message.text
    bot.send_message(chat_id, f"Ваш профиль Instagram: {message.text}")
    show_main_menu(chat_id)

def process_instagram_password(message):
    chat_id = message.chat.id
    user_data[chat_id]['instagram_password'] = message.text
    bot.send_message(chat_id, "Ваш пароль Instagram успешно сохранен.")
    show_main_menu(chat_id)

def process_target_profile(message):
    chat_id = message.chat.id
    user_data[chat_id]['target_profile'] = message.text
    bot.send_message(chat_id, f"Профиль таргет пользователя: {message.text}")
    show_main_menu(chat_id)

def start_bestbot2(target_username, username, password):
    # Запуск bestbot2.py с параметрами
    subprocess.Popen(['python3', 'bestbot2.py', target_username, username, password])

# Запуск бота
bot.polling(none_stop=True)
