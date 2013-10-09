#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import platform

dbw = web.database(dbn='mysql', host='127.0.0.1', db='forecast', user='root', pw='root')
dbr = web.database(dbn='mysql', host='127.0.0.1', db='forecast', user='root', pw='root')

const_root_local = 'D:\\gaotp\\stocks' if platform.system() == 'Windows' else '/Users/gaotianpu/Documents/stocks'
