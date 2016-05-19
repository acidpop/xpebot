#-*- coding: utf-8 -*-
import os
import sys
import time
import feedparser
import dsdownload
import main

from LogManager import log

# pip install psycopg2

class TorrentManager(object):
    """description of class"""

    rssUrl = """https://torrentkim1.net/bbs/rss.php?k="""
    navi = feedparser.FeedParserDict()

    dsm_id = main.botConfig.GetDsmId()

    def tor_search(self, keyword, bot, chat_id):
        bot.sendMessage(chat_id, '토렌트 검색 중...')
        self.navi = feedparser.parse(self.rssUrl+keyword.encode('utf-8'))

        outList = []
        show_keyboard = {'keyboard': "not found"}

        if not self.navi.entries:
            bot.sendMessage(chat_id, '검색결과가 없습니다. 다시 입력하세요.')
            #print('검색결과가 없습니다. 다시 입력하세요.')
            return False

        title_list = ''

        for (i,entry) in enumerate(self.navi.entries):
            if i == 10: break
            title = str(i+1) + ". " + entry.title

            templist = []
            templist.append(title)
            outList.append(templist)
            title_list += title
            title_list += '\n'

        show_keyboard = {'keyboard': outList, 'resize_keyboard': True}

        bot.sendMessage(chat_id, '받을 Torrent를 선택 하세요')
        bot.sendMessage(chat_id, title_list, reply_markup=show_keyboard)

        return True

    def torrent_download(self, selected, bot, chat_id):
        ds = dsdownload.dsdownload()

        log.info('DS Torrent download')

        ret, items = ds.db_query("SELECT * FROM USER_SETTING WHERE username='" + self.dsm_id + "';")
        if ret == False:
            log.info('DS Download User Setting not found..')
            return

        ds_user = items[0][0]
        sh_dir = items[0][2]
        log.info('DS Download Config, Download Directory : %s', sh_dir)
       
        index = int(selected.split('.')[0]) - 1 
        magnet = self.navi.entries[index].link

        log.info("DS Download, user:'%s', DownloadPath:'%s', Magnet Link : '%s'", ds_user, sh_dir.decode('utf-8'), magnet)

        query = u"INSERT INTO download_queue (username, url, status, filename, pid, created_time, destination) VALUES ('%s', '%s', 1, 'Magnet Link', %d, %d, '%s');" % (ds_user, magnet, os.getpid(), int(time.time()), sh_dir.decode('utf-8')) 
        log.debug(query)
        ret = ds.db_exec(query.encode('utf-8'))
        log.info('torrent download query complete')

        hide_keyboard = {'hide_keyboard': True}
        if ret == True:
            msg = self.navi.entries[index].title + u' 다운로드를 시작합니다'
            bot.sendMessage(chat_id, msg, reply_markup=hide_keyboard) 
            self.navi.clear()
        else:
            bot.sendMessage(chat_id, u'다운로드 실패', reply_markup=hide_keyboard) 


    def ReceiveTorrentFile(self, fileid, file_name, file_ext, file_type, bot, chat_id):
        watch_dir = main.botConfig.GetTorrentWatchDir()
        filename = file_name + "." + file_ext

        ds = dsdownload.dsdownload()

        log.info('DS Torrent download')

        ret, items = ds.db_query("SELECT * FROM USER_SETTING WHERE username='" + self.dsm_id + "';")
        if ret == False:
            log.info('DS Download User Setting not found..')
            return

        ds_user = items[0][0]
        #watch_dir = items[0][5]

        log.info('ReceiveTorrentFile, ds_user:%s, Watch:%s', ds_user, watch_dir)

        bot.download_file(fileid, watch_dir + file_name.encode('utf-8') )
        
        log.info('%s download success', filename)

        hide_keyboard = {'hide_keyboard': True}
        #msg = file_name + ' 파일을 ' + watch_dir + ' 경로에 다운로드 하였습니다';
        #bot.sendMessage(chat_id, msg, reply_markup=hide_keyboard) 

        return True



