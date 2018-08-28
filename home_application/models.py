# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""

# from django.db import models

from django.db import models
#字典模型
class Dicts (models.Model):
    dict_class=models.CharField(u"字典类别",max_length=255)
    dict_type=models.CharField(u"字典类型",max_length=255)
    dict_name=models.CharField(u"字典名称",max_length=255)
    dict_value=models.CharField(u"字典值",max_length=255)
    dict_status=models.IntegerField(u"字典状态")
    dict_mark=models.CharField(u"字典备注",max_length=1000,null=True,blank=True)


#应用配置模型
class APPConfig (models.Model):
    app_name=models.CharField(u"应用名称",max_length=255)
    app_host_ip=models.CharField(u"应用所属主机",max_length=255)
    #app_type=models.IntegerField(u"业务类型")
    app_type=models.ForeignKey(Dicts)
    app_biz_id=models.IntegerField(u"主机业务ID")
    host_os_type=models.CharField(u"主机操作系统类别",max_length=255)
    host_source=models.CharField(u"主机源",max_length=255,null=True,blank=True)
    app_biz_name=models.CharField(u"主机业务名",max_length=255,null=True,blank=True)
    app_config_file_path=models.CharField(u"应用配置路径",max_length=1000)
    app_bak_path=models.CharField(u"应用备份路径",max_length=1000)
    app_check_cycle=models.BigIntegerField(u"检查周期")
    app_check_unit=models.CharField(u"单位",max_length=255,null=True,blank=True)
    app_status=models.IntegerField(u"应用状态")
    app_create_time=models.DateTimeField(u"创建时间")
    app_creator=models.CharField(u"创建人",max_length=10)
    app_mark=models.CharField(u"应用备注",max_length=1000,null=True,blank=True)
    app_last_bak_time=models.DateTimeField(u"最后备份时间",null=True,blank=True)
    app_last_bak_md5=models.CharField(u"最后备份MD5",max_length=255,null=True,blank=True)
    check_time=models.DateTimeField(u"校验时间",null=True,blank=True)
    check_result=models.CharField(u"校验结果",max_length=255,null=True,blank=True)
    

#备份中间表，该模型的记录未存在时插入，存在时仅更新
class APPChangeRel (models.Model):
    app_id=models.IntegerField(u"应用ID")
    change_file=models.CharField(u"变更文件",max_length=1000)
    bak_time=models.DateTimeField(u"备份时间")
    bak_path=models.CharField(u"备份路径",max_length=255)
    task_id=models.CharField(u"任务ID",max_length=255)
    file_md5=models.CharField(u"备份时间点文件MD5",max_length=255)
    check_time=models.DateTimeField(u"检查时间",null=True,blank=True)
    check_result=models.CharField(u"检查结果",max_length=255,null=True,blank=True)

       
class APPChange (models.Model):
    app_id=models.IntegerField(u"应用ID")
    app_in_host=models.CharField(u"应用所属主机",max_length=255)
    app_name=models.CharField(u"应用名称",max_length=255)
    app_type=models.CharField(u"应用类型",max_length=255)
    type_id=models.IntegerField(u"类型ID")
    change_type=models.IntegerField(u"变更类型",null=True,blank=True)
    change_file=models.CharField(u"变更文件",max_length=1000,null=True,blank=True)
    app_last_bak_time=models.DateTimeField(u"最近成功备份时间",null=True,blank=True)
    bak_time=models.DateTimeField(u"备份时间",null=True,blank=True)
    bak_result=models.CharField(u"备份结果",max_length=255,null=True,blank=True)
    bak_path=models.CharField(u"备份路径",max_length=255,null=True,blank=True)
    change_time=models.DateTimeField(u"变更时间",null=True,blank=True)
    change_result=models.CharField(u"变更结果",max_length=255,null=True,blank=True)
    confirm_status=models.CharField(u"状态确认",max_length=255,null=True,blank=True)
    confirm_time=models.DateTimeField(u"确认时间",null=True,blank=True)
    confirm_mark=models.CharField(u"确认备注",max_length=255,null=True,blank=True)
    check_time=models.DateTimeField(u"检查时间",null=True,blank=True)
    check_result=models.CharField(u"检查结果",max_length=255,null=True,blank=True)
    task_id=models.CharField(u"任务ID",max_length=255,null=True,blank=True)
    is_get_task_exe_result=models.IntegerField(u"是否已获取结果执行结果",null=True,blank=True)
    
class APPChangeTask (models.Model):
    app_id=models.IntegerField(u"应用ID")
    app_in_host=models.CharField(u"应用所属主机",max_length=255)
    app_name=models.CharField(u"应用名称",max_length=255)
    app_type=models.CharField(u"应用类型",max_length=255) 
    type_id=models.IntegerField(u"类型ID")
    change_type=models.IntegerField(u"变更类型",null=True,blank=True)
    change_file=models.CharField(u"变更文件",max_length=1000,null=True,blank=True)
    app_last_bak_time=models.DateTimeField(u"最近成功备份时间",null=True,blank=True)
    bak_time=models.DateTimeField(u"备份时间",null=True,blank=True)
    bak_result=models.CharField(u"备份结果",max_length=255,null=True,blank=True)
    bak_path=models.CharField(u"备份路径",max_length=255,null=True,blank=True)
    change_time=models.DateTimeField(u"变更时间",null=True,blank=True)
    change_result=models.CharField(u"变更结果",max_length=255,null=True,blank=True)
    confirm_status=models.CharField(u"状态确认",max_length=255,null=True,blank=True)
    confirm_time=models.DateTimeField(u"确认时间",null=True,blank=True)
    confirm_mark=models.CharField(u"确认备注",max_length=255,null=True,blank=True)
    check_time=models.DateTimeField(u"检查时间",null=True,blank=True)
    check_result=models.CharField(u"检查结果",max_length=255,null=True,blank=True)
    task_id=models.CharField(u"任务ID",max_length=255,null=True,blank=True)
    is_get_task_exe_result=models.IntegerField(u"是否已获取结果执行结果",null=True,blank=True)
