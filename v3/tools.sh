

rm -f data/future.all.csv
cat data/future/* >  data/future.all.csv
mysql -uroot -proot stocks -e ""
#LOAD DATA LOCAL INFILE 'data/future.all.csv' INTO TABLE train_data FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' 


#mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u root -p Database TableName.csv
mysqlimport --ignore-lines=1 --fields-terminated-by=, --local -u root -p stocks TableName.csv

#LOAD DATA INFILE 'data/future.all.csv' INTO TABLE future FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' 
#future

# -- select count(*),min(rate),max(rate) from future ;

select count(*),
sum(if(future_rate>0.08,1,0)) as a,sum(if(future_rate>0.08,1,0))/count(*) as b,
sum(if(future_rate<=0.08 and future_rate>=-0.1,1,0)) as c,sum(if(future_rate<=0.08 and future_rate>=-0.1,1,0))/count(*) as d,
sum(if(future_rate<-0.1,1,0)) as e,sum(if(future_rate<-0.1,1,0))/count(*) as f
from train_data;

# (使用未来5日内最高价 - 当前收盘价）/ 当前收盘价， 未来3天有下降？
# up 0.3170
# m  0.3628
# down 0.3201
# select up/total,middle/total,down/total from(
# select count(*) as total,
# sum( if(rate>0.06,1,0) ) as up,
# sum( if(rate between 0.02 and 0.06,1,0) ) as middle,
# sum( if(rate<0.02,1,0) ) as down
# from future ) as t;
