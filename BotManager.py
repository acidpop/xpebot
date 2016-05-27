#-*- coding: utf-8 -*-

import sys
import os
import traceback
import time
import datetime
import feedparser
import telepot
import subprocess
import json
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
import botCBManager

from LogManager import log

# Emoji Unicode 참고 : http://apps.timwhitlock.info/emoji/tables/unicode

class BOTManager(telepot.Bot):

    cur_mode = ''
    hide_keyboard = {'hide_keyboard': True}
    
    # Torrent 클래스
    tor = torrent.TorrentManager()
    helper = BotHelp.BotHelp()
    ds = dsdownload.dsdownload()
    wt = weather.weather()
    wol = wol.wol()
    naverApi = NaverApi.NaverApi()
    rssManager = rssManager.rssManager()
    airKorea = airkorea.airkorea()
    namuWiki = namuwiki.NamuWiki()
    torKim = TorrentKim.TorrentKim()
    CBMgr = botCBManager.botCBManager()

    ds.db_connect()

    dsdown_monitor = ExTimer.ExTimer(3, ds.download_db_timer)
    dsdown_monitor.start()
    
    bot_update_loop = None
    
    TOKEN = main.botConfig.GetBotToken()
    bot = telepot.Bot(TOKEN)

    valid_user = main.botConfig.GetValidUser()

    def __init__(self, *args, **kwargs):
        super(BOTManager, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        if self.bot_update_loop == None:
            log.info('bot getUpdates loop start...')
            self.bot_update_loop = ExTimer.ExTimer(60, self.getUpdatesLoop)
            self.bot_update_loop.start()
        
        return

    def current_mode_handler(self, command, chat_id):
        log.info('current mode handler : ' +  self.cur_mode)
        

        # cur_mode == torrentsearch 이면 받은 command 를 Torrent Keywork 로 검색
        if self.cur_mode == 'torrentsearch':
            result = self.tor.tor_search(command, self, chat_id)
            if result == True:
                self.cur_mode = 'torrent_list'
            else:
                self.cur_mode = 'torrentsearch'

        # torrent_list 모드이면 입력받은 값을 기준으로 Torrent 를 다운로드 한다.
        elif self.cur_mode == 'torrent_list':
            self.tor.torrent_download(command, self, chat_id)
            self.cur_mode = ''
        # cur_mode 가 wol 이면 등록된 WOL 디바이스 목록을 보여준다. 등록된게 없다면 WOL 등록 시작
        elif self.cur_mode == 'addwol':
            #AddDevice(self, MAC, DeviceName, BroadCastAddr="192.168.0.1"): 
            self.wol.RegiDevice(command, self, chat_id)
            self.cur_mode = ''
        elif self.cur_mode == 'wol':
            self.wol.WOLDevice(command, self, chat_id)
            self.cur_mode = ''
        elif self.cur_mode == 'delwol':
            self.wol.UnregiDevice(command, self, chat_id)
            self.cur_mode = ''
        elif self.cur_mode == 'weather':
            self.wt.GetDongneWether(self, chat_id, command)
            self.cur_mode = ''

        # Naver Developer API
        elif self.cur_mode == 'en2ko':
            response = self.naverApi.TranslateEn2Ko(command, self, chat_id)
            self.cur_mode = ''
        elif self.cur_mode == 'ko2en':
            response = self.naverApi.TranslateKo2En(command, self, chat_id)
            self.cur_mode = ''
        elif self.cur_mode == 'shorturl':
            response = self.naverApi.ShortUrl(command, self, chat_id)
            self.cur_mode = ''
        elif self.cur_mode == 'txt2voice':
            response = self.naverApi.TextToVoice(command, self, chat_id)
            self.cur_mode = ''
        elif self.cur_mode == 'namuwiki':
            self.namuWiki.SearchDocument(command.encode('utf-8'), self, chat_id)
            self.cur_mode = ''
        elif self.cur_mode == 'torkim':
            result, keyboard = self.torKim.SearchTorrentKim(command)
            self.cur_mode = ''
            if result == True:
                self.sendMessage(chat_id, 'Torrent Kim 검색 결과', reply_markup=keyboard)
            else:
                self.sendMessage(chat_id, 'Torrent Kim 검색 실패')
        elif self.cur_mode == 'gettorrent':
            result, keyboard = self.torKim.SearchTorrentKim(command, 2)
            self.cur_mode = ''
            if result == True:
                self.sendMessage(chat_id, 'Torrent Kim 다운로드 목록', reply_markup=keyboard)
            else:
                self.sendMessage(chat_id, 'Torrent Kim 검색 실패')
        return
    
    # 전송된 메시지를 처리 하는 함수
    def command_handler(self, command, chat_id):
        log.info("cmd_handle - Command[%s], cur_mode[%s]", command, self.cur_mode)

        if command == '/cancel':
            self.sendMessage(chat_id, '모드를 취소합니다', reply_markup=self.hide_keyboard)
            self.cur_mode = ''
            return

        if command == '/start':
            start_keyboard = {'keyboard': [['/torrentsearch'], 
                                           ['/weather'], 
                                           ['/wol', '/addwol', '/delwol'],
                                           ['/help']
                                           ]}
            self.sendMessage(chat_id, u'사용 하실 명령을 선택하세요 \U0001f60f', reply_markup=start_keyboard)
            self.cur_mode = ''
            return

        if self.cur_mode:
            self.current_mode_handler(command, chat_id)
            return

        self.cur_mode = ''

        if command == '/torrentsearch' or command == u'/토렌트':
            log.info("cmd_handle : Torrent Search")
            self.cur_mode = 'torrentsearch'
            self.sendMessage(chat_id, u'검색 할 Torrent 제목을 입력하세요', reply_markup=self.hide_keyboard)

        elif command == '/weather' or command == u'/날씨':
            log.info("cmd_handle : Weather")
            self.cur_mode = 'weather'
            weather_keyboard = {'keyboard': [[u'전국 날씨']], 'resize_keyboard': True}
            self.sendMessage(chat_id, u'전국 날씨 선택 또는 동네 이름을 입력하세요', reply_markup=weather_keyboard)

        elif command == '/wol':
            log.info("cmd_handle : WOL")
            if self.wol.WOLDeviceCount() == 0:
                self.sendMessage(chat_id, u'등록 된 Device 없습니다.')
                self.sendMessage(chat_id, u'Device 등록 과정을 시작합니다.\n다음 형식으로 입력하세요\nMAC, DeviceName, BroadCastAddr\nex)1a:2b:3c:4d:5e:6f, 거실PC, 192.168.0.255')
                self.cur_mode = 'regiwol'
            else:
                self.wol.ShowWOLDeviceList(u'WOL 패킷을 보낼 Device를 선택 하세요', self, chat_id)
                self.cur_mode = 'wol'

        elif command == '/addwol':
            log.info("cmd_handle : Add WOL Device")
            self.sendMessage(chat_id, u'Device 등록 과정을 시작합니다.\n다음 형식으로 입력하세요\nMAC, DeviceName, BroadCastAddr\nex)1a:2b:3c:4d:5e:6f, 거실PC, 192.168.0.255\nBroadCast 주소의 가장 끝은 255입니다', reply_markup=self.hide_keyboard)
            self.cur_mode = 'addwol'

        elif command == '/delwol':
            log.info("cmd_handle : Unregister WOL Device")
            self.wol.ShowWOLDeviceList(u'삭제 할 WOL Device를 선택 하세요', self, chat_id)
            self.cur_mode = 'delwol'

        elif command == '/systeminfo':
            log.info("cmd_handle : System Info")
            self.sendMessage(chat_id, u'시스템 리소스를 측정 중입니다.')
            sysinfo = systemutil.system_status(3)
            log.info('sysinfo : %s', sysinfo.decode('utf-8'))
            self.SendMarkupMessage(chat_id, sysinfo.decode('utf-8'), self.hide_keyboard)

        # Naver Developer API
        elif command == '/en2ko' or command == u'/영한':
            if self.naverApi.naver_api_use:
                self.sendMessage(chat_id, u'한국어로 번역 할 영어 문장을 입력하세요', reply_markup=self.hide_keyboard)
                self.cur_mode = 'en2ko'
        elif command == '/ko2en' or command == u'/한영':
            if self.naverApi.naver_api_use:
                self.sendMessage(chat_id, u'영어로 번역 할 한국어 문장을 입력하세요', reply_markup=self.hide_keyboard)
                self.cur_mode = 'ko2en'
        elif command == '/shorturl' :
            if self.naverApi.naver_api_use:
                self.sendMessage(chat_id, u'짧게 줄일 URL을 입력하세요', reply_markup=self.hide_keyboard)
                self.cur_mode = 'shorturl'
        elif command == '/txt2voice' :
            if self.naverApi.naver_api_use:
                self.sendMessage(chat_id, u'음성으로 변환 할 문장을 입력하세요', reply_markup=self.hide_keyboard)
                self.cur_mode = 'txt2voice'

        elif command == '/news' or command == u'/뉴스':
            response = self.rssManager.RssNewsReader()
            self.sendMessage(chat_id, response, reply_markup=self.hide_keyboard, parse_mode='HTML', disable_web_page_preview=True)

        elif command == '/airkorea' or command == u'/통합대기':
            self.sendMessage(chat_id, '통합 대기 지수를 조회 중 입니다...', reply_markup=self.hide_keyboard)
            response = self.airKorea.SendAirKorea(self, chat_id)

        elif command == '/namuwiki' or command == '/nw' or command == u'/나무위키':
            self.sendMessage(chat_id, '나무 위키 문서를 검색 할 키워드를 입력하세요', reply_markup=self.hide_keyboard)
            self.cur_mode = 'namuwiki'

        elif command == '/torkim':
            show_keyboard = {'hide_keyboard': False}
            self.sendMessage(chat_id, '검색 할 Torrent 제목을 입력하세요', reply_markup=show_keyboard);
            self.cur_mode = 'torkim'
        elif command == '/gettorrent':
            show_keyboard = {'hide_keyboard': False}
            self.sendMessage(chat_id, '검색 할 Torrent 제목을 입력하세요', reply_markup=show_keyboard);
            self.cur_mode = 'gettorrent'

        elif command == '/help':
            log.info("cmd_handle : Help Mode")
            self.SendMarkupMessage(chat_id, self.helper.HelpText, self.hide_keyboard)
        
        else:
            start_keyboard = {'keyboard': [['/torrentsearch', '/weather', '/systeminfo'], 
                                           ['/wol', '/addwol', '/delwol'],
                                           ['/en2ko', '/ko2en', '/shorturl'],
                                           ['/news', '/airkorea', '/namuwiki'],
                                           ['/torkim', '/help', '/cancel']
                                           ]}
            self.sendMessage(chat_id, u'사용 하실 명령을 선택하세요', reply_markup=start_keyboard)
            self.cur_mode = ''


    def group_command_handler(self, command, chat_id):
        log.info("Group Command Handler, Cmd:'%s', chat_id:'%s'", command, chat_id)
        groupCmd = command
        idx = groupCmd.rfind('@')
        if idx >= 0:
            groupCmd = groupCmd[:idx]

        if groupCmd == '/cancel':
            self.sendMessage(chat_id, '모드를 취소합니다', reply_markup=self.hide_keyboard)
            self.cur_mode = ''
            return

        # cur_mode 가 존재 한다면 가장 앞의 / 기호 제거
        if self.cur_mode:
            groupCmd = groupCmd[1:]

        self.command_handler(groupCmd, chat_id)

        return groupCmd

    # 전송된 파일을 처리 하는 함수
    def file_handler(self, file_name, file_id, file_ext, file_type, chat_id):
        log.info('file_name:%s, id:%s, ext:%s', file_name, file_id, file_ext)
        if file_type == 'application/x-bittorrent':
            self.tor.ReceiveTorrentFile(file_id, file_name, file_ext, file_type, self.bot, chat_id)
            return
        else:
            log.info('unknown file type, ext:%s', file_ext)

    def SendMessage(self, chat_id, message, show_keyboard):
        if show_keyboard == '':
            self.sendMessage(chat_id, message)
        else:
            self.sendMessage(chat_id, message, reply_markup=show_keyboard)

    def SendMarkupMessage(self, chat_id, message, show_keyboard):
        log.debug(message)
        if show_keyboard == '':
            self.sendMessage(chat_id, message, parse_mode='Markdown')
        else:
            self.sendMessage(chat_id, message, parse_mode='Markdown', reply_markup=show_keyboard)

    def SendHtmlMessage(self, chat_id, message):
        log.debug(message)
        self.sendMessage(chat_id, message, parse_mode='HTML')

    def PrintMsg(self, msg):
        timestr = time.strftime('%Y/%m/%d %H:%M:%S',  time.localtime(msg['date']))
        log.info('Recv Message : ' + json.dumps(msg,indent=4, ensure_ascii=False))

    def PrintMsgCB(self, msg):
        log.info('Recv Message : ' + json.dumps(msg,indent=4, ensure_ascii=False))

    def on_chat_message(self, msg):

        try:
            flavor = telepot.flavor(msg)

            # inline query test code...
            # Have to answer inline query to receive chosen result
            log.info('flavor : %s', flavor)
            if flavor == 'inline_query':
                log.info('inline query!!')
                query_id, from_id, query_string = telepot.glance(msg, flavor=flavor)
                log.info('Inline Query: id:%s, from:%d, msg:%s', query_id, from_id, query_string)

                articles = [{'type': 'article',
                                 'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]
                self.bot.answerInlineQuery(query_id, articles)
                return

            content_type, chat_type, chat_id = telepot.glance(msg)

            log.info("ContentType : '%s'", content_type)
            log.info("chat_type : '%s'", chat_type)
            log.info("chat_id : %d", chat_id)

            # Message to Log Write
            self.PrintMsg(msg)

            # Valid User Check
            if not chat_id in self.valid_user:
                log.info("Invalid user : %d", chat_id)
                return

            log.debug("chat_type:'%s'", chat_type)
            if chat_type == 'group':
                groupMsg = self.group_command_handler(unicode(msg['text']), chat_id)
                log.info("Group Message : %s", groupMsg)
                return


            if content_type is 'text':
                self.command_handler(unicode(msg['text']), chat_id)
                log.info(msg['text'])
                return

            if content_type is 'document':
                file_name = msg['document']['file_name']
                file_id = msg['document']['file_id']
                file_ext = os.path.splitext(file_name)
                file_type = msg['document']['mime_type']
                self.file_handler(file_name, file_id, file_ext[1], file_type, chat_id)
                return
        except Exception, e:
            log.error(e, exc_info=True)
        except:
            log.error('XPEBot on_chat_message Exeption')
            sys.excepthook = main.exception_hook
            
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        self.PrintMsgCB(msg)

        chat_id = 0

        query_type = msg['message']['chat']['type']
        if query_type == 'group':
            chat_id = int(msg['message']['chat']['id'])
        else:
            chat_id = from_id
        
        log.info("Callback Query - query Id:'%s', cb_type:'%s', From:%d, chat_id:%d, query:'%s'", query_id, query_type, from_id, chat_id, query_data)
        self.CBMgr.CBParser(query_data, self, chat_id)
        
    def on_inline_query(self, msg):
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)
        log.info("Inline query - query Id:'%s', From:%d, query:'%s'", query_id, from_id, query_string);

        def compute_answer():
            # Compose your own answers
            articles = [{'type': 'article',
                            'id': 'abc', 'title': query_string, 'message_text': query_string}]

            return articles

        self._answerer.answer(msg, compute_answer)

    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
        print('Chosen Inline Result:', result_id, from_id, query_string)

        
    def on_close(self, exception):
        if type(exception) == telepot.helper.WaitTooLong:
            log.debug('Wait Timeout')
            if self.cur_mode != '':
                #self.sender.sendMessage('입력 시간이 초과 되었습니다', reply_markup=self.hide_keyboard)
                self.cur_mode = ''
        else:
            log.error('on_close - exception :')
            log.error(exception)
            log.exception("on_close - exception :")
            traceback.print_exc(file=sys.stdout)
        
        
    def close(code=None, reason=None):
        log.info('close')

    def ManagerClose(self):
        log.info('Bot Manager Close')
        self.dsdown_monitor.cancel()
        self.bot_update_loop.cancel()

    def getUpdatesLoop(self):
        response = self.bot.getUpdates()
