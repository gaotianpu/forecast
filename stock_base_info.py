#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import urllib 
import datetime
import os
import BeautifulSoup

const_root_url = 'http://app.finance.ifeng.com/list/stock.php?'
const_root_local = '/Users/gaotianpu/Documents/stocks/'

const_tmarkets = 'ha,sa,hb,sb,zxb,cyb,zs'

def get_url(params):
    return const_root_url + '&'.join(["%s=%s" % (k,v) for k,v in params.items()])

def get_local_file_name(params):
    fsegs = '_'.join(["%s-%s" % (k,v) for k,v in params.items()])
    local_file = datetime.datetime.now().strftime('%Y%m%d') + '_' + fsegs + '.html'
    lfile = const_root_local + local_file
    return lfile

def download(params):
    lfile = get_local_file_name(params)
    if not os.path.exists(lfile):
        url = get_url(params)
        print url
        req = urllib.urlretrieve(url,lfile)  #try..catch ... logging?
    print lfile
    return lfile

def parse_html(lfile):
    soup = BeautifulSoup.BeautifulSoup(open(lfile))
    tables =  soup.findAll('table')
    
    if len(tables)<1:
        return False 

    result = []
    allrows = tables[0].findAll('tr')
    for row in allrows:
        result.append([])
        allcols = row.findAll('td')
        for col in allcols:
          thestrings = [unicode(s) for s in col.findAll(text=True)]
          thetext = ''.join(thestrings)
          result[-1].append(thetext)

    return result 
    
def download_all_stocks():
    t_li = const_tmarkets.split(',')
    for t in t_li:
        for p in range(1,10):
            fname = download({'t':t,'p':p,'f':'symbol','o':'asc'})
            parse_html(fname)


if __name__ == '__main__':
    download_all_stocks()