#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""基于sklearn实现逻辑回归
https://www.cnblogs.com/nxf-rabbit75/p/10282672.html
https://www.jianshu.com/p/0f0159a9cec9
"""
import os
import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression,LinearRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import GradientBoostingClassifier
# 模型评估方法 https://blog.csdn.net/CherDW/article/details/55813071
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.calibration import CalibratedClassifierCV

import joblib

dataset = np.loadtxt('data/train.regression.txt', delimiter=',', dtype=float)

# 数据划分方法：k折交叉验证，留一法，随机划分 https://www.jianshu.com/p/db7ed9735095
X_train, X_test, y_train, y_test = train_test_split(
    dataset[:, 2:], dataset[:, 0], test_size=0.30, random_state=0)
print(y_train.shape, y_test.shape)

# 数据归一化，对lr，svm等非常有用 https://www.cnblogs.com/shine-lee/p/11779514.html


def data_scale(dataset, X_train, X_test):
    """数据缩放"""
    # scaler_file = 'model/min_max.scaler'
    # scaler = MinMaxScaler()
    # if True:  # not os.path.exists(scaler_file):
    #     scaler.fit(dataset[:, 2:])
    #     joblib.dump(scaler, scaler_file)
    # else:
    #     scaler = joblib.load(scaler_file)

    scaler_file = 'model/standard.scaler'
    scaler = StandardScaler()
    if True:
        scaler.fit(dataset[:, 2:])
        joblib.dump(scaler, scaler_file)
    else:
        scaler = joblib.load(scaler_file)

    return (scaler.transform(X_train), scaler.transform(X_test))


def train(X_train, X_test, y_train, y_test):
    clf = LinearRegression()
    clf.fit(X_train, y_train)
    joblib.dump(clf, 'model/linearRegression.model')

   


X_train, X_test = data_scale(dataset, X_train, X_test)
train(X_train, X_test, y_train, y_test)