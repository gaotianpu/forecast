#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main
"""
import os
import sys
import datetime
import time
import traceback

home_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(home_dir + "/bin")
sys.path.append(home_dir + "/conf") 
import common
import etl
import make_train_data
import common

log = common.init_logger()

def main():
    """主函数"""
    stocks = common.load_all_stocks()
    for i, stock in enumerate(stocks): 
        try:
            # if i < 2809:
            #     continue 
            stock_no = stock['stock_no']
            start = stock['start']  
            log.info("run %s,%s,%s" %(stock_no,start,i)) 
            
            # etl.download(stock_no,start) #下载
            etl.convert(stock_no) #转换
            make_train_data.gen_future(stock_no) #未来5天最高价格
            
            # 导入mysql？

            # if i > 2:
            #     break 
        except Exception as e:
            log.error(traceback.format_exc())
            print e

# rsync -av --exclude=data ./ ~/data/             

if __name__ == "__main__":
    main()


# nohup ./main.py &