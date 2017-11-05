#!/bin/bash
#
# 配置文件
readonly DATA_ROOT=$PROJECT_ROOT/data 

readonly ALL_STOCKS_FILE=$DATA_ROOT/all_stocks.csv  #所有A股信息

readonly HISTORY_DATA_PATH=$DATA_ROOT/history 
readonly HISTORY_CONVERTED_PATH=$HISTORY_DATA_PATH/converted
readonly STAT_DATA_PATH=$DATA_ROOT/stat

readonly ALL_STOCKS_WITHOUT_HEADER_FILE=$DATA_ROOT/all_stocks_without_header.csv
readonly ALL_HISTORY_FILE=$DATA_ROOT/history.csv 
readonly SQLITE3_DB_FILE=$DATA_ROOT/FORECAST.db
    