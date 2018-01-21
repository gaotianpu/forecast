#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
knn
"""
import os
import sys
import numpy as np  
import sklearn


from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score 

def main():
    # 加载iris数据集
    iris = sklearn.datasets.load_iris()
    print iris.data.shape, iris.target.shape
    print iris.data[:4]

    # 读取特征
    iris_X = iris.data
    # 读取分类标签
    iris_y = iris.target
    # 将数据分为训练、测试两部分
    X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size = 0.2)
    
    # 定义分类器
    knn = KNeighborsClassifier(20)

    scores = cross_val_score(knn, iris_X, iris_y, cv = 5, scoring = 'accuracy')
    print scores

    # # 进行分类
    # knn.fit(X_train, y_train)

    
    # # 计算预测值
    # y_predict = knn.predict(X_test)
    # # 计算准确率, 由于每次数据集划分不同, 可能不一样
    # print np.sum(np.fabs(y_predict - y_test)) / float(len(y_test)) 
     
    # # #预测  
    # predict = knn.predict([[0.1,0.2,0.3,0.4]])  
    # print iris.target_names[predict]



if __name__ == "__main__": 
    main()
