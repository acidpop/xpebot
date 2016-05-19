#-*- coding: utf-8 -*-


import main
from LogManager import log
import requests


class NamuWiki(object):

    namuwiki_url = "https://namu.wiki/w/"


    def SearchDocument(self, keyword, bot, chat_id):
        url = self.namuwiki_url + keyword

        r = requests.get(url)
    
        if r.status_code != 200:
            msg = "*'" + keyword + "'*" + '에 해당하는 문서를 찾지 못하였습니다.'
            #sender.sendMessage(msg)
            sender.sendMessage(msg, parse_mode='Markdown')
            return

        #wikiContent = (r.te[:75] + '..') if len(data) > 75 else data

        bot.sendMessage(chat_id, r.url)

        log.info('NamuWiki Found Document : %s', keyword)

        return
