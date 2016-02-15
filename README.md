**bot.sh.ori, xpebot.cfg.ori 파일은 필히 bot.sh, xpebot.cfg 로 '복사' 하셔서 사용하세요 안그러면 소스 업데이트가 안됩니다.**

------

**3시간 정도 사용 안할 때 BOT이 응답이 없는 문제는 아래 링크를 통해 임시로 해결 하실 수 있습니다**

http://blog.acidpop.kr/214

------

### 변경 내역

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

	4) VALID_USER 는 인증된 사용자의 chat_id 값을 입력한다. 여러명일 경우 ,(콤마)를 이용해 구분한다.

	5) NAVER_API 섹션에 발급 받은 CLIENT_ID_KEY 값과 CLIENT_SECRET_KEY 값을 입력한다.

	6) RSS_NEWS 섹션에 보고 싶은 뉴스의 RSS 주소를 입력한다.

 

9. xpebot 을 다음 명령어로 실행 한다.

```
  시작
  ./bot.sh start
 
  종료 
  ./bot.sh stop
  
  실행 여부 확인
  ./bot.sh chk
```

  
  
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

**/systeminfo**
- NAS System 리소스 조회

**/en2ko**
- 영어 문장을 한글로 기계 번역 (Naver Developers 에 등록된 키가 있어야 함)

**/ko2en**
- 한글 문장을 영어로 기계 번역 (Naver Developers 에 등록된 키가 있어야 함)

**/shorturl**
- url 을 짧게 줄여주는 기능 (Naver Developers 에 등록된 키가 있어야 함)

**/news**
- RSS 뉴스 URL 조회

**/cancel**
- 모드 취소

**/help**
- 도움말

