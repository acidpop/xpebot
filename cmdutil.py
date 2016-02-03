#-*- coding: utf-8 -*-

from LogManager import log
from subprocess import Popen, PIPE
import shlex


def ExecuteCommand(command):
    cmd = shlex.split(command)
    log.info('ExecuteCommand : %s', command)
    process = Popen(cmd, stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    log.info('ExecuteCommand Result : %s', output)
    return output, err




