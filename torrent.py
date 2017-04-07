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

    rssUrl = """https://torrentkim10.net/bbs/rss.php?k="""
    navi = feedparser.FeedParserDict()

    dsm_id = main.botConfig.GetDsmId()

    def tor_search(self, keyword, bot, chat_id, is_group_chat=False):
        bot.sendMessage(chat_id, '토렌트 검색 중...')
        self.navi = feedparser.parse(self.rssUrl+keyword.encode('utf-8'))

        outList = []

        if not self.navi.entries:
            bot.sendMessage(chat_id, '검색결과가 없습니다. 다시 입력하세요.')
            #print('검색결과가 없습니다. 다시 입력하세요.')
            return False

        title_list = ''

        for (i,entry) in enumerate(self.navi.entries):
            if i == 10: break
            if is_group_chat:
                title = '/' + str(i+1) + ". " + entry.title
            else:
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

        if type(selected) is int == False:
            log.info('Torrent Download, Selected number type is not int!')
            bot.sendMessage(chat_id, u'입력값 오류') 
            return False

        ret, items = ds.db_query("SELECT * FROM USER_SETTING WHERE username='" + self.dsm_id + "';")
        if ret == False:
            log.info('DS Download User Setting not found..')
            return False

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

        return True

    def RegisterMagnetLink(self, magnetLink, bot, chat_id):
        ds = dsdownload.dsdownload()

        log.info('DS Torrent download for magnetLink')

        ret, items = ds.db_query("SELECT * FROM USER_SETTING WHERE username='" + self.dsm_id + "';")
        if ret == False:
            log.info('DS Download User Setting not found..')
            return False

        ds_user = items[0][0]
        sh_dir = items[0][2]
        log.info('DS Download Config, Download Directory : %s', sh_dir)

        log.info("DS Download, user:'%s', DownloadPath:'%s', Magnet Link : '%s'", ds_user, sh_dir.decode('utf-8'), magnetLink)

        query = u"INSERT INTO download_queue (username, url, status, filename, pid, created_time, destination) VALUES ('%s', '%s', 1, 'Magnet Link', %d, %d, '%s');" % (ds_user, magnetLink, os.getpid(), int(time.time()), sh_dir.decode('utf-8')) 
        log.debug(query)
        ret = ds.db_exec(query.encode('utf-8'))
        log.info('torrent download query complete')

        hide_keyboard = {'hide_keyboard': True}
        if ret == True:
            msg = 'Magnet Link 가 등록 되었습니다.\n다운로드를 시작합니다.'
            bot.sendMessage(chat_id, msg, reply_markup=hide_keyboard) 
        else:
            bot.sendMessage(chat_id, u'Magnet Link 등록 실패', reply_markup=hide_keyboard) 

        return True


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

        log.info('ReceiveTorrentFile, ds_user:%s, Watch:%s', ds_user, watch_dir.decode('utf-8'))

        bot.download_file(fileid, watch_dir + file_name.encode('utf-8'))

        log.debug('downoad success')
        
        log.info('%s download success', filename)

        hide_keyboard = {'hide_keyboard': True}
        #msg = file_name.decode('utf-8') + ' 파일을 ' + watch_dir.decode('utf-8') + ' 경로에 다운로드 하였습니다';
        #msg = "%s 파일을\n'%s'\n경로에 다운로드 하였습니다" % (filename.encode('utf-8'), watch_dir.encode('utf-8'))
        msg = 'Torrent 파일을 Watch 경로에 다운로드 하였습니다\n잠시 후 다운로드가 시작됩니다'
        bot.sendMessage(chat_id, msg, reply_markup=hide_keyboard) 

        return True



