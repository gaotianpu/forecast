#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
读取股票编码
"""
import os
import sys
import datetime
import csv
import web

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)
sys.path.append(home_dir + "/conf")
import conf

db = web.database(dbn='sqlite', db=conf.SQLITE3_DB_FILE)


def load_all():
    return load_from_file()


def load_from_file():
    with open(conf.ALL_STOCKS_FILE) as f:
        rows = csv.DictReader(f)
        for row in rows:
            yield row


def load_from_db():
    rows = db.select('stocks')
    return rows


if __name__ == "__main__":
    rows = load_from_db()
    for i, row in enumerate(rows):
        print row
        if i > 5:
            break
