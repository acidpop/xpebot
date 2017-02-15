#-*- coding: utf-8 -*-

from LogManager import log
from subprocess import Popen, PIPE
#import shlex
import os


def ExecuteCommand(command):
    #cmd = shlex.split(command.encode('utf-8'))
    log.info('ExecuteCommand : %s', command)
    #process = Popen(command, stdout=PIPE)
    #(output, err) = process.communicate()
    #exit_code = process.wait()
    output = os.popen(command).read()
    log.info('ExecuteCommand Result : %s', output)
    return output


def ExecutePSQL(query):
    log.info('Execute PSQL query:%s', query)

    cmd = 'psql -U postgres -d download -c "' + query + '"'

    output = os.popen(cmd).read()
    log.info('ExecuteCommand Result : %s', output)
    return output

