#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""基于sklearn实现逻辑回归
https://www.cnblogs.com/nxf-rabbit75/p/10282672.html
https://www.jianshu.com/p/0f0159a9cec9
"""
import os
import sys
import time
import random
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
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


class TrainModel:
    def __init__(self, show_auc=False):
        self.show_auc = show_auc
        self.dataType = "train"
        self.scaler = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

    def load_data(self, dataType="train"):
        self.dataType = dataType

        if dataType == "train":
            train_file = "data/train.txt"
            test_file = "data/test.txt"
        else:
            train_file = "data/train.release.txt"
            test_file = "data/predict.txt"

        train = np.loadtxt(train_file, delimiter=',', dtype=float)

        scaler_file = 'model/standard.scaler'
        scaler = StandardScaler()
        # scaler = MinMaxScaler()
        if True:
            scaler.fit(train[:, 2:])
            joblib.dump(scaler, scaler_file)
        else:
            scaler = joblib.load(scaler_file)
        self.scaler = scaler

        # print(type(train))
        # return 

        # 解决样本均衡
        # https://blog.csdn.net/xiaoxy97/article/details/82898812 
        # https://blog.csdn.net/qq_27802435/article/details/81201357?utm_source=blogxgwz0
        label_0_ids = []
        label_1_ids = []
        for i,t in enumerate(train):
            # print(t)
            # if i>10: break 
            if t[0]==0.0:
                label_0_ids.append(i)
            elif t[0]==1.0:
                label_1_ids.append(i)

        label_0_len = len(label_0_ids)
        label_1_len = len(label_1_ids)

        sample_label_ids = label_1_ids + random.sample(label_0_ids,int(label_1_len*1.0))
        train = train[sample_label_ids]
        # print(len(x),x[:5])

        # print(train[sample_label_ids].shape)
        # return 

        # tmp = []
        # for i,t in enumerate(train):
        #     if i in sample_label_ids:
        #         tmp.append(t)

        # newtrain = np.array(tmp)
        # print(newtrain.shape)
        
        # # tmp = label_1_ids + x 
        # print(len(train),len(label_0_ids),len(label_1_ids) ) #,print(len(tmp)))
        # return  

        train, tmp = train_test_split(train, test_size=0.00001, random_state=0)
        self.X_train = scaler.transform(train[:, 2:])
        self.y_train = train[:, 0]
        self.id_train = train[:, 1]

        test = np.loadtxt(test_file, delimiter=',', dtype=float)
        self.X_test = scaler.transform(test[:, 2:])
        self.y_test = test[:, 0]
        self.id_test = test[:, 1]
        print("load_data,dataType=%s,X_train=%s,X_test=%s" %
              (self.dataType, self.X_train.shape, self.X_test.shape))

    def LogisticRegression_train(self):
        print("==%s:LogisticRegression_train=========" % (self.dataType))
        lr = LogisticRegression(class_weight='balanced', max_iter=2000)  #
        lr.fit(self.X_train, self.y_train) 
        joblib.dump(lr, 'model/%s_lr.model' % (self.dataType) )

        if self.dataType == "train":
            # print(lr.n_iter_)  # 实际迭代次数
            print(lr.intercept_)  # bias,特征权重
            for i, x in enumerate(lr.coef_[0]):
                print(i, x)

            score_train = lr.score(self.X_train, self.y_train)
            print("lr train_:%s" % (score_train))

        return lr

    def gbdt_train(self):
        print("==%s:GradientBoostingClassifier_train=========" % (self.dataType))
        clf = GradientBoostingClassifier()
        clf.fit(self.X_train, self.y_train)
        joblib.dump(clf, 'model/%s_gbdt.model' % (self.dataType) )

        if self.dataType == "train":
            for i, x in enumerate(clf.feature_importances_):
                print(i, x)

            print(clf.get_params())

            score_train = clf.score(self.X_train, self.y_train)
            print("gbdt train_score:%s" % (score_train))
        return clf

    def train_for_vailidate(self): 
        self.load_data("train")

        lr = self.LogisticRegression_train()
        self.validate(lr, "LogisticRegression")

        gbdt = self.gbdt_train()
        self.validate(gbdt, "gbdt")

    def train_for_predict(self,useCache=False):
        print("\n\n========train_for_predict==========")

        self.load_data("predict")
        if not useCache:
            lr = self.LogisticRegression_train()
            gbdt = self.gbdt_train()

        lr = joblib.load('model/%s_lr.model' % (self.dataType))
        self.predict(lr, "lr")

        gbdt = joblib.load('model/%s_gbdt.model' % (self.dataType))
        self.predict(gbdt, "gbdt") 
        

    def predict(self, model, model_name):
        xx  = model.predict(self.X_test)
        proba = model.predict_proba(self.X_test)[:, 1]  # model.predict_proba(x)
        # print(xx.shape,proba.shape)
        # return 

        up = sum(xx)
        t = self.X_test.shape[0]

        pecent = up*100/t
        print("model=%s,up percent:%f, up=%d, total=%d" %
              (model_name, pecent, up, t))

        li = []
        for i, val in enumerate(proba):
            # print(val)
            li.append([str(int(self.id_test[i]))[8:], val])

        li.sort(key=lambda x: x[1], reverse=True)

        for i, val in enumerate(li):
            if i > 20:
                break
            print(val)
        print("===================================")

    def validate(self, model, model_name):
        y_test_pre = model.predict(self.X_test) 
        predict_proba = model.predict_proba(self.X_test) 

        score_test = accuracy_score(self.y_test, y_test_pre)
        auc_score = roc_auc_score(self.y_test, predict_proba[:, 1])
        p = precision_score(self.y_test, y_test_pre)
        recall_socre = recall_score(self.y_test, y_test_pre)
        f1_val = f1_score(self.y_test, y_test_pre)
        print("%s: accuracy_test=%f,up_cnt=%s p=%f,recall=%f,f1=%f,auc=%f" %
              (model_name, score_test, sum(y_test_pre), p, recall_socre, f1_val, auc_score))

        if self.show_auc:
            self.show_auc(predict_proba[:, 1],
                          "%s: ROC and AUC" % (model_name))

    def show_auc(self, predict_proba, title="ROC & AUC"):
        """绘制 auc https://www.jianshu.com/p/90106243d231
        """
        fpr, tpr, thresholds = roc_curve(self.y_test, predict_proba)
        roc_auc = auc(fpr, tpr)  # tpr = recall rate

        plt.title(title)
        plt.plot(fpr, tpr, 'b', label='AUC = %0.3f' % roc_auc)
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], 'r--')  # 对角线？
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
        plt.ylabel('TPR/Recall')
        plt.xlabel('FPR/false positive rate')
        plt.show()


if __name__ == "__main__":
    obj = TrainModel()
    # obj.load_data('train')
    obj.train_for_vailidate()
    obj.train_for_predict()
