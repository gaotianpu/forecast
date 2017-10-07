#!/bin/bash
# 初始化脚本
#

PROJECT_ROOT=$(cd "$(dirname "$0")"; cd ..; pwd)  
source $PROJECT_ROOT/conf/conf.sh

#######################################
# 初始化SQLite
# Globals:
#   PROJECT_ROOT 
#   SQLITE3_DB_FILE
# Arguments:
#   None
# Returns:
#   None
####################################### 
function create_db_schema(){ 
    echo "create_db_schema"
    if [ -f $SQLITE3_DB_FILE ]; then 
        rm -rf $SQLITE3_DB_FILE 
    fi

    sqlite3 $SQLITE3_DB_FILE < $PROJECT_ROOT/setup/schema.sql || exit 
} 

function make_lable(){
    forecast_day=$1
    echo "make_label $forecast_day"
    $PROJECT_ROOT/bin/make_label.py $forecast_day > $STAT_DATA_PATH/lablel_$forecast_day.csv 
    time sqlite3 $SQLITE3_DB_FILE -separator ',' ".import $STAT_DATA_PATH/lablel_$forecast_day.csv  stocks_forecast_day$forecast_day"

}

#######################################
# 主函数
# Globals: 
#   DATA_ROOT
#   HISTORY_N  回溯多长时间的历史数据
# Arguments:
#   None
# Returns:
#   None
####################################### 
function main(){
    create_db_schema 

    echo "import stocks" 
    time sqlite3 $SQLITE3_DB_FILE -separator ',' ".import $ALL_STOCKS_FILE stocks" 

    echo "convert trade records"
    time $PROJECT_ROOT/bin/history_data.py > $HISTORY_DATA_PATH/all.csv  || exit 
    
    echo "import stocks trade records"
    time sqlite3 $SQLITE3_DB_FILE -separator ',' "delete from stocks_trade_records"  || exit 
    time sqlite3 $SQLITE3_DB_FILE -separator ',' ".import $HISTORY_DATA_PATH/all.csv stocks_trade_records" || exit 

    make_lable 1 
    make_lable 2
    make_lable 3 
}


main "$@"   