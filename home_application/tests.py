# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.


This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# import from apps here

import sys,os
sys.path.append('home_application/')
os.environ['DJANGO_SETTINGS_MODULE'] ='settings'
from .models import *
# import from lib
from django.test import TestCase
import unittest
from models import Dicts

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # 打开文件
        # 读取内
        pass

    def tearDown(self):
        # 关闭文件
        pass
    
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         print "123456"
#         self.assertEqual(1 + 1, 2)
#         
#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
# 
#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

    def test_split(self):
        #dicts = APPConfig.objects.all()
        print ""
            
    #对象列表转换成字典
def convert_objs_to_dicts(model_obj):
    import inspect, types
    
    object_array = []
    list_data = [] 
    for obj in model_obj:
        # 获取到所有属性
        field_names_list = obj._meta.get_all_field_names()
        #print field_names_list
        for fieldName in field_names_list:
            dict_data = {}
            try:
                fieldValue = getattr(obj, fieldName)  # 获取属性值
                print fieldName, "--", type(fieldValue), "--", hasattr(fieldValue, "__dict__")
                if type(fieldValue) is datetime.date or type(fieldValue) is datetime.datetime:
    #                     fieldValue = fieldValue.isoformat()
                    fieldValue = datetime.datetime.strftime(fieldValue, '%Y-%m-%d %H:%M:%S')
                #外键与cache字段的解决办法
                #if hasattr(fieldValue, "__dict__"):
                #     fieldValue = convert_obj_to_dicts(fieldValue)
            
                dict_data[fieldName]=fieldValue
                #setattr(obj, fieldName, fieldValue)
                #print fieldName, "\t", fieldValue
            except Exception, ex:
                print ex
                pass
        list_data.append(dict_data)
        # 先把Object对象转换成Dict
        dict = {}
        dict.update(obj.__dict__)
        dict.pop("_state", None)  # 此处删除了model对象多余的字段
        object_array.append(dict)
    print list_data
    
    return list_data

            
if __name__ == '__main__':
    unittest.main()