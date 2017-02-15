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

def signal_handler(sig, frame):
    log.info('recv signal : %s[%d]', SIGNALS_TO_NAMES_DICT[sig], sig)

def signal_term_handler(sig, frame):
    log.info('recv signal : %s[%d]', SIGNALS_TO_NAMES_DICT[sig], sig)
    log.info('SIGTERM signal ignore')
    #botConfig.SetLoop(False)

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
        signal.signal(signal.SIGTERM, signal_term_handler)
        signal.signal(signal.SIGABRT, signal_handler)
        signal.signal(signal.SIGSEGV, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        log.info('signal Register success')

        bot = BotManager.BOTManager(TOKEN)

        botManager = bot

        log.info('Telegram BOT Init OK')

        bot.message_loop()

        while botConfig.IsLoop():
            time.sleep(10)

        bot.close()
        log.info('Telegram BOT Exit...')

        os.kill(os.getpid(), signal.SIGINT)
    #except Exception as e:
    #    log.error(e, exc_info=True)
    except:
        log.error('XPEBot Exeption')
        sys.excepthook = exception_hook


    return

if __name__ == "__main__":
    main()


