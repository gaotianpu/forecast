#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
from sklearn.datasets import load_svmlight_file
x_train, y_train = load_svmlight_file("mq2008.train")
"""
import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split


dataset = np.loadtxt('data/train.txt', delimiter=',', dtype=float)
X_train, X_test, y_train, y_test = train_test_split(
    dataset[:, 1:], dataset[:, 0], test_size=0.30, random_state=0)


def process(x, y, file):
    rows = []
    for i, row in enumerate(x):
        # if i>10:break
        qid = int(str(row[0])[:8])
        label = int(y[i])
        tmp = []
        tmp.append(label)
        tmp.append(qid)
        for r in row[1:]:
            tmp.append(r)
        rows.append(tmp)
    rows.sort(key=lambda x: x[1], reverse=True)

    lines = []
    for row in rows:
        fields = []
        fields.append(row[0])
        fields.append("qid:"+str(row[1]))
        for i, f in enumerate(row[3:]):
            fields.append("%d:%s" % (i+1, f))
        line = ' '.join([str(f) for f in fields])
        # print(line)
        lines.append(line)

    with open(file, 'w') as f:
        f.write("\n".join(lines))


process(X_train, y_train, "data/train.svmlight")
process(X_test, y_test, "data/test.svmlight")
