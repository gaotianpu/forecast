#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""基于sklearn实现逻辑回归 
https://www.cnblogs.com/nxf-rabbit75/p/10282672.html
https://www.jianshu.com/p/0f0159a9cec9
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_and_analyse_data(data_file):
    data = pd.read_csv(data_file)
    count_classes = data.loc[:,"1"].value_counts()
    print(count_classes)
    count_classes.plot(kind='bar')  # 柱状图画图
    plt.title('Fraud class histogram')
    plt.xlabel('Class')
    plt.ylabel('Frequency')
    plt.show()


if __name__ == "__main__":
    load_and_analyse_data('data/train.txt')
