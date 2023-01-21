import os
import telebot
from users_api import UsersApi
from tg_user import User
from telebot import types
from exaroton_api import exa_api


TOKEN_TG = ""

users = UsersApi()
base_way = os.path.abspath(os.curdir)
base_way += "/"

# get telegram bot token
if not( os.path.exists(base_way + "tg_token.txt") ):
    file = open(base_way + "tg_token.txt", 'w')
    file.close()
else:
    file = open(base_way + "tg_token.txt", 'r')
    TOKEN_TG = file.read() 
    file.close()
    

bot = telebot.TeleBot(TOKEN_TG)


@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    username = str(message.chat.username)
    us = users.find(username)
    if not isinstance(us, User):
        user = User(username)
        users.add_user(user)
        bot.reply_to(message, "Привет, твой аккаунт добавлен в нашу систему!)")
    else:
        bot.reply_to(message, "Привет, этот аккаунт у нас уже есть ;)")
        activate(message)


@bot.message_handler(commands=['help'])
def info_o_users(message):
    str = users.showAll()
    bot.send_message(message.chat.id, str)


@bot.message_handler(commands=['set_token'])
def set_token(message):
    username = str(message.chat.username)
    stringList = message.text.split(" ")
    if len(stringList) == 2:
        token = stringList[1]
        us = users.find(username)
        if isinstance(us, User):
            us.set_token(token)
            users.update_user(us)
            bot.send_message(message.chat.id, "Токен задан")
            users.file_save()
    else:
        bot.send_message(message.chat.id, "Не валидный токен, попробуй еще раз")

    activate(message)


@bot.message_handler(commands=['set_server_id'])
def set_server_id(message):
    username = str(message.chat.username)
    stringList = message.text.split(" ")
    if len(stringList) == 2:
        server_id = stringList[1]
        us = users.find(username)
        if isinstance(us, User):
            us.set_server_id(server_id)
            users.update_user(us)
            bot.send_message(message.chat.id, "Сервер id задан")
            users.file_save()
    else:
        bot.send_message(message.chat.id, "Сервер id не задан, попробуй еще раз")

    activate(message)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_first_name = str(message.chat.first_name)

    username = str(message.chat.username)
    stringList = message.text.split(" ")
    if len(stringList) == 1:
        us = users.find(username)
        if isinstance(us, User):
            if us.isValid() :
                exa = exa_api(us.get_token(), us.get_server_id())
                out_command = ""

                if stringList[0] == "Старт":
                    exa.server_start()
                    bot.send_message(message.chat.id, "Сервер запущен")
                elif stringList[0] == 'Стоп':
                    exa.server_stop()
                    bot.send_message(message.chat.id, "Сервер выключается")
                elif stringList[0] == 'Рестарт':
                    exa.server_restart()
                    bot.send_message(message.chat.id, "Сервер перезапущен")
                elif stringList[0] == 'Статус':
                    out_command = exa.get_status()
                    bot.send_message(message.chat.id, "Статус сервер: " + out_command)
                # elif stringList[0] == 'Логи':
                    # exa.
        
            return
    
    bot.reply_to(message, f"Извини {user_first_name}, но такого я не заню :с")


def activate(message):
    username = str(message.chat.username)
    us = users.find(username)
    if isinstance(us, User):
        # print( "main: activate ", us.isValid())
        if us.isValid() :
            markup = types.ReplyKeyboardMarkup()
            start = types.KeyboardButton('Старт')
            stop = types.KeyboardButton('Стоп')
            reboot = types.KeyboardButton('Рестарт')
            status = types.KeyboardButton('Статус')
            log = types.KeyboardButton('Логи')
            markup.row(start, stop)
            markup.row(reboot, status, log)
            bot.send_message(message.chat.id, "Все данные заполнены, теперь можно управлять", reply_markup=markup)

    

bot.infinity_polling()