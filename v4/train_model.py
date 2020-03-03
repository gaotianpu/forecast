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

dataset = np.loadtxt('data/train.txt', delimiter=',', dtype=float)

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


X_train, X_test = data_scale(dataset, X_train, X_test)


def show_auc(target, predict_proba, title="ROC & AUC"):
    """绘制 auc https://www.jianshu.com/p/90106243d231
    """
    fpr, tpr, thresholds = roc_curve(target, predict_proba)
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


def lr_train(X_train, X_test, y_train, y_test):
    """LogisticRegression 产出基线性能评估"""
    start = time.time()

    # solver='liblinear',  C=0.5,  max_iter=2000
    lr = LogisticRegression(class_weight='balanced')
    lr.fit(X_train, y_train)
    time_c = time.time() - start

    joblib.dump(lr, 'model/lr.model')

    print(lr.n_iter_)  # 实际迭代次数
    print(lr.intercept_, lr.coef_)  # bias,特征权重

    y_test_pre = lr.predict(X_test)
    predict_proba = lr.predict_proba(X_test)

    score_train = lr.score(X_train, y_train)
    score_test = accuracy_score(y_test, y_test_pre)

    auc_score = roc_auc_score(y_test, predict_proba[:, 1])

    p = precision_score(y_test, y_test_pre)
    recall_socre = recall_score(y_test, y_test_pre)
    f1_val = f1_score(y_test, y_test_pre)
    print("time=%s,accuracy_train=%f,accuracy_test=%f,p=%f,recall=%f,f1=%f,auc=%f" %
          (time_c, score_train, score_test, p, recall_socre, f1_val, auc_score))

    show_auc(y_test, predict_proba[:, 1], "LR: ROC and AUC")


def LinearSVC_train(X_train, X_test, y_train, y_test):
    start = time.time()
    clf = LinearSVC(random_state=0, tol=1e-5, class_weight='balanced',max_iter=8000)
    clf = CalibratedClassifierCV(clf)

    clf.fit(X_train, y_train)
    # print(clf.coef_)
    # print(clf.intercept_)
    time_c = time.time() - start

    y_test_pre = clf.predict(X_test)
    score_train = clf.score(X_train, y_train)
    score_test = clf.score(X_test, y_test)

    p = precision_score(y_test, y_test_pre)
    recall_socre = recall_score(y_test, y_test_pre, average='macro')
    f1_score_val = f1_score(y_test, y_test_pre)
    print("time=%s,accuracy_train=%f,accuracy_test=%f,precision=%f,recall=%f,f1=%f" %
          (time_c, score_train, score_test, p, recall_socre, f1_score_val))

    joblib.dump(clf, 'model/linear_svc.model')

    proba = clf.predict_proba(X_test)
    show_auc(y_test, proba[:, 1], "LinearSVM: ROC and AUC")


def gbdt_train(X_train, X_test, y_train, y_test):
    # class_weight='balanced' , 样本均衡问题？
    start = time.time()
    clf = GradientBoostingClassifier(random_state=10, subsample=0.75)
    # {'max_depth': 13, 'min_samples_leaf': 60, 'min_samples_split': 100, 'n_estimators': 80, 'subsample': 0.9}

    # clf = GradientBoostingClassifier(learning_rate=0.1, n_estimators=80, max_depth=13,
    #                                  min_samples_split=100, min_samples_leaf=60,
    #                                  max_features='sqrt', subsample=0.9, random_state=10)
    clf.fit(X_train, y_train)
    time_c = time.time() - start
    joblib.dump(clf, 'model/gbdt.model')

    y_pred = clf.predict(X_train)
    y_predprob = clf.predict_proba(X_train)[:, 1]

    train_score = accuracy_score(y_train, y_pred)
    print("Train Accuracy : %.4g" % train_score)
    print("Train AUC Score (Train): %f" %
          roc_auc_score(y_train, y_predprob))

    y_test_pre = clf.predict(X_test)
    y_predprob_test = clf.predict_proba(X_test)[:, 1]

    acc_test = accuracy_score(y_test, y_test_pre)
    auc_score = roc_auc_score(y_test, y_test_pre)
    p = precision_score(y_test, y_test_pre)
    recall_socre = recall_score(y_test, y_test_pre)
    f1_val = f1_score(y_test, y_test_pre)
    print("time=%s,accuracy_train=%f,accuracy_test=%f,p=%f,recall=%f,f1=%f,auc=%f" %
          (time_c, train_score, acc_test, p, recall_socre, f1_val, auc_score))

    # print("Test Accuracy : %.4g" % accuracy_score(y_test, y_test_pre))
    # print("Test AUC Score (Test): %f" %
    #       roc_auc_score(y_test, y_test_pre))
    show_auc(y_test, y_predprob_test, "GBDT: ROC and AUC")


def svm_c(x_train, x_test, y_train, y_test):
    start = time.time()
    svc = SVC(kernel='rbf', class_weight='balanced',
              C=512.0, gamma=8, probability=True)
    clf = svc.fit(x_train, y_train)
    time_c = time.time() - start

    joblib.dump(clf, 'model/svc.model')

    y_test_pre = clf.predict(X_test)

    score_train = clf.score(X_train, y_train)
    score_test = accuracy_score(y_test, y_test_pre)

    p = precision_score(y_test, y_test_pre)
    recall_socre = recall_score(y_test, y_test_pre)
    f1_val = f1_score(y_test, y_test_pre)
    print("time=%s,accuracy_train=%f,accuracy_test=%f,p=%f,recall=%f,f1=%f" %
          (time_c, score_train, score_test, p, recall_socre, f1_val))

    # print(sum(y_test_pre))
    # print(sum(y_test))

    # score = svc.score(x_test, y_test)

    # p = precision_score(y_test, y_test_pre)
    # recall_socre = recall_score(y_test, y_test_pre)
    # f1_val = f1_score(y_test, y_test_pre)
    # print("time=%f,accuracy_test=%f,p=%f,recall=%f,f1=%f" %
    #       (time_c, score, p, recall_socre, f1_val))

    # score_train = clf.score(X_train, y_train)
    # score_test = clf.score(X_test, y_test)

    # recall_socre = recall_score(y_test_pre, y_test, average='macro')
    # f1_score_val = f1_score(y_test_pre, y_test)
    # print("tim_c=%s,accuracy_train=%s,accuracy_test=%s,recall=%s,f1=%s" %
    #       (time_c,score_train, score_test, recall_socre, f1_score_val))

    proba = clf.predict_proba(X_test)
    show_auc(y_test, proba[:, 1], "SVM: ROC and AUC")


def svm_grid(x_train, x_test, y_train, y_test):
    """https://www.cnblogs.com/huanping/p/9330849.html
    https://www.cnblogs.com/jiaxin359/p/8641976.html
    """
    start = time.time()
    # rbf核函数，设置数据权重 #,probability=True
    svc = SVC(kernel='rbf', class_weight='balanced')
    c_range = np.logspace(-5, 15, 11, base=2)
    gamma_range = np.logspace(-9, 3, 13, base=2)
    # 网格搜索交叉验证的参数范围，cv=3,3折交叉
    param_grid = [{'kernel': ['rbf'], 'C': c_range, 'gamma': gamma_range}]
    grid = GridSearchCV(svc, param_grid, cv=3, n_jobs=-1)
    # 训练模型
    clf = grid.fit(x_train, y_train)
    time_c = time.time() - start

    # 计算测试集精度
    score = grid.score(x_test, y_test)

    # score_train = grid.score(X_train, y_train)
    # score_test = grid.score(X_test, y_test)
    # y_test_pre = grid.predict(X_test)
    # recall_socre = recall_score(y_test_pre, y_test, average='macro')
    # f1_score_val = f1_score(y_test_pre, y_test)
    # print("accuracy_train=%s,accuracy_test=%s,recall=%s,f1=%s" %
    #       (score_train, score_test, recall_socre, f1_score_val))

    print('tim_c=%s,accuracy_test=%s' % (time_c, score))
    print(grid.best_params_)  # {'C': 32768.0, 'gamma': 8.0, 'kernel': 'rbf'}
    # proba = clf.predict_proba(X_test)
    # show_auc(y_test, proba[:, 1], "SVM: ROC and AUC")


if __name__ == "__main__":
    lr_train(X_train, X_test, y_train, y_test)
    # gbdt_train(X_train, X_test, y_train, y_test)
    # LinearSVC_train(X_train, X_test, y_train, y_test)
    # svm_grid(X_train, X_test, y_train, y_test)
    # svm_c(X_train, X_test, y_train, y_test)
