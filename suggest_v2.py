#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import math
import da
import re
import datetime
from decimal import *
import config
from config import const_root_local,init_log,dbr,dbw
import comm
import util
from util import browser

def load_high_stocks():
    #'high_date_90=trade_date and high_date_188=trade_date and close=high and open<>close';
    results = dbr.select('stock_base_infos',where="high_date_188=trade_date and market_code<>'sb'")
    return list(results)