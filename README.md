XPEnology 전용 Telegram BOT 프로젝트


설치 방법
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
   5) cd xpebot

7. bot.sh 파일을 수정한다.
  1) 3번째 줄의 DSM_ACCOUNT="admin" 이 부분에서 admin 을 자신의 계정으로 변경한다.
  
8. xpebot.cfg 환경 설정 파일을 변경한다.
  1) NOTY_CHAT_ID 는 Downlaod Staion 에서 다운로드 진행 현황 알림을 받을 사용자의 Chat ID 값을 입력한다.
  2) DSM_ID 는 자신의 DSM ID 를 입력한다.
  3) BOT_TOKEN 은 Telegram 의 Bot Father 에서 /newbot 을 요청하여 BOT 생성 후 자신의 BOT TOKEN 값을 입력한다.
 

9. xpebot 을 다음 명령어로 실행 한다.
  ./bot.sh start
 
  종료 
  ./bot.sh stop
  
  실행 여부 확인
  .bot.sh chk
  
10. Telegram 으로 생성한 BOT 에서 다음 메시지를 전송한다.
    /dsdownloadregister
    DS Download 모니터가 등록되었습니다 라고 나오면 성공
  
  
# 사용 방법
  
**/torrentsearch**
- 토렌트 검색

**/weather**
- 동네 날씨 또는 전국 날씨 요약 정보 조회

**/wol**
- Wake On Lan 기능

**/regiwol**
- Wake On Lan Device 등록

**/delwol**
- Wake On Lan Device 삭제

**/dsdownloadregister**
- DS Download 모니터링 Query 등록

**/help**
- 도움말

