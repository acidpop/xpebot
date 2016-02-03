#-*- coding: utf-8 -*-

# pip install psutil
import psutil
import CommonUtil

from LogManager import log

"""
System Status JSON Format

{ cpu_percent : 10.0,
  cpu_count : 2,
  cpu_core_percent : [5.6, 10.3],


"""
def system_status(interval_value=0.1):
    vmem_info = psutil.virtual_memory()
    swap_info = psutil.swap_memory()

    system_info = { 'cpu_percent' : psutil.cpu_percent(interval=interval_value, percpu=False),
                    'cpu_count' : psutil.cpu_count(),
                    'cpu_core_percent' : psutil.cpu_percent(interval=interval_value, percpu=True),
                    'vmem_total' : CommonUtil.hbytes(vmem_info.total),
                    'vmem_used' : CommonUtil.hbytes(vmem_info.used),
                    'vmem_free' : CommonUtil.hbytes(vmem_info.free),
                    'vmem_percent' : vmem_info.percent,
                    'swap_total' : CommonUtil.hbytes(swap_info.total),
                    'swap_used' : CommonUtil.hbytes(swap_info.used),
                    'swap_free' : CommonUtil.hbytes(swap_info.free),
                    'swap_percent' : swap_info.percent,
                  }

    # Disk Info
    disk_part = psutil.disk_partitions()
    idx = 1
    for x in disk_part:
        disk_usage = psutil.disk_usage(x.mountpoint)
        key = 'disk%d_total' % (idx)
        system_info[key] = CommonUtil.hbytes(disk_usage.total)
        key = 'disk%d_used' % (idx)
        system_info[key] = CommonUtil.hbytes(disk_usage.used)
        key = 'disk%d_free' % (idx)
        system_info[key] = CommonUtil.hbytes(disk_usage.free)
        key = 'disk%d_percent' % (idx)
        system_info[key] = disk_usage.percent
        idx += 1


    return system_info

