#-*- coding: utf-8 -*-
import psycopg2

def UpdateDBFunction():
    try:
        conn = psycopg2.connect(database='download', user='postgres', password='')
        conn.autocommit = True
        curs = conn.cursor()

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

        curs.execute(query.decode('utf-8'))
    except Exception as e:
        print "dsdownload db_connect error"
        print e
        curs.close()
        conn.close()
        return False
    except:
        print 'db update exception!!'
        curs.close()
        conn.close()
        return False

    print 'xpebot database function update complete'
    return True


if __name__ == "__main__":
    print 'try xpebot database function update...'
    UpdateDBFunction()
    
