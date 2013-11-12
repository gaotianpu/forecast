#!/usr/bin/env python
# -*- coding: utf-8 -*-

def run(openp,close,high,low):
    t = [openp,close,high,low]
    t.sort()
    base = high - low
    l = [close>openp]
    for i in range(0,3):
        l.append((t[i+1]-t[i])/base)
        print t[i], t[i+1]-t[i], (t[i+1]-t[i])/base


    print l



if __name__ == '__main__':
    run(11.12,10.88,11.16,10.75)
