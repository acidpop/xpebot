#-*- coding: utf-8 -*-
import urllib
import BeautifulSoup
import sqlite3
import main
from LogManager import log


class weather(object):
    """description of class"""
    
    db_path = main.botConfig.GetExecutePath() + "/tgbot.db"

    def GetSummaryUrl(self, LocalName):
        if LocalName == u'강원도':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=105&x=28&y=16"
        elif LocalName == u'서울특별시' or LocalName == u'인천광역시' or LocalName == u'경기도':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=109&x=23&y=5"
        elif LocalName == u'부산광역시' or LocalName == u'울산광역시' or LocalName == u'경상남도':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=159&x=32&y=14"
        elif LocalName == u'대구광역시' or LocalName == u'경상북도':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=143&x=15&y=16"
        elif LocalName == u'광주광역시' or LocalName == u'전라남도':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=156&x=19&y=18"
        elif LocalName == u'전라북도':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=146&x=30&y=2"
        elif LocalName == u'제주특별자치도':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=184&x=27&y=10"
        elif LocalName == u'대전광역시' or LocalName == u'충청남도':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=133&x=31&y=16"
        elif LocalName == u'충청북도':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=131&x=36&y=9"
        elif LocalName == u'전국날씨' or LocalName == u'전국 날씨':
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=108&x=14&y=11"
        else:
            return "http://www.kma.go.kr/weather/forecast/summary.jsp?stnId=108&x=14&y=11"

    
    def GetWeatherSummary(self, LocalName):
        log.info('GetWeatherSummary : ' + LocalName)
        sumurl = self.GetSummaryUrl(LocalName)
        
        log.debug('url : ' + sumurl)

        data = urllib.urlopen(sumurl)

        soup = BeautifulSoup.BeautifulSoup(data)

        week_summary = soup.findAll('table', attrs={'class':'table_announcementtime'})

        today_summary = LocalName + ' ' + week_summary[0].find('caption').text + '\n' + \
                        week_summary[0].find('p').text.replace(u'다.', u'다.\n') + '\n'
        tomorrow_summary =  LocalName + ' ' + week_summary[1].find('caption').text + '\n' + \
                            week_summary[1].find('p').text.replace(u'다.', u'다.\n') + '\n'

        soup.close()
        data.close()
        
        return today_summary, tomorrow_summary


    def GetDongneWether(self, sender, dongne_name):
        query = u"select code, sido, gugun, dong from kma_dongne where dong like '%" + dongne_name + "%';"
        log.debug(query)

        hide_keyboard = {'hide_keyboard': True}

        if dongne_name == u'전국 날씨':
            today, tomorrow = self.GetWeatherSummary(u'전국날씨')
            sender.sendMessage(today, reply_markup=hide_keyboard) 
            return
            
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        cursor.execute(query)
        rowdata = cursor.fetchall()

        before_sido = ''

        # 동네 이름이 여러개 있을 경우 모두 출력
        for row in rowdata:
            code = str(row[0])
            sido = row[1]
            gugun = row[2]
            dong = row[3]
        
            dong_url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=" + code + '00'
            
            log.info('dongne weather url : %s', dong_url)
            
            data = urllib.urlopen(dong_url)
            
            sp = BeautifulSoup.BeautifulSoup(data)
            
            dongne = sp.findAll('data', attrs={'seq':'0'})

            # 풍속의 소수점이 길게 나오는 케이스로 인해 소수점 2자리까지만 표현
            ws = round(float(dongne[0].find('ws').text), 2)

            weather_info = sido + ' ' + gugun + ' ' + dong + u' 날씨\n'\
                            u'날씨 : ' + dongne[0].find('wfkor').text + u'\n'\
                            u'온도 : ' + dongne[0].find('temp').text + u"℃\n"\
                            u'풍속 : ' + str(ws) + u"m/s\n"\
                            u'풍향 : ' + dongne[0].find('wdkor').text + u"향\n"\
                            u'습도 : ' + dongne[0].find('reh').text + u"%\n"\
                            u'강수 확률 : ' + dongne[0].find('pop').text + u"%\n"
            
            sp.close()
            data.close()

            sender.sendMessage(weather_info, reply_markup=hide_keyboard) 

        # 시도별 날씨 요약본 가져 오기
        today, tomorrow = self.GetWeatherSummary(sido)
        sender.sendMessage(today, reply_markup=hide_keyboard)
        
        cursor.close()
        db.close()

