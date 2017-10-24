#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
绘图练习：
1. A股整体涨跌幅概率密度分布？
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                        os.path.pardir)
sys.path.append(home_dir + "/conf")
import conf
import setting

#
def normfun(x,mean,std):
    """正态分布的概率密度函数。可以理解成 x 是 mean（均值）和 std（标准差）的函数"""
    pdf = np.exp(-((x - mean)**2)/(2*std**2)) / (std * np.sqrt(2*np.pi))
    return pdf


field_names = setting.FIELDS_SORT.split(',')
df = pd.read_csv(conf.HISTORY_CONVERTED_PATH + '/convert_603988.csv',
                 header=None, names=field_names, index_col=['trade_date'])
# print field_names
# print df.head()

close = df["vo_turn_over"][df.close>0]
# close = df["PCHG"][df.PCHG!='None']
max_val = close.max()
min_val = close.min()
mean_val = close.mean()
std_val = close.std()
# print max_val,min_val,mean_val,std_val

# 设定 x 轴前两个数字是 X 轴的开始和结束，第三个数字表示步长，或者区间的间隔长度
x = np.arange(min_val,int(max_val)+1,100) 
#设定 y 轴，载入刚才的正态分布函数
y = normfun(x, mean_val, std_val)
plt.plot(x,y)

#画出直方图，最后的“normed”参数，是赋范的意思，数学概念
plt.hist(close, bins=40, rwidth=0.8, normed=True)

plt.title('Close distribution')
plt.xlabel('Close')
plt.ylabel('Probability')
#输出
plt.show()



# print df.mean()
# print df.mean(1)
# print df.apply(lambda x: x.max() - x.min())


# df[ df.PCHG is not None ]['PCHG'].mean()

# pchg = df['PCHG']
# print pchg
# plt.show(df.plot())
# print pchg

# mean = df[1:]['PCHG'].mean()
# std = pchg.std()
# print mean,std
# raise TypeError('Could not convert %s to numeric' % str(x))

# df['PCHG'].plot()
# plt.legend(loc='best')

#TypeError: Empty 'DataFrame': no numeric data to plot
