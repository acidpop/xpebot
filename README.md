**bot.sh.ori, xpebot.cfg.ori 파일은 필히 bot.sh, xpebot.cfg 로 '복사' 하셔서 사용하세요 안그러면 소스 업데이트가 안됩니다.**

------
XPEnology 에서 git 명령 실행시 

fatal: Unable to find remote helper for 'https'

위와 같은 오류가 나는 분들은 다음 글을 이용하여 해결이 될것으로 보입니다.

http://blog.acidpop.kr/228

Telepot 8.1 업데이트시 Torrent 파일을 봇에게 전송 하면 CPU 점유율이 올라가는 문제가 있습니다.

------

### 변경 내역

**0.4.4 (2016-06-01)**

봇 명령시 나오는 사용자 키보드를 그룹 채팅방에서는 앞에 '/' 기호를 붙이도록 변경

Naver API 가 작동 하지 않던 문제 수정

tgbot.db 파일은 최종으로 업데이트 (이후부터는 수정 될 예정 없음)

------

**0.4.3 (2016-05-27)**

Group 대화방에서 Bot 작동 할 수 있도록 추가 개발

Group 대화방에 초대 후 /torrentsearch@xpebot

형태로 커맨드를 보낸 후 /var/log/xpebot.log 를 확인 하면 Group 대화방의 chat id 확인 가능

해당 Group ID 를 xpebot.cfg 의 invalid user 에 추가

그룹 대화방에서 봇은 "/" Slash 가 앞에 있어야만 메시지를 받을 수 있습니다

```
사용자	: /torrentsearch@xpebot
BOT		: 검색 할 Torrent 제목을 입력하세요
사용자	: /다큐멘터리
BOT		: 검색 결과 
```

위와 같은 방법으로 사용 가능하다.

------

**0.4.2 (2016-05-25)**

토렌트 파일 제목에 _ (underbar) 또는 * 문자가 들어가면 메시지를 보내지 못하는 문제 수정
tgbot.db 파일 git pull 할때 오류 시 

git checkout -- tgbot.db

위 명령으로 강제 업데이트 하실 수 있습니다.

tgbot.db 파일은 이 버전 이후에 되도록 업데이트가 없을 예정입니다.

------

**0.4.1 (2016-05-23)**
- tgbot.db 와 torrent 검색 결과를 저장하는 DB를 분리
- Torrent 검색 기능 로그 상세화
- /cancel 모드 도움말에 추가

------

**0.4 (2016-05-19)**
- 다음 패키지를 설치 해야 합니다. pip install Pillow
- Telepot 8.0 (BOT API 2.0) 에 맞춰 업데이트 하였습니다.  easy_install --upgrade telepot 명령을 이용하여 기존 telepot 사용자는 업데이트 하셔야 합니다. telepot 6.x 이하는 사용 불가
- torrent 파일 전송시 Watch Directory 에 파일을 다운로드 합니다. cfg 파일에서 watch_dir 키에 watch_directory 경로를 입력하세요.
- /airkorea - 미세 먼지 조회기능 추가 (data.go.kr 에서 '대기오염정보 조회' API에 대해 활용 신청 후 서비스 키가 필요합니다.)
- /torkim 추가 - TorrentKim 에서 Magnet 이 아닌 Torrent 파일을 검색하여 Watch Directory에 다운로드 하는 기능, 추천 수를 표시합니다 (TorrentKim 사정에 의해 작동이 안될 수 있습니다)
- /gettorrent 추가 - TorrentKim 에서 Magnet 이 아닌 Torrent 파일을 검색하여 사용자에게 파일을 전송 하는 기능 (TorrentKim 사정에 의해 작동이 안될 수 있습니다)
- /namuwiki - 나무 위키에서 키워드를 검색하여 해당 문서 링크를 찾아 주는 기능

/torkim, /gettorrent 명령은 이번에 추가된 BOT API 2.0 을 사용합니다. Inline Keyboard 를 이용하여 사용자에게 선택 버튼을 제공합니다.

xpebot.cfg.ori 와 bot.sh.ori 파일이 업데이트 되었습니다.

다시 복사 하셔서 사용하세요

내부적으로 사용하는 File DB가 업데이트 되었습니다.

tgbot.db 파일을 다른 이름으로 변경 후에 git 소스를 업데이트 하셔야 합니다.

기존에 등록된 WOL 데이터를 다시 등록 하셔야 합니다.

입력 시간 초과 기능은 삭제 되었습니다.

0.4 버전에서 Telepot 8.0 버전을 지원하며 새로운 기능들이 추가 되어서 작동이 안될 수 있습니다.

문의 사항이 있으시면 http://blog.acidpop.kr/notice/225 블로그 또는 github 의 issue 를 이용하여주세요.


------

**0.3 (2016-02-15)**
- bot.sh 에서 실행 경로 변경(/volume1/homes -> /var/service/homes)
- 날씨 정보 조회시 시,도,구가 다르고 동 이름이 같을 경우 요약 정보를 잘 못 보내던 문제 수정

bot.sh.ori 파일이 업데이트 되었습니다.

------

**0.2 (2016-02-13)**
- RSS 뉴스 리더 기능 추가
- NAS 의 시스템 리소스 조회 기능 추가(cpu, ram, disk)
- /start 명령 추가 (사용 가능 기능을 Custom Keyboard로 보여주기)
- 등록 되지 않은 명령어 입력시 /start 명령과 동일한 동작을 하도록 변경
- 네이버 REST Open API 일부 기능 지원 (Naver Developers 에 내 애플리케이션이 등록 되어 있어야 하고 비로그인 오픈 API 기능이 체크 되어야 함)
- xpebot.cfg 에 Naver API 와 RSS 링크 섹션 추가
- dsdownloadregister 명령 삭제
- DS Download Monitor Query 는 자동으로 등록 하도록 변경
- Torrent 검색 목록이 Custom Keyboard 로만 보여지던것을 메시지에도 표시
- /로 시작하는 명령 입력 후 사용자 입력이 120초(2분) 이내에 응답이 없으면 '입력 시간이 초과 되었습니다' 라는 메시지 전송하고 초기 모드로 돌아감
- 날씨 정보에서 풍향을 XX풍에서 XX향 으로 변경
- 날씨 정보에서 'C 를 ℃ 문자로 변경
- BOT 시작시 보내는 메시지 삭제

xpebot.cfg.ori 와 bot.sh.ori 파일이 업데이트 되었습니다.

다시 복사 하셔서 사용하세요

------

**0.1 (2016-02-05)**

- /regiwol 을 /addwol 로 변경
- Download Station 에서 대상 경로가 한글 일 경우 작동 안되는 문제  
- 동네 날씨 조회시 계속 같은 정보를 보내주는 문제 수정
- xpebot.cfg 에서 VALID_USER 에 콤마가 없을 경우 오작동 하는 문제 수정
 
 
 ------



#XPEnology 전용 Telegram BOT 프로젝트


##설치 방법

1. DSM 에 접속하여 패키지 센터에서 "Git Server", "Python Module", "Download Station" 을 설치 한다.

2. Download Station 을 실행 하여 대상 경로를 설정 한다.

3. DSM 의 제어판에서 터미널 및 SNMP 항목을 클릭 후 "SSH 서비스 활성화"를 체크한다.

   제어판에서 사용자 항목으로 이동 후 고급 탭에서 "사용자 홈 서비스 활성화"를 체크한다.

   적용 버튼을 누른다. 

4. SSH 접속 툴(putty 또는 xshell등)을 이용하여 XPEnology IP 주소로 접속한다.

    (5.2-5644 기준으로 ID 는 'root' 암호는 관리자 계정(admin)의 암호이다) 

5. SSH로 접속 하였다면 자신의 홈 디렉토리로 이동한다. 

    cd /var/services/homes/{자신의계정}
    
6. xpebot 을 설치 한다.

    1) git clone "https://github.com/acidpop/xpebot"

    2) wget "https://bootstrap.pypa.io/get-pip.py"
   
    3) python ./get-pip.py
   
    4) pip install telepot
   
    5) pip install BeautifulSoup
   
    6) pip install psycopg2
    
    7) pip install Pillow
   
    8) cd xpebot
    
    9) cp bot.sh.ori bot.sh
    
    10) cp xpebot.cfg.ori xpebot.cfg

    **bot.sh.ori 파일과 xpebot.cfg.ori 파일은 필히 bot.sh, xpebot.cfg 로 복사 하여 사용**

7. bot.sh 파일을 수정한다.

    1) 3번째 줄의 DSM_ACCOUNT="admin" 이 부분에서 admin 을 자신의 계정으로 변경한다.
  
8. xpebot.cfg 환경 설정 파일을 변경한다.

    1) NOTY_CHAT_ID 는 Downlaod Staion 에서 다운로드 진행 현황 알림을 받을 사용자의 Chat ID 값을 입력한다.
  
    2) DSM_ID 는 자신의 DSM ID 를 입력한다.
  
    3) BOT_TOKEN 은 Telegram 의 Bot Father 에서 /newbot 을 요청하여 BOT 생성 후 자신의 BOT TOKEN 값을 입력한다.

	4) VALID_USER 는 인증된 사용자의 chat_id 값을 입력한다. 여러명일 경우 ,(콤마)를 이용해 구분한다.

	5) NAVER_API 섹션에 발급 받은 CLIENT_ID_KEY 값과 CLIENT_SECRET_KEY 값을 입력한다.

	6) RSS_NEWS 섹션에 보고 싶은 뉴스의 RSS 주소를 입력한다.
    
    7) DATA 섹션에 data.go.kr 에서 발급 받은 서비스 키를 입력한다.

 

9. xpebot 을 다음 명령어로 실행 한다.

    ```
      시작
      ./bot.sh start
     
      종료 
      ./bot.sh stop
      
      실행 여부 확인
      ./bot.sh chk
    ```

  

------

## BotFather 에 Command 등록 하기

1. /secommands 메시지 보내기

2. 설정 할 BOT 계정 선택

3. 다음 메시지 보내기

    ```
    torrentsearch - 토렌트 검색
    weather - 동네 날씨 또는 전국 날씨 요약 정보 조회
    wol - Wake On Lan 기능
    systeminfo - NAS System 리소스 조회
    en2ko - 영어 문장을 한글로 기계 번역
    ko2en - 한글 문장을 영어로 기계 번역
    shorturl - url 을 짧게 줄여주는 기능
    txt2voice - 한글 문장을 음성으로 변환
    news - RSS 뉴스 URL 조회
    airkorea - 통합대기 지수 조회
    namuwiki - Namu Wiki 조회
    torkim - TorrentKim 조회
	gettorrent - TorrentKim 조회 후 토렌트 파일 다운로드
    help - 도움말
    ```

4. Bot Father 에게 Success! Command list updated. /help 메시지가 오면성공


------
  
# 사용 방법
  
**/torrentsearch**
- 토렌트 검색

**/torkim**
- Torrent Kim 조회

**/gettorrent**
- Torrent Kim 조회 후 Torrent 파일 받기

**/weather**
- 동네 날씨 또는 전국 날씨 요약 정보 조회

**/wol**
- Wake On Lan 기능

**/addwol**
- Wake On Lan Device 등록

**/delwol**
- Wake On Lan Device 삭제

**/systeminfo**
- NAS System 리소스 조회

**/en2ko**
- 영어 문장을 한글로 기계 번역 (Naver Developers 에 등록된 키가 있어야 함)

**/ko2en**
- 한글 문장을 영어로 기계 번역 (Naver Developers 에 등록된 키가 있어야 함)

**/shorturl**
- url 을 짧게 줄여주는 기능 (Naver Developers 에 등록된 키가 있어야 함)

**/txt2voice**
- 한글 문장을 음성으로 변환

**/airkorea**
- 통합대기 지수 조회 (data.go.kr 에서 대기오염정보 조회 API 서비스 키가 필요 함)

**/namuwiki**
- Namu Wiki 조회

**/news**
- RSS 뉴스 URL 조회

**/cancel**
- 모드 취소

**/help**
- 도움말


------
