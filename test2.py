#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from config import dbr,dbw

tableName = 'stock_daily'
categoryField = 'future1_range'
featureFields =('trend_3','trend_5','candle_sort','up_or_down','volume_level')

def updateP(p,count,category,feature,featureField):
    cfKey = "%s|%s" % (feature,category) if featureField else (category if category else 'none')
    cfKey = "%s|%s" % (cfKey,featureField)
    row = list(dbr.select('category_feature_probability',where='cfKey=$cfKey',vars=locals()))
    sql = "insert into category_feature_probability set probability=%s,category='%s',feature='%s',cfKey='%s',count=%s,field='%s'"  % (p,category,feature,cfKey,count,featureField) 
    if row:
        sql = "update category_feature_probability set probability=%s,category='%s',feature='%s',count=%s,field='%s' where id=%s"  % (p,category,feature,count,featureField,row[0].id) 
    dbw.query(sql)

def loadP():
    d={}
    rows = dbr.select('category_feature_probability')
    for r in rows:
        d[r.cfKey] = r
    return d   

def getCategories(): #where %s is not null
    sql = """select %s,count(*) as count from %s  group by %s """ % (categoryField,tableName,categoryField)
    l = list(dbr.query(sql))
    print l
    count_sum = sum([r.count for r in l])
    
    d = {}
    for i in l:
        if not i[categoryField]:
            continue   #none的情况
        probability = float(i.count)/count_sum
        cat = i[categoryField]  
        d[cat] = web.storage(category=cat,count=i.count,probability=probability) 
        updateP(probability,i.count,cat,'','')
    
    return d

def computeOneFeatue(categories,field):
    #where category is not null and feature1 is not null  
    sql="select %s,%s,count(*) as count from %s where %s is not null and %s is not null group by %s,%s" % (field,categoryField,tableName,field,categoryField,field,categoryField)
    l = list(dbr.query(sql))
    total_count = sum([r.count for r in l]) 
    features = list(set([r[field] for r in l]))    
    d={}
    for cat,catV in categories.items():       
        for f in features:
            if not f:
                continue   #none的情况?
            f_count = sum([r.count for r in l if r[categoryField]==cat and r[field]==f])
            probability = float(f_count)/catV.count
            d['%s|%s'%(f,cat)] = web.storage(probability=probability,count=f_count) 
            updateP(probability,f_count,cat,f,field)
    return d 

def computeMultiFeatures(categories):
    d = categories
    for f in featureFields:
        tmpD = computeOneFeatue(categories,f)
        d = dict(d,**tmpD)    
    return d

def compute():
    categories = getCategories()    
    allpp = computeMultiFeatures(categories)

def run(features,categories,allpp):    
    d={}
    for catName,cat in categories.items():
        p = cat.probability
        for field,f  in features.items():
            k = '%s|%s|%s'%(f,cat.category,field)
            print k
            if k in allpp: 
                p =  allpp[k].probability * p
            else:
                p = 0        
         
        d[cat.category] = p    
  
    print '-------------------------'
    for k,v in d.items():
        print k,v
    #d[2]/abp[1] #上升概率是下降概率的多少倍
    return d #l

#####
def getFeatures(featureField):
    sql = "select distinct %s from %s " % (featureField,tableName)
    return [r[featureField] for r in dbr.query(sql)]

def tmp():
    categories = getCategories()
    allpp = loadP() 

    l = []
    fvals3 = getFeatures('trend_3')
    fvals5 = getFeatures('trend_5')
    for f3 in fvals3:
        if not f3:
            continue
        for f5 in fvals5:
            if not f5:
                continue
            abp = run([f3,f5],categories,allpp)

            l.append(web.storage(features='%s|%s'%(f3,f5), probability=abp[2]/abp[1]) ) 
    l=sorted(l,key=lambda x:x.probability)
    for i in l :
        print i.features,i.probability
    return l

     
if __name__ == "__main__":
    compute()

    a = 4.11657157258e-05
    b = 1.0775093246e-05
    print b/a

    #categories = getCategories()
    #allpp = loadP() 
    #run([u'321',u'12345'],categories,allpp)
    #tmp()
    #compute()
    #l = run([u'321',u'12345'])
    #for  i in l:
    #    print i.category, i.probability
    
    # d = computeMultiFeatures()
    
    # for k,v in d.items():
    #     print k,v.probability,v.count    
