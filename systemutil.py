#-*- coding: utf-8 -*-

# pip install psutil
import psutil
import CommonUtil
import json
import os
import main

from operator import itemgetter
from LogManager import log

# CPU, Memory Top3 Process list
def GetTopProcess(count=3):
    proc_cpu = dict()
    proc_mem = dict()

    process_list = psutil.get_pid_list()

    for pid in process_list:
        try:
            info = psutil.Process(pid)
            proc_cpu[info.name()] = info.get_cpu_percent()

            temp_mem = info.memory_percent()
            for child in info.children(recursive=True):
                temp_mem += child.memory_percent()

            proc_mem[info.name()] = temp_mem
        except:
            log.info('GetTopProcess except')
            continue

    cpu_top = sorted(proc_cpu.iteritems(), key=itemgetter(1), reverse=True)[:count]
    mem_top = sorted(proc_mem.iteritems(), key=itemgetter(1), reverse=True)[:count]

    result = '\n*Top ' + str(count) + ' cpu use*\n'

    for cpu in cpu_top:
        temp = '%s : %.1f\n' % (cpu[0], cpu[1])
        result += temp

    result += '\n*Top ' + str(count) + ' memory use*\n'
    for mem in mem_top:
        temp = '%s : %.1f\n' % (mem[0], mem[1])
        result += temp

    return result



def system_status(interval_value=0.1):
    
    vmem_info = psutil.virtual_memory()

    system_info = '*' + main.botConfig.GetHostName() + u' 시스템 정보*\n\n'

    system_info += 'CPU : %.1f%%\n' % ( psutil.cpu_percent(interval=interval_value, percpu=False) )
    system_info += 'RAM : %.1f%%\n' % ( psutil.virtual_memory().percent )

    system_info += GetTopProcess(1)
    
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

