#!/bin/bash

function recur(){

if [ $# -eq 1 ];then
    if [ -d $1 ];then
        for file in `ls $1`
        do
            if [ -d $1/$file ];then
                recur $1/$file
            else
                python markup.py < $1/$file > $1/$file.html
            fi
            
        done
    elif [ -f $1 ];then
        python markup.py < $1 > $1.html
    fi
fi

}
 
recur $1
