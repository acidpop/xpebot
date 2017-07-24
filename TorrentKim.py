#-*- coding: utf-8 -*-
#! /usr/bin/python

#import grequests
import sys
import os
import requests
import BeautifulSoup
import telepot
import urllib2
import sqlite3
import linecache
import hashlib
import traceback

from LogManager import log

from urllib import quote,unquote
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from operator import itemgetter

import main



class TorrentKim(object):
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

        log.info('TorKim Query : %s', query)
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
            
    
    def SearchTorrentKim(self, keyword, type=1, max_count=10, page_count = 2):

        if type < 1 or type > 2:
            log.info('Search Torrent Kim, Unknown Type:%d', type)
            return False, None, None

        try:
            log.info("Torrent kim Search , keyword=%s", keyword)
            tor_url = 'https://torrentkim10.net/bbs/s.php?k='
    
            urlTest = tor_url + quote(keyword.encode('utf-8'))

            log.info("url : %s", urlTest)
            
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')]
            data = opener.open(urlTest)
            
            sp = BeautifulSoup.BeautifulSoup(data)
            
            pageList = self.GetPageLink(sp, page_count)
            
            titleList = self.GetTitle(sp)
            if not titleList:
                log.info("%s not found torrent", keyword)
                return False, None, None
            
            for page in pageList:
                data = opener.open(page)
                sp = BeautifulSoup.BeautifulSoup(data)
                titleList.update(self.GetTitle(sp, len(titleList)))
            
            sortTorList = sorted(titleList.items(), reverse=True)
    
            inline_keyboard = self.MakeTorrentInlineKeyboard(sortTorList, type, max_count)
    
            outTitleList = self.MakeTorrentTitleList(sortTorList, max_count)
    
            if outTitleList == None:
                log.info("Get Title List fail")
                return False, None, None

        except:
            self.PrintException()
            return False, None, None

        return True, inline_keyboard, outTitleList

        

    def GetTitle(self, bs, start_idx = 0):
        torTable = bs.find('table', attrs={'class':'board_list'})

        if torTable == None:
            log.info("Not Found Torrent")
            return None
    
        torTRs = torTable.findAll('tr', attrs={'class':'bg1'})
    
        idx = start_idx
    
        titleList = dict()
        listValue = list()
    
        sortRatingList = list()
    
        
        for item in torTRs:
            if item.find('font'):
                Rating = item.find('font').text
            else:
                continue

            TargetItem = item.find('a', attrs={'target':'s'})
            if TargetItem == None:
                continue
            Title = TargetItem.text

            torUrl = 'https://torrentkim10.net' + item.find('a', attrs={'target':'s'})['href'][2:]
    
            titleList[torUrl] = list()
            
            titleList[torUrl].append(Rating)
            titleList[torUrl].append(Title)
    
            idx = idx + 1
    
        return titleList
    
    
    def GetPageLink(self, bs, page_count=2):
        baseUrl = 'https://torrentkim10.net/bbs/s.php'
        pageDiv = bs.find('div', attrs={'class':'board_page'})
        pageLinks = pageDiv.findAll('a')

        count = 0
    
        pageLinkList = list()
    
        for item in pageLinks:
            if count >= page_count:
                break

            pageLinkList.append(baseUrl + item['href'])
            count = count + 1
    
        return pageLinkList


    
    def GetTorrentFileLink(self, bbsUrl):
        try:
            """
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')]
            
            log.info("TorrentKim bbs URL : %s", bbsUrl)

            data = opener.open(bbsUrl)

            sp = BeautifulSoup.BeautifulSoup(data)
            """
            header = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'}

            req_data = requests.get(bbsUrl, headers=header)

            if req_data.status_code != 200:
                log.info("TorrentKim Get Url Page fail")
                return '', '', ''

            torkimhostidx = req_data.url.find('/', 8)
            torkimhost = req_data.url[0:torkimhostidx]
            referUrl = req_data.url
            
            sp = BeautifulSoup.BeautifulSoup(req_data.content)
        
            ATags = sp.findAll('a', {'rel' : 'nofollow', 'target' : 'hiddenframe'})
            fullLink = ATags[0]['href']

            start = fullLink.find("'")+1
            end = fullLink.find("'", start)
    
            #fileLink = 'https://torrentkim10.net' + fullLink[start:end]
            fileLink = torkimhost + fullLink[start:end]

            log.info("TorrentKim File URL : %s", fileLink)

            torrentTitleSpan = ATags[0].find('span')
            if torrentTitleSpan == None:
                log.info("Torrent Title not found")
                torStr = fullLink[start:end] + '.torrent'
            else:
                tempStr = torrentTitleSpan.text
                torStr = tempStr[0:tempStr.rfind('.torrent') + 8]
                log.info("Torrent Title Found : %s", torStr)

            torrentName = torStr

        except urllib2.HTTPError as e:
            log.error("GetTorrentFileLink Fail, HTTPError:'%d', Except :'%s'", e.code, e)
            return '', '', ''
        except urllib2.URLError as e:
            log.error("GetTorrentFileLink Fail, URLError:'%s', Except :'%s'", str(e.reason), e)
            return '', '', ''
        except:
            log.error("GetTorrentfile Exception : %s", traceback.format_exc())
            return '', '', ''


        try:
            torrentName.decode('ascii')
        except UnicodeDecodeError:
            log.info("GetTorrentfile Exception : it was not a ascii-encoded unicode string")
            start = bbsUrl.rfind('/')+1
            end = bbsUrl.rfind('.html')
            torrentName = bbsUrl[start:end]
        except UnicodeEncodeError:
            log.info("GetTorrentfile Exception : It may have been an ascii-encoded unicode string")
            start = bbsUrl.rfind('/')+1
            end = bbsUrl.rfind('.html')
            torrentName = bbsUrl[start:end]
        except:
            log.info("GetTorrentfile Exception : it is wrong string")
            start = bbsUrl.rfind('/')+1
            end = bbsUrl.rfind('.html')
            torrentName = bbsUrl[start:end]
    
        return fileLink, torrentName, referUrl
    
    
    def GetTorrentFile(self, bbsUrl):
        try:
            torrentUrl, torrentName, referUrl = self.GetTorrentFileLink(bbsUrl)
            if torrentUrl == '' or torrentName == '':
                log.error("GetTorrentFile| GetTorrentFileLink Fail")
                return False, 'Torrent Link 또는 Torrent 파일 이름이 없음'

            #torrentName = "/tmp/" + torrentName
            torrentName = os.path.join(u"/tmp/", torrentName)

            if torrentName[-8:] != '.torrent':
                torrentName = torrentName + '.torrent'

            r = requests.get(torrentUrl, stream=True, headers={'referer': referUrl})

            contentType = r.headers["content-type"]
            if contentType.find('text') >= 0:
                log.error('GetTorrentFile Fail, Response data is text')
                return False, 'Torrent File 다운로드 실패'
    
            #size = float(r.headers['content-length']) / 1024.0
    
            #with open(torrentName.encode('utf-8', 'ignore'), 'wb') as f: 
            with open(torrentName, 'wb') as f: 
                chunks = enumerate(r.iter_content(chunk_size=1024)) 
                for index, chunk in chunks: 
                    if chunk: 
                        f.write(chunk) 
                        f.flush() 
        except requests.exceptions.RequestException as e: 
            log.error('GetTorrentFile Fail, Request Exception : %s', e)
            log.error("GetTorrentfile Exception : %s", traceback.format_exc())
            return False, 'Torrent 파일 다운로드 오류'
        except:
            log.error("Get Torrent File Fail, url:'%s'", referUrl)
            log.error("GetTorrentfile Exception : %s", traceback.format_exc())
            return False, 'Torrent 파일 다운로드 오류'

        return True, torrentName.encode('utf-8')
    
    
    
    def MakeTorrentInlineKeyboard(self, torList, type=1, max_count=10):
        # sqlite ID, Type, Value
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()

        inline_keyboard_list = list()
        idx = 0
    
        for item in torList:
            if idx >= max_count:
                break
    
            # 고유키는 Url 링크를 SHA-1 으로 처리 한 값으로 한다.
            unique_id = hashlib.sha1(item[0].encode('utf-8')+str(type)).hexdigest()
            query = "INSERT OR REPLACE INTO TG_CB VALUES('%s', %d, '%s');" % (unique_id, type, item[0])
            log.info('TorKim Query : %s', query)
            cursor.execute(query)

            if type == 1:
                itemText = str(idx+1) + '. [' + item[1][0] + '] ' + item[1][1]
            elif type == 2:
                itemText = 'DOWNLOAD:[' + item[1][0] + '] ' + item[1][1]
                
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

        for item in torList:
            if idx >= max_count:
                break
            itemText = str(idx+1) +'. [' + item[1][0] + '] ' + item[1][1]
            outList += itemText
            outList += '\n'

            idx = idx + 1

        return outList




