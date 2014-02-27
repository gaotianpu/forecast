#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import pylab
import numpy 


def test():
    x = [1, 2, 3, 4, 5]# Make an array of x values
    y = [1, 4, 9, 16, 25]# Make an array of y values for each x value
    pl.plot(x, y)# use pylab to plot x and y
    pl.show()# show the plot on the screen

def test1():
    lfile = './sample_data/300052.sz_gd.csv'
    lines = []
    with open(lfile,'rb') as f:
        lines = f.readlines()
    
    x = []
    y = []
    for l in lines:
        r = l.strip().split(',') 
        x.append(r[0])
        y.append(r[1])
    pylab.plot(x, y,'o')# use pylab to plot x and y
    pylab.show()# show the plot on the screen

import pylab
import numpy 
def draw_1(lfile):    
    data = numpy.loadtxt(lfile,delimiter=',')    
    pylab.plot(data[:,0],data[:,1],'ro')
    pylab.xlabel('x')
    pylab.ylabel('y')
    pylab.savefig('foo.png')
    pylab.show()


if __name__ == "__main__":
    draw_1('./sample_data/300052.sz_gd.csv')
