#!/usr/bin/python

# Python modules
import time, sys, os
# GoldRusher modules
from GoldRusher.conf.config import *
from GoldRusher.utils.misc import *

# Gray, Red, Green, Yellow, Blue, Magenta, Cyan, White, Crimson
colorIndex = [ "30", "31", "32", "33", "34", "35", "36", "37", "38" ]

####################
# Defining Methods #
####################
def prettyPrint(msg, mode="info", decoration=True):
    """
    Pretty prints a colored message
    :param msg: The message to print
    :type msg: str
    :param mode: The mode of printing which dictates the color
    :type mode: str
    :param decoration: Whether to decorate with message (e.g., with timestamp)
    :type decoration: boolean
    :return: None
    """
    if mode == "info":
        color = "32" # Green
    elif mode == "error":
        color = "31" # Red
    elif mode == "warning":
        color = "33" # Yellow
    elif mode == "info2":
        color = "34" # Blue
    elif mode == "output":
        color = "35" # Magenta
    elif mode == "debug":
        color = "37" # White
    else:
        color = "32"
    if decoration:
        msg = "[*] %s. %s" % (msg, getTimestamp(includeDate=True))
    print("\033[1;%sm%s\033[1;m" % (color, msg))
    # Log the message if LOGGING is enabled
    if LOGGING and mode != "info":
        logEvent("%s: %s" % (getTimestamp(includeDate=True), msg))

def prettyPrintError(ex):
    """
    Pretty prints an error/exception message
    :param ex: The exception message
    :type ex: str
    :return: None
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    msg = "Error \"%s\" encountered in \"%s\" line %s: %s" % (exc_type, fname, exc_tb.tb_lineno, ex)
    prettyPrint(msg, "error")

