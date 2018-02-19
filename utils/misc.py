#!/usr/bin/python

from GoldRusher.conf.config import *

import random, string, os, glob, subprocess, time, hashlib
from datetime import datetime
import string


def averageList(inputList, roundDigits=2):
   return round(float(sum(inputList))/float(len(inputList)), roundDigits)

def checkRoot():
    if os.getuid() != 0:
        return False
    else:
        return True
def getRandom(chars, length=8):
    return ''.join(random.choice(chars) for _ in range(length))

def getRandomHash(algorithm):
    if algorithm in hashlib.algorithms:
        h = hashlib.new(algorithm)
        h.update(getRandomAlphaNumeric())
        return h.hexdigest()
    else:
        return hashlib.sha1(getRandomAlphaNumeric()).hexdigest()    
    

def getRandomNumber(length=8):
    return ''.join(random.choice(string.digits) for i in range(length))

def getRandomAlphaNumeric(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def getRandomString(length=8):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def getTimestamp(includeDate=False):
    if includeDate:
        return "[%s]"%str(datetime.now())
    else:
        return "[%s]"%str(datetime.now()).split(" ")[1]

def logEvent(msg):
    logFile = open(LOG_FILE, "w+")
    logFile.write("%s\n" % msg)
    logFile.close()

# Copied from the "googleplay_api" helpers.py
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

