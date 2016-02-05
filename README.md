**bot.sh.ori, xpebot.cfg.ori 파일은 꼭 bot.sh, xpebot.cfg 로 '복사' 하셔서 사용하세요 안그러면 소스 업데이트가 안됩니다.**

------

### 변경 내역

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
    cd /volume1/homes/{자신의계정}
    
6. xpebot 을 설치 한다.

    1) git clone "https://github.com/acidpop/xpebot"

    2) wget "https://bootstrap.pypa.io/get-pip.py"
   
    3) python ./get-pip.py
   
    4) pip install telepot
   
    5) pip install BeautifulSoup
   
    6) pip install psycopg2
   
    7) cd xpebot
    
    8) cp bot.sh.ori bot.sh
    
    9) cp xpebot.cfg.ori xpebot.cfg

    **bot.sh.ori 파일과 xpebot.cfg.ori 파일은 필히 bot.sh, xpebot.cfg 로 복사 하여 사용**

7. bot.sh 파일을 수정한다.

    1) 3번째 줄의 DSM_ACCOUNT="admin" 이 부분에서 admin 을 자신의 계정으로 변경한다.
  
8. xpebot.cfg 환경 설정 파일을 변경한다.

    1) NOTY_CHAT_ID 는 Downlaod Staion 에서 다운로드 진행 현황 알림을 받을 사용자의 Chat ID 값을 입력한다.
  
    2) DSM_ID 는 자신의 DSM ID 를 입력한다.
  
    3) BOT_TOKEN 은 Telegram 의 Bot Father 에서 /newbot 을 요청하여 BOT 생성 후 자신의 BOT TOKEN 값을 입력한다.
 

9. xpebot 을 다음 명령어로 실행 한다.

    ```
      시작
      ./bot.sh start
     
      종료 
      ./bot.sh stop
      
      실행 여부 확인
      ./bot.sh chk
    ```

10. Telegram 으로 생성한 BOT 에서 다음 메시지를 전송한다.

    **/dsdownloadregister**

    DS Download 모니터가 등록되었습니다 라고 나오면 성공
  

------

## BotFather 에 Command 등록 하기

1. /secommands 메시지 보내기

2. 설정 할 BOT 계정 선택

3. 다음 메시지 보내기

    ```
    torrentsearch - 토렌트 검색
    weather - 날씨 검색
    wol - WOL
    addwol - WOL 장비 추가
    delwol - WOL 장비 삭제
    cancel - 모드 취소
    help - 도움말
    ```

4. Bot Father 에게 Success! Command list updated. /help 메시지가 오면성공


------
  
# 사용 방법
  
**/torrentsearch**
- 토렌트 검색

**/weather**
- 동네 날씨 또는 전국 날씨 요약 정보 조회

**/wol**
- Wake On Lan 기능

**/addwol**
- Wake On Lan Device 등록

**/delwol**
- Wake On Lan Device 삭제

**/dsdownloadregister**
- DS Download 모니터링 Query 등록

**/cancel**
- 모드 취소

**/help**
- 도움말


------
