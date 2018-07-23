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

from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request,get_client_by_user
from doctest import script_from_examples
from conf.default import STATICFILES_DIRS
from home_application.models import Dicts
from home_application.models import APPConfig
from home_application.models import APPChange
from home_application.models import APPChangeRel
import os,base64,copy,datetime,re,json
from django.core import serializers
from common.log import logger
from django.core.cache import cache, caches
import time
from django.apps.registry import apps

def index(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/index.html')


def home(request):
    return render_mako_context(request, '/home_application/home.html')

def apply_manage(request):
    return render_mako_context(request, '/home_application/apply_manage.html')

def apply_type(request):
    return render_mako_context(request, '/home_application/apply_type.html')

def apply_version_manage(request):
    return render_mako_context(request, '/home_application/apply_version_manage.html')

def apply_version_query(request):
    return render_mako_context(request, '/home_application/apply_version_query.html')

def edit_apply_info(request):
    return render_mako_context(request, '/home_application/edit_apply_info.html')

def add_apply_info(request):
    return render_mako_context(request, '/home_application/add_apply_info.html')

def apply_vm_box(request):
    return render_mako_context(request, '/home_application/apply_vm_box.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')

def doAddAPPTypeDict(request):
    """定义
    dict_class=models.CharField(u"字典类别",max_length=255)
    dict_type=models.CharField(u"字典类型",max_length=255)
    dict_name=models.CharField(u"字典名称",max_length=255)
    dict_value=models.CharField(u"字典值",max_length=255)
    dict_status=models.IntegerField(u"字典状态")
    dict_mark=models.CharField(u"字典备注",max_length=1000,null=True,blank=True)
    """
    dict_class="CONFCHECK"
    dict_type="APP_TYPE"
    dict_name=request.GET.get("name")
    dict_value=request.GET.get("name")
    dict_status=0
    dict_mark=request.GET.get("name")
    ret_text = "保存成功"
    ret_code = True
    try:
        Dicts.objects.create(dict_class=dict_class,dict_type=dict_type
                             ,dict_name=dict_name,dict_value=dict_value
                             ,dict_status=dict_status,dict_mark=dict_mark)
    except:
        ret_code = False
        ret_text = "保存异常"
    return render_json({'code':ret_code, 'text':ret_text})

def doModifyAppTypeict(request):
    id=request.GET.get("id")
    if id == None or id == "":
        return render_json({'code':False, 'text':"必须传入数据ID信息"})
    try:
        dict = Dicts.objects.get(id=id)
    except:
        return render_json({'code':False, 'text':"没有查到对应的数据记录"})    
    dict_name=request.GET.get("name")
    dict_value=request.GET.get("name")
    #dict_mark=request.POST.get("dict_mark")
    if dict_name == None or dict_name == "":
        return render_json({'code':False, 'text':"字典名称不能为空"})
    dict.dict_name=dict_name
    dict.dict_value=dict_value
    #if dict_mark == None and dict_mark != "":
    #    dict.dict_mark=dict_mark
    dict.save()
    return render_json({'code':True, 'text':"数据更新成功"})

def doDelAppTypeDict(request):
    id=request.GET.get("id")
    if id == None or id == "":
        return render_json({'code':False, 'text':"必须传入数据ID信息"}) 
    ret_text = "删除成功"
    ret_code = True   
    try: 
        apps = APPConfig.objects.filter(app_type=id)
        if apps != None and len(apps) > 0:
            return render_json({'code':ret_code, 'text':"类型下已有应用配置，不能删除"})
        Dicts.objects.filter(id=id).delete()             
    except:
        ret_code = False
        ret_text = "删除记录异常"
    return render_json({'code':ret_code, 'text':ret_text})

def getPagingAPPTypeDictList(rq):
    try:
        page_size = int(rq.GET.get("pageSize"))
        page_number = int(rq.GET.get("pageNumber"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    dicts = Dicts.objects.filter(dict_type="APP_TYPE")[startPos:endPos]
    total = Dicts.objects.filter(dict_type="APP_TYPE").count()
    #pageCount = total / page_size
    pageCount = (total  +  page_size  - 1) / page_size
    if pageCount <= 0:
        pageCount = 1
    lastPage = True
    firstPage = True
    if(page_number != 1):
        firstPage = False
    if(lastPage != pageCount):
        lastPage=False
    return render_json({'code':True,'text':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list':  convert_objs_to_dicts(dicts)
                        ,"firstPage":firstPage,"lastPage":lastPage})

def getDictByType(rq):
    type=rq.GET.get("dict_type")
    if type == None or type =="":
        return render_json({'code':False, 'text':"字典类型不能为空"}) 
    try: 
        dicts = Dicts.objects.filter(dict_type=type)             
    except:
        return render_json({'code':False, 'text':"查询数据出错"})
    return render_json({'code':True, 'text':"查询数据成功",'list':convert_objs_to_dicts(dicts)})

def getDictById(rq):
    id=rq.GET.get("id")
    if id == None or id =="":
        return render_json({'code':False, 'text':"ID不能为空"}) 
    try: 
        dict = Dicts.objects.get(id=id)             
    except:
        return render_json({'code':False, 'text':"查询数据出错"})
    return render_json({'code': True, 'text':"查询成功",'list':convert_obj_to_dicts(dict)})

"""
records = {
        app_id:x,
        app_name:x,
        os_type:x,
        host_ip:InnerIP,
        source:source
        
}
"""
def getUserIps(request):
    biz_name = request.GET.get("biz_name")
    if biz_name == None or biz_name == "":
        return render_json({'code':False, 'text':"业务名称不能为空"})
    username = request.user.username
    if username == None or username == "":
        return render_json({'code':False, 'text':"获取用户信息错误"})  
    host_ip = {}   
    record = {}
    records = []
    ret_text = "调用成功"
    ret_code = True
    ret_num = 0
    try: 
        client = get_client_by_request(request)
        apps = client.cc.get_app_by_user(username)
        if apps.get('code') == 0:
            app_num = 0
            for app in apps.get('data'):
                app_id = app.get('ApplicationID')
                app_name = app.get('ApplicationName')
                if app_id == biz_name:
                    app_num += 1
                    kwargs = {
                        "app_id":app_id 
                    }
                    hosts = client.cc.get_app_host_list(kwargs)
                    if hosts.get('code') == 0:
                        record["app_id"] = app_id
                        record["app_name"] = app_name
                        host_ip.clear()
                        ipsss=hosts.get('data')
                        for host in hosts.get('data'):
                            osType = host.get('osType')
                            record["os_type"] = osType
                            if osType == "linux":
                                InnerIP = host.get('InnerIP')
                                Source = host.get('Source')
                                record["host_ip"] = copy.deepcopy(InnerIP)
                                record["source"] = copy.deepcopy(Source)                          
                                records.append(copy.deepcopy(record))
            records=removeObj(records)
    except:
        ret_code = False
        ret_text = "获取用户业务主机异常"
        
    return render_json({'code':ret_code, 'text':ret_text,'list':records})


def removeObj(records):
    objs=[]
    for obj in records:
       if isExsit(objs,obj) == False:
           objs.append(obj)
    return objs


def isExsit(objs,host):
    ret = False
    try:
        if objs != None and len(objs) > 0:
            for obj in objs:
                if obj["host_ip"] == host["host_ip"]:
                    ret = True
                else:
                    ret = False
        else:
            ret = False
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'repr(e):\t', repr(e)
        ret = False
    return ret

def get_user_ips(request):
    username = request.user.username  
    host_ip = {};   
    record = {};
    records = {};
    ret_text = "调用成功";
    ret_code = True;
    ret_num = 0;
    if username == "":
        return render_json({'result':False, 'ret_text':"未获取到用户信息"});
    try: 
        client = get_client_by_request(request)
        apps = client.cc.get_app_by_user(username)
        if apps.get('code') == 0:
            app_num = 0;
            for app in apps.get('data'):
                app_id = app.get('ApplicationID')
                app_name = app.get('ApplicationName')
                app_num += 1;
                kwargs = {
                    "app_id":app_id 
                }
                hosts = client.cc.get_app_host_list(kwargs)
                if hosts.get('code') == 0:
                    record["app_id"] = app_id;
                    record["app_name"] = app_name;
                    host_ip.clear();
                    for host in hosts.get('data'):
                        osType = host.get('osType')
                        if osType == "linux":
                            InnerIP = host.get('InnerIP')
                            Source = host.get('Source')
                            host_ip[InnerIP] = Source;                               
                    ret_num += len(host_ip.keys()); 
                    record["host_ip"] = copy.deepcopy(host_ip);
                records[str(app_id)] = copy.deepcopy(record);
    except:
        ret_code = False;
        ret_text = "获取用户业务主机异常"
        
    if ret_num == 0:
        ret_code = False;
        ret_text = "没有查询到相关业务主机数据"
         
    return render_json({'result':ret_code, 'text':ret_text,  'renum':ret_num , 'list':records});

def get_user_biz(request):
    username = request.user.username
    records =[]
    ret_text = "调用成功"
    ret_code = True
    ret_num = 0
    if username == "":
        return render_json({'result':False, 'ret_text':"未获取到用户信息"})
    try: 
        client = get_client_by_request(request)
        apps = client.cc.get_app_by_user(username)
        if apps.get('code') == 0:
            app_num = 0
            for app in apps.get('data'):
                app_id = app.get('ApplicationID')
                app_name = app.get('ApplicationName')
                ret_num += 1 
                obj={}
                #records[str(app_id)] = app_name
                obj["buseName"] = app_name 
                obj["buseId"] = app_id
                records.append(obj)                
    except:
        ret_code = False
        ret_text = "获取用户业务数据异常"
        
    if ret_num == 0:
        ret_code = False
        ret_text = "没有查询到相关业务"
         
    return render_json({'code':ret_code, 'text':ret_text,  'renum':ret_num , 'list':records})


def doAddAPPConfig(request):
    """定义
    app_name=models.CharField(u"应用名称",max_length=255)
    app_in_host=models.CharField(u"应用所属主机",max_length=255)
    app_type=models.IntegerField(u"应用类型")
    app_exe_file_path=models.CharField(u"应用执行文件路径",max_length=1000)
    app_config_file_path=models.CharField(u"应用配置路径",max_length=1000)
    app_src_path=models.CharField(u"应用源路径",max_length=1000)
    app_bak_path=models.CharField(u"应用备份路径",max_length=1000)
    app_check_cycle=models.IntegerField(u"检查周期(秒)")
    app_status=models.IntegerField(u"应用状态")
    app_create_time=models.DateField(u"创建时间")
    app_creator=models.CharField(u"创建人",max_length=10)
    app_mark=models.CharField(u"应用备注",max_length=1000,null=True,blank=True)
    app_last_bak_time=models.DateField(u"最后备份时间")
    """
    app_name=request.GET.get("app_name")
    app_host_ip=request.GET.get("selectHost")
    app_type=int(request.GET.get("selectApplyType"))
    app_biz_id=int(request.GET.get("biz_id"))
    host_os_type=request.GET.get("os_type")
    host_source=request.GET.get("host_source")
    app_biz_name=request.GET.get("biz_name")
    app_config_file_path=request.GET.get("deployPath")
    app_bak_path=request.GET.get("appBakPath")
    app_check_cycle=request.GET.get("checkTime")
    app_check_unit=request.GET.get("timeType")
    #app_mark=request.GET.get("app_mark")
    app_status=0
    app_create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    app_creator=request.user.username
    ret_text = "保存成功" 
    ret_code = True
    try:
        APPConfig.objects.create(app_name=app_name,app_host_ip=app_host_ip
                             ,app_type=app_type,app_biz_id=app_biz_id
                             ,host_os_type=host_os_type,host_source=host_source
                             ,app_biz_name=app_biz_name
                             ,app_config_file_path=app_config_file_path
                             ,app_bak_path=app_bak_path,app_check_cycle=app_check_cycle
                             ,app_status=app_status,app_create_time=app_create_time
                             ,app_creator=app_creator,app_check_unit=app_check_unit)
        load_apps_config_cache()
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'repr(e):\t', repr(e)
        ret_code = False
        ret_text = "保存异常"
    return render_json({'code':ret_code, 'text':ret_text})


def doModifyAPPConfig(request):
    id=request.GET.get("id")
    if id == None or id == "":
        return render_json({'code':False, 'text':"必须传入数据ID信息"})
    try:
        appCfg = APPConfig.objects.get(id=id)
    except:
        return render_json({'code':False, 'text':"没有查到对应的数据记录"})    
    app_name=request.GET.get("app_name")
    app_host_ip=request.GET.get("selectHost")
    app_type=int(request.GET.get("selectApplyType"))
    app_biz_id=int(request.GET.get("biz_id"))
    host_os_type=request.GET.get("os_type")
    host_source=request.GET.get("host_source")
    app_biz_name=request.GET.get("biz_name")
    app_config_file_path=request.GET.get("deployPath")
    app_bak_path=request.GET.get("appBakPath")
    app_check_cycle=request.GET.get("checkTime")
    app_check_unit=request.GET.get("timeType")
    #app_mark=request.GET.get("app_mark")
    appCfg.app_check_unit=app_check_unit
    appCfg.app_check_cycle=app_check_cycle
    appCfg.app_biz_name=app_biz_name
    appCfg.host_source=host_source
    appCfg.host_os_type=host_os_type
    appCfg.app_biz_id=app_biz_id
    app_status=request.GET.get("app_status")
    if app_name == None or app_name == "":
        return render_json({'code':False, 'text':"应用名称不能为空"})
    appCfg.app_name=app_name
    if app_host_ip == None or app_host_ip == "":
        return render_json({'code':False, 'text':"应用主机不能为空"})
    appCfg.app_host_ip=app_host_ip
    if app_type == None or app_type == "":
        return render_json({'code':False, 'text':"应用类型不能为空"})
    appCfg.app_type=app_type
    if app_config_file_path == None or app_config_file_path == "":
        return render_json({'code':False, 'text':"配置文件不能为空"})
    appCfg.app_config_file_path=app_config_file_path
    if app_bak_path == None or app_bak_path == "":
        return render_json({'code':False, 'text':"备份目录不能为空"})
    appCfg.app_bak_path=app_bak_path
    if app_status == None or app_status == "":
        appCfg.app_status=0
    else:
        appCfg.app_status=app_status
    appCfg.save()
    
    apps=cache.get("APPConfig")
    print apps
    #cache.set("APPConfig",APPConfig.objects.all())
    load_apps_config_cache()
    
    return render_json({'code':True, 'text':"数据更新成功"})

def doDelAPPConfig(request):
    id=request.GET.get("id")
    if id == None or id == "":
        return render_json({'code':False, 'text':"必须传入数据ID信息"}) 
    ret_text = "删除成功"
    ret_code = True
    try: 
        APPConfig.objects.filter(id=id).delete()
        load_apps_config_cache()             
    except:
        ret_code = False
        ret_text = "删除记录异常"
    return render_json({'code':ret_code, 'text':ret_text})


def load_apps_config_cache():
    # 调用定时任务
    cache.set("APPConfig", APPConfig.objects.all())
    

def getPagingAPPConfigList(rq):
    load_apps_config_cache()
    try:
        app_name = rq.GET.get("appName")
        app_ip = rq.GET.get("appIp")
        type_id = int(rq.GET.get("applyType"))
        page_size = int(rq.GET.get("pageSize"))
        page_number = int(rq.GET.get("pageNumber"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    searchCondition = {}#'md5__icontains' : md5 ,'filename__icontains':filename
    if app_name !=None and app_name != "" :
        searchCondition['app_name__icontains']=app_name
    if app_ip !=None and app_ip != "":
        searchCondition['app_host_ip__icontains']=app_ip
    if type_id !=None and type_id != 0:
        searchCondition['app_type']=type_id
    
    kwargs = getKwargs(searchCondition)
    dicts = APPConfig.objects.filter(**kwargs)[startPos:endPos]
    total = APPConfig.objects.filter(**kwargs).count()
    #dicts = APPConfig.objects.all()[startPos:endPos]
    #total = APPConfig.objects.count()
    #pageCount = total / page_size
    pageCount = (total  +  page_size  - 1) / page_size
    if pageCount <=0:
        pageCount = 1
    lastPage = True
    firstPage = True
    if(page_number != 1):
        firstPage = False
    if(lastPage != pageCount):
        lastPage=False
    return render_json({'code':True,'text':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list':  convert_objs_to_dicts(dicts)
                        ,"firstPage":firstPage,"lastPage":lastPage})
    
    
#对象列表转换成字典
def convert_objs_to_dicts(model_obj):
    import inspect, types
    
    object_array = []
     
    for obj in model_obj:
#         obj.last_update_time = obj.last_update_time.isoformat()
#         obj.create_time = obj.create_time.isoformat()
        # 获取到所有属性
        field_names_list = obj._meta.get_all_field_names()
        print field_names_list
        for fieldName in field_names_list:
            try:
                fieldValue = getattr(obj, fieldName)  # 获取属性值
                print fieldName, "--", type(fieldValue), "--", hasattr(fieldValue, "__dict__")
                if type(fieldValue) is datetime.date or type(fieldValue) is datetime.datetime:
    #                     fieldValue = fieldValue.isoformat()
                    fieldValue = datetime.datetime.strftime(fieldValue, '%Y-%m-%d %H:%M:%S')
                #外键与cache字段的解决办法
                #if hasattr(fieldValue, "__dict__"):
                #     fieldValue = convert_obj_to_dicts(fieldValue)
            
                setattr(obj, fieldName, fieldValue)
                #print fieldName, "\t", fieldValue
            except Exception, ex:
                print ex
                pass
        # 先把Object对象转换成Dict
        dict = {}
        dict.update(obj.__dict__)
        dict.pop("_state", None)  # 此处删除了model对象多余的字段
        object_array.append(dict)
    print object_array
    
    return object_array

#对象转换成字典
def convert_obj_to_dicts(obj):
    import inspect, types
    
    object_array = []
     # 获取到所有属性
    field_names_list = obj._meta.get_all_field_names()
    print field_names_list
    for fieldName in field_names_list:
        try:
            fieldValue = getattr(obj, fieldName)  # 获取属性值
            print fieldName, "--", type(fieldValue), "--", hasattr(fieldValue, "__dict__")
            if type(fieldValue) is datetime.date or type(fieldValue) is datetime.datetime:
    #           fieldValue = fieldValue.isoformat()
                fieldValue = datetime.datetime.strftime(fieldValue, '%Y-%m-%d %H:%M:%S')
                # 没想好外键与cache字段的解决办法
#                 if hasattr(fieldValue, "__dict__"):
#                     fieldValue = convert_obj_to_dicts(model_obj)
            
                setattr(obj, fieldName, fieldValue)
#                 print fieldName, "\t", fieldValue
        except Exception, ex:
            print ex
            pass
    # 先把Object对象转换成Dict
    dict = {}
    dict.update(obj.__dict__)
    dict.pop("_state", None)  # 此处删除了model对象多余的字段
    object_array.append(dict)
    print object_array
    
    return object_array

def getAPPConfigById(rq):
    id=rq.GET.get("id")
    if id == None or id =="":
        return render_json({'code':False, 'text':"ID不能为空"}) 
    try: 
        dict = APPConfig.objects.get(id=id)             
    except:
        return render_json({'code':False, 'text':"查询数据出错"})
    return render_json({'code':True, 'text':"查询数据成功",'list':convert_obj_to_dicts(dict)})


# 把MyObj对象转换成dict类型的对象
def convert_to_builtin_type(obj):
   d = {}
   d.update(obj.__dict__)
   return d


#分页查询未确认的变更
def getPagingAPPChangeByUnConfirm(rq):
    try:
        page_size = int(rq.GET.get("pageSize"))
        page_number = int(rq.GET.get("pageNumber"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    list = APPChange.objects.filter(confirm_status="0",is_get_task_exe_result=1)[startPos:endPos]
    total = APPChange.objects.filter(confirm_status="0",is_get_task_exe_result=1).count()
    #pageCount = total / page_size
    pageCount = (total  +  page_size  - 1) / page_size
    if pageCount <= 0:
        pageCount = 1
    lastPage = True
    firstPage = True
    if(page_number != 1):
        firstPage = False
    if(lastPage != pageCount):
        lastPage=False
    return render_json({'code':True,'text':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list':  convert_objs_to_dicts(list)
                        ,"firstPage":firstPage,"lastPage":lastPage})


#分页查询已确认的变更
def getPagingAPPChangeByConfirmed(rq):
    """
    WSGIRequest: <WSGIRequest: GET '/getPagingAPPChangeByConfirmed/?
     pageNumber=1&pageSize=10&appName=32&appIp=32&checkTime=2018-07-03+-+2018-08-
     16&applyType=3&changeResult=1&changeType=1'>
    """
    try:
        page_size = int(rq.GET.get("pageSize"))
        page_number = int(rq.GET.get("pageNumber"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    app_in_host = rq.GET.get("appIp")
    app_name = rq.GET.get("appName")
    type_id = int(rq.GET.get("applyType"))
    changeType = int(rq.GET.get("changeType"))
    changeResult = int(rq.GET.get("changeResult"))
    checkTime = rq.GET.get("checkTime")
    bak_result=""
    start_time=""
    end_time=""
    if checkTime != "":
        start_time=checkTime.split("~")[0]
        end_time=checkTime.split("~")[1]
    if changeResult == 1:
        bak_result="成功"
    elif changeResult == 2:
        bak_result="失败"
    obj="" 
    #obj = Q(title__icontains=keyword)|Q(content__icontains=keyword)|Q(author__icontains=keyword)
    if app_in_host == "" and app_name == "" and type_id == 0 and changeType == 0 and changeResult == 0 and checkTime == "":
        list = APPChange.objects.filter(confirm_status="1",is_get_task_exe_result=1)[startPos:endPos]
        total = APPChange.objects.filter(confirm_status="1",is_get_task_exe_result=1).count()
    else:
        searchCondition = {'confirm_status':"1","is_get_task_exe_result":1}#'md5__icontains' : md5 ,'filename__icontains':filename
        if app_in_host != "" and app_in_host !=None:
            searchCondition['app_in_host__icontains']=app_in_host
        if app_name != "" and app_name !=None:
            searchCondition['app_name__icontains']=app_name
        if bak_result != "" and bak_result !=None:
            searchCondition['bak_result__icontains']=bak_result
        if type_id != 0 and type_id !=None:
            searchCondition['type_id']=type_id
        if changeType != 0 and changeType !=None:
            searchCondition['change_type']=changeType
        if start_time != None and start_time != "" and end_time != None and end_time !="":
            searchCondition['check_time__range']=(datetime.datetime.strptime(start_time,'%Y-%m-%d'),datetime.datetime.strptime(end_time,'%Y-%m-%d'))#####
        #if start_time != 
        kwargs = getKwargs(searchCondition)
        list = APPChange.objects.filter(**kwargs)[startPos:endPos]
        #list = APPChange.objects.filter(confirm_status="1",is_get_task_exe_result=1).\
        #filter(app_in_host__icontains=app_in_host).filter(app_name__icontains=app_name).\
        #filter(type_id=type_id).filter(change_type=change_type).\
        #filter(bak_result__icontains=bak_result).filter(change_time__range=(start_time,end_time))[startPos:endPos]
        
        total = APPChange.objects.filter(**kwargs).count()
    #pageCount = total / page_size
    pageCount = (total  +  page_size  - 1) / page_size
    if pageCount <= 0:
        pageCount = 1
    lastPage = True
    firstPage = True
    if(page_number != 1):
        firstPage = False
    if(lastPage != pageCount):
        lastPage=False
    return render_json({'code':True,'text':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list':  convert_objs_to_dicts(list)
                        ,"firstPage":firstPage,"lastPage":lastPage})
    

# 获取动态过滤条件
def getKwargs(data={}):
   kwargs = {}
   for (k , v)  in data.items() :
       if v is not None and v != u'' :
           kwargs[k] = v          
   return kwargs


#根据id查询变更记录
def getChangeByid(rq):
    id=rq.POST.get("id")
    if id == None or id =="":
        return render_json({'code':False, 'text':"ID不能为空"}) 
    try: 
        dict = APPChange.objects.get(id=id)             
    except:
        return render_json({'code':False, 'text':"查询数据出错"})
    return render_json({'code':False, 'text':ret_text,'list':convert_obj_to_dicts(dict)})


#确认变更，前台修改变更状态
def confirmCahngeStatus(rq):
    id=rq.GET.get("id")
    if id == None or id == "":
        return render_json({'code':False, 'text':"必须传入数据ID信息"})
    try:
        appchg = APPChange.objects.get(id=id)
    except:
        return render_json({'code':False, 'text':"没有查到对应的数据记录"})
    change_type=int(rq.GET.get("changeType"))
    confirm_mark=rq.GET.get("versionMark")
    if change_type == None or change_type =="":
        return render_json({'code':False, 'text':"变更类型不能为空"})
    appchg.change_type = change_type
    if confirm_mark != None:
        appchg.confirm_mark=confirm_mark
    appchg.confirm_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    appchg.confirm_status="1"
    appchg.save()
    return render_json({'code':True, 'text':"状态更新成功"})


#检查发现有变更后（或第一次校验）调用该方法插入变更数据
def addChange(app_in_host,app_name,task_id,change_file,app_id,bak_file_dir):
    change_type=0
    check_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    check_result="检查成功，未返回检查结果"
    is_get_task_exe_result=0
    ret_text = "保存成功"
    ret_code = True
    try:
        APPChange.objects.create(app_id=app_id,app_in_host=app_in_host,app_name=app_name
                             ,task_id=task_id,change_file=change_file
                             ,check_time=check_time,check_result=check_result
                             ,is_get_task_exe_result=is_get_task_exe_result,bak_path=bak_file_dir)
        updAppCheck(app_id,check_time,check_result)
    except:
        logger.error(u"检查后保存数据失败：{}".format(datetime.datetime.now()))

#每次检查如果无变更也去更新时间和task_id
def updAppCheck(id,check_time,check_result):
    try:
        appchg = APPConfig.objects.filter(id=id).update(check_time=check_time,check_result=check_result)
    except:
        return

    

#任务执行过程
"""
任务1：
1、扫描应用配置表，判断周期时间是否到：
        如果 周期时间<当前时间-上次check时间，校验，调用sh，
       无变更 ，更新应用校验时间，校验结果
       有变更，备份失败，加入变更表，还要是否已经备份失败过，根据上次备份时间
       有变更，备份成功，直接加，更新应用表
任务2：
1、
"""
def exec_task_test(rq):
    id=rq.POST.get("id")
    if id == None or id =="":
        return render_json({'code':False, 'text':"ID不能为空"}) 
    try: 
        app = APPConfig.objects.get(id=id)             
    except:
        return render_json({'code':False, 'text':"查询数据出错"})
    user_name = rq.user.username
    curr_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    bak_file_dir = app.app_bak_path+"/"+curr_time
    
    #判断是否达到check时间，如果check时间为空，则表示第一次校验，先执行一次备份
    if app.check_time != None and app.check_time != "":
        curr_time = datetime.datetime.now()
        check_time = app.check_time
        if app.app_check_cycle < (curr_time - check_time).seconds:
            #调用check方法，传入文件路径，MD5值，备份路径目录
            #这里的文件路径主要来源于执行文件路径，和配置文件路径两个字段，每个字段均可能有多个文件，多个文件时用","分隔
            strs_conf = app.app_config_file_path.split(",")
            files = strs_conf
            for file in files:
                biz_ips = {}
                biz_ips["ip"] = app.app_host_ip
                biz_ips["source"] = app.host_source
                ip_list = []
                bak_file_dir = bak_file_dir+"/"+file.split('.')[0]
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
                    "script_param":param,
                    "ip_list":ip_list, "type":1, "account":'root',            
                }
                result = client.job.fast_execute_script(kwargs)
                if result['code'] != 0:
                    logger.error(u"执行脚本失败：{}".format(datetime.datetime.now()))
                task_instance_id = result['data']['taskInstanceId']
                addChange(app.app_host_ip,app.app_name,task_instance_id,file,app.id,bak_file_dir)
                return render_json({'code':True, 'text':"校验成功"})
        else:
            return render_json({'code':True, 'text':"未到校验时间"})
    else :
        #调用check方法，传入文件路径，MD5值，备份路径目录
        #这里的文件路径主要来源于执行文件路径，和配置文件路径两个字段，每个字段均可能有多个文件，多个文件时用","分隔
        strs_conf = app.app_config_file_path.split(",")
        files = strs_conf
        for file in files:
            biz_ips = {}
            biz_ips["ip"] = app.app_host_ip
            biz_ips["source"] = app.host_source
            ip_list = []
            bak_file_dir = bak_file_dir+"/"+file.split('.')[0]
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
        
        return render_json({'code':True, 'text':"校验成功"})

def get_exec_task_test_result(rq):
    client = get_client_by_user(rq.user.username)
    dicts = APPChange.objects.filter(is_get_task_exe_result=0)
    #if dicts == None and len(dicts) <= 0:
        #for obj in dicts:
    task_instance_id = int(rq.POST.get("task_instance_id"))
    #app_id = int(obj.app_id)
    kwargs = {
        "task_instance_id": task_instance_id
    }
    currTime = datetime.datetime.now()
    #checkTime = obj.check_time
    #if (currTime - checkTime).seconds > 1: #校验1秒后去获取结果
    result = client.job.get_task_ip_log(kwargs)
    ipLogContent = result.get('data')[0].get('stepAnalyseResult')[0].get('ipLogContent')[0]
    """
    dict: {u'totalTime': 1.190999984741211, u'isJobIp': 1, u'endTime': u'2018-07-13 17:29:49', 
     u'stepInstanceId': 1, u'ip': u'192.168.1.164', u'displayIp': u'', u'errCode': 0, u'source': 0, u'logContent': 
     u'[2018-07-13 17:29:49][PID:7252] job_start\nfile_md5=76b825a4b0d53119aae5344741e25179\n', 
     u'status': 9, u'startTime': u'2018-07-13 17:29:48', u'retryCount': 0, u'tag': u'', u'exitCode': 0}
     
     dict: {u'totalTime': 0, u'isJobIp': 1, u'endTime': u'', u'stepInstanceId': 201, u'ip': u'192.168.1.164', 
     u'displayIp': u'', u'errCode': 0, u'source': 0, u'logContent': u'', u'status': 7, u'startTime': u'2018-07-17 22:
     09:02', u'retryCount': 0, u'tag': u'', u'exitCode': 0}
     
     dict: {u'totalTime': 0.6259999871253967, u'isJobIp': 1, u'endTime': u'2018-07-17 22:10:01', 
 u'stepInstanceId': 202, u'ip': u'192.168.1.164', u'displayIp': u'', u'errCode': 0, u'source': 0, u'logContent': 
 u'[2018-07-17 22:10:01][PID:10498] job_start\nfile_md5=76b825a4b0d53119aae5344741e25179\n', 
 u'status': 104, u'startTime': u'2018-07-17 22:10:00', u'retryCount': 0, u'tag': u'', u'exitCode': 3}
 
 dict: {u'totalTime': 1.1030000448226929, u'isJobIp': 1, u'endTime': u'2018-07-17 22:11:02', 
 u'stepInstanceId': 203, u'ip': u'192.168.1.164', u'displayIp': u'', u'errCode': 0, u'source': 0, u'logContent': 
 u'[2018-07-17 22:11:02][PID:15573] job_start\nfile_md5=76b825a4b0d53119aae5344741e25179\n', 
 u'status': 104, u'startTime': u'2018-07-17 22:11:01', u'retryCount': 0, u'tag': u'', u'exitCode': 3}
    """
    
    exitCode = ipLogContent.get('exitCode')
    logmsg =  "The length of  is %d" % (exitCode)
    logger.info(logmsg)
    return render_json({'code':True, 'text':"校验成功"})

def redExecFile(file_name):
    staticdir = ','.join(STATICFILES_DIRS);
    script_path = os.path.join(staticdir, str('script'))
    file = os.path.join(script_path, file_name)
    with open(file) as f:
        script_content = f.read()
    f.close()
    return script_content


#功能：比较a，b两个字符串是否相同
def comparison(a,b):
    ib=0
    for ia in range(len(a)):
        if ord(a[ia:ia+1])-ord(b[ib:ib+1])==0:
            ib=ib+1
            if ib==len(b):
               return True
        else:
            return False
            break


def recover_his_version(rq):
    user_name=rq.user.username
    id = rq.GET.get("id")
    if id == None or id == "":
        return render_json({'code':False, 'text':"ID不能为空"})
    try:
        chg = APPChange.objects.get(id=id)
    except:
        return render_json({'code':False, 'text':"变更数据不存在"})  
    try:  
        app = APPConfig.objects.get(id=chg.app_id)
    except:
        return render_json({'code':False, 'text':"变更数据所属应用不存在"})  
    biz_ips = {}
    biz_ips["ip"] = app.app_host_ip
    biz_ips["source"] = app.host_source
    ip_list = []
    bak_file_dir = chg.bak_path
    recover_path="/tmp/recover"+chg.bak_path
    bak_file_dir = bak_file_dir+"/"+chg.change_file.split('/')[-1]
    ip_list.append(biz_ips)
    param = '%s %s' % (bak_file_dir,recover_path)
    client = get_client_by_user(user_name)
    kwargs = {
        "username":user_name, 
        "app_id":app.app_biz_id,
        "content":base64.encodestring(redExecFile("getbakfile.sh")),
        "script_param":param,
        "ip_list":ip_list, "type":1, "account":'root',            
    }
    result = client.job.fast_execute_script(kwargs)
    if result['code'] != 0:
        msg = result['message']
        logger.error(u"执行脚本失败-提取：{}".format(datetime.datetime.now()))
        return render_json({'code':False, 'text':"提取历史版本失败："+msg.encode("utf-8")})
    else:
        #脚本执行成功，
        task_instance_id = result['data']['taskInstanceId']
        time.sleep(5)   #休眠5秒后去获取结果
        client = get_client_by_user(user_name)
        kwargs = {
            "task_instance_id": task_instance_id
        }
        result = client.job.get_task_ip_log(kwargs)
        ipLogContent = result.get('data')[0].get('stepAnalyseResult')[0].get('ipLogContent')[0]
        exitCode = ipLogContent.get('exitCode')
        if exitCode == 1:#参数不全
            return render_json({'code':False, 'text':"提取结果失败，调用脚本参数不全"})
        elif exitCode == 2:#校验配置文件不存在
            return render_json({'code':False, 'text':'提取结果失败，文件'+bak_file_dir.encode("utf-8")+'不存在'})
        elif exitCode == 0:#拷贝成功
            return render_json({'code':True, 'text':'提取结果成功，文件'+bak_file_dir.encode("utf-8")+'已提取','IP':app.app_host_ip,'path':recover_path})
        else:
            return render_json({'code':False, 'text':"提取结果失败，系统异常",'IP':app.app_host_ip,'path':recover_path})


#首页大类统计
def home_type_count(rq):
    dicts = Dicts.objects.filter(dict_type="APP_TYPE")
    list=[]
    obj={}
    if dicts != None and len(dicts) > 0:
        for dict in dicts:
            dict_count = APPConfig.objects.filter(app_type=dict.id).count()
            obj["type_id"]=dict.id
            obj["type_name"]=dict.dict_name
            obj["change_totle"]=dict_count
            list.append(copy.deepcopy(obj))
    return render_json({'code':True, 'text':u"提取结果成功","list":list})


#首页柱状图统计
def home_chart_count(rq):
    dicts = Dicts.objects.filter(dict_type="APP_TYPE")
    list=[]
    obj={}
    if dicts != None and len(dicts) > 0:
        for dict in dicts:
            obj["type_id"]=dict.id
            obj["type_name"]=dict.dict_name
            no_changes=0
            apps = APPConfig.objects.filter(app_type=dict.id)
            if apps != None and len(apps) > 0:
                for app in apps:
                    listAPPS = APPChange.objects.filter(confirm_status="0",is_get_task_exe_result=1,app_id=app.id)
                    no_changes += len(listAPPS)
            obj["no_changes"]=no_changes
            list.append(copy.deepcopy(obj))
    return render_json({'code':True, 'text':u"提取结果成功","list":list}) 


#首页柱状图统计最近一个月
def home_chart_count_time(rq):
    end_date = datetime.datetime.now()
    start_date = _last_month(end_date)
    dicts = Dicts.objects.filter(dict_type="APP_TYPE")
    list=[]
    obj={}
    if dicts != None and len(dicts) > 0:
        for dict in dicts:
            obj["type_id"]=dict.id
            obj["type_name"]=dict.dict_name
            no_changes=0
            already_change=0
            apps = APPConfig.objects.filter(app_type=dict.id)
            if apps != None and len(apps) > 0:
                for app in apps:
                    listAPPS = APPChange.objects.filter(confirm_status="0",is_get_task_exe_result=1,app_id=app.id).\
                    filter(bak_time__range=(start_date, end_date)).count()
                    lists = APPChange.objects.filter(confirm_status="1",is_get_task_exe_result=1,app_id=app.id).\
                    filter(bak_time__range=(start_date, end_date)).count()
                    no_changes += listAPPS
                    already_change += lists
            obj["no_changes"]=no_changes
            obj["already_change"]=already_change
            list.append(copy.deepcopy(obj))
    return render_json({'code':True, 'text':u"提取结果成功","list":list})  

def _last_month(now_time):
    last_month = now_time.month - 1
    last_year = now_time.year
    if last_month == 0:
        last_month = 12
        last_year -= 1
    month_time = datetime.datetime(month=last_month, year=last_year, day=now_time.day)
    return month_time     