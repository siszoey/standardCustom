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
    

class Building(models.Model):
    buid_name=models.CharField(u"楼宇",max_length=255,null=True,blank=True)
    service_addr=models.CharField(u"接口地址",max_length=255,null=True,blank=True)
    
class Students(models.Model):
    stu_code = models.CharField(u"学号",max_length=255,unique=True)
    stu_name = models.CharField(u"姓名",max_length=255)
    stu_class = models.CharField(u"班级",max_length=255)
    stu_build = models.CharField(u"楼宇",max_length=255)
    stu_room = models.CharField(u"寝室",max_length=255)
    stu_img = models.CharField(u"照片",max_length=255)
    stu_status_date = models.DateTimeField(u"状态时间",auto_now = True)
    
class StuFlows(models.Model):
    stu_code = models.CharField(u"学号",max_length=255)
    stu_flow_date = models.DateTimeField(u"抓拍时间")
    stu_img = models.CharField(u"照片",max_length=255)
    in_or_out = models.CharField(u"进出类型",max_length=255)
    
class StuOut(models.Model):
    stu_out_flow_date = models.DateTimeField(u"抓拍时间")
    stu_out_img = models.CharField(u"照片",max_length=255)
    in_or_out = models.CharField(u"进出类型",max_length=255)
    type = models.CharField(u"是否人工处理",max_length=255)
    
    

