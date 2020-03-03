#!/bin/bash

#下载数据
/anaconda3/bin/python download_history.py

#生成训练数据
/anaconda3/bin/python gen_train_data.py train bool > data/train.txt 
#/anaconda3/bin/python gen_train_data.py train float > data/train.regression.txt 
/anaconda3/bin/python gen_train_data.py predict bool> data/predict.txt 

#xgboost 需要的格式？
/anaconda3/bin/python svmlight_format.py > data/train.svmlight

#模型训练
/anaconda3/bin/python train_model.py 1 > train_model.out
#/anaconda3/bin/python train_LinearRegression.py 1 > train_LinearRegression.out

#预测
/anaconda3/bin/python predict.py