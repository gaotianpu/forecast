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

    sqlite3 $SQLITE3_DB_FILE < $PROJECT_ROOT/setup/schema.sql 
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

    echo "convert"
    # time $PROJECT_ROOT/bin/history_data.py > $HISTORY_DATA_PATH/all.csv 
    
    echo "import"
    time sqlite3 $SQLITE3_DB_FILE -separator ',' "delete from stocks_trade_records" 
    time sqlite3 $SQLITE3_DB_FILE -separator ',' ".import $HISTORY_DATA_PATH/all.csv stocks_trade_records" 
}

main "$@"   