#!/bin/bash

anynowtime="date +'%Y-%m-%d %H:%M:%S'"
NOW="echo [\`$anynowtime\`][PID:$$]"

##### 可在脚本开始运行时调用，打印当时的时间戳及PID。
function job_start
{
    echo "`eval $NOW` job_start"
}

##### 可在脚本执行成功的逻辑分支处调用，打印当时的时间戳及PID。 
function job_success
{
    MSG="$*"
    echo "`eval $NOW` job_success:[$MSG]"
    exit 0
}

##### 可在脚本执行失败的逻辑分支处调用，打印当时的时间戳及PID。
function job_fail
{
    MSG="$*"
    echo "`eval $NOW` job_fail:[$MSG]"
    exit 1
}

##### 打印当时的时间戳及步骤id。
function job_status()
{
    MSG="$*"
    echo "`eval $NOW` job_step:[$1]"
}

job_start

###### 可在此处开始编写您的脚本逻辑代码
###### 作业平台中执行脚本成功和失败的标准只取决于脚本最后一条执行语句的返回值
###### 如果返回值为0，则认为此脚本执行成功，如果非0，则认为脚本执行失败
#conf_file, md5, bakpath

job_status 1
if [ $# -lt 3 ]; then exit 1; fi        #参数不全

conf_file=$1

job_status 2
if [ ! -f $conf_file ]; then exit 2 ; fi     #配置文件不存在

job_status 3
file_md5=`md5sum $conf_file |cut -d ' ' -f1`
echo "file_md5=$file_md5"

job_status 4
if [ $file_md5 == $2 ]; then exit 3; fi     #md5相同

job_status 5
bakpath=$3

if [ ! -d $bakpath ]; then
	mkdir -p $bakpath
else
	exit 4;       #路径已存在
fi

job_status 6

cp $conf_file $bakpath

job_status 7

exit 0;