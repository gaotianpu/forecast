#!/bin/bash
#
PROJECT_ROOT=$(cd "$(dirname "$0")";pwd) 
source $PROJECT_ROOT/conf/conf.sh
source $PROJECT_ROOT/common/common.sh

set -e 

function download(){
    echo ''
}

# https://stackoverflow.com/questions/1521462/looping-through-the-content-of-a-file-in-bash
function main(){
    while read line; do
        #1. 下载数据
        $PROJECT_ROOT/bin/download.py $line 

        #2. 特征提取

        #3. 统计分析绘图等？

    done < $ALL_STOCKS_FILE 
}

main "$@" 