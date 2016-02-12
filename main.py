#-*- coding: utf-8 -*-

import sys
import os

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
global bot

botConfig = BotConfig.BotConfig( sys.argv[1] )
bot = None

from LogManager import log

SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) for n in dir(signal) if n.startswith('SIG') and '_' not in n )

def signal_handler(signal, frame):
    log.info('recv signal : %s[%d]', SIGNALS_TO_NAMES_DICT[signal], signal)
    

if __name__ == "__main__":
    TOKEN = botConfig.GetBotToken()

    log.info('Telegram BOT Initialize...')

    # signal Register
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
    signal.signal(signal.SIGSEGV, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    log.info('signal Register success')

    bot = telepot.DelegatorBot(TOKEN, [
        (per_from_id(), create_open(BotManager.BOTManager, timeout=120)),
    ])

    log.info('Telegram BOT Init OK')
    
    bot.sendMessage(botConfig.GetChatId(), 'XPEnology BOT Service start...')

    bot.notifyOnMessage(run_forever=True)

    log.info('Telegram BOT Exit...')

