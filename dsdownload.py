#-*- coding: utf-8 -*-
import main
import psycopg2
import CommonUtil
import telepot
import traceback

from LogManager import log


# psycopg2 document page : http://initd.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries

class dsdownload(object):
    """description of class"""

    #global conn
    #global curs

    TOKEN = main.botConfig.GetBotToken()
    dsm_id = main.botConfig.GetDsmId()
    chat_id = main.botConfig.GetChatId()

    conn = None
    curs = None

    bot = telepot.Bot(TOKEN)
    

    def db_connect(self, host='localhost', dbname='download', user='postgres', password=''):
        #global curs
        #global conn

        try:
            self.conn = psycopg2.connect(database=dbname, user=user, password=password)
            self.conn.autocommit = True
        except Exception as e:
            log.error("dsdownload db_connect error")
            log.error(e)
            return False

        self.curs = self.conn.cursor()

        return True

    def db_query(self, query):
        
        ret = True
        if self.curs == None:
            ret = self.db_connect()

        if ret == True:
            try:
                self.curs.execute(query.decode('utf-8'))
                result = self.curs.fetchall()
            except psycopg2.IntegrityError as err:
                if err.pgcode != '23505':
                    log.error('db_query|DB IntegrityError : %s',  err)
                else:
                    log.error('db_query|DB Not Intergrity Error : %s', err)
                
                self.curs.close()
                self.conn.close()
                self.curs = None
            except Exception as err:
                log.error('db_query|DB Exception : %s',  err)
                self.curs.close()
                self.conn.close()
                self.curs = None
                return False, ''
            except:
                log.error("db_query|psycopg except : " + e)
                self.curs.close()
                self.conn.close()
                self.curs = None
                return False, ''
        
        return True, result

        

    def db_exec(self, query):
        ret = True
        if self.curs == None:
            ret = self.db_connect()

        if ret == True:
            try:
                self.curs.execute(query)
                log.info('db_exec complete')
                return True
            except psycopg2.IntegrityError as err:
                if err.pgcode != '23505':
                    log.error('db_exec|DB IntegrityError : %s',  err)
                else:
                    log.error('db_exec|DB Not Intergrity Error : %s', err)
                
                self.curs.close()
                self.conn.close()
                self.curs = None
            except Exception as err:
                log.error('db_exec|DB Exception : %s',  err)
                self.curs.close()
                self.conn.close()
                self.curs = None
            except:
                log.error("db_exec|psycopg except : " + e)
                self.curs.close()
                self.conn.close()
                self.curs = None

        return False

    

    def CreateMonitorTable(self):
        
        query = """CREATE TABLE btdownload_event(
    task_id           integer   NOT NULL,
    username          character varying(128),
    filename          text,
    status            integer,
    total_size        bigint,
    isread            integer,
    create_time       date
);"""

        if self.db_exec(query) :
            log.info('CreateMonitorTable Success')
        else:
            log.info('CreateMonitorTable Fail')

        return

    def CreateMonitorProcedure(self):
        query = """CREATE OR REPLACE FUNCTION process_btdownload_event() RETURNS TRIGGER AS $btdownload_event$
    DECLARE
        rec_count integer;
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            RETURN NEW;
        ELSIF (TG_OP = 'UPDATE') THEN
            IF (NEW.status = 2 AND NEW.total_size > 0 AND NEW.current_size > 0) THEN
                SELECT COUNT(*) into rec_count FROM btdownload_event WHERE task_id = NEW.task_id AND status = 2;
                IF ( rec_count = 0 ) THEN
                    INSERT INTO btdownload_event VALUES(NEW.task_id, NEW.username, NEW.filename, NEW.status, NEW.total_size, 0, now());
                END IF;
            ELSIF (NEW.status = 5 ) THEN
                SELECT COUNT(*) into rec_count FROM btdownload_event WHERE task_id = NEW.task_id AND status = 5;
                IF ( rec_count = 0 ) THEN
                    INSERT INTO btdownload_event VALUES(NEW.task_id, NEW.username, NEW.filename, NEW.status, NEW.total_size, 0, now());
                END IF;
            ELSIF (NEW.status = 118) THEN
                UPDATE download_queue SET status = 5, extra_info = '' WHERE task_id = NEW.task_id;
                DELETE FROM task_plugin WHERE task_id = NEW.task_id;
                DELETE FROM thumbnail WHERE task_id = NEW.task_id;
            END IF;
            RETURN NEW;
        ELSIF (TG_OP = 'DELETE') THEN
                DELETE FROM btdownload_event WHERE task_id = OLD.task_id;
            RETURN OLD;
        END IF;
        RETURN NULL;
    END;
$btdownload_event$ LANGUAGE plpgsql;"""

        if self.db_exec(query) :
            log.info('CreateMonitorProcedure Success')
        else:
            log.info('CreateMonitorProcedure Fail')

        return


    def CreateMonitorTrigger(self):
        query = """CREATE TRIGGER btdownload_event
AFTER INSERT OR UPDATE OR DELETE ON download_queue
FOR EACH ROW EXECUTE PROCEDURE process_btdownload_event();"""

        if self.db_exec(query) :
            log.info('CreateMonitorTrigger Success')
        else:
            log.info('CreateMonitorTrigger Fail')

        return

    def dsdown_status_to_str(self, status):
        if status == 1:
            return "대기 중"
        elif status == 2:
            return "다운로드 중"
        elif status == 3:
            return "일시 정지"
        elif status == 4:
            return "종료 중"
        elif status == 5:
            return "다운로드 완료"
        elif status == 6:
            return "해시 체크 중"
        elif status == 7:
            return "시딩 중"
        elif status == 8:
            return "파일 호스팅 대기"
        elif status == 9:
            return "압축 해제 중"
        else:
            return "알 수 없는 코드 [" + str(status) + "]"


    def CheckDownloadMonitorTable(self):

        log.info('CheckDownloadMonitorTable start...')

        # Check DSM Version
        ver = CommonUtil.GetDSMMajorVersion()
        if ver != "5":
            log.info("DSM Major Version : %s, Create Table pass", ver)
            return

        log.info("DSM Major Version : %s, DownloadStation Table Check", ver)

        ret = True
        if self.curs == None:
            ret = self.db_connect()

        
        if ret == True:
            table_query = "select count(*) from information_schema.tables where table_name = 'btdownload_event';"
            proc_query = "select count(*) from pg_proc where proname = 'process_btdownload_event';"
            trigger_query = "select count(*) from pg_trigger where tgname = 'btdownload_event';"

            try:
                # Check Table Exist
                self.curs.execute(table_query)
                rowitem = self.curs.fetchone()
                if rowitem[0] == 0:
                    log.info('monitor table is not exist.. try create table')
                    self.CreateMonitorTable()
                    self.bot.sendMessage(self.chat_id, 'DS Download Monitor Table 등록')

                # Check Procedure Exist
                self.curs.execute(proc_query)
                rowitem = self.curs.fetchone()
                if rowitem[0] == 0:
                    log.info('monitor procedure is not exist.. try create procedure')
                    self.CreateMonitorProcedure()
                    self.bot.sendMessage(self.chat_id, 'DS Download Monitor Procedure 등록')

                # Check Trigger Exist
                self.curs.execute(trigger_query)
                rowitem = self.curs.fetchone()
                if rowitem[0] == 0:
                    log.info('monitor trigger is not exist... try create trigger')
                    self.CreateMonitorTrigger()
                    self.bot.sendMessage(self.chat_id, 'DS Download Monitor Trigger 등록')

            except psycopg2.IntegrityError as err:
                if err.pgcode != '23505':
                    log.error('CheckDownloadMonitorTable|DB IntegrityError : %s',  err)
                else:
                    log.error('CheckDownloadMonitorTable|DB Not Intergrity Error : %s', err)
                self.curs.close()
                self.conn.close()
                self.curs = None
            except Exception as err:
                log.error('CheckDownloadMonitorTable|DB Exception : %s',  err)
                self.curs.close()
                self.conn.close()
                self.curs = None
            except:
                log.error("CheckDownloadMonitorTable|psycopg except : " + e)
                self.curs.close()
                self.conn.close()
                self.curs = None

            log.info('CheckDownloadMonitorTable exit...')
            return

    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        #print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
        log.info('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

    def download_db_timer(self):
        ret = True
        if self.curs == None:
            ret = self.db_connect()

        if ret == True:
            query = 'SELECT * FROM btdownload_event WHERE isread=0;'
            try:
                self.curs.execute(query)
                rowitems = self.curs.fetchall()
                if len(rowitems) > 0:
                    for row in rowitems:
                        # task_id|username|filename|status|total_size|isread|create_time
                        task_id = row[0]
                        username = row[1]
                        tor_name = row[2]
                        status = self.dsdown_status_to_str(row[3])
                        total_size = CommonUtil.hbytes(row[4])

                        # bot.sendMessage(24501560, "<b>Bold Text</b>\n<pre color='blue'>Test Message</pre>\nHTML Mode", parse_mode='HTML')
                        # Markdown 문법에서 _ 는 * 로 대체 되므로 \_ 로 변경
                        tor_name = tor_name.replace('_', '\_')
                        # Markdown 문법에서 *는 MarkDown 문법을 시작하는 문자이므로 \* 로 변경
                        tor_name = tor_name.replace('*', '\*')

                        msg = '*상태* : %s\n*이름* : %s\n*크기* : %s\n*사용자* : %s' % (status, tor_name, total_size, username)
                        
                        self.bot.sendMessage(self.chat_id, msg, parse_mode='Markdown')

                        query = "UPDATE btdownload_event SET isread = 1 WHERE task_id = %d" % (task_id)
                        self.curs.execute(query)
            except psycopg2.IntegrityError as err:
                if err.pgcode != '23505':
                    log.error('download_db_timer|DB IntegrityError : %s',  err)
                else:
                    log.error('download_db_timer|DB Not Intergrity Error : %s', err)
                self.curs.close()
                self.conn.close()
                self.curs = None
            except Exception as err:
                log.error('download_db_timer|DB Exception : %s',  err)
                log.error("download_db_timer Exception : %s", traceback.format_exc())
                strErr = str(err.message)
                log.error('error ---- %s, %d', strErr, strErr.find('relation "btdownload_event" does not exist'))
                if strErr.find('relation "btdownload_event" does not exist') != -1:
                    self.CheckDownloadMonitorTable()

                self.curs.close()
                self.conn.close()
                self.curs = None
            except:
                log.error("download_db_timer|psycopg except : " + e)
                self.curs.close()
                self.conn.close()
                self.curs = None
            #finally:
                



