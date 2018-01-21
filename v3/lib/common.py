#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re 
import logging
from logging.handlers import TimedRotatingFileHandler

def init_logger(log_name="main"):
    """初始化日志
    https://stackoverflow.com/questions/22807972/python-best-practice-in-terms-of-logging
    https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/

    http://python.jobbole.com/86887/  日志重复输出？
    """  
    log_file = '%s/main' % (conf.LOG_ROOT)
    log_level = conf.log_level

    log_obj = logging.getLogger(__name__) 
    log_obj.setLevel(log_level)  

    #避免日志重复打印
    if log_obj.handlers:  
        return log_obj

    # log_obj.removeHandler(log_file_handler) 
    log_format = '%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s' 
    formatter = logging.Formatter(log_format)

    ## 日志天级分割
    log_file_handler = TimedRotatingFileHandler(
        filename=log_file, when="midnight", interval=1, backupCount=20)
    log_file_handler.suffix = "%Y%m%d.log"
    log_file_handler.extMatch = re.compile(r"^\d{8}.log$") 
    log_file_handler.setFormatter(formatter)  
    log_obj.addHandler(log_file_handler)   

    return log_obj