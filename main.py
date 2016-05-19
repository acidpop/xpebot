#-*- coding: utf-8 -*-

import sys
import os
import traceback
import time
import StringIO
import logging

import telepot
import subprocess
from telepot.delegate import per_chat_id, per_from_id, create_open
import signal
import BotManager
import BotConfig

# wget "https://raw.github.com/pypa/pip/master/contrib/get-pip.py"
# python ./get-pip.py
# pip install telepot
# pip install BeautifulSoup
# pip install psycopg2
# pip install sqlite3

global botConfig

botConfig = BotConfig.BotConfig( sys.argv[1] )
global botManager
botManager = None

from LogManager import log

SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) for n in dir(signal) if n.startswith('SIG') and '_' not in n )

def signal_handler(signal, frame):
    log.info('recv signal : %s[%d]', SIGNALS_TO_NAMES_DICT[signal], signal)
    traceback.print_stack(frame)

def exception_hook(exc_type, exc_value, exc_traceback):
    log.error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )
    

def main():
    global botManager

    try:
        TOKEN = botConfig.GetBotToken()

        log.info('Telegram BOT Initialize...')

        # signal Register
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGABRT, signal_handler)
        signal.signal(signal.SIGSEGV, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        log.info('signal Register success')

        bot = BotManager.BOTManager(TOKEN)

        botManager = bot

        log.info('Telegram BOT Init OK')
        
        bot.message_loop()
        
        while 1:
            time.sleep(10)
        
        log.info('Telegram BOT Exit...')
    except Exception, e:
        log.error(e, exc_info=True)
    except:
        log.error('XPEBot Exeption')
        sys.excepthook = exception_hook

    return

if __name__ == "__main__":
    main()


