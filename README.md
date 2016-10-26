**bot.sh.ori, xpebot.cfg.ori 파일은 필히 bot.sh, xpebot.cfg 로 '복사' 하셔서 사용하세요 안그러면 소스 업데이트가 안됩니다.**

------

### 자주 묻는 질문

- 사용자들이 자주 접하게 되는 문제들은 아래 링크로 대체 하였습니다.

- **[QNA.md](https://github.com/acidpop/xpebot/blob/master/QNA.md)** 이 링크를 참고하세요

------

### 이번 업데이트 내역

**0.5.5 (2016-10-26)**

DownloadStation 에서 Torrent 제목에 대괄호([])가 포함 되어 있고 대괄호 사이 공백이 있는 경우 메시지 전송을 못하는 문제 수정

DownloadStation 에서 Torrent 다운로드 도중에 제거 하였을 경우 다운로드 취소 메시지 전송 기능 추가

잘못된 Torrent 파일 업로드 시 오류 메시지 전송 하도록 수정 (봇 재시작 후 "/xpebotupdate" 메시지를 보내야 적용 됩니다)

마찬가지로 DSM 6.0 이상 사용자는 "http://blog.acidpop.kr/240" 블로그를 참조 하여 2.Create OR Replace function 코드를 적용 하셔야 합니다.

------

### 자세한 변경 사항은 다음 링크 참조

- 변경 내역이 길어져서 changelog 파일을 별도로 분리 하였습니다.

- **[CHANGELOG.md](https://github.com/acidpop/xpebot/blob/master/CHANGELOG.md)** 이 링크를 참고하세요

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

5. DSM 6.0 이상 사용자는 다음 링크를 참고하여 DB에 코드를 업데이트해야 한다.

- **[DSM 6.0 xpebot 설정하기](http://blog.acidpop.kr/240)**

6. SSH로 접속 하였다면 자신의 홈 디렉토리로 이동한다. 

    cd /var/services/homes/{자신의계정}
    
7. xpebot 을 설치 한다.

    1) git clone "https://github.com/acidpop/xpebot"

    2) wget "https://bootstrap.pypa.io/get-pip.py"
   
    3) python ./get-pip.py
   
    4) pip install telepot
   
    5) pip install BeautifulSoup
   
    6) pip install psycopg2
    
    7) pip install Pillow
    
    8) pip install psutil
   
    9) cd xpebot
    
    10) cp bot.sh.ori bot.sh
    
    11) cp xpebot.cfg.ori xpebot.cfg

    **bot.sh.ori 파일과 xpebot.cfg.ori 파일은 필히 bot.sh, xpebot.cfg 로 복사 하여 사용**

8. bot.sh 파일을 수정한다.

    1) 3번째 줄의 DSM_ACCOUNT="admin" 이 부분에서 admin 을 자신의 계정으로 변경한다.
  
9. xpebot.cfg 환경 설정 파일을 변경한다.

    1) NOTY_CHAT_ID 는 Downlaod Staion 에서 다운로드 진행 현황 알림을 받을 사용자의 Chat ID 값을 입력한다.
  
    2) DSM_ID 는 자신의 DSM ID 를 입력한다.
  
    3) BOT_TOKEN 은 Telegram 의 Bot Father 에서 /newbot 을 요청하여 BOT 생성 후 자신의 BOT TOKEN 값을 입력한다.

	4) VALID_USER 는 인증된 사용자의 chat_id 값을 입력한다. 여러명일 경우 ,(콤마)를 이용해 구분한다.

	5) NAVER_API 섹션에 발급 받은 CLIENT_ID_KEY 값과 CLIENT_SECRET_KEY 값을 입력한다.

	6) RSS_NEWS 섹션에 보고 싶은 뉴스의 RSS 주소를 입력한다.
    
    7) DATA 섹션에 data.go.kr 에서 발급 받은 서비스 키를 입력한다.

 

10. xpebot 을 다음 명령어로 실행 한다.

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
