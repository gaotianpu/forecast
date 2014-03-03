#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web 
import numpy 
import matplotlib.pyplot as plt

def test(): #the first test
    x = [1, 2, 3, 4, 5]# Make an array of x values
    y = [1, 4, 9, 16, 25]# Make an array of y values for each x value
    plt.plot(x, y)# use plt to plot x and y
    plt.show()# show the plot on the screen

def test1(lfile): #load data from file
    x,y = [],[] 
    with open(lfile,'rb') as f:
        lines = f.readlines() 
        for l in lines:
            r = l.strip().split(',') 
            x.append(r[0])
            y.append(r[1]) 

    plt.plot(x, y,'o')# use plt to plot x and y
    plt.plot([29.8,29.8],[0,29])
    plt.show()# show the plot on the screen

 
def draw_1(lfile): #load data with numpy   
    data = numpy.loadtxt(lfile,delimiter=',') 
    
    #draw line
    max_y = max(data[:,1])
    point_x = data[:,0][list(data[:,1]).index(max_y)]  #,  max(data[:,0]), 
    plt.plot([point_x,point_x],[0,max_y*1.1])

    plt.plot(data[:,0],data[:,1],'ro')
    plt.xlabel('price')
    plt.ylabel('count')
    # plt.savefig('foo.png')
    plt.show()


if __name__ == "__main__":
    # test1()
    test1('./sample_data/300052.sz_gd.csv')
