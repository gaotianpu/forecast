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

import math
def cos_dist(a, b):
    if len(a) != len(b):
        return None
    part_up = 0.0
    a_sq = 0.0
    b_sq = 0.0
    for a1, b1 in zip(a,b): #zip , 2+ list -> tuple list
        part_up += a1*b1
        a_sq += a1**2
        b_sq += b1**2
    part_down = math.sqrt(a_sq*b_sq) #sqrt
    if part_down == 0.0:
        return None
    else:
        return part_up / part_down

x = [59026244,212249601,76074355,67940834,79014200]
if __name__ == '__main__':
    d1 = (59026244,212249601,76074355,67940834,79014200)
    d1a  = reduce(lambda x, y: x + y, d1) / len(d1)

    d2 = (13909720,13969662,24662293,9156857,13934423)
    d2a  = reduce(lambda x, y: x + y, d2) / len(d2)

    q = [d1a,d1a,d1a,d1a,d1a]
    print cos_dist(d1,[d1a,d1a,d1a,d1a,d1a])
    print cos_dist(d2,[d2a,d2a,d2a,d2a,d2a])

    # d2 = (0, 0.9, 0.4)
    # q = (1, 2, 1)
    # print cos_dist(d1, d2)
    # print cos_dist(d1, q)
    # print cos_dist(d2, q)
    # # rows = get_prices(6.28,5.1)
    # for r in rows:
    #     print r
    # map()
    
     
