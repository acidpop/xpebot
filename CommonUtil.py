#-*- coding: utf-8 -*-

# byte to Human Readable convert - MAX : TB
def hbytes(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.2f%s" % (num, x)
        num /= 1024.0
    return "%3.2f%s" % (num, 'TB')


def dequote(s):
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s


def GetDSMMajorVersion():
    parseVars = {}
    with open("/etc/VERSION") as versionFile:
         for line in versionFile:
             key, value = line.partition("=")[::2]
             parseVars[key.strip()] = dequote(value.strip())

    return parseVars['majorversion']


