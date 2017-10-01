#!/bin/bash
#
PROJECT_ROOT=$(cd "$(dirname "$0")"; cd ..; pwd) 
source $PROJECT_ROOT/conf/conf.sh

function run_sql(){
    sqlite3 $SQLITE3_DB_FILE -separator ',' "$1"
}

function main(){
    # total=`run_sql "select count(*) from stocks_trade_records"`  
    # echo $total 

    run_sql "select IFNULL(count(case when PCHG>1 then trade_date end),0) 
        from stocks_trade_records"
}

main "$@"