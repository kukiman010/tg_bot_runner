import os
import telebot
import logger
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
    if TOKEN_TG == '':
        logger.logger_add_critical('Не задан токен для Телеграм бота!')

    file.close()
    

bot = telebot.TeleBot(TOKEN_TG)


@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    username = str(message.chat.username)
    us = users.find(username)
    if not isinstance(us, User):
        user = User(username)
        users.add_user(user)
        bot.reply_to(message, "Аккаунт добавлен в систему. Теперь нужен токен и сервер_id. \nОтправляй в формате /set_token [токен] и /set_server_id [сервер_id].")
    else:
        bot.reply_to(message, "Ты уже добавлен. Если задал токен и сервер_id, можешь управлять сервером. Если нет, задавай в формате /set_token [токен]и /set_server_id [сервер_id].")
        logger.logger_add_info('Пользователь ' + username + ' пытается повторно авторизоваться')
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
            logger.logger_add_info('Задан токен для пользователя ' + username)
    else:
        bot.send_message(message.chat.id, "Невалидный токен")

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
            bot.send_message(message.chat.id, "ID сервера задан")
            users.file_save()
            logger.logger_add_info('Задан ID сервера для пользователя ' + username)
    else:
        bot.send_message(message.chat.id, "Неправильный ID сервера")

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
                    logger.logger_add_info('Пользователь ' + username + ' запросил запуск сервера')
                elif stringList[0] == 'Стоп':
                    exa.server_stop()
                    bot.send_message(message.chat.id, "Сервер выключается")
                    logger.logger_add_info('Пользователь ' + username + ' запросил выключение сервера')
                elif stringList[0] == 'Рестарт':
                    exa.server_restart()
                    bot.send_message(message.chat.id, "Сервер перезапущен")
                    logger.logger_add_info('Пользователь ' + username + ' запросил рестарт сервера')
                elif stringList[0] == 'Статус':
                    out_command = exa.get_status()
                    bot.send_message(message.chat.id, "Статус сервера: " + out_command)
                    logger.logger_add_info('Пользователь ' + username + ' запросил статус сервера')

                if stringList[0] == 'Логи':
                    out_command = logger.logger_get_last_messages(50)
                    bot.send_message(message.chat.id, "50 последних логов окружния:")
                    if len(out_command) > 4095:
                        for x in range(0, len(out_command), 4095):
                            bot.reply_to(message, text=out_command[x:x+4095])
                    else:
                        bot.reply_to(message, text=out_command)
                    logger.logger_add_info('Пользователь ' + username + ' запросил логи')
            return

    # elif len(stringList) == 2:
    #     us = users.find(username)
    #     if isinstance(us, User):
    #         if us.isValid() :
    #             exa = exa_api(us.get_token(), us.get_server_id())
    #             out_command = ""


    #             if stringList[0] == 'Логи' and stringList[1] == 'окружния':
    #                 out_command = logger.logger_get_last_messages(50)
    #                 print( len(out_command) )

    
<<<<<<< HEAD
    # bot.reply_to(message, f"{user_first_name}, ты вообще кто?")
=======
    bot.reply_to(message, f"{user_first_name}, ты вообще кто?")
>>>>>>> main


def activate(message):
    username = str(message.chat.username)
    us = users.find(username)
    if isinstance(us, User):
        if us.isValid() :
            markup = types.ReplyKeyboardMarkup()
            start = types.KeyboardButton('Старт')
            stop = types.KeyboardButton('Стоп')
            reboot = types.KeyboardButton('Рестарт')
            status = types.KeyboardButton('Статус')
            log_other = types.KeyboardButton('Логи')
            markup.row(start, stop)
            markup.row(reboot, status, log_other)
            bot.send_message(message.chat.id, "Все данные заполнены, теперь можно управлять", reply_markup=markup)

            logger.logger_add_info('Активирован пользователь ' + username)

    

bot.infinity_polling()