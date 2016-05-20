#-*- coding: utf-8 -*-
import socket
import re
import sqlite3

import main
from LogManager import log

class wol(object):
    """description of class"""

    db_path = main.botConfig.GetExecutePath() + "/tgbot.db"

    def GetMacHex(self, macAddress, separator=":"):
        if(macAddress.find(separator) == -1):
            separator = "-"
        macHex = macAddress.lower().replace(separator, "")
        if(re.match("[0-9a-f]{12}$", macHex)):
            return macHex.decode("hex")
        else:
            log.warning("MAC Address is not valid [" + macAddress + "]")
            raise Exception("MAC address is not valid")

    # port 는 9번 포트로 설정 하였으나 혹여 다른 포트로 변경이 필요하다면 아래 port=9 에서 포트 번호만 변경
    def WakeOnLan(self, MAC, BroadCastAddr="192.168.0.1", port=9):
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sendBytes = soc.sendto("\xff"*6 + self.GetMacHex(MAC)*16, (BroadCastAddr, port))
        log.info("Wake On Lan Execute - MAC[%s], Broadcast[%s], Port[%d], SendByte[%d]", MAC, BroadCastAddr, port, sendBytes)
        return sendBytes

    def WOLDeviceCount(self):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()

        query = "SELECT COUNT(MAC) FROM WOL_DEVICE;"
        cursor.execute(query)

        row = cursor.fetchone()

        count = row[0]

        cursor.close()
        db.close()

        log.info("WOL Device Count[%d]", count)

        return count

    def AddDevice(self, MAC, DeviceName, BroadCastAddr="192.168.0.1"):
        # insert into wol_device (MAC, DEVNAME, BROADCAST_ADDR, REG_DATE) values('28:92:4A:30:6E:A7', 'test', '192.168.0.1' datetime('now','localtime'));
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = u"INSERT INTO WOL_DEVICE (MAC, DEVNAME, BROADCAST_ADDR, REG_DATE) VALUES('%s', '%s', '%s', datetime('now','localtime'));" % (MAC, DeviceName, BroadCastAddr)
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()

        log.info("WOL Add Device, MAC[%s], Name[%s], Broadcast[%s]", MAC, DeviceName, BroadCastAddr)

        return True

    def RegiDevice(self, command, bot, chat_id):
        # Command 를 ',' 로 파싱하여 AddDevice
        parts = command.split(",")
        if len(parts) <= 0 or len(parts) > 3:
            bot.sendMessage(chat_id, u'형식이 맞지 않습니다')
            return False
        
        MAC = parts[0].strip()
        DevName = parts[1].strip()
        if len(parts) == 3:
            BroadAddr = parts[2].strip()
        else:
            BroadAddr = '192.168.0.255'
            
        if self.AddDevice(MAC, DevName, BroadAddr):
            bot.sendMessage(chat_id, u'등록 되었습니다')
        else:
            bot.sendMessage(chat_id, u'등록 실패')

        return True

    def UnregiDevice(self, SelectDevice, bot, chat_id):
        items = SelectDevice.split("|")

        if len(items) < 2:
            bot.sendMessage(chat_id, u'형식이 잘못 되었습니다')
            return

        DevName = items[0].strip()
        MAC = items[1].strip()

        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = u"DELETE FROM WOL_DEVICE WHERE MAC = '%s'" % (MAC)
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()

        hide_keyboard = {'hide_keyboard': True}
        msg = SelectDevice + u' WOL Device 삭제 완료'
        bot.sendMessage(chat_id, msg, reply_markup=hide_keyboard)

        log.info("WOL Delete Device, MAC[%s], Name[%s]", MAC, DevName)


    def ShowWOLDeviceList(self, sendMsg, bot, chat_id):
        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = "SELECT * FROM WOL_DEVICE;"
        cursor.execute(query)

        rowdata = cursor.fetchall()

        if len(rowdata) == 0:
            bot.sendMessage(chat_id, u'WOL - 등록 된 Device가 없습니다')
        else:
            outList = []
            # TABLE : IDX[0], MAC[1], DEVNAME[2], BROADCAST_ADDR[3], REG_DATE[4]
            for row in rowdata:
                keyboard_title = row[2] + " | " + row[1]
                templist = []
                templist.append(keyboard_title)
                outList.append(templist)

            wol_keyboard = {'keyboard': outList, 'resize_keyboard': True}
            bot.sendMessage(chat_id, sendMsg, reply_markup=wol_keyboard)

        cursor.close()
        db.close()

    def WOLDevice(self, SelectDevice, bot, chat_id):

        items = SelectDevice.split("|")
        DevName = items[0].strip()
        MAC = items[1].strip()

        db = sqlite3.connect(self.db_path)
        cursor = db.cursor()
        query = u"SELECT * FROM WOL_DEVICE WHERE MAC LIKE '%s'" % (MAC)
        cursor.execute(query)

        hide_keyboard = {'hide_keyboard': True}

        row = cursor.fetchone()
        if len(row) == 0:
            bot.sendMessage(chat_id, u'없는 Device', reply_markup=hide_keyboard)
        else:
            WOL_MAC = row[1]
            WOL_DEV_NAME = row[2]
            WOL_BROAD_ADDR = row[3]
            #def WakeOnLan(self, MAC, BroadCastAddr="192.168.0.1", port=9):
            self.WakeOnLan(WOL_MAC, WOL_BROAD_ADDR)
            msg = u'WOL 요청 완료 - %s' % (WOL_DEV_NAME)
            bot.sendMessage(chat_id, msg, reply_markup=hide_keyboard)
        
        cursor.close()
        db.close()

        return
