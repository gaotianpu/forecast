#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import datetime
import numpy
import web
import config
import util
import mailer
import download


def load_daily_stocks(date):       
    lfile = '%s%s.am.csv' %(config.daily_data_dir,date)
    with open(lfile,'rb') as f:
        lines = f.readlines()        
        f.close() 
        
    li = []
    for l in lines:
        x=l.strip().split(',')         
        
        o = float(x[1]) #open
        lc = float(x[2]) #last close
        c = float(x[3]) #current price equal close
        h = float(x[4]) #high
        l = float(x[5]) #low 

        #compute
        jump = (o-lc)*100/lc #是否跳空 (今开 - 昨收) / 昨收
        oc = (c-o)*100/o #计算涨幅
        lcc = (c-lc)*100/lc        
        hl = (h-l)*100/o #蜡烛图的形态，high-low

        r = web.storage(stock_no = x[0],date=x[8],time=x[9],          
            open= o,last_close= lc, close= c, high= h,low=l,volume=int(x[6]),amount=float(x[7]),            
            jump= jump, oc = oc, lcc = lcc, hl = hl)  
        li.append(r)

    return li 

def tmp(date):
    li =  load_daily_stocks(date)   
    #统计        
    print len(li)
    print len([i for i in li if i.jump<0]),len([i for i in li if i.lcc>=1]),len([i for i in li if i.oc>=1]),len([i for i in li if i.oc>=1 and i.lcc>=1])

    print 'jump'    
    print len([i for i in li if i.jump>=0]),len([i for i in li if i.jump<0]) 
    print len([i for i in li if i.jump>=0 and i.lcc>=1])*100/len([i for i in li if i.jump>=0]) ,len([i for i in li if i.jump<0 and i.lcc>=1])*100/len([i for i in li if i.jump<0])
    narray = numpy.array([i.jump for i in li]) 
    mean = narray.mean()
    std = narray.std()
    print "----"
    print len([i for i in li if i.jump>=mean]),len([i for i in li if i.jump<mean]) 
    print len([i for i in li if i.jump>=mean and i.lcc>=1])*100/len([i for i in li if i.jump>=mean]) ,len([i for i in li if i.jump<mean and i.lcc>=1])*100/len([i for i in li if i.jump<mean])
    
    # print '%0.2f'%mean,'%0.2f'%std,len([i for i in li if i.jump<mean]) 

    print 'lcc'
    print len([i for i in li if i.lcc>=1]),len([i for i in li if i.lcc<1]) 
    narray = numpy.array([i.lcc for i in li]) 
    mean = narray.mean()
    std = narray.std()
    print '%0.2f'%mean,'%0.2f'%std,len([i for i in li if i.lcc<mean])

    print 'oc'
    print len([i for i in li if i.oc>=1]),len([i for i in li if i.oc<1]) 
    print len([i for i in li if i.oc>=1 and i.jump<0]) , len([i for i in li if i.lcc>=1 and i.jump<0])
    narray = numpy.array([i.oc for i in li]) 
    mean = narray.mean()
    std = narray.std()
    print '%0.2f'%mean,'%0.2f'%std,len([i for i in li if i.oc<mean])


    # tmp = [i for i in li if i.jump<0 and i.co>0]
    # tmp.sort(key=lambda x:x.jump)  #低开|低走|高走
    # print len(tmp), tmp[0].date,tmp[0].time,

    # c = '<br/>'.join( ["%s,%s,%s,%s" %(i.stock_no[2:], '%0.2f'%i.lcc,'%0.2f'%i.co,'%0.2f'%i.jump)  for i in tmp[0:10]])
    # c = '%s<br/>%s' % (str(len(tmp)),c)

    # print c 
    # mailer.send('d_%s_%s'%(tmp[0].date,tmp[0].time), c  )

    # print len(tmp)
    # for t in tmp:
    #     print t
    #     break


def jump_p(li):    
    li_jump_1 = [i for i in li if i.jump>0]
    

    total =  len(li)
    lcc_1 = len([i for i in li if i.lcc>=1])
    lcc_0 = len([i for i in li if i.lcc<1])
    jump_1 = len(li_jump_1)
    jump_0 = len([i for i in li if i.jump<=0]) 
    lcc_1_jump_1 = len([i for i in li if i.lcc>=1 and i.jump>0])
    lcc_0_jump_1 = len([i for i in li if i.lcc<1 and i.jump>0])
    lcc_1_jump_0 = len([i for i in li if i.lcc>=1 and i.jump<=0])
    lcc_0_jump_0 = len([i for i in li if i.lcc<1 and i.jump<=0])

    data = web.storage(total=total,
        lcc_1= "%s,%s%%" %(lcc_1,100*lcc_1/total),
        lcc_0= "%s,%s%%" %(lcc_0,100*lcc_0/total),
        jump_1= "%s,%s%%" %(jump_1,100*jump_1/total), 
        jump_0= "%s,%s%%" %(jump_0,100*jump_0/total), 
        lcc_1_jump_1=  "%s,%s%%" %(lcc_1_jump_1,100*lcc_1_jump_1/jump_1),  
        lcc_1_jump_0= "%s,%s%%" %(lcc_1_jump_0,100*lcc_1_jump_0/jump_0)  , 
        lcc_0_jump_1 = "%s,%s%%" %(lcc_0_jump_1,100*lcc_0_jump_1/jump_1) , 
        lcc_0_jump_0= "%s,%s%%" %(lcc_0_jump_0,100*lcc_0_jump_0/jump_0)  )  
     
    
    t = web.template.Template('''$def with (x)\n<table width="100%">
    <tr><td></td><td>up</td><td>down</td><td>lcc-V</td></tr>
    <tr><td>up</td><td>$(x.lcc_1_jump_1)</td><td>$(x.lcc_1_jump_0)</td><td>$(x.lcc_1)</td></tr>
    <tr><td>down</td><td>$(x.lcc_0_jump_1)</td><td>$(x.lcc_0_jump_0)</td><td>$(x.lcc_0)</td></tr>
    <tr><td>jump》</td><td>$(x.jump_1)</td><td>$(x.jump_0)</td><td>$(x.total)</td></tr>
    </table><br/>''') 

    ht = t(data)

    li_jump_1 = [r for r in li_jump_1 if r.low<r.open and r.close > r.open and  r.jump<9]
    li_jump_1.sort(key=lambda x:x.jump,reverse=True)
    str_list =  '<br/>'.join(['<a href="https://www.xxxx.com/s?wd=%s" target="_blank">%s</a> , %s%%' % (x.stock_no[2:],x.stock_no[2:],'%0.2f'%x.jump)  for x in li_jump_1])

    html = str(ht) + str_list

    # print html

    mailer.send('d_%s_%s'%(li[0].date,li[0].time), html)

    
          

def run():
    if not util.is_trade_day():return 
    download.download_latest()
    latest_day = util.get_today()
    li =  load_daily_stocks(latest_day)
    jump_p(li)


if __name__ == "__main__" : 
    run()
    

    




