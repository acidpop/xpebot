#-*- coding: utf-8 -*-

# pip install psutil
import psutil
import CommonUtil
import json
import os
import main

from LogManager import log


def system_status(interval_value=0.1):
    
    vmem_info = psutil.virtual_memory()

    system_info = '*' + main.botConfig.GetHostName() + u' 시스템 정보*\n\n'

    system_info += 'CPU : %.1f%%\n' % ( psutil.cpu_percent(interval=interval_value, percpu=False) )
    system_info += 'RAM : %.1f%%\n' % ( psutil.virtual_memory().percent )
    
    # Disk Info
    disk_list = os.popen("df | grep volume | cut -d ' ' -f 7").read()
    for volume in disk_list.splitlines():
        if volume != '':
            system_info += '\n*' + volume[1:] + u' Disk 정보*\n'
            diskinfo = psutil.disk_usage(volume)
            system_info += u'전체 : %s\n' % (CommonUtil.hbytes(diskinfo.total))
            system_info += u'사용된 공간 : %s\n' % (CommonUtil.hbytes(diskinfo.used))
            system_info += u'사용 가능 공간 : %s\n' % (CommonUtil.hbytes(diskinfo.free))
            system_info += u'사용율 : %s%%\n' % (diskinfo.percent)

    return system_info.encode('utf-8')

