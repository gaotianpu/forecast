#!/usr/bin/python
import os
import math
import browser


const_base_url="http://hq.sinajs.cn/list="
const_root_local = "/Users/gaotianpu/Documents/stocks/"
# http://hq.sinajs.cn/list=sh600000,sh600004,sh600005,sh600006,sh600007,sh600008,sh600009,sh600010,sh600011,sh600012,sh600015,sh600016,sh600017,sh600018,sh600019,sh600020,sh600021,sh600022,sh600026,sh600027,sh600028,sh600029,sh600030,sh600031,sh600033,sh600035,sh600036,sh600037,sh600038,sh600039,sh600048,sh600050,sh600052,sh600053,sh600054,sh600055,sh600056,sh600057,sh600059,sh600060,sh600061,sh600062,sh600063,sh600064,sh600066,sh600067,sh600068,sh600069,sh600070,sh600071,sh600072,sh600073,sh600075,sh600076,sh600077,sh600078,sh600079,sh600080,sh600081,sh600082,sh600083,sh600084,sh600085,sh600086,sh600088,sh600089,sh600090,sh600091,sh600093,sh600094,sh600095,sh600096,sh600097,sh600098,sh600099,sh600100,sh600101,sh600103,sh600104,sh600105,sh600106,sh600107,sh600108,sh600109,sh600110,sh600111,sh600112,sh600113

# http://table.finance.yahoo.com/table.csv?s=000001.sz

def load_all_stocks():
    stocks = []
    with open('/Users/gaotianpu/github/forecast/v2/all_stocks_list.txt','rb') as f:
        lines = f.readlines()
        stocks = [(s.strip(),s[2:].strip()+'.'+s[:2].replace('sh','ss'))  for s in lines]
        f.close()
    return stocks
        


def download_history(stock_no):    
    url = 'http://table.finance.yahoo.com/table.csv?s=%s' % (stock_no)
    print url  
    lfile = '%s/dailyh/%s.csv' %(const_root_local,stock_no)
    try:
        if not os.path.exists(lfile):
            browser.downad_and_save(url,lfile)
        return 
    except Exception,e:
        print str(e) 


def download_daily():
    pagesize = 88
    stocks = load_all_stocks()
    count = len(stocks)
    params = [s[0] for s in stocks]     
    pagecount = int(math.ceil(count/pagesize))    

    for i in range(0,pagecount+1):
        url = const_base_url + ','.join(params[i*pagesize:(i+1)*pagesize])
        print i,url
        try:
            browser.downad_and_save(url,lfile)
        except Exception,e:
            print str(e)



def download_all_history():
    stocks = load_all_stocks()
    for stock in stocks:
        download_history(stock[1])


if __name__ == "__main__" :
    download_history('600000.ss')
    # download_daily()



