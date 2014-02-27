#!/usr/bin/env python
# -*- coding: utf-8 -*-
import da


def run(openp,close,high,low):
    t = [openp,close,high,low]
    t.sort()
    base = high - low
    l = [close>openp]
    for i in range(0,3):
        l.append((t[i+1]-t[i])/base)
        print t[i], t[i+1]-t[i], (t[i+1]-t[i])/base


    print l

def set_test():
    split_cn()
    a = set(['a','b','c','d'])
    b = set(['a','c','e','f','d'])
    print b-a 

def map():
    rows=[['ma5',1], ['ma10',4],['ma20',8],['ma50',1],['ma100',2],['ma200',3],]
    rows = sorted(rows, cmp=lambda x,y : cmp(y[1], x[1]))
    print '_'.join([r[0].replace('ma','') for r in rows])  
       

def get_prices(high,low):
    l = []
    l.append(low)     
    for i in range(int(low*100),int(high*100)):
        l.append(float(i)/100) 
    l.append(high)
    return l 
    

if __name__ == '__main__':
    rows = get_prices(6.28,5.1)
    for r in rows:
        print r
    # map()
    
     
