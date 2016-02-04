#-*- coding: utf-8 -*-

import sys
import os

import telepot
import subprocess
from telepot.delegate import per_chat_id, create_open
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


def signal_handler(signal, frame):
    log.info('recv signal : ' + str(signal))
    

def signal_sigint(signal, frame):
    #global th
    #th.end()
    #BotManager.BOTManager.ManagerClose()
    
    log.info('signal handler : ' +  str(signal))
    #sys.exit(0)
    #os.kill(os.getpid(), signal.SIGINT)
    

if __name__ == "__main__":
    TOKEN = botConfig.GetBotToken()

    log.info('Telegram BOT Initialize...')

    bot = telepot.DelegatorBot(TOKEN, [
        (per_chat_id(), create_open(BotManager.BOTManager, timeout=30)),
    ])

    log.info('Telegram BOT Init OK')
    
    bot.sendMessage(botConfig.GetChatId(), 'XPEnology BOT Service start...')

    # signal Register
    #signal.signal(signal.SIGINT, signal_sigint)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
    signal.signal(signal.SIGSEGV, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)

    bot.notifyOnMessage(run_forever=True)

    log.info('Telegram BOT Exit...')

