#!/bin/bash
#
PROJECT_ROOT=$(cd "$(dirname "$0")"; cd ..; pwd) 
source $PROJECT_ROOT/conf/conf.sh

PCHG_HIGH_THRESHOLD=1.0
PCHG_LOW_THRESHOLD=-3.0


#######################################
# 简化执行sqlite sql语句
# Globals: 
#   SQLITE3_DB_FILE
# Arguments:
#   $1  sql语句
# Returns:
#   None
####################################### 
function run_sql(){
    sqlite3 $SQLITE3_DB_FILE -separator ',' "$1"
}

updown_select_fields="all_count,up_count,1.0*up_count/all_count as up_percent,
        down_count,1.0*down_count/all_count as down_percent"
updown_count_fields="count(*) as all_count,
    IFNULL(count(case when PCHG>$PCHG_HIGH_THRESHOLD then trade_date end),0) as up_count,
    IFNULL(count(case when PCHG<$PCHG_LOW_THRESHOLD then trade_date end),0) as down_count"

#######################################
# 统计给定时间段的涨跌数统计
# Globals: 
#   PCHG_HIGH_THRESHOLD
#   PCHG_LOW_THRESHOLD
# Arguments:
#   $1  begin  20170900
#   $2  end  20271000
# Returns:
#   None
####################################### 
function stat_updown(){ 
    time run_sql "select $updown_select_fields
        from ( select $updown_count_fields from stocks_trade_records 
        where trade_date>=$1 and trade_date<$2 ) as t" > $STAT_DATA_PATH/stat_updown_$2_$1.csv

}

#######################################
# 按 交易日 统计涨跌数
# Globals: 
#   PCHG_HIGH_THRESHOLD
#   PCHG_LOW_THRESHOLD
# Arguments:
#   $1  begin  20170900 
# Returns:
#   None
####################################### 
function stat_updown_by_days(){
    time run_sql "select trade_date,$updown_select_fields
        from ( select trade_date,$updown_count_fields from stocks_trade_records where trade_date>$1
        group by trade_date ) as t order by t.trade_date desc " > $STAT_DATA_PATH/stat_updown_by_days_$1.csv
}

#######################################
# 按 股票 统计涨跌数
# Globals: 
#   PCHG_HIGH_THRESHOLD
#   PCHG_LOW_THRESHOLD
# Arguments:
#   $1  begin  20170900 
# Returns:
#   None
####################################### 
function stat_updown_by_stocks(){
    time run_sql "select stock_no,$updown_select_fields
        from ( select stock_no,$updown_count_fields from stocks_trade_records where trade_date>$1
        group by stock_no ) as t order by t.stock_no" > $STAT_DATA_PATH/stat_updown_by_stocks_$1.csv
}

function main(){
    stat_updown 0 20270921  #all   
    stat_updown_by_days 0 
    stat_updown_by_stocks 0

    stat_updown 20170901 20171000 #9 mon  

    #~/run/forecast_v3/data/group_by_stocks.csv
    #~/run/forecast_v3/data/group_by_days.csv

    
}

main "$@"