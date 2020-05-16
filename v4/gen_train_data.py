#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import logging
import datetime
from sklearn.preprocessing import OneHotEncoder


class TrainData:
    def __init__(self, log):
        self.log = log
        self.all_stocks_meta_file = "schema/dict/all_stocks_meta.txt"
        self.WINDOWS_LEN = 20

    def load_data(self, stockno):
        rows = []

        local_file = 'data/history_raw/%s.csv' % (stockno)
        if not os.path.exists(local_file):
            self.log.warning("file not exists,file=%s", local_file)
            return False

        with codecs.open(local_file, 'r', 'gbk') as f:
            for i, line in enumerate(f):
                fields = line.strip().split(',')
                if fields[2] == "0.0":
                    continue

                row = {}
                row['date_stock'] = int(fields[0].replace(
                    '-', '') + fields[1].replace("'", ''))
                row['date'] = datetime.datetime.strptime(fields[0], "%Y%m%d")
                row['close'] = float(fields[2])  # 收盘价-2
                row['high'] = float(fields[3])  # 最高价-3
                row['low'] = float(fields[4])  # 最低价-4
                row['open'] = float(fields[5])  # 开盘价-5
                row['lclose'] = float(fields[6])  # 前收盘-6
                row['chg'] = float(fields[7])  # 涨跌额-7
                row['pchg'] = float(fields[8])  # 涨跌幅-8
                row['TURNOVER'] = float(fields[9])  # 换手率-9
                row['VOTURNOVER'] = float(fields[10])  # 成交量-10
                row['VATURNOVER'] = float(fields[11])  # 成交金额-11
                row['TCAP'] = float(fields[12])  # 总市值-12
                row['MCAP'] = float(fields[13])  # 流通市值-13

                rows.append(row)
            return rows

    def get_features(self, rows, last_idx):
        features = []  # 特征

        last_day = rows[last_idx]

        features.append(last_day['date_stock'])  # sampleId, date_stockno

        # 交易日是星期几
        weekday = [0, 0, 0, 0, 0]  # 星期几,转one-hot
        weekday[last_day['date'].isoweekday()-1] = 1
        features = features + weekday   #0-4

        # 0 0.017770334824818816
        # 1 0.00218701617745131
        # 2 0.004212369614498419
        # 3 0.05508972314390036
        # 4 0.061471732668612465

        # 最后一交易日的基本情况 # 5- 14

        # gbdt模型分析，这几个特征效果很差
        # features.append(last_day['open']) # 5
        # features.append(last_day['close'])  #6 最后一日收盘价格，单价对比
        # features.append(last_day['high']) #7
        # features.append(last_day['low']) #8
        # features.append(last_day['lclose']) #9

        features.append(last_day['chg'])  # 5 涨跌额度 0.0049971583634313066
        features.append(last_day['pchg'])  #6 涨跌幅度 0.06817451593907843
        features.append(last_day['TURNOVER']) #7 换手率 0.14748948646434967
        features.append(last_day['VATURNOVER'])  #8 最后一日成交金额 0.005333749300287914
        features.append(last_day['MCAP'])  #9 流通市值 0.0014722593690831985

        features.append(
            (last_day['open'] - last_day['lclose'])/last_day['lclose']) #10 0.24983986352584592
        features.append(
            (last_day['high'] - last_day['low'])/last_day['lclose']) #11 0.10651984881499339

        # 与过去WINDOWS_LEN(20)天情况对比
        FIRST_IDX = last_idx + 1 + self.WINDOWS_LEN
        # WINDOWS_LEN(20)天内最高、最低价格
        high_price = max([r['high']
                          for r in rows[last_idx:FIRST_IDX]])
        low_price = min([r['low']
                         for r in rows[last_idx:FIRST_IDX] if r['low'] > 0])
        features.append(high_price) #12 0.0019214389494553725
        features.append(low_price)  #13 0.003994987631814801
        for f in ['open', 'close', 'high', 'low']: #14，15，16，17
            features.append((last_day[f] - low_price)/(high_price-low_price))

        # 20天内最大、最小成交量
        max_VOTURNOVER = max([r['VOTURNOVER']
                              for r in rows[last_idx:FIRST_IDX]])
        min_VOTURNOVER = min([r['VOTURNOVER']
                              for r in rows[last_idx:FIRST_IDX] if r['VOTURNOVER'] > 0])
        features.append(max_VOTURNOVER) #18
        features.append(min_VOTURNOVER) #19
        # 最后一天的成交量，or n天的成交量
        for day in range(10): #20，28
            vot = rows[last_idx+1+day]['VOTURNOVER']
            features.append(
                (vot - min_VOTURNOVER)/(max_VOTURNOVER - min_VOTURNOVER))

        last_close = last_day['close']
        for day in range(10): #29 39
            start_close = rows[last_idx+1+day]['close']
            features.append((last_close - start_close)*100/start_close)

        return features

    def process(self, stockno, genType="train", labelType="bool"):
        rows = self.load_data(stockno)
        if not rows:
            self.log.warning("stock_no=%s has no data", stockno)
            return

        if genType == "predict":  # 倒数第1天，
            fields = []
            fields.append(0)  # label,没有未来的涨跌幅，纯预测用
            fields = fields + self.get_features(rows, 0)
            print(','.join([str(f) for f in fields]))
            self.log.info("finish predict stock_no=%s", stockno)
            return

        if genType == "test":  # 到数第2天，用来做测试集
            fields = []
            row = rows[0]
            # label = 1 if row['pchg'] > 2 else 0
            pchg1 = (row['close'] - row['open'])*100/row['open']
            label = 1 if pchg1 > 2 else 0
            fields.append(label)
            fields = fields + self.get_features(rows, 1)
            print(','.join([str(f) for f in fields]))
            self.log.info("finish test stock_no=%s", stockno)
            return

        start_idx = 2  # or 2
        line_count = len(rows)
        for i, row in enumerate(rows):
            if i < start_idx:
                continue

            if i > 80 or i + self.WINDOWS_LEN > line_count:  # 5*16周，4个月
                break

            fields = []
            # 训练数据格式: label|数值,id(date+stockno),feature1,feature2,feature3
            tomorrow = rows[i-1] 
            pchg1 = (tomorrow['close'] - tomorrow['open']) * \
                100/tomorrow['open']

            if labelType == "bool":
                # label,未来一天涨幅>2%认为是1,其他0 
                label = 1 if pchg1 > 2 else 0 
                fields.append(label)
            else:
                fields.append(pchg1) 
             
            fields = fields + self.get_features(rows, i)
            print(','.join([str(f) for f in fields]))

        self.log.info("finish stock_no=%s", stockno)

    def process_all(self, genType="predict", labelType="bool"):  # bool,float
        with open(self.all_stocks_meta_file, 'r') as f:
            for line in f:
                fields = line.strip().split(',')
                if len(fields) > 2 and fields[2] in ['del', 'pause']:
                    continue
                stock, date = fields[0:2]
                self.process(stock, genType, labelType)


# nohup python gen_train_data.py train bool > data/train.txt  &
# nohup python gen_train_data.py test bool> data/test.txt  &
# nohup python gen_train_data.py predict bool> data/predict.txt  &
# nohup python gen_train_data.py train float > data/train.regression.txt  &
if __name__ == "__main__":
    genType = sys.argv[1]
    labelType = sys.argv[2]
    log_file = 'log/gen_%s_data.log' % (genType)
    os.system("rm -f %s" % log_file)
    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format='%(levelname)s:%(asctime)s:%(lineno)d:%(funcName)s:%(message)s')

    obj = TrainData(logging)
    obj.process_all(genType, labelType)
    # # obj.load_data("600012")
    # obj.process("600012",genType)
