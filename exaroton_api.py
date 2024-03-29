import requests
import json
# import logger

STATUS_BAR = {
    0  :  'OFFLINE',
    1  :  'ONLINE',
    2  :  'STARTING',
    3  :  'STOPPING',
    4  :  'RESTARTING',
    5  :  'SAVING',
    6  :  'LOADING',
    7  :  'CRASHED',
    8  :  'PENDING',
    10 :  'PREPARING'
    }

STATUS_BAR_RU = {
    0  :  'Не работает',
    1  :  'Работает',
    2  :  'Запускается',
    3  :  'Остановлен',
    4  :  'Перезагрузка',
    5  :  'Сохранение',
    6  :  'Загрузка',
    7  :  'Упал',
    8  :  'Ожидание',
    10 :  'Подготовка'
    }

class exa_api:
    def __init__(self, token, server_id):
        self.IAM_TOKEN = token
        self.SERVER_ID = server_id
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.IAM_TOKEN)
        }

    def get_status(self):
        response = requests.post('https://api.exaroton.com/v1/servers/', headers = self.headers)

        media = json.loads(response.text)
        # print( "\n\n Пакет:", response.text, "\n\n")
        answer = media['data'][0]['status'] # написать проверку 
        
        
        for i in STATUS_BAR_RU:
            if i == answer:
                # logger.logger_add_info('Запрошен статус сервера. Результат: ' + STATUS_BAR_RU[i] )
                return STATUS_BAR_RU[i] 
        # logger.logger_add_critical('Запрошеный статус сервера не найдет в системе. Статус сервера: ' + answer )
        

    def get_logs_server(self):
        logs = ''

        logs += 'Почти реализовано'

        # logger.logger_add_info('Запрошены логи сервера' )
        return logs

    def mode_server(self, str ):
        url = 'https://api.exaroton.com/v1/servers/' + self.SERVER_ID + '/'

        if str == 'start':
            url += 'start'
        elif str == 'stop':
            url += 'stop'
        elif str == 'restart':
            url += 'restart'
        else: # dont valid arg
            # logger.logger_add_info('Задан не корректный режим сервера: ' + str )
            return False 

        response = requests.post(url, headers = self.headers)
        # logger.logger_add_info('Задан новый режим работы сервера \"' + str +'\". полный адрес запроса: ' + url)
        # print(response.text)

    def server_start(self):
        self.mode_server('start');

    def server_stop(self):
        self.mode_server('stop');

    def server_restart(self):
        self.mode_server('restart');

