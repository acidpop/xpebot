#-*- coding: utf-8 -*-


import feedparser
import urllib
import main

from LogManager import log

class rssManager(object):
    """description of class"""

    rssNewsUrl = main.botConfig.GetRssNewsUrl()
    rssNewsCount = main.botConfig.GetRssNewsCount()


    rssNews = feedparser.FeedParserDict()

    def RssNewsReader(self):
        log.info('Rss News Reader')
        self.rssNews = feedparser.parse(self.rssNewsUrl)
        newsMessage = '<strong>' + self.rssNews.feed.title + '</strong>\n\n'
        for (i,entry) in enumerate(self.rssNews.entries):
            if i == self.rssNewsCount: break
            log.info(entry.title)
            newsMessage += '<a href="%s">%d. %s</a>\n' % (entry.link, i+1, entry.title)

        log.info('Rss News : %s', newsMessage)
        return newsMessage

