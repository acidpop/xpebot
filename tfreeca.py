# -*- coding: utf-8 -*-
#!/usr/bin/env python


import os
import sys
import urllib2
import requests
import BeautifulSoup
import base64
import urlparse
import sqlite3
import linecache
import hashlib
import traceback

from LogManager import log
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

import main


class tfreeca(object):
    """description of class"""

    db_path = main.botConfig.GetExecutePath() + "/cbbot.db"


    def __init__(self):
        # DB fail if not exists - Create DB
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()

        query = """CREATE TABLE IF NOT EXISTS "TG_CB" (
	                `ID`	TEXT NOT NULL,
	                `TYPE`	INTEGER NOT NULL,
	                `VALUE`	TEXT NOT NULL,
	                PRIMARY KEY(ID)
                );"""

        log.info('tfreeca Query : %s', query)
        cursor.execute(query)
        db.commit()

        cursor.close()
        db.close()
        
    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        log.error('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
            

    def SearchTfreeca(self, keyword, torType=3, max_count=20):
        if torType < 3 or torType > 4:
            log.info('Search tfreeca, Unknown Type:%d', torType)
            return False, None, None

        try:
            torList = self.GetTorrentList(keyword.encode('utf-8'), torType)

            sortTorList = sorted(torList.items(), reverse=True)
    
            inline_keyboard = self.MakeTorrentInlineKeyboard(sortTorList, torType, max_count)
    
            outTitleList = self.MakeTorrentTitleList(sortTorList, max_count)
    
            if outTitleList == None:
                log.info("Get Title List fail")
                return False, None, None

        except:
            self.PrintException()
            return False, None, None

        return True, inline_keyboard, outTitleList



    def GetTitle(self, board, keyword, torType=3):
        if torType == 3:
            typeMap = {"tdrama": 3, "tent" : 4, "tv" : 5}
        else:
            typeMap = {"tdrama": 6, "tent" : 7, "tv" : 8}

        url = "http://www.tfreeca22.com/board.php?b_id=" + board + "&mode=list&sc=" + keyword + "&x=0&y=0"

        boardType = typeMap.get(board, 999)

        if boardType == 999:
            log.info("tfreeca get title unknown board")
            return None

        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'), ('Cookie', 'uuoobe=on;')]
        data = opener.open(url)

        sp = BeautifulSoup.BeautifulSoup(data)

        bList = sp.find('table', attrs={'class':'b_list'})

        if bList == None:
            return None

        torTRs = bList.findAll('td', attrs={'class':'subject'})

        titleList = dict()
        listValue = list()

        for item in torTRs:
            alink = item.find('a', attrs={'class':['stitle1','stitle2', 'stitle3', 'stitle4', 'stitle5', 'stitle6']})
            torUrl = "http://www.tfreeca22.com/" + alink['href']
            torTitle = alink.text
            par = urlparse.parse_qs(urlparse.urlparse(torUrl).query)
            torId = str(par["id"][0])

            titleList[torId] = list()
            titleList[torId].append(torTitle)
            titleList[torId].append(boardType)

        return titleList



    def GetTorrentList(self, keyword, torType=3):
        boardList = ['tdrama', 'tent', 'tv']

        torList = dict()

        for item in boardList:
            tempList = self.GetTitle(item, keyword, torType)
            if tempList == None:
                continue

            torList.update(tempList)

        return torList

    def GetTorrentFile(self, torType, id):
        typeMap = {3 : "tdrama",
                   4 : "tent",
                   5 : "tv",
                   6 : "tdrama",
                   7 : "tent",
                   8 : "tv"}

        board = typeMap.get(torType, "unknown")
        if board == "unknown":
            log.info('tfreeca get torrent fail, unknown type:%d', torType)
            return False, ''

        torId = str(id)
        torrentEnc = base64.encodestring(board + '|' + torId + '|')
        torrentUrl = "http://file.filetender.com/Execdownload.php?link=" + torrentEnc

        torrentName = torId + ".torrent"

        try:
            r = requests.get(torrentUrl, stream=True, headers={'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                                                                'Connection' : 'keep-alive',
                                                                'Content-Type' : 'application/x-bittorrent',
                                                                'pragma' : 'no-cache',
                                                                'expires' : '0',
                                                                'Content-Disposition' : 'attachment; filename=\"' + torId + '.torrent\"',
                                                                'content-description' : 'php generated data'})

            with open(torrentName, 'wb') as f: 
                chunks = enumerate(r.iter_content(chunk_size=4096)) 
                for index, chunk in chunks: 
                    if chunk: 
                        f.write(chunk) 
                        f.flush()
        except requests.exceptions.RequestException as e: 
            log.error('tfreeca GetTorrentFile Fail, Request Exception : %s', e)
            log.error("tfreeca GetTorrentfile Exception : %s", traceback.format_exc())
            return False, ''
        except:
            log.error("tfreeca Get Torrent File Fail, url:'%s'", bbsUrl)
            log.error("tfreeca GetTorrentfile Exception : %s", traceback.format_exc())
            return False, ''

        return True, torrentName.encode('utf-8')
    
    def MakeTorrentInlineKeyboard(self, torList, cmdType=3, max_count=10):
        # sqlite ID, Type, Value
        log.info("1111")
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        log.info("222")

        inline_keyboard_list = list()
        idx = 0

        log.info("3333")

    
        #for k, v in torList.iteritems():
        for item in torList:
            if idx >= max_count:
                break
    
            # 고유키는 Url 링크를 SHA-1 으로 처리 한 값으로 한다.
            #torType = v[1]
            torType = item[1][1]
            unique_id = hashlib.sha1(item[0].encode('utf-8')+str(torType)).hexdigest()
            query = "INSERT OR REPLACE INTO TG_CB VALUES('%s', %d, '%s');" % (unique_id, torType, item[0])
            log.info('Tfreeca Query : %s', query)
            cursor.execute(query)

            if cmdType == 3:
                itemText = str(idx+1) + '. ' + item[1][0].encode('utf-8')
            elif cmdType == 4:
                itemText = 'DOWNLOAD:[' +  item[1][0].encode('utf-8')
                
            callbackText = "%s" % (unique_id)
    
            tempList = list()
            tempList.append(InlineKeyboardButton(text=itemText, callback_data=callbackText))
            inline_keyboard_list.append(tempList)
    
            idx = idx + 1

        db.commit()

        cursor.close()
        db.close()
    
        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard_list)


    def MakeTorrentTitleList(self, torList, max_count=10):
        outList = ''
        idx = 0

        #for k, v in torList.iteritems():
        for item in torList:
            if idx >= max_count:
                break
            itemText = str(idx+1) +'. ' + item[1][0]
            outList += itemText
            outList += '\n'

            idx = idx + 1

        return outList