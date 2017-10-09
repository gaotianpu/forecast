#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
读取股票编码
"""
import os
import sys
import datetime
import csv
home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)
sys.path.append(home_dir + "/conf")
import conf


def load_all(): 
    with open(conf.ALL_STOCKS_FILE) as f:
        rows = csv.DictReader(f)
        for row in rows:
            yield row

# def load_from_db():
#     pass 

# def load_from_file():
#     with open(conf.ALL_STOCKS_FILE) as f:
#         rows = csv.DictReader(f)
#         for row in rows:
#             yield row 

def p(x):
    print x


def main():
    map(p, load_all())
    # map(lambda x: print (x), load()) #error ?


if __name__ == "__main__":
    main()
