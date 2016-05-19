#-*- coding: utf-8 -*-


import main
import BotManager
from LogManager import log

import os
import sys
import datetime
import time
from PIL import Image, ImageDraw, ImageFont
import requests
import linecache


# pip install Pillow

class airkorea(object):

    grade_color = { 1 : (78, 137, 246, 255),
                    2 : (91, 212, 100, 255),
                    3 : (254, 127, 65, 255),
                    4 : (249, 74, 75, 255)}

    sido_xy = { '서울': [104, 84], 
    			'인천': [40,107],
    			'강원': [194,84],
    			'경기': [122,116],
    			'충북': [164,133],
    			'충남': [82, 154],
    			'대전': [132, 177],
    			'경북': [222, 152],
    			'전북': [112, 210],
    			'대구': [185, 191],
    			'울산': [240, 198],
    			'광주': [62, 259],
    			'경남': [173, 245],
    			'부산': [236, 233],
    			'전남': [118, 278],
    			'제주': [75, 331]
    }
    
    sido_list = {'서울', '인천', '강원', '경기', '충북', '충남', '대전', '경북', '전북', '대구', '울산', '광주', '경남', '부산', '전남', '제주'}
                
    # 통합대기 등급 0~50, 51~100, 101~250, 251~
    # 미세먼지 등급 0~30, 31~80, 81~150, 151~
    # 초미세먼지 등급 0~15, 16~50, 51~100, 101~
    def GetKHAIGradeColor(self, val):
        if val >= 0 and val <= 50:
            return self.grade_color[1]
        elif val >= 51 and val <= 100:
            return self.grade_color[2]
        elif val >= 101 and val <= 250:
            return self.grade_color[3]
        else:
            return self.grade_color[4]

    def GetPM10GradeColor(self, val):
        if val >= 0 and val <= 30:
            return self.grade_color[1]
        elif val >= 31 and val <= 80:
            return self.grade_color[2]
        elif val >= 81 and val <= 150:
            return self.grade_color[3]
        else:
            return self.grade_color[4]

    def GetPM25GradeColor(self, val):
        if val >= 0 and val <= 15:
            return self.grade_color[1]
        elif val >= 16 and val <= 50:
            return self.grade_color[2]
        elif val >= 51 and val <= 100:
            return self.grade_color[3]
        else:
            return self.grade_color[4]

    
    def isNum(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def ChangeTimeString(self, strTime):
        time1 = time.strptime(strTime, "%Y-%m-%d %H:%M")
        strDate = time.strftime("%Y.%m.%d %H:00 기준")
        return strDate
    
    
    def GetSidoAirData(self, sido):
        serviceKey = main.botConfig.GetDataServiceKey()
        url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?numOfRows=200&pageNo=1&sidoName=" + sido + "&ver=1.0&ServiceKey=" + serviceKey + "&_returnType=json"
        
        try:
            r = requests.get(url)
    
            if r.status_code != 200:
                return -1, -1, -1, ''
    
            response = r.json()
            
            items = response['list']
            
            khai_value = 0
            khai_count = 0
            
            pm10_value = 0
            pm10_count = 0
            
            pm25_value = 0
            pm25_count = 0
    
            dataTime = items[0]['dataTime']
            
            for item in items:
                if item.get('khaiValue') != None and self.isNum(item['khaiValue']):
                    khai = int(item['khaiValue'])
                    khai_value += khai
                    khai_count += 1
            
                if item.get('pm10Value') != None and self.isNum(item['pm10Value']):
                    pm10 = int(item['pm10Value'])
                    pm10_value += pm10
                    pm10_count += 1
            
                if item.get('pm25Value') != None and self.isNum(item['pm25Value']):
                    pm25 = int(item['pm25Value'])
                    pm25_value += pm25
                    pm25_count += 1
            
        except requests.exceptions.RequestException as e:
            log.info('Request Exception : %s', e)
            return -1, -1, -1, ''
        except:
            self.PrintException()
            return -1, -1, -1, ''
    
        return int(khai_value / khai_count), int(pm10_value / pm10_count), int(pm25_value / pm25_count), dataTime
    
    
    def SendAirKorea(self, bot, chat_id):
        execute_path = main.botConfig.GetExecutePath()
    
        font_path = execute_path + '/NanumGothicExtraBold.ttf'
        fnt = ImageFont.truetype(font_path, 14)
    
        font2_path = execute_path + '/NanumBarunGothic.ttf'
        fnt2 = ImageFont.truetype(font2_path, 12)
    
        img_map_path = execute_path + '/airmap.png'
        base = Image.open(img_map_path).convert('RGBA')
        khai_img = Image.new('RGBA', base.size, (255,255,255,0))
        drow_khai = ImageDraw.Draw(khai_img)
    
        pm10_img = Image.new('RGBA', base.size, (255,255,255,0))
        drow_pm10 = ImageDraw.Draw(pm10_img)
    
        pm25_img = Image.new('RGBA', base.size, (255,255,255,0))
        drow_pm25 = ImageDraw.Draw(pm25_img)
    
        date = ''
    
        for sido in self.sido_list:
            khai, pm10, pm25, dataTime = self.GetSidoAirData(sido)
        
            if khai == -1 and pm10 == -1 and pm25 == -1:
                break
        
            xy = self.sido_xy.get(sido)
            if xy == None:
                continue
            
            khai_val = str(khai)
            w, h = drow_khai.textsize(khai_val)
            x = xy[0] - (w / 2) - 1
            y = xy[1]
            drow_khai.text((x, y), khai_val, font=fnt, fill=self.GetKHAIGradeColor(int(khai_val)))
            
            pm10_val = str(pm10)
            w, h = drow_pm10.textsize(pm10_val)
            x = xy[0] - (w / 2) - 1
            y = xy[1]
            drow_pm10.text((x, y), pm10_val, font=fnt, fill=self.GetPM10GradeColor(int(pm10_val)))
            
            pm25_val = str(pm25)
            w, h = drow_pm25.textsize(pm25_val)
            x = xy[0] - (w / 2) - 1
            y = xy[1]
            drow_pm25.text((x, y), pm25_val, font=fnt, fill=self.GetPM25GradeColor(int(pm25_val)))

            date = self.ChangeTimeString(dataTime).decode('utf-8')

    

        drow_khai.text((15, 5), u'통합대기', font=fnt, fill=(0, 0, 0, 255))
        drow_khai.text((90, 5), date, font=fnt, fill=(0, 0, 0, 255))
        
        drow_pm10.text((15, 5), u'미세먼지', font=fnt, fill=(0, 0, 0, 255))
        drow_pm10.text((90, 5), date, font=fnt, fill=(0, 0, 0, 255))
    
        drow_pm25.text((15, 5), u'초미세먼지', font=fnt, fill=(0, 0, 0, 255))
        drow_pm25.text((90, 5), date, font=fnt, fill=(0, 0, 0, 255))
    
        # 통합대기 등급 0~50, 51~100, 101~250, 251~
        drow_khai.ellipse(((210,300),(223,312)), fill=(78, 137, 246, 255), outline="white")
        drow_khai.ellipse(((210,318),(223,330)), fill=(91, 212, 100, 255), outline="white")
        drow_khai.ellipse(((210,336),(223,348)), fill=(254, 127, 65, 255), outline="white")
        drow_khai.ellipse(((210,354),(223,366)), fill=(249, 74, 75, 255), outline="white")
        drow_khai.rectangle(((205, 296), (312, 368)), fill=None, outline=(190, 190, 190, 255))
    
        drow_khai.text((227, 300), u'좋음 0~50', font=fnt2, fill=(0, 0, 0, 255))
        drow_khai.text((227, 318), u'보통 51~100', font=fnt2, fill=(0, 0, 0, 255))
        drow_khai.text((227, 336), u'나쁨 101~250', font=fnt2, fill=(0, 0, 0, 255))
        drow_khai.text((227, 354), u'매우 나쁨 251~', font=fnt2, fill=(0, 0, 0, 255))
    
        # 미세먼지 등급 0~30, 31~80, 81~150, 151~
        drow_pm10.ellipse(((210,300),(223,312)), fill=(78, 137, 246, 255), outline="white")
        drow_pm10.ellipse(((210,318),(223,330)), fill=(91, 212, 100, 255), outline="white")
        drow_pm10.ellipse(((210,336),(223,348)), fill=(254, 127, 65, 255), outline="white")
        drow_pm10.ellipse(((210,354),(223,366)), fill=(249, 74, 75, 255), outline="white")
        drow_pm10.rectangle(((205, 296), (312, 368)), fill=None, outline=(190, 190, 190, 255))
    
        drow_pm10.text((227, 300), u'좋음 0~30', font=fnt2, fill=(0, 0, 0, 255))
        drow_pm10.text((227, 318), u'보통 31~80', font=fnt2, fill=(0, 0, 0, 255))
        drow_pm10.text((227, 336), u'나쁨 81~150', font=fnt2, fill=(0, 0, 0, 255))
        drow_pm10.text((227, 354), u'매우 나쁨 151~', font=fnt2, fill=(0, 0, 0, 255))
    
    
        # 초미세먼지 등급 0~15, 16~50, 51~100, 101~
        drow_pm25.ellipse(((210,300),(223,312)), fill=(78, 137, 246, 255), outline="white")
        drow_pm25.ellipse(((210,318),(223,330)), fill=(91, 212, 100, 255), outline="white")
        drow_pm25.ellipse(((210,336),(223,348)), fill=(254, 127, 65, 255), outline="white")
        drow_pm25.ellipse(((210,354),(223,366)), fill=(249, 74, 75, 255), outline="white")
        drow_pm25.rectangle(((205, 296), (312, 368)), fill=None, outline=(190, 190, 190, 255))
    
        drow_pm25.text((227, 300), u'좋음 0~15', font=fnt2, fill=(0, 0, 0, 255))
        drow_pm25.text((227, 318), u'보통 16~50', font=fnt2, fill=(0, 0, 0, 255))
        drow_pm25.text((227, 336), u'나쁨 51~100', font=fnt2, fill=(0, 0, 0, 255))
        drow_pm25.text((227, 354), u'매우 나쁨 101~', font=fnt2, fill=(0, 0, 0, 255))
    
    
        out_khai = Image.alpha_composite(base, khai_img)
        out_pm10 = Image.alpha_composite(base, pm10_img)
        out_pm25 = Image.alpha_composite(base, pm25_img)
    
        out_khai.save('/tmp/air_khai.png')
        out_pm10.save('/tmp/air_pm10.png')
        out_pm25.save('/tmp/air_pm25.png')
            
        #sender.sendMessage(date)
        #sender.sendPhoto(open('/tmp/air_khai.png'))
        #sender.sendPhoto(open('/tmp/air_pm10.png'))
        #sender.sendPhoto(open('/tmp/air_pm25.png'))

        #bot = BotManager.BOTManager().GetBot()
        bot.sendMessage(chat_id, date)
        bot.sendPhoto(chat_id, open('/tmp/air_khai.png'))
        bot.sendPhoto(chat_id, open('/tmp/air_pm10.png'))
        bot.sendPhoto(chat_id, open('/tmp/air_pm25.png'))



