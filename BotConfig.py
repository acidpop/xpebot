#-*- coding: utf-8 -*-

import sys
import os
import ConfigParser

class BotConfig(object):
    """description of class"""

    #config_file_path = './xpebot.cfg'
    #config_file_path = self.configPath

    notify_chat_id = 0
    dsm_id = ""
    bot_token = ""
    valid_user_list = None
    log_path = ""
    log_size = 0
    log_count = 0
    execute_path = ""

    def __init__(self, *args, **kwargs):
        
        config_file_path = str(args[0])

        config = ConfigParser.RawConfigParser()
        config.read(config_file_path)

        self.notify_chat_id = config.get('TELEGRAM', 'NOTY_CHAT_ID')
        self.dsm_id = config.get('TELEGRAM', 'DSM_ID')
        self.bot_token = config.get('TELEGRAM', 'BOT_TOKEN')
        self.valid_user_list = eval(config.get('TELEGRAM', 'VALID_USER'))
        self.log_path = config.get('TELEGRAM', 'LOG_PATH')
        self.log_size = config.getint('TELEGRAM', 'LOG_MAX_SIZE')
        self.log_count = config.getint('TELEGRAM', 'LOG_COUNT')

        temp_path = os.path.split(sys.argv[0])
        self.execute_path = temp_path[0]
        print "Execute Path : " + self.execute_path


    def GetChatId(self):
        return self.notify_chat_id

    def GetDsmId(self):
        return self.dsm_id

    def GetBotToken(self):
        return self.bot_token

    def GetValidUser(self):
        return self.valid_user_list

    def GetLogPath(self):
        return self.log_path

    def GetLogSize(self):
        return self.log_size

    def GetLogCount(self):
        return self.log_count

    def GetExecutePath(self):
        return self.execute_path
