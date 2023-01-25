import os
import logging


base_way = os.path.abspath(os.curdir)
base_way += "/"
LOGFILE = base_way + 'log.log'

logging.basicConfig(filename=LOGFILE, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def logger_add_debug(str):
    logging.debug(str)

def logger_add_info(str):
    logging.info(str)

def logger_add_warning(str):
    logging.warning(str)

def logger_add_error(str):
    logging.error(str)

def logger_add_critical(str):
    logging.critical(str)


def logger_get_last_messages(count):
    logs = ''
    with open(LOGFILE) as file:
        for line in (file.readlines() [-count:]):
            logs += line
    return logs


def count_lines(filename, chunk_size=1<<13):
    with open(filename) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))

