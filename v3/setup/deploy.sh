#!/bin/bash
#
PROJECT_ROOT=$(cd "$(dirname "$0")"; cd ..; pwd) 
# source $PROJECT_ROOT/bin/common.sh 

OUT_PATH=~/out 
APP_PATH=$OUT_PATH/forecast_v3
RUN_PATH=~/run/forecast_v3

function deploy(){
    if [ ! -d $OUT_PATH ];then
        mkdir $OUT_PATH
    fi 
    if [ ! -d $RUN_PATH ];then
        mkdir ~/run
        mkdir $RUN_PATH
    fi 

    rm -fR $APP_PATH 
    rm -fR $OUT_PATH/forecast_v3.tar.gz 

    rsync -av --exclude=data  $PROJECT_ROOT/ $APP_PATH 

    rm -fR $APP_PATH/data  
    # rm -fR $APP_PATH/conf  

    find $APP_PATH -name "*.pyc" -exec rm -rf {} \; 
    find $APP_PATH -name '.?*' -exec rm -rf {} \;

    cd $APP_PATH
    tar -czvf $OUT_PATH/forecast_v3.tar.gz  ./

    cp -af $APP_PATH/  $RUN_PATH
}

function main(){
    # git checkout .
    # git pull 
    deploy
}

main  "$@" 