# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from common.log import logger
from blueking.component.shortcuts import get_client_by_request,get_client_by_user
from doctest import script_from_examples
from conf.default import STATICFILES_DIRS
import os,base64,copy,datetime,re,json
from django.core.cache import cache
import time



#task-work
@task()
def async_task_load_app_config():
    """
            定义一个 celery 异步任务,负责更新应用配置列表，当有应用数据更新时触发
    """
    logger.info(u"async_task_load_app_config 定时任务加载应用配置数据成功：{}".format(now))


"""
         执行 celery 异步任务

        调用celery任务方法:
    task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
    task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
    delay(): 简便方法，类似调用普通函数
    apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
            详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
"""
def execute_task():
    now = datetime.datetime.now()
    logger.info(u"正在通知任务刷新缓存，当前时间：{}".format(now))
    # 调用定时任务
    async_task_load_app_config.apply_async()


#后台任务-周期执行，判断配置表是否到达check时间
"""
celery 周期任务示例

run_every=crontab(minute='*/10', hour='*', day_of_week="*")：每 10 分钟执行一次任务
periodic_task：程序运行时自动触发周期任务
"""
@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def exec_app_check_task():
    return None

def exec_app_check(apps):
    logger.info(u"应用 第一次校验成功，当前时间：{}".format(now))


#检查发现有变更后（或第一次校验）调用该方法插入变更数据
def addChange(app_in_host,app_name,task_id,change_file,app_id,bak_file_dir):
    logger.error(u"检查后保存数据失败：{}".format(datetime.datetime.now()))

#每次检查如果无变更也去更新时间和task_id
def updAppCheck(id,check_time,check_result):
    return None

#读配置文件
def redExecFile(file_name):
    staticdir = ','.join(STATICFILES_DIRS);
    script_path = os.path.join(staticdir, str('script'))
    file = os.path.join(script_path, file_name)
    with open(file) as f:
        script_content = f.read()
    f.close()
    return script_content



"""
上部为校验的task，下部为获取结果的task
"""
@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def load_app_check_result_task():
    logger.info(u"task_id 未到获取结果时间,当前时间：{}".format(now))
