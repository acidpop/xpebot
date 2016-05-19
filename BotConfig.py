#-*- coding: utf-8 -*-

import sys
import os
import socket
import ConfigParser

class BotConfig(object):
    """description of class"""

    #config_file_path = './xpebot.cfg'
    #config_file_path = self.configPath

    notify_chat_id = 0
    dsm_id = ""
    bot_token = ""
    valid_user_list = None
    
    watch_dir = ""
    
    log_path = ""
    log_size = 0
    log_count = 0
    execute_path = ""

    # Naver API Config
    naver_api_use = False
    naver_client_id = ''
    naver_secret_key = ''
    
    # Rss New Url
    rss_news_url = ''
    rss_news_count = 10
    
    # data.go.kr Service Key
    data_service_key = ''

    host_name = ''

    def __init__(self, *args, **kwargs):
        
        config_file_path = str(args[0])

        config = ConfigParser.RawConfigParser()
        config.read(config_file_path)

        self.notify_chat_id = config.get('TELEGRAM', 'NOTY_CHAT_ID')
        self.dsm_id = config.get('TELEGRAM', 'DSM_ID')
        self.bot_token = config.get('TELEGRAM', 'BOT_TOKEN')
        temp_valid_user = str(config.get('TELEGRAM', 'VALID_USER'))
        if temp_valid_user.find(',') == -1:
            temp_valid_user += ', '
        self.valid_user_list = eval(temp_valid_user)
        
        self.watch_dir = config.get('TELEGRAM', 'WATCH_DIR')
        
        self.log_path = config.get('TELEGRAM', 'LOG_PATH')
        self.log_size = config.getint('TELEGRAM', 'LOG_MAX_SIZE')
        self.log_count = config.getint('TELEGRAM', 'LOG_COUNT')

        # Naver API Config
        self.naver_client_id = config.get('NAVER_API', 'CLIENT_ID_KEY')
        self.naver_secret_key = config.get('NAVER_API', 'CLIENT_SECRET_KEY')
        if self.naver_client_id and self.naver_secret_key:
            self.naver_api_use = True

        # RSS News
        self.rss_news_url = config.get('RSS_NEWS', 'RSS_URL')
        self.rss_news_count = config.getint('RSS_NEWS', 'RSS_COUNT')
        
        # data.go.kr Service Key
        self.data_service_key = config.get('DATA', 'SERVICE_KEY')

        temp_path = os.path.split(sys.argv[0])
        self.execute_path = temp_path[0]

        self.host_name = socket.gethostname()

    def GetChatId(self):
        return self.notify_chat_id

    def GetDsmId(self):
        return self.dsm_id

    def GetBotToken(self):
        return self.bot_token

    def GetValidUser(self):
        return self.valid_user_list

    def GetTorrentWatchDir(self):
        return self.watch_dir

    def GetLogPath(self):
        return self.log_path

    def GetLogSize(self):
        return self.log_size

    def GetLogCount(self):
        return self.log_count

    def GetExecutePath(self):
        return self.execute_path

    def GetNaverApiUse(self):
        return self.naver_api_use

    def GetNaverClientId(self):
        return self.naver_client_id

    def GetNaverClientSecret(self):
        return self.naver_secret_key

    def GetRssNewsUrl(self):
        return self.rss_news_url

    def GetRssNewsCount(self):
        return self.rss_news_count
        
    def GetDataServiceKey(self):
        return self.data_service_key

    def GetHostName(self):
        return self.host_name

