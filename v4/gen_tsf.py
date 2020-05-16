#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import logging
import datetime
import pandas as pd 

#m:Label,m:Query,m:Url
def process(file):
    dataset = pd.read_csv(file, sep=",", header=0)
    # print(dataset.shape[1])
    header = []
    header.append("m:Label")  # m:Queryid
    header.append("m:Query")
    header.append("m:Url")
    for i in range(dataset.shape[1]-2):
        header.append("F_%s"%(i))
    print("\t".join(header))

    for idx, row in dataset.iterrows():
        # if idx>3: break
        lrow = list(row)
        lrow[0] = str(int(lrow[0]))
        x = lrow[1]
        q = str(x)[:8]
        # print(q)
        lrow.insert(1,q)
        print( "\t".join( [str(r) for r in lrow ] ) )
        

        # print("\t".join(lrow[0:1] + lrow[3:]  ))

# python gen_tsf.py data/train.txt > data/train.tsf
# python gen_tsf.py data/test.txt > data/test.tsf
if __name__ == "__main__":
    f = sys.argv[1]
    process(f) 