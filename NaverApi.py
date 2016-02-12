#-*- coding: utf-8 -*-

import main
import cmdutil
import json
from LogManager import log


# 베타 테스트 중입니다. 정식으로 사용 할 수 없는 기능입니다.

class NaverApi(object):
    """description of class"""
    #TOKEN = main.botConfig.GetBotToken()
    naver_api_use = main.botConfig.GetNaverApiUse()
    naver_client_id = main.botConfig.GetNaverClientId()
    naver_client_secret = main.botConfig.GetNaverClientSecret()

    def TranslateEn2Ko(self, text, sender):

        if self.naver_api_use == False:
            return 'Not Support'

        text = text.replace('"', '\\"')
        
        cmd = 'curl -s -k -H "X-Naver-Client-Id: %s" -H "X-Naver-Client-Secret: %s" -d "source=en" -d "target=ko" -d "text=%s" https://openapi.naver.com/v1/language/translate' % (self.naver_client_id, self.naver_client_secret, text)
        log.info('Naver API TranslateEn2Ko Command : %s', cmd)
        response_json = cmdutil.ExecuteCommand(cmd.encode('utf-8'))

        response = json.loads(response_json.decode('utf-8'))

        if response['message'] and response['message']['result'] and response['message']['result']['translatedText']:
            translateText = response['message']['result']['translatedText']
            log.info('Translate Message : %s', translateText)
        else:
            log.info('Translate Fail')
            log.info(response_json)
            translateText = response['errorMessage']
        
        return translateText


    def TranslateKo2En(self, text, sender):
        if self.naver_api_use == False:
            return 'Not Support'

        text = text.replace('"', '\\"')

        cmd = 'curl -s -k -H "X-Naver-Client-Id: %s" -H "X-Naver-Client-Secret: %s" -d "source=ko" -d "target=en" -d "text=%s" https://openapi.naver.com/v1/language/translate' % (self.naver_client_id, self.naver_client_secret, text)
        log.info('Naver API TranslateKo2En Command : %s', cmd)
        response_json = cmdutil.ExecuteCommand(cmd.encode('utf-8'))

        response = json.loads(response_json.decode('utf-8'))

        if response['message'] and response['message']['result'] and response['message']['result']['translatedText']:
            translateText = response['message']['result']['translatedText']
            log.info('Translate Message : %s', translateText)
        else:
            log.info('Translate Fail')
            log.info(response_json)
            translateText = response['errorMessage']
        
        return translateText

    def ShortUrl(self, url, sender):
        # curl -s -k -H "X-Naver-Client-Id: YLjsWM1fVoSKeTsJpYu0" -H "X-Naver-Client-Secret: xjQFC37UAJ" -d "url=%s" https://openapi.naver.com/v1/util/shorturl
        # {message=ok, result={hash=GNALNDIU, url=http://me2.do/GNALNDIU, orgUrl=https://github.com/nickoala/telepot/blob/master/examples/emodi.py}, code=200}
        if self.naver_api_use == False:
            return 'Not Support'

        cmd = 'curl -s -k -H "X-Naver-Client-Id: %s" -H "X-Naver-Client-Secret: %s" -d "url=%s" https://openapi.naver.com/v1/util/shorturl.json' % (self.naver_client_id, self.naver_client_secret, url)
        log.info('Naver API ShortUrl Command : %s', cmd)
        response_json = cmdutil.ExecuteCommand(cmd.encode('utf-8'))

        log.info('Naver API ShortUrl Response : %s', response_json)
        response = json.loads(response_json)

        if response['message'] == 'ok':
            short_url = response['result']['url']
        else:
            short_url = response['message']

        log.info('Naver API ShortUrl Result : %s', short_url)
        
        return short_url

