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
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, roc_auc_score

import joblib

# dataset = np.loadtxt('data/test.txt', delimiter=',', dtype=float)
dataset = np.loadtxt('data/predict.txt', delimiter=',', dtype=float)
x, y, ids = dataset[:, 2:], dataset[:, 0], dataset[:, 1]

# 数据缩放
scaler_file = 'model/standard.scaler'
scaler = StandardScaler()
scaler = joblib.load(scaler_file)
x = scaler.transform(x)


def show_results(model, model_name):
    # y_test_pre = model.predict(x)
    # predict_proba = model.predict_proba(x)

    # score_test = accuracy_score(y, y_test_pre)
    # auc_score = roc_auc_score(y, predict_proba[:, 1])
    # p = precision_score(y, y_test_pre)
    # recall_socre = recall_score(y, y_test_pre)
    # f1_val = f1_score(y, y_test_pre)
    # print("%s accuracy_test=%f,p=%f,recall=%f,f1=%f,auc=%f" %
    #       (model_name,  score_test, p, recall_socre, f1_val, auc_score))
    # return

    pred = model.predict(x)
    proba = model.predict_proba(x)

    up = sum(pred)
    t = len(x)

    pecent = up*100/t
    print("model=%s,up percent:%f, up=%d, total=%d" %
          (model_name, pecent, up, t))

    li = []
    for i, val in enumerate(proba):
        li.append([str(int(ids[i]))[8:], val[1]])

    li.sort(key=lambda x: x[1], reverse=True)

    for i, val in enumerate(li):
        if i > 10:
            break
        print(val)
    print("===================================")


def show_results_reg(model, model_name):
    # print(dir(model))
    # print(type(model),model.__class__)
    # return
    # pred = model.predict(x)
    proba = model.predict(x)  # model.predict_proba(x)

    up = sum([1 if p > 0 else 0 for p in proba])
    t = len(x)

    pecent = up*100/t
    print("model=%s,up percent:%f, up=%d, total=%d" %
          (model_name, pecent, up, t))

    li = []
    for i, val in enumerate(proba):
        # print(val)
        li.append([str(int(ids[i]))[8:], val])

    li.sort(key=lambda x: x[1], reverse=True)

    for i, val in enumerate(li):
        if i > 28:
            break
        print(val)
    print("===================================")


show_results(joblib.load("model/lr.model"), "lr")
show_results(joblib.load("model/gbdt.model"), "gbdt")
# show_results(joblib.load("model/linear_svc.model"), "linear_svc")
# show_results_reg(joblib.load("model/linearRegression.model"), "linearRegression")
