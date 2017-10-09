#!/bin/bash
# 初始化脚本
#

PROJECT_ROOT=$(cd "$(dirname "$0")"; cd ..; pwd)  
source $PROJECT_ROOT/conf/conf.sh

#######################################
# 创建目录
# Globals:
#   DATA_ROOT 
#   HISTORY_DATA_PATH
#   STAT_DATA_PATH
# Arguments:
#   None
# Returns:
#   None
####################################### 
function make_dirs(){
    for path in $DATA_ROOT $HISTORY_DATA_PATH $HISTORY_CONVERTED_PATH $STAT_DATA_PATH
    do 
        if [ ! -d $path ];then
            mkdir $path 
        fi  
    done 
}

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

function download_convert(){
    if [ ! -f $ALL_HISTORY_FILE ];then
        echo "convert trade records" 
        time $PROJECT_ROOT/bin/history_data.py || exit  # > $HISTORY_DATA_PATH/all.csv  || exit 
        echo "merge trade records" 

        cd $HISTORY_CONVERTED_PATH
        time cat * > $ALL_HISTORY_FILE || exit 
    fi 
}

function init(){
    make_dirs  

    download_convert

    create_db_schema   

    echo "import stocks"  
    grep -v 'stock_no' $ALL_STOCKS_FILE > $ALL_STOCKS_WITHOUT_HEADER_FILE     
    time sqlite3  -separator ',' $SQLITE3_DB_FILE ".import $ALL_STOCKS_WITHOUT_HEADER_FILE stocks"  
     
    echo "import stocks trade records" 
    time sqlite3  -separator ',' $SQLITE3_DB_FILE  ".import $ALL_HISTORY_FILE stocks_trade_records" || exit 

     
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
    # init 

    make_lable 1 
    make_lable 2
    make_lable 3 
}


main "$@"   


# notes
# sqlite3: Error: too many options: "," 解决办法： -separator ',' 放置在dbfile前  
# sqlite导入Csv时，忽略标题行？
# -bash: /bin/cat: Argument list too long ?