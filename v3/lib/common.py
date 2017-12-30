#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re 
import logging
from logging.handlers import TimedRotatingFileHandler

def init_logger(log_file):
    """初始化日志
    https://stackoverflow.com/questions/22807972/python-best-practice-in-terms-of-logging
    https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
    """ 
    # 日志天级分割
    # log_file = '%s/log/push_qingyuedu' % (conf.DATA_ROOT)
    log_file_handler = TimedRotatingFileHandler(
        filename=log_file, when="midnight", interval=1, backupCount=20)
    log_file_handler.suffix = "%Y%m%d.log"
    log_file_handler.extMatch = re.compile(r"^\d{8}.log$")
    log_format = '%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s'
    #log_format ='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    formatter = logging.Formatter(log_format)
    log_file_handler.setFormatter(formatter)
    log_obj = logging.getLogger('')
    log_obj.addHandler(log_file_handler)
    log_obj.setLevel(logging.DEBUG) #conf.log_level
    return log_obj