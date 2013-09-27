#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web

dbw = web.database(dbn='mysql', host='127.0.0.1', db='forecast', user='root', pw='root')
dbr = web.database(dbn='mysql', host='127.0.0.1', db='forecast', user='root', pw='root')

const_root_local = '/Users/gaotianpu/Documents/stocks'