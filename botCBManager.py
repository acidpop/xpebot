#-*- coding: utf-8 -*-

import sys
import os
import shutil
import traceback
import time
import datetime
import feedparser
import telepot
import subprocess
import json
import sqlite3
from telepot.delegate import per_chat_id, create_open

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply 
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton 
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent 


import main
import CommonUtil
import torrent
import BotHelp
import systemutil
import ExTimer
import dsdownload
import weather
import wol
import NaverApi
import rssManager
import airkorea
import namuwiki
import TorrentKim

from LogManager import log


class botCBManager(object):

    callback_db_path = main.botConfig.GetExecutePath() + "/cbbot.db"
    watch_dir = main.botConfig.GetTorrentWatchDir()

    torKim = TorrentKim.TorrentKim()
    """description of class"""

    def GetTypeValue(self, unique_id):
        query = "SELECT * FROM TG_CB WHERE ID = '%s';" % (unique_id)
        log.info("CBParser - callback_db_path:'%s', query:'%s'", self.callback_db_path, query)
        db = sqlite3.connect(self.callback_db_path)
        cursor = db.cursor()

        cursor.execute(query)

        row = cursor.fetchone()

        if row == None or len(row) == 0:
            cursor.close()
            db.close()
            log.info("GetTypeValue | Query result is 0")
            return None, ''
        
        type = row[1]
        value = row[2]
        
        log.info("GetTypeValue - type:%d, value:'%s'", type, value)

        cursor.close()
        db.close()

        return type, value

    def CBParser(self, unique_id, bot, chat_id):
        typeFuncMap = {
                        1:self.TorrentKimUrlDownload,
                        2:self.TorrentKimGetFile
                    }

        type, value = self.GetTypeValue(unique_id)

        if type == None:
            bot.sendMessage(chat_id, '검색된 데이터가 없습니다\n다시 검색하여 주세요')
            return False

        if typeFuncMap.get(type) == None:
            msg = '지원하지 않는 타입(%d) 입니다' % (type)
            bot.sendMessage(chat_id, msg)
            return False
        
        return typeFuncMap.get(type)(value, bot, chat_id)
        
    def TorrentKimUrlDownload(self, value, bot, chat_id):

        bot.sendMessage(chat_id, 'Torrent File 다운로드 시도')

        result, fileName = self.torKim.GetTorrentFile(value)

        if result == False:
            log.error("url:'%s' Download Fail", value)
            bot.sendMessage(chat_id, 'Torrent File 다운로드 시도 실패')
            return False

        log.info("File Move '%s' to '%s'", fileName, self.watch_dir.encode('utf-8'))
        try:
            shutil.move(fileName, self.watch_dir.encode('utf-8'))
        except Exception  as e:
            log.error("File Move Exception, '%s'", e)
            return False

        try:
            log.info("File '%s' Download Complete", fileName)
            msg = "%s 파일을\n'%s'\n경로에 다운로드 하였습니다" % (fileName, self.watch_dir.encode('utf-8'))
            bot.sendMessage(chat_id, msg)
        except Exception  as e:
            log.error("BOT SendMessage Error, '%s'", e)

        return True

    def TorrentKimGetFile(self, value, bot, chat_id):

        bot.sendMessage(chat_id, 'Torrent File 다운로드 시도')

        result, fileName = self.torKim.GetTorrentFile(value)

        if result == False:
            log.error("url:'%s' Download Fail", value)
            bot.sendMessage(chat_id, 'Torrent File 다운로드 시도 실패')
            return False

        log.info("Torrent Kim File Download Success, File Name:'%s'", fileName)

        bot.sendDocument(chat_id, open(fileName, 'rb'))

        return False
