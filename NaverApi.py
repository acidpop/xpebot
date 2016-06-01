#-*- coding: utf-8 -*-

import main
import cmdutil
import time
import json
import os
import requests
from LogManager import log


# 베타 테스트 중입니다. 정식으로 사용 할 수 없는 기능입니다.

class NaverApi(object):
    """description of class"""
    #TOKEN = main.botConfig.GetBotToken()
    naver_api_use = main.botConfig.GetNaverApiUse()
    naver_client_id = main.botConfig.GetNaverClientId()
    naver_client_secret = main.botConfig.GetNaverClientSecret()

    def TranslateEn2Ko(self, text, bot, chat_id):

        if self.naver_api_use == False:
            return 'Not Support'

        text = text.replace('"', '\\"')
        
        data = {'source' : 'en',
                'target' : 'ko',
                'text' : text}
        header = {'X-Naver-Client-Id': self.naver_client_id,
                  'X-Naver-Client-Secret': self.naver_client_secret
                  }

        req_data = requests.post('https://openapi.naver.com/v1/language/translate', data=data, headers=header)

        if req_data.status_code != 200:
            log.info('TranslateEn2Ko Requests error:%d, text:%s' % req_data.status_code, text)
            return

        response_json = req_data.content

        response = json.loads(response_json.decode('utf-8'))

        if response['message'] and response['message']['result'] and response['message']['result']['translatedText']:
            translateText = response['message']['result']['translatedText']
            log.info('Translate Message : %s', translateText)
        else:
            log.info('Translate Fail')
            log.info(response_json)
            translateText = response['errorMessage']

        bot.sendMessage(chat_id, translateText)
        
        return


    def TranslateKo2En(self, text, bot, chat_id):
        if self.naver_api_use == False:
            return 'Not Support'

        text = text.replace('"', '\\"')

        data = {'source' : 'ko',
                'target' : 'en',
                'text' : text}
        header = {'X-Naver-Client-Id': self.naver_client_id,
                  'X-Naver-Client-Secret': self.naver_client_secret
                  }

        req_data = requests.post('https://openapi.naver.com/v1/language/translate', data=data, headers=header)

        if req_data.status_code != 200:
            log.info('TranslateKo2En Requests error:%d, text:%s' % req_data.status_code, text)
            return

        response_json = req_data.content

        response = json.loads(response_json.decode('utf-8'))

        if response['message'] and response['message']['result'] and response['message']['result']['translatedText']:
            translateText = response['message']['result']['translatedText']
            log.info('Translate Message : %s', translateText)
        else:
            log.info('Translate Fail')
            log.info(response_json)
            translateText = response['errorMessage']
        
        bot.sendMessage(chat_id, translateText)
        return

    def ShortUrl(self, url, bot, chat_id):
        if self.naver_api_use == False:
            return 'Not Support'

        data = {'url' : url}
        header = {'X-Naver-Client-Id': self.naver_client_id,
                  'X-Naver-Client-Secret': self.naver_client_secret
                  }

        req_data = requests.post('https://openapi.naver.com/v1/util/shorturl', data=data, headers=header)

        if req_data.status_code != 200:
            log.info('ShortUrl Requests error:%d, url:%s' % req_data.status_code, url)
            return

        response_json = req_data.content

        log.info('Naver API ShortUrl Response : %s', response_json)
        response = json.loads(response_json)

        if response['message'] == 'ok':
            short_url = response['result']['url']
        else:
            short_url = response['message']

        log.info('Naver API ShortUrl Result : %s', short_url)
        
        bot.sendMessage(chat_id, short_url)
        return


    def TextToVoice(self, text, bot, chat_id):
        headers = {'X-Naver-Client-Id' : self.naver_client_id, 'X-Naver-Client-Secret' : self.naver_client_secret}
        # mijin:미진(한국어, 여성)
        # jinho:진호(한국어, 남성)
        # clara:클라라(영어, 여성)
        # matt:매튜(영어, 남성)
        # yuri:유리(일본어, 여성)
        # shinji:신지(일본어, 남성)
        # meimei:메이메이(중국어, 여성)

        # -5 ~ 5 사이 정수로 -5면 0.5배 빠른, 5면 0.5배 느린, 0이면 정상 속도
        data = {'speaker': 'mijin', 'speed': 0, 'text': text}

        r = requests.post('https://openapi.naver.com/v1/voice/tts.bin', data = data, headers = headers)

        now = time.localtime()
        fname = '/tmp/%d%02d%02d%02d%02d%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        f = open(fname, 'wb')
        f.write(r.content)
        f.close()
        
        response = bot.sendVoice(chat_id, open(fname, 'rb'))

        log.info('TextToVoice, len:%d', len(r.content))

        #os.remove(fname)

        return response['voice']['file_id']


