#!/bin/bash
#
PROJECT_ROOT=$(cd "$(dirname "$0")"; cd ..; pwd) 
# source $PROJECT_ROOT/bin/common.sh 
 

function main(){
    find $PROJECT_ROOT -name "*.pyc" -exec rm -rf {} \; 
     
}


main  "$@" 