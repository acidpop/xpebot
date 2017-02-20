### 변경 내역

**0.5.12 (2017-02-20)**

/torkim 명령 사용후 토렌트 선택시 일부 특수문자가 포함된 torrent 파일 다운로드가 실패하는 문제 수정

------

**0.5.11 (2017-02-15)**

/torkim 명령 사용시 간혹 Torrent 파일 이름을 제대로 가져오지 못하는 문제 수정

------

**0.5.10 (2017-02-10)**

/torkim 명령 사용시 검색 결과가 없을때 오류 나는 문제 수정

/torkim 명령 결과에 대한 전체 텍스트를 미리 전송 하고 Inline Keyboard 가 보이도록 변경

------

**0.5.9 (2017-01-25)**

/start 명령 수행시 지원하는 명령 키보드가 제대로 표시 되지 않던 문제 수정.

------

**0.5.8 (2017-01-22)**

torrentsearch 동작에 이상이 있는 현상을 수정 하였습니다.

torrent 관련 명령 사용시 봇으로 SIGTERM 이 오는데 해당 시그널을 무시 하도록 변경 하였습니다.

------

**0.5.7 (2017-01-20)**

torrentsearch 명령 수행 후 cancel 을 하지 않고 다른 명령 수행시 오류 발생 부분을 수정하였습니다.

airkorea 수행 시 밤 12시 인경우 python 오류를 수정하였습니다.

------

**0.5.6 (2017-01-02)**

DSM 6.x 전용 bot.sh 파일 추가

DSM 6.x 에서는 최초 설치 후 bot6.sh.ori 파일을 bot.sh 로 복사 하셔서 사용하시면 됩니다.

telepot 이 업데이트 되면서 ReplyKeyboardHide 이름이 ReplyKeyboardRemove 이름으로 변경 되어 소스상에 업데이트 하였습니다.

pip install telepot --upgrade 를 수행 하신 다음 xpebot 을 업데이트 하셔서 사용하시면 됩니다.

토렌트 파일 전송시 파일 이름에 특정 내용이 있을 경우 문자열 인코딩 실패 오류를 수정하였습니다.

------

**0.5.5 (2016-10-26)**

DownloadStation 에서 Torrent 제목에 대괄호([])가 포함 되어 있고 대괄호 사이 공백이 있는 경우 메시지 전송을 못하는 문제 수정

잘못된 Torrent 파일 업로드 시 오류 메시지 전송 하도록 수정 (봇 재시작 후 "/xpebotupdate" 메시지를 보내야 적용 됩니다)

마찬가지로 DSM 6.0 이상 사용자는 "http://blog.acidpop.kr/240" 블로그를 참조 하여 2.Create OR Replace function 코드를 적용 하셔야 합니다.

------

**0.5.4 (2016-10-18)**

Download Station 을 체크 하는 DB Function 업데이트가 있습니다.

※ xpebot 을 0.5.4 버전으로 처음 시작 하시는 분은 아래 과정이 필요 없습니다.

토렌트 파일이나 마그넷 링크 등록시 "파일 다운로드가 시작되었습니다." 라는 메시지 없이 다운로드가 완료 되었습니다 메시지만 오는 

경우가 있어 조건식을 업데이트 하였습니다.

git pull 로 소스 업데이트 하신 다음 봇을 재시작 하신 다음

텔레그램 봇에게 "/xpebotupdate" 메시지를 보내주시면 업데이트가 완료 됩니다.


단, DSM 6.0 이상 사용자는 "http://blog.acidpop.kr/240" 해당 링크를 참조 하여 DownloadStation 계정으로 로그인 한 다음 psql 에 로그인 하여 

"2. Create OR Replace function" 에 해당 하는 코드를 붙여 넣기 하셔서 실행 하시면 됩니다.

------

**0.5.3 (2016-10-17)**

TorrentKim Url 변경 적용 (/torkim 명령 이용시 Torrent 파일이 잘못 다운로드 되는 문제 수정)

------

**0.5.2 (2016-10-12)**

Magnet Link 검출 기능 추가.

Magnet 링크를 봇에게 보내면 Download Station 에 등록하는 기능

------

**0.5.1 (2016-08-29)**

DSM Version Check Bug 수정

------

**0.5.0 (2016-08-29)**

DSM 6.0 이상 버전에서 api 오류들 수정

6.0 이상에서는 다음 과정이 필요하다. (<a href="http://blog.acidpop.kr/240" target="_blank">http://blog.acidpop.kr/240</a>)

------

**0.4.7 (2016-07-20)**

그룹 채팅방에서는 커스텀 키보드가 보이지 않도록 변경

Torrent 파일을 봇에게 전달 하면 오류가 발생하던 문제 수정

------

**0.4.6 (2016-07-01)**

/torkim 또는 /gettorrent 명령 사용시 검색 결과가 없으면 exception 이 발생 하는 문제 수정

검색 결과가 없으면 "검색 결과가 없다는 결과 메시지 전송"

------

**0.4.5 (2016-06-27)**

/torkim 명령 사용시 유니코드 파일명이 정상적으로 다운로드 되지 않는 문제 수정

/airkorea 기능에서 미세먼지와 초미세먼지의 좋음, 나쁨 등급 기준치 수정

Bot 에서 .torrent 파일을 전송 하면 정상적으로 작동 하지 않던 문제 수정

------

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