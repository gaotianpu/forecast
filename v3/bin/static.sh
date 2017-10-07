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
    echo $1 >&2  #输出至stderr 
    sqlite3 $SQLITE3_DB_FILE -separator ',' "$1"
}
#cast(100.0*up_count/all_count as decimal(2,2))
updown_select_fields="all_count,up_count,
        100.0*up_count/all_count as up_percent,
        down_count,
        100.0*down_count/all_count as down_percent"
        
updown_count_fields="count(*) as all_count,
    IFNULL(count(case when PCHG>$PCHG_HIGH_THRESHOLD then trade_date end),0) as up_count,
    IFNULL(count(case when PCHG<$PCHG_LOW_
    THRESHOLD then trade_date end),0) as down_count"

insert_fields="all_count,up_count,up_percent,down_count,down_percent"

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
# 按 $1 统计涨跌数
# Globals: 
#   PCHG_HIGH_THRESHOLD
#   PCHG_LOW_THRESHOLD
# Arguments:
#   $1  field  e.g. trade_date or stock_no 
#   $2  begin  20170900 
# Returns:
#   None
####################################### 
function stat_updown_groupby(){
    time run_sql "select $1,$updown_select_fields
        from ( select $1,$updown_count_fields from stocks_trade_records where trade_date>$2
        group by $1 ) as t order by $1" > $STAT_DATA_PATH/stat_updown_$1_$2.csv
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
    time stat_updown_groupby "trade_date" $1 
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
    time stat_updown_groupby "stock_no" $1
}

function main(){
    # stat_updown 0 20270921  #all 
    # stat_updown 20170901 20171000 #9 mon  

    # stat_updown_by_days 0 
    stat_updown_by_stocks 0 
}

main "$@"