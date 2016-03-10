#coding=utf-8

'''
log helper
author : 'cowboyyang'
date : 2016-03-10
'''
import logging
import logging.handlers

class LogHelper:
    _logger = None
    @staticmethod
    def init_log_content(logfile):
        handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024*1024, backupCount=5) #实例化handler
        fmt = '[%(asctime)s]|[%(filename)s:%(lineno)s]|[%(message)s]'
        formatter = logging.Formatter(fmt)   # 实例化formatter
        handler.setFormatter(formatter)
        LogHelper._logger = logging.getLogger()
        LogHelper._logger.addHandler(handler)
        LogHelper._logger.setLevel(logging.NOTSET)

    @staticmethod
    def getlogger(logfile):
        if LogHelper._logger is None:
            LogHelper.init_log_content(logfile)
        return LogHelper._logger

LOG_DBG = LogHelper.getlogger("convert.log").debug
LOG_ERR = LogHelper.getlogger("convert.log").error