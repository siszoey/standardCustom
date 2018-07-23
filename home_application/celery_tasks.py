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
from home_application.models import Dicts,APPConfig,APPChange,APPChangeRel,APPChangeTask
import os,base64,copy,datetime,re,json
from django.core.cache import cache
import time



#task-work
@task()
def async_task_load_app_config():
    """
            定义一个 celery 异步任务,负责更新应用配置列表，当有应用数据更新时触发
    """
    now = datetime.datetime.now()
    logger.info(u"async_task_load_app_config 定时任务加载应用配置数据：{}".format(now))
    cache.set("APPConfig", APPConfig.objects.all())
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
    now = datetime.datetime.now()
    apps=cache.get("APPConfig")
    print "缓存数据:"
    print apps
    if apps == None or len(apps) <= 0:
        execute_task()
        logger.info(u"加载应用配置缓存数据成功  {}".format(now))
        apps=cache.get("APPConfig")
        print "缓存数据:"
        print apps
    if apps == None or len(apps) <= 0:
        logger.error(u"缓存无数据，从数据库加载数据：{}".format(now))
        apps = APPConfig.objects.all()
    #调用校验方法
    exec_app_check(apps)

def exec_app_check(apps):
    now = datetime.datetime.now()
    if apps != None or len(apps) > 0:
        for app in apps:
            user_name = app.app_creator
            curr_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            bak_file_dir = app.app_bak_path+"/"+curr_time
            check_cycle = 0
            if app.app_check_unit == "day":
                check_cycle = app.app_check_cycle * 24 * 60 * 60
            elif app.app_check_unit == "hour":
                check_cycle = app.app_check_cycle * 60 * 60
            elif app.app_check_unit == "minute":
                check_cycle = app.app_check_cycle * 60 
            #判断是否达到check时间，如果check时间为空，则表示第一次校验，先执行一次备份
            #调用check方法，传入文件路径，MD5值，备份路径目录
            #这里的文件路径主要来源于执行文件路径，和配置文件路径两个字段，每个字段均可能有多个文件，多个文件时用","分隔
            strs_conf = app.app_config_file_path.split(",")
            files = strs_conf
            for file in files:
                #检查是否已经存在备份记录，不存在则认为是第一次校验
                chg_rel = APPChangeRel.objects.filter(app_id=app.id,change_file=file)
                if chg_rel != None and len(chg_rel) > 0:
                    logger.info(u"开始校验应用  已有校验记录 当前时间：{}".format(now))
                    #logger.info(u"开始校验应用 "+app.app_name+u" 校验周期为："+check_cycle+u"秒,上次校验时间为："+chg_rel[0].check_time+u" 当前时间：{}".format(now))    
                    curr_time = datetime.datetime.now()
                    check_time = chg_rel[0].check_time
                    if check_cycle < (curr_time - check_time).seconds:
                        biz_ips = {}
                        biz_ips["ip"] = app.app_host_ip
                        biz_ips["source"] = app.host_source
                        ip_list = []
                        bak_file_dir = bak_file_dir+file.split('.')[0]
                        ip_list.append(biz_ips)
                        chg_rel = APPChangeRel.objects.filter(app_id=app.id,change_file=file)
                        if chg_rel != None and len(chg_rel) > 0:#文件已存在备份记录
                            file_md5=chg_rel[0].file_md5
                            param = '%s %s %s' % (file, file_md5,bak_file_dir)
                            client = get_client_by_user(user_name)
                            kwargs = {
                                "username":user_name, 
                                "app_id":app.app_biz_id,
                                "content":base64.encodestring(redExecFile("filemd5.sh")),
                                "script_timeout":60,
                                "script_param":param,
                                "ip_list":ip_list, "type":1, "account":'root',            
                            }
                            result = client.job.fast_execute_script(kwargs)
                            if result['code'] != 0:
                                logger.error(u"执行脚本失败：{}".format(datetime.datetime.now()))
                            task_instance_id = result['data']['taskInstanceId']
                            addChange(app.app_host_ip,app.app_name,task_instance_id,file,app.id,bak_file_dir)
                            logger.info(u"应用文件校验成功， 当前时间：{}".format(now))
                    else:
                        logger.info(u"应用 件未到校验时间， 当前时间：{}".format(now)) 
                else :
                    logger.info(u"应用开始第一次校验，当前时间：{}".format(now))    
                    #调用check方法，传入文件路径，MD5值，备份路径目录
                    #这里的文件路径主要来源于执行文件路径，和配置文件路径两个字段，每个字段均可能有多个文件，多个文件时用","分隔
                    biz_ips = {}
                    biz_ips["ip"] = app.app_host_ip
                    biz_ips["source"] = app.host_source
                    ip_list = []
                    bak_file_dir = bak_file_dir+file.split('.')[0]
                    ip_list.append(biz_ips)
                    param = '%s %s %s' % (file, app.app_last_bak_md5,bak_file_dir)
                    client = get_client_by_user(user_name)
                    kwargs = {
                        "username":user_name, 
                        "app_id":app.app_biz_id,
                        "content":base64.encodestring(redExecFile("filemd5.sh")),
                        "script_param":param,
                        "ip_list":ip_list, "type":1, "account":'root',            
                    }
                    result = client.job.fast_execute_script(kwargs)
                    if result['code'] != 0:
                        logger.error(u"执行脚本失败：{}".format(datetime.datetime.now()))
                    else:
                        #脚本执行成功，
                        task_instance_id = result['data']['taskInstanceId']
                        addChange(app.app_host_ip,app.app_name,task_instance_id,file,app.id,bak_file_dir)       
                            
                        logger.info(u"应用 第一次校验成功，当前时间：{}".format(now))


#检查发现有变更后（或第一次校验）调用该方法插入变更数据
def addChange(app_in_host,app_name,task_id,change_file,app_id,bak_file_dir):
    change_type=0
    check_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    check_result=u"检查成功，未返回检查结果"
    is_get_task_exe_result=0
    app = APPConfig.objects.get(id=app_id)
    dict = Dicts.objects.get(id=app.app_type)
    try:
        APPChangeTask.objects.create(app_id=app_id,app_in_host=app_in_host,app_name=app_name
                             ,task_id=task_id,change_file=change_file
                             ,check_time=check_time,check_result=check_result
                             ,is_get_task_exe_result=is_get_task_exe_result,bak_path=bak_file_dir
                             ,app_type=dict.dict_name,type_id=dict.id)
        updAppCheck(app_id,check_time,check_result)
    except:
        logger.error(u"检查后保存数据失败：{}".format(datetime.datetime.now()))

#每次检查如果无变更也去更新时间和task_id
def updAppCheck(id,check_time,check_result):
    try:
        appchg = APPConfig.objects.filter(id=id).update(check_time=check_time,check_result=check_result)
    except:
        return

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
    now = datetime.datetime.now()
    dicts = APPChangeTask.objects.filter(is_get_task_exe_result=0)
    if dicts != None and len(dicts) > 0:
        for obj in dicts:
            task_instance_id = int(obj.task_id)
            app_id = int(obj.app_id)
            app = APPConfig.objects.get(id=app_id)
            client = get_client_by_user(app.app_creator)
            kwargs = {
                "task_instance_id": task_instance_id
            }
            currTime = datetime.datetime.now()
            checkTime = obj.check_time
            if (currTime - checkTime).seconds > 10: #校验10秒后去获取结果
                result = client.job.get_task_ip_log(kwargs)
                ipLogContent = result.get('data')[0].get('stepAnalyseResult')[0].get('ipLogContent')[0]
                exeStatus = int(ipLogContent.get('status'))
                if exeStatus == 9 or exeStatus == 104:
                    exitCode = ipLogContent.get('exitCode')
                    #logger.info(u"task_id  获取结果成功,当前时间：{}".format(now))
                    if exitCode == 1:#参数不全
                        #APPChange.objects.filter(task_id=task_instance_id).update(check_result="调用脚本参数不全",is_get_task_exe_result=1)  
                        APPChangeTask.objects.filter(task_id=task_instance_id).delete()
                        #APPConfig.objects.filter(id=app_id).update(check_time=ipLogContent.get('startTime')
                        #                                           ,check_result="调用脚本参数不全")
                        chg_rel = APPChangeRel.objects.filter(app_id=app_id,change_file=obj.change_file)
                        if chg_rel != None and len(chg_rel) > 0:#文件已存在备份记录
                            chg_rel[0].task_id=task_instance_id
                            chg_rel[0].check_time=ipLogContent.get('startTime')
                            chg_rel[0].check_result=u"调用脚本参数不全"
                            chg_rel[0].save()
                        logger.info(u"task_id获取结果成功-调用脚本参数不全, 当前时间：{}".format(now))
                        #return render_json({'code':True, 'text':"提取结果成功，调用脚本参数不全"})
                    elif exitCode == 2:#校验配置文件不存在
                        #APPChange.objects.filter(task_id=task_instance_id).update(check_result="调用脚本参数不全",is_get_task_exe_result=1)
                        APPChangeTask.objects.filter(task_id=task_instance_id).delete()
                        #APPConfig.objects.filter(id=app_id).update(check_time=ipLogContent.get('startTime')
                        #                                           ,check_result="校验配置文件不存在")
                        chg_rel = APPChangeRel.objects.filter(app_id=app_id,change_file=obj.change_file)
                        if chg_rel != None and len(chg_rel) > 0:#文件已存在备份记录
                            chg_rel[0].task_id=task_instance_id
                            chg_rel[0].check_time=ipLogContent.get('startTime')
                            chg_rel[0].check_result=u"校验配置文件不存在"
                            chg_rel[0].save()
                        logger.info(u"task_id 获取结果成功, 校验配置文件不存在, 当前时间：{}".format(now))
                        #return render_json({'code':True, 'text':"提取结果成功，校验配置文件不存在"})
                    elif exitCode == 3:#文件未发生变化
                        #APPChange.objects.filter(task_id=task_instance_id).update(check_result="文件未发生变化",is_get_task_exe_result=1)
                        APPChangeTask.objects.filter(task_id=task_instance_id).delete()
                        #APPConfig.objects.filter(id=app_id).update(check_time=ipLogContent.get('startTime')
                        #                                           ,check_result="文件未发生变化")
                        chg_rel = APPChangeRel.objects.filter(app_id=app_id,change_file=obj.change_file)
                        if chg_rel != None and len(chg_rel) > 0:#文件已存在备份记录
                            chg_rel[0].task_id=task_instance_id
                            chg_rel[0].check_time=ipLogContent.get('startTime')
                            chg_rel[0].check_result=u"文件未发生变化"
                            chg_rel[0].save()
                        logger.info(u"task_id 获取结果成功, 文件未发生变化, 当前时间：{}".format(now))
                        #return render_json({'code':True, 'text':"提取结果成功，文件未发生变化"})  
                    elif exitCode == 0:#拷贝成功
                        checkContent = ipLogContent.get('logContent') 
                        file_md5 = re.findall("file_md5=\w+", checkContent)[0].split("=")[1]
                        #APPConfig.objects.filter(id=app_id).update(check_time=ipLogContent.get('startTime')
                        #                                          ,check_result="文件发生变化，并备份成功")
                        is_get_task_exe_result=1
                        chg_rel = APPChangeRel.objects.filter(app_id=app_id,change_file=obj.change_file)
                        if chg_rel != None and len(chg_rel) > 0:#文件已存在备份记录
                            #更新变更表
                            cfg_task = APPChangeTask.objects.filter(task_id=task_instance_id)
                            if cfg_task != None and len(cfg_task) > 0 and chg_rel[0].file_md5 != file_md5:
                                APPChange.objects.create(app_id=cfg_task[0].app_id,app_in_host=cfg_task[0].app_in_host
                                                         ,app_name=cfg_task[0].app_name
                                                         ,app_type=cfg_task[0].app_type
                                                         ,type_id=cfg_task[0].type_id,change_file=cfg_task[0].change_file
                                                         ,bak_result=u"成功"
                                                         ,app_last_bak_time=chg_rel[0].bak_time
                                                         ,bak_time=ipLogContent.get('startTime')
                                                         ,bak_path=obj.bak_path
                                                         ,confirm_status="0"
                                                         ,check_result=u"文件发生变化，并备份成功"
                                                         ,check_time=cfg_task[0].check_time
                                                         ,is_get_task_exe_result=is_get_task_exe_result) 
                            APPChangeTask.objects.filter(task_id=task_instance_id).delete()#不保存已知类型错误或成功
                            chg_rel[0].bak_time=ipLogContent.get('startTime')
                            chg_rel[0].bak_path=obj.bak_path
                            chg_rel[0].file_md5=file_md5
                            chg_rel[0].task_id=task_instance_id
                            chg_rel[0].check_time=cfg_task[0].check_time
                            chg_rel[0].check_result=u"文件发生变化，并备份成功"
                            chg_rel[0].save()
                        else:#文件未存在备份记录
                            APPChangeRel.objects.create(app_id=app_id,change_file=obj.change_file
                                                        ,bak_time=ipLogContent.get('startTime')
                                                        ,bak_path=obj.bak_path,task_id=task_instance_id
                                                        ,file_md5=file_md5,check_time=ipLogContent.get('startTime')
                                                        ,check_result=u"文件发生变化，并备份成功")
                        
                            #更新变更表
                            cfg_task = APPChangeTask.objects.filter(task_id=task_instance_id)
                            if cfg_task != None and len(cfg_task) > 0:
                                APPChange.objects.create(app_id=cfg_task[0].app_id,app_in_host=cfg_task[0].app_in_host
                                                         ,app_name=cfg_task[0].app_name,app_type=cfg_task[0].app_type
                                                         ,type_id=cfg_task[0].type_id,change_file=cfg_task[0].change_file
                                                         ,app_last_bak_time=ipLogContent.get('startTime')
                                                         ,bak_time=ipLogContent.get('startTime')
                                                         ,bak_result=u"成功"
                                                         ,bak_path=obj.bak_path
                                                         ,confirm_status="0"
                                                         ,check_result=u"文件发生变化，并备份成功"
                                                         ,check_time=cfg_task[0].check_time
                                                         ,is_get_task_exe_result=is_get_task_exe_result)
                                APPChangeTask.objects.filter(task_id=task_instance_id).delete()#不保存已知类型错误或成功
                        logger.info(u"task_id 获取结果成功,结果拷贝成功, 当前时间：{}".format(now))
                    else:#文件发生变化，备份异常失败,保留该task
                        chg_rel = APPChangeRel.objects.filter(app_id=app_id,change_file=obj.change_file)
                        if chg_rel != None and len(chg_rel) > 0:#文件已存在备份记录
                            app_last_bak_time=chg_rel[0].bak_time
                            cfg_task = APPChangeTask.objects.filter(task_id=task_instance_id)
                            if cfg_task != None and len(cfg_task) > 0 and chg_rel[0].file_md5 != file_md5:
                                APPChange.objects.create(app_id=cfg_task[0].app_id,app_in_host=cfg_task[0].app_in_host
                                                             ,app_name=cfg_task[0].app_name,app_type=cfg_task[0].app_type
                                                             ,type_id=cfg_task[0].type_id,change_file=cfg_task[0].change_file
                                                             ,app_last_bak_time=app_last_bak_time
                                                             ,bak_time=ipLogContent.get('startTime')
                                                             ,bak_result=u"失败"
                                                             ,bak_path=obj.bak_path
                                                             ,confirm_status="0"
                                                             ,check_result=u"文件发生变化，备份未成功"
                                                             ,check_time=cfg_task[0].check_time
                                                             ,is_get_task_exe_result=is_get_task_exe_result)
                            APPChangeTask.objects.filter(task_id=task_instance_id).update(check_result=u"文件发生变化，备份未成功"
                                                             ,check_time=ipLogContent.get('startTime')
                                                             ,is_get_task_exe_result=exeStatus
                                                             ,bak_result=u"失败"
                                                             ,app_last_bak_time=app_last_bak_time)
                        else:
                            cfg_task = APPChangeTask.objects.filter(task_id=task_instance_id)
                            if cfg_task != None and len(cfg_task) > 0:
                                APPChange.objects.create(app_id=cfg_task[0].app_id,app_in_host=cfg_task[0].app_in_host
                                                             ,app_name=cfg_task[0].app_name,app_type=cfg_task[0].app_type
                                                             ,type_id=cfg_task[0].type_id,change_file=cfg_task[0].change_file
                                                             ,app_last_bak_time=ipLogContent.get('startTime')
                                                             ,bak_time=ipLogContent.get('startTime')
                                                             ,bak_result=u"失败"
                                                             ,bak_path=obj.bak_path
                                                             ,confirm_status="0"
                                                             ,check_result=u"文件发生变化，备份未成功"
                                                             ,check_time=cfg_task[0].check_time
                                                             ,is_get_task_exe_result=is_get_task_exe_result)
                            APPChangeTask.objects.filter(task_id=task_instance_id).update(check_result=u"文件发生变化，备份未成功"
                                                             ,check_time=ipLogContent.get('startTime')
                                                             ,is_get_task_exe_result=exeStatus
                                                             ,bak_result=u"失败"
                                                             ,app_last_bak_time=ipLogContent.get('startTime'))     
                        logger.info(u"task_id获取结果成功,结果 文件发生变化，备份异常失败, 当前时间：{}".format(now))
                elif exeStatus == 7 or exeStatus == 5:#不正常exeStatus
                    is_get_task_exe_result = 0
                    chg_rel = APPChangeRel.objects.filter(app_id=app_id,change_file=obj.change_file)
                    if chg_rel != None and len(chg_rel) > 0:#文件已存在备份记录
                        app_last_bak_time=chg_rel[0].bak_time
                        APPChangeTask.objects.filter(task_id=task_instance_id).\
                        update(check_result=u"正在校验，脚本未执行结束"
                               ,check_time=ipLogContent.get('startTime')
                               ,is_get_task_exe_result=is_get_task_exe_result
                               ,bak_result=u"失败"
                               ,app_last_bak_time=app_last_bak_time)
                    else:
                        APPChangeTask.objects.filter(task_id=task_instance_id).\
                        update(check_result=u"正在校验，脚本未执行结束"
                               ,check_time=ipLogContent.get('startTime')
                               ,is_get_task_exe_result=is_get_task_exe_result
                               ,bak_result=u"失败"
                               ,app_last_bak_time=ipLogContent.get('startTime'))
                    logger.info(u"task_id未取到结果，脚本执行未结束,当前时间：{}".format(now))
                else:
                    chg_rel = APPChangeRel.objects.filter(app_id=app_id,change_file=obj.change_file)
                    if chg_rel != None and len(chg_rel) > 0:#文件已存在备份记录
                        app_last_bak_time=chg_rel[0].bak_time
                        APPChangeTask.objects.filter(task_id=task_instance_id).\
                        update(check_result=u"脚本执行返回未知异常"
                               ,check_time=ipLogContent.get('startTime')
                               ,is_get_task_exe_result=exeStatus
                               ,bak_result=u"失败"
                               ,app_last_bak_time=app_last_bak_time)
                    else:
                        APPChangeTask.objects.filter(task_id=task_instance_id).\
                        update(check_result=u"脚本执行返回未知异常"
                               ,check_time=ipLogContent.get('startTime')
                               ,is_get_task_exe_result=exeStatus
                               ,bak_result=u"失败"
                               ,app_last_bak_time=ipLogContent.get('startTime'))
                    logger.info(u"task_id未取到结果，脚本执行返回异常,当前时间：{}".format(now))    
            else:
                logger.info(u"task_id 未到获取结果时间,当前时间：{}".format(now))
