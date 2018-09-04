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
import os,base64,copy,datetime,re,json
from django.core import serializers
from home_application.models import Building,Students,StuFlows,StuOut
from common_utils.model_to_dicts import convert_obj_to_dicts,convert_objs_to_dicts,getKwargs
from common_utils.server import runser
from common_utils.excel_utils import export_excel
from common.log import logger
from django.core.cache import cache, caches
import time
from django.apps.registry import apps
from common_utils import bking_ifc_req
import HTMLParser
import requests
from amqp.five import items

def index(request):
    """
             首页
    """
    if not request.session.get('user_is_login'):
        request.session['user_is_login'] = False
        request.session['user_id'] = ""
        request.session['user_name'] = ""
        request.session['login_code'] = ""
    try:
        #runser()
        print "----"
    except Exception,e:
        pass
    return render_mako_context(request, '/home_application/index.html')

def stus_view(request):
    return render_mako_context(request, '/home_application/stumgr.html')

def stu_view(request):
    return render_mako_context(request, '/home_application/stu_flow_mgr.html')

def stu_out_view(request):
    return render_mako_context(request, '/home_application/stu_out_mgr.html')

def build_view(request):
    return render_mako_context(request, '/home_application/build_view.html')

def home_page(request):
    return render_mako_context(request, '/home_application/home_page.html')

def web_socket(request):
    return render_mako_context(request, '/home_application/Websocket.html')

def dict_view(request):
    return render_mako_context(request, '/home_application/dictmgr.html')


def do_add_application_type(request):
    """定义
    dict_class=models.CharField(u"字典类别",max_length=255)
    dict_type=models.CharField(u"字典类型",max_length=255)
    dict_name=models.CharField(u"字典名称",max_length=255)
    dict_value=models.CharField(u"字典值",max_length=255)
    dict_status=models.IntegerField(u"字典状态")
    dict_mark=models.CharField(u"字典备注",max_length=1000,null=True,blank=True)
    """
    dict_class=request.POST.get("dict_class")
    dict_type=request.POST.get("dict_type")
    dict_name=request.POST.get("dict_name")
    dict_value=request.POST.get("dict_value")
    dict_status=0
    dict_mark=request.POST.get("dict_mark")
    try:
        dicts = Dicts.objects.filter(dict_class=dict_class,dict_type=dict_type,dict_value=dict_value,dict_name=dict_name)
        if dicts.exists():
            return render_json({'code':True, 'msg':u"已存在相同记录信息"})
        Dicts.objects.create(dict_class=dict_class,dict_type=dict_type
                             ,dict_value=dict_value,dict_name=dict_name
                             ,dict_status=dict_status,dict_mark=dict_mark)
        logger.info('insert object to Dicts is success')
        return render_json({'code':True, 'msg':u"数据保存成功"})
    except Exception, e:
        logger.error('insert object to Dicts is error:{}'.format(repr(e)))
        return render_json({'code':False, 'msg':u"数据保存失败"})

def get_dict_by_id(rq):
    id=rq.POST.get("id")
    if id == None or id =="":
        return render_json({'code':False, 'msg':"ID不能为空"}) 
    try: 
        dict = Dicts.objects.get(id=id)             
    except:
        return render_json({'code':False, 'msg':"查询数据出错"})
    return render_json({'code': True, 'msg':"查询成功",'list':convert_obj_to_dicts(dict)})

def get_paging_application_type(req):
    try:
        page_size = int(req.POST.get("limit"))
        page_number = int(req.POST.get("page"))
        dict_class=req.POST.get("dict_class")
        dict_type=req.POST.get("dict_type")
        dict_name=req.POST.get("dict_name")
        searchCondition = {}
        if dict_name !=None and dict_name != "" :
            searchCondition['dict_name__icontains']=dict_name
        if dict_class !=None and dict_class !="":
            searchCondition['dict_class']=dict_class
        if dict_type !=None and dict_type !="":
            searchCondition['dict_type']=dict_type
        kwargs = getKwargs(searchCondition)
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    #dicts = Dicts.objects.filter()[startPos:endPos]
    #total = Dicts.objects.filter().count()
    dicts = Dicts.objects.filter(**kwargs)[startPos:endPos]
    total = Dicts.objects.filter(**kwargs).count()
    pageCount = (total  +  page_size  - 1) / page_size
    if pageCount <= 0:
        pageCount = 1
    lastPage = True
    firstPage = True
    if(page_number != 1):
        firstPage = False
    if(lastPage != pageCount):
        lastPage=False
    return render_json({'code':True,'msg':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list':  convert_objs_to_dicts(dicts)
                        ,"firstPage":firstPage,"lastPage":lastPage})

def do_modify_application_type(request):
    id=request.POST.get("id")
    if id == None or id == "":
        return render_json({'code':False, 'msg':"必须传入数据ID信息"})
    try:
        dict = Dicts.objects.get(id=id)
    except:
        return render_json({'code':False, 'msg':"没有查到对应的数据记录"})    
    dict_class=request.POST.get("dict_class")
    dict_type=request.POST.get("dict_type")
    dict_name=request.POST.get("dict_name")
    dict_value=request.POST.get("dict_value")
    dict_status=request.POST.get("dict_status")
    dict_mark=request.POST.get("dict_mark")
    if dict_name == None or dict_name == "":
        return render_json({'code':False, 'msg':"字典编码不能为空"})
    try:
        dicts = Dicts.objects.filter(dict_class=dict_class,dict_type=dict_type,dict_value=dict_value,dict_name=dict_name)
        if dicts.exists():
            for dict in dicts:
                if dict.id != id:
                    return render_json({'code':True, 'msg':u"已存在相同记录信息"})
    except Exception, e:
        logger.error('modify object to Dicts is error:{}'.format(repr(e)))
        return render_json({'code':False, 'msg':u"数据保存失败"})
    if dict_class != None and dict_class != "":
        dict.dict_class=dict_class
    if dict_type != None and dict_type != "":
        dict.dict_type=dict_type
    if dict_mark != None and dict_mark != "":
        dict.dict_mark=dict_mark
    if dict_name != None and dict_name != "":
        dict.dict_name=dict_name
    if dict_value != None and dict_value != "":
        dict.dict_value=dict_value
    if dict_status != None and dict_status != "":
        dict.dict_status=dict_status
    dict.save()
    return render_json({'code':True, 'msg':"数据更新成功"})

def do_del_application_type(request):
    ids=request.POST.getlist("ids")
    if ids == None or ids == "":
        return render_json({'code':False, 'msg':"必须传入数据ID信息"}) 
    ret_text = "删除成功"
    ret_code = True   
    try: 
        for id in ids:
            Dicts.objects.filter(id=id).delete()             
    except:
        ret_code = False
        ret_text = "删除记录异常"
    return render_json({'code':ret_code, 'msg':ret_text})

def get_dict_type(rq):
    dict_type="DICT_TYPE"
    if type == None or type =="":
        return render_json({'code':False, 'msg':"字典类型不能为空"}) 
    try: 
        dicts = Dicts.objects.filter(dict_type=dict_type)             
    except:
        return render_json({'code':False, 'msg':"查询数据出错"})
    return render_json({'code':True, 'msg':"查询数据成功",'list':convert_objs_to_dicts(dicts)})


def async_koala_data(req):
    dict_type="base_conf"
    if type == None or type =="":
        return render_json({'code':False, 'msg':"字典类型不能为空"}) 
    try: 
        dicts = Dicts.objects.filter(dict_type=dict_type)             
    except:
        return render_json({'code':False, 'msg':"查询数据出错"})
    return render_json({'code':True, 'msg':"查询数据成功",'list':convert_objs_to_dicts(dicts)})


def get_dict_class(rq):
    dict_class="DICT_CLASS"
    if type == None or type =="":
        return render_json({'code':False, 'msg':"字典类别不能为空"}) 
    try: 
        dicts = Dicts.objects.filter(dict_type=dict_class)             
    except:
        return render_json({'code':False, 'msg':"查询数据出错"})
    return render_json({'code':True, 'msg':"查询数据成功",'list':convert_objs_to_dicts(dicts)})


def test_add_student(req):
    try:
        stu_code = req.POST.get("stu_code")
        stu_name = req.POST.get("stu_name")
        stu_class = req.POST.get("stu_class")
        stu_build = req.POST.get("stu_build")
        stu_room = req.POST.get("stu_room")
        stu_img = req.POST.get("stu_img")
        #Students.objects.create(stu_code=stu_code,stu_name=stu_name,stu_class=stu_class,stu_build=stu_build,
        #                        stu_room=stu_room,stu_img=stu_img)
        return render_json({'code':True, 'msg':u"操作成功"})
    except Exception,e:
        return render_json({'code':False, 'msg':u"操作失败"})

def test_add_student_out(req):
    try: 
        type = req.POST.get("type")
        stu_out_flow_date = req.POST.get("stu_flow_date")
        stu_out_flow_date=stu_out_flow_date.replace(u'&nbsp;', u' ')
        stu_out_flow_date=datetime.datetime.strptime(stu_out_flow_date,'%Y-%m-%d %H:%S:%M')
        in_or_out = req.POST.get("in_or_out") 
        stu_out_img = req.POST.get("stu_img")
        StuOut.objects.create(type=type,stu_out_flow_date=stu_out_flow_date,
                                in_or_out=in_or_out,stu_out_img=stu_out_img)
        return render_json({'code':True, 'msg':u"操作成功"})
    except Exception,e:
        return render_json({'code':False, 'msg':u"操作失败"})
   
def test_add_student_in(req):
    try: 
        stu_code = req.POST.get("stu_code")
        stu_flow_date = req.POST.get("stu_flow_date")
        stu_flow_date=stu_flow_date.replace(u'&nbsp;', u' ')
        stu_flow_date=datetime.datetime.strptime(stu_flow_date,'%Y-%m-%d %H:%S:%M')
        in_or_out = req.POST.get("in_or_out") 
        stu_img = req.POST.get("stu_img")
        StuFlows.objects.create(stu_code=stu_code,stu_flow_date=stu_flow_date,
                                in_or_out=in_or_out,stu_img=stu_img)
        return render_json({'code':True, 'msg':u"操作成功"})
    except Exception,e:
        return render_json({'code':False, 'msg':u"操作失败"})

def do_add_build(req):
    try:
        build_name = req.POST.get("build_name")
        service_addr = req.POST.get("service_addr")
        Building.objects.create(buid_name=build_name,service_addr=service_addr)
        return render_json({'code':True, 'msg':u"操作成功"})
    except Exception,e:
        return render_json({'code':False, 'msg':u"操作失败"})
    
def get_build(req):
    id = req.POST.get("id")
    try:
        item = Building.objects.get(id=id)
        return render_json({'code':True, 'msg':u"操作成功",'list':convert_obj_to_dicts(item)})
    except Exception,e:
        return render_json({'code':False, 'msg':u"操作失败"})
        pass
    
def do_modify_build(req):
    id = req.POST.get("id")
    build_name = req.POST.get("build_name")
    service_addr = req.POST.get("service_addr")
    try:
        item = Building.objects.get(id=id)
        if build_name != None and build_name !="":
            item.buid_name=build_name
        if service_addr != None and service_addr !="":
            item.service_addr=service_addr
        item.save()  
        return render_json({'code':True, 'msg':u"操作成功"})
    except Exception,e:
        return render_json({'code':False, 'msg':u"操作失败"})
        pass

def do_del_build(req):
    ids = req.POST.getlist("ids")
    if ids == None or len(ids) == 0:
        return render_json({'code':False, 'msg':u"必须传递参数id且值不为空"})
    try:
        for id in ids:
            item = Building.objects.filter(id=id).delete()
        return render_json({'code':True, 'msg':u"操作成功"})
    except Exception,e:
        return render_json({'code':False, 'msg':u"操作失败"})
        pass

    
def get_build_paging(req):
    try:
        build_name = req.POST.get("build_name")
        page_size = int(req.POST.get("limit"))
        page_number = int(req.POST.get("page"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    searchCondition = {}
    if build_name !=None and build_name != "" :
        searchCondition['buid_name__icontains']=build_name
        
    kwargs = getKwargs(searchCondition)
    
    dicts = Building.objects.filter(**kwargs)[startPos:endPos]
    total = Building.objects.filter(**kwargs).count()
    pageCount = (total  +  page_size  - 1) / page_size
    if pageCount <=0:
        pageCount = 1
    lastPage = True
    firstPage = True
    if(page_number != 1):
        firstPage = False
    if(lastPage != pageCount):
        lastPage=False
    return render_json({'code':True,'msg':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list':  convert_objs_to_dicts(dicts)
                        ,"firstPage":firstPage,"lastPage":lastPage})

def get_stu_out_paging(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t1.id,t1.stu_code,t1.stu_name,t1.stu_build,t1.stu_class,t1.stu_room,t2.in_or_out,date_format(t2.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,t2.stu_img\
            FROM home_application_students t1,home_application_stuflows t2\
            WHERE t1.stu_code=t2.stu_code and t2.in_or_out='离寝'"
    sqlcount =u"SELECT  t1.id \
                FROM home_application_students t1,home_application_stuflows t2 \
                WHERE t1.stu_code=t2.stu_code and t2.in_or_out='离寝' "
    try:
        stu_build = req.POST.get("stu_build")
        stu_class = req.POST.get("stu_class")
        q_date_start = req.POST.get("q_date_start")
        if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
        if q_date_start == None or q_date_start == "":
            q_date_start = str(datetime.datetime.now())
        page_size = int(req.POST.get("limit"))
        page_number = int(req.POST.get("page"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    if stu_build !=None and stu_build != "" :
        sql += u" and t1.stu_build like '%%"+stu_build+u"%%'"
        sqlcount += u" and t1.stu_build like '%%"+stu_build+u"%%'"
    if stu_class !=None and stu_class != "" :
        sql += u" and t1.stu_class like '%%"+stu_class+u"%%'"
        sqlcount += u" and t1.stu_class like '%%"+stu_class+u"%%'"
    if q_date_start != None and q_date_start != "":
        sqldate = u"select * from (\
            select * from (\
                select t.id,t.stu_code,t.in_or_out,date_format(t.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,\
                    ABS(str_to_date('"+q_date_start+u"','%Y-%m-%d %H:%i:%s')-t.stu_flow_date)  AS diffTime\
                FROM home_application_stuflows t,home_application_students s\
                WHERE t.stu_code=s.stu_code\
                order by stu_code,in_or_out,diffTime asc) a\
            group by a.stu_code asc,in_or_out asc,diffTime asc\
            ORDER BY a.stu_code asc,diffTime asc\
            )b\
            group by b.stu_code"
            
        sql += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
        sqlcount += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
        sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
        #onestus = Students.objects.raw(sql)
        #objs2 = convert_objs_to_dicts(onestus)
        cursor.execute(sql)
        objs2 =dictfetchall(cursor)
        cursor.execute(sqlcount)
        objs3 =dictfetchall(cursor)
        total = len(list(objs3))
        pageCount = (total  +  page_size  - 1) / page_size
        if pageCount <=0:
            pageCount = 1
        lastPage = True
        firstPage = True
        if(page_number != 1):
            firstPage = False
        if(lastPage != pageCount):
            lastPage=False
        return render_json({'code':True,'msg':"查询列表成功."
                    ,'totalRow':total,'totalPage':pageCount
                    ,'pageSize':page_size,'pageNumber':page_number
                    ,'list':  objs2
                    ,"firstPage":firstPage,"lastPage":lastPage})   
        
    else:
        sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
        #dicts = Students.objects.raw(sql)
        #total = len(list(Students.objects.raw(sqlcount)))
        cursor.execute(sql)
        objs2 =dictfetchall(cursor)
        cursor.execute(sqlcount)
        objs3 =dictfetchall(cursor)
        total = len(list(objs3))
        pageCount = (total  +  page_size  - 1) / page_size
        if pageCount <=0:
            pageCount = 1
        lastPage = True
        firstPage = True
        if(page_number != 1):
            firstPage = False
        if(lastPage != pageCount):
            lastPage=False
        return render_json({'code':True,'msg':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list':  objs2
                        ,"firstPage":firstPage,"lastPage":lastPage})
        
def get_stu_flow_out_paging(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t1.id,t1.stu_code,t1.stu_name,t1.stu_build,t1.stu_class,t1.stu_room,t2.in_or_out,date_format(t2.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,t2.stu_img\
            FROM home_application_students t1,home_application_stuflows t2\
            WHERE t1.stu_code=t2.stu_code and t2.in_or_out='离寝'"
    sqlcount =u"SELECT  t1.id \
                FROM home_application_students t1,home_application_stuflows t2 \
                WHERE t1.stu_code=t2.stu_code and t2.in_or_out='离寝' "
    try:
        stu_code = req.POST.get("stu_code")
        stu_name = req.POST.get("stu_name")
        q_date_start = req.POST.get("q_date_start")
        if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
        #if q_date_start == None or q_date_start == "":
        #    q_date_start = str(datetime.datetime.now())
        page_size = int(req.POST.get("limit"))
        page_number = int(req.POST.get("page"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    if stu_code !=None and stu_code != "" :
        sql += u" and t1.stu_code = '"+stu_code+u"'"
        sqlcount += u" and t1.stu_code = '"+stu_code+u"'"
    if stu_name !=None and stu_name != "" :
        sql += u" and t1.stu_name = '"+stu_name+u"'"
        sqlcount += u" and t1.stu_name = '"+stu_name+u"'"
    if q_date_start != None and q_date_start != "":
        sqldate = u"select * from (\
            select * from (\
                select t.id,t.stu_code,t.in_or_out,date_format(t.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,\
                    ABS(str_to_date('"+q_date_start+u"','%Y-%m-%d %H:%i:%s')-t.stu_flow_date)  AS diffTime\
                FROM home_application_stuflows t,home_application_students s\
                WHERE t.stu_code=s.stu_code\
                order by stu_code,in_or_out,diffTime asc) a\
            group by a.stu_code asc,in_or_out asc,diffTime asc\
            ORDER BY a.stu_code asc,diffTime asc\
            )b\
            group by b.stu_code"
            
        sql += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
        sqlcount += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
        sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
        #onestus = Students.objects.raw(sql)
        #objs2 = convert_objs_to_dicts(onestus)
        cursor.execute(sql)
        objs2 =dictfetchall(cursor)
        cursor.execute(sqlcount)
        objs3 =dictfetchall(cursor)
        total = len(list(objs3))
        pageCount = (total  +  page_size  - 1) / page_size
        if pageCount <=0:
            pageCount = 1
        lastPage = True
        firstPage = True
        if(page_number != 1):
            firstPage = False
        if(lastPage != pageCount):
            lastPage=False
        return render_json({'code':True,'msg':"查询列表成功."
                    ,'totalRow':total,'totalPage':pageCount
                    ,'pageSize':page_size,'pageNumber':page_number
                    ,'list':  objs2
                    ,"firstPage":firstPage,"lastPage":lastPage})   
        
    else:
        sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
        #dicts = Students.objects.raw(sql)
        #total = len(list(Students.objects.raw(sqlcount)))
        cursor.execute(sql)
        objs2 =dictfetchall(cursor)
        cursor.execute(sqlcount)
        objs3 =dictfetchall(cursor)
        total = len(list(objs3))
        pageCount = (total  +  page_size  - 1) / page_size
        if pageCount <=0:
            pageCount = 1
        lastPage = True
        firstPage = True
        if(page_number != 1):
            firstPage = False
        if(lastPage != pageCount):
            lastPage=False
        return render_json({'code':True,'msg':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list':  objs2
                        ,"firstPage":firstPage,"lastPage":lastPage})


def get_stu_in_paging(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t1.id,t1.stu_code,t1.stu_name,t1.stu_build,t1.stu_class,t1.stu_room,t2.in_or_out,date_format(t2.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,t2.stu_img\
            FROM home_application_students t1,home_application_stuflows t2\
            WHERE t1.stu_code=t2.stu_code and t2.in_or_out='归寝'"
    sqlcount =u"SELECT  t1.id \
                FROM home_application_students t1,home_application_stuflows t2 \
                WHERE t1.stu_code=t2.stu_code and t2.in_or_out='归寝' "
    try:
        stu_build = req.POST.get("stu_build")
        stu_class = req.POST.get("stu_class")
        q_date_start = req.POST.get("q_date_start")
        if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
        if q_date_start == None or q_date_start == "":
            q_date_start = str(datetime.datetime.now())
            #q_date_start=datetime.datetime.strptime(q_date_start,'%Y-%m-%d %H:%S:%M')
        page_size = int(req.POST.get("limit"))
        page_number = int(req.POST.get("page"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    if stu_build !=None and stu_build != "" :
        sql += u" and t1.stu_build like '%%"+stu_build+u"%%'"
        sqlcount += u" and t1.stu_build like '%%"+stu_build+u"%%'"
    if stu_class !=None and stu_class != "" :
        sql += u" and t1.stu_class like '%%"+stu_class+u"%%'"
        sqlcount += u" and t1.stu_class like '%%"+stu_class+u"%%'"
    if q_date_start != None and q_date_start != "":
        sqldate = u"select * from (\
            select * from (\
                select t.id,t.stu_code,t.in_or_out,date_format(t.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,\
                    ABS(str_to_date('"+q_date_start+u"','%Y-%m-%d %H:%i:%s')-t.stu_flow_date)  AS diffTime\
                FROM home_application_stuflows t,home_application_students s\
                WHERE t.stu_code=s.stu_code\
                order by stu_code,in_or_out,diffTime asc) a\
            group by a.stu_code asc,in_or_out asc,diffTime asc\
            ORDER BY a.stu_code asc,diffTime asc\
            )b\
            group by b.stu_code"
        sql += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
        sqlcount += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
        sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
        #onestus = Students.objects.raw(sql)
        #objs2 = convert_objs_to_dicts(onestus)
        #total = len(list(Students.objects.raw(sqlcount)))
        cursor.execute(sql)
        objs2 =dictfetchall(cursor)
        cursor.execute(sqlcount)
        objs3 =dictfetchall(cursor)
        total = len(list(objs3))
        pageCount = (total  +  page_size  - 1) / page_size
        if pageCount <=0:
            pageCount = 1
        lastPage = True
        firstPage = True
        if(page_number != 1):
            firstPage = False
        if(lastPage != pageCount):
            lastPage=False
        return render_json({'code':True,'msg':"查询列表成功."
                    ,'totalRow':total,'totalPage':pageCount
                    ,'pageSize':page_size,'pageNumber':page_number
                    ,'list':  objs2
                    ,"firstPage":firstPage,"lastPage":lastPage})   
        
    else:
        sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
        #dicts = Students.objects.raw(sql)
        #total = len(list(Students.objects.raw(sqlcount)))
        cursor.execute(sql)
        objs2 =dictfetchall(cursor)
        cursor.execute(sqlcount)
        objs3 =dictfetchall(cursor)
        total = len(list(objs3))
        pageCount = (total  +  page_size  - 1) / page_size
        if pageCount <=0:
            pageCount = 1
        lastPage = True
        firstPage = True
        if(page_number != 1):
            firstPage = False
        if(lastPage != pageCount):
            lastPage=False
        return render_json({'code':True,'msg':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list': objs2
                        ,"firstPage":firstPage,"lastPage":lastPage})


def get_stu_flow_in_paging(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t1.id,t1.stu_code,t1.stu_name,t1.stu_build,t1.stu_class,t1.stu_room,t2.in_or_out,date_format(t2.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,t2.stu_img\
            FROM home_application_students t1,home_application_stuflows t2\
            WHERE t1.stu_code=t2.stu_code and t2.in_or_out='归寝'"
    sqlcount =u"SELECT  t1.id \
                FROM home_application_students t1,home_application_stuflows t2 \
                WHERE t1.stu_code=t2.stu_code and t2.in_or_out='归寝' "
    try:
        stu_code = req.POST.get("stu_code")
        stu_name = req.POST.get("stu_name")
        q_date_start = req.POST.get("q_date_start")
        if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
        #if q_date_start == None or q_date_start == "":
        #    q_date_start = str(datetime.datetime.now())
            #q_date_start=datetime.datetime.strptime(q_date_start,'%Y-%m-%d %H:%S:%M')
        page_size = int(req.POST.get("limit"))
        page_number = int(req.POST.get("page"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    if stu_code !=None and stu_code != "" :
        sql += u" and t1.stu_code = '"+stu_code+u"'"
        sqlcount += u" and t1.stu_code = '"+stu_code+u"'"
    if stu_name !=None and stu_name != "" :
        sql += u" and t1.stu_name = '"+stu_name+u"'"
        sqlcount += u" and t1.stu_name = '"+stu_name+u"'"
    if q_date_start != None and q_date_start != "":
        sqldate = u"select * from (\
            select * from (\
                select t.id,t.stu_code,t.in_or_out,date_format(t.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,\
                    ABS(str_to_date('"+q_date_start+u"','%Y-%m-%d %H:%i:%s')-t.stu_flow_date)  AS diffTime\
                FROM home_application_stuflows t,home_application_students s\
                WHERE t.stu_code=s.stu_code\
                order by stu_code,in_or_out,diffTime asc) a\
            group by a.stu_code asc,in_or_out asc,diffTime asc\
            ORDER BY a.stu_code asc,diffTime asc\
            )b\
            group by b.stu_code"
        sql += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
        sqlcount += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
        sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
        #onestus = Students.objects.raw(sql)
        #objs2 = convert_objs_to_dicts(onestus)
        #total = len(list(Students.objects.raw(sqlcount)))
        cursor.execute(sql)
        objs2 =dictfetchall(cursor)
        cursor.execute(sqlcount)
        objs3 =dictfetchall(cursor)
        total = len(list(objs3))
        pageCount = (total  +  page_size  - 1) / page_size
        if pageCount <=0:
            pageCount = 1
        lastPage = True
        firstPage = True
        if(page_number != 1):
            firstPage = False
        if(lastPage != pageCount):
            lastPage=False
        return render_json({'code':True,'msg':"查询列表成功."
                    ,'totalRow':total,'totalPage':pageCount
                    ,'pageSize':page_size,'pageNumber':page_number
                    ,'list':  objs2
                    ,"firstPage":firstPage,"lastPage":lastPage})   
        
    else:
        sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
        #dicts = Students.objects.raw(sql)
        #total = len(list(Students.objects.raw(sqlcount)))
        cursor.execute(sql)
        objs2 =dictfetchall(cursor)
        cursor.execute(sqlcount)
        objs3 =dictfetchall(cursor)
        total = len(list(objs3))
        pageCount = (total  +  page_size  - 1) / page_size
        if pageCount <=0:
            pageCount = 1
        lastPage = True
        firstPage = True
        if(page_number != 1):
            firstPage = False
        if(lastPage != pageCount):
            lastPage=False
        return render_json({'code':True,'msg':"查询列表成功."
                        ,'totalRow':total,'totalPage':pageCount
                        ,'pageSize':page_size,'pageNumber':page_number
                        ,'list': objs2
                        ,"firstPage":firstPage,"lastPage":lastPage})


def get_stu_out_unin_paging(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t2.id,t2.type,date_format(t2.stu_out_flow_date, '%Y-%m-%d %H:%m:%s') as stu_out_flow_date,t2.in_or_out,t2.stu_out_img\
        FROM home_application_stuout t2\
        WHERE t2.in_or_out='离开'"
    sqlcount =u"SELECT  t2.id \
                FROM home_application_stuout t2 \
                WHERE t2.in_or_out='离开' "
    try:
        q_date_start = req.POST.get("q_date_start")
        q_date_end = req.POST.get("q_date_end")
        if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
        if q_date_end != None and q_date_end != "":
            q_date_end=q_date_end.replace(u'&nbsp;', u' ')
        page_size = int(req.POST.get("limit"))
        page_number = int(req.POST.get("page"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    if q_date_start != None and q_date_end != None:
        sql += u" and t2.stu_out_flow_date between '"+q_date_start+u"' and '"+q_date_end+u"'"
        sqlcount += u" and t2.stu_out_flow_date between '"+q_date_start+u"' and '"+q_date_end+u"'"
    sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
    cursor.execute(sql)
    dicts =dictfetchall(cursor)
    cursor.execute(sqlcount)
    count =dictfetchall(cursor)
    #dicts = Students.objects.raw(sqldate)
    #onestus = Students.objects.raw(sql)
    #objs2 = convert_objs_to_dicts(onestus)
    total = len(count)
    pageCount = (total  +  page_size  - 1) / page_size
    if pageCount <=0:
        pageCount = 1
    lastPage = True
    firstPage = True
    if(page_number != 1):
        firstPage = False
    if(lastPage != pageCount):
        lastPage=False
    return render_json({'code':True,'msg':"查询列表成功."
                    ,'totalRow':total,'totalPage':pageCount
                    ,'pageSize':page_size,'pageNumber':page_number
                    ,'list':  dicts
                    ,"firstPage":firstPage,"lastPage":lastPage})   

def get_stu_out_in_paging(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t2.id,t2.type,date_format(t2.stu_out_flow_date, '%Y-%m-%d %H:%m:%s') as stu_out_flow_date,t2.in_or_out,t2.stu_out_img\
        FROM home_application_stuout t2\
        WHERE t2.in_or_out='到访'"
    sqlcount =u"SELECT  t2.id \
                FROM home_application_stuout t2 \
                WHERE t2.in_or_out='到访'"
    try:
        q_date_start = req.POST.get("q_date_start")
        q_date_end = req.POST.get("q_date_end")
        if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
        if q_date_end != None and q_date_end != "":
            q_date_end=q_date_end.replace(u'&nbsp;', u' ')
        page_size = int(req.POST.get("limit"))
        page_number = int(req.POST.get("page"))
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    if q_date_start != None and q_date_end != None:
        sql += u" and t2.stu_out_flow_date between '"+q_date_start+u"' and '"+q_date_end+u"'"
        sqlcount += u" and t2.stu_out_flow_date between '"+q_date_start+u"' and '"+q_date_end+u"'"
    sql += u" limit "+str(startPos)+u","+str(endPos)+u" "
    cursor.execute(sql)
    dicts =dictfetchall(cursor)
    cursor.execute(sqlcount)
    count =dictfetchall(cursor)
    #dicts = Students.objects.raw(sqldate)
    #onestus = Students.objects.raw(sql)
    #objs2 = convert_objs_to_dicts(onestus)
    total = len(count)
    pageCount = (total  +  page_size  - 1) / page_size
    if pageCount <=0:
        pageCount = 1
    lastPage = True
    firstPage = True
    if(page_number != 1):
        firstPage = False
    if(lastPage != pageCount):
        lastPage=False
    return render_json({'code':True,'msg':"查询列表成功."
                    ,'totalRow':total,'totalPage':pageCount
                    ,'pageSize':page_size,'pageNumber':page_number
                    ,'list':  dicts
                    ,"firstPage":firstPage,"lastPage":lastPage}) 
   

def search_business(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    bizs = bking_ifc_req.search_business(req)
    if bizs['result']:
        return render_json({'code':True,'count':bizs['data']['count'], 'msg':u"获取业务信息成功"})
    return render_json({'code':True,'count':0, 'msg':u"获取业务信息失败"})


def search_app_info(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    apps = bking_ifc_req.get_app_info(req)
    if apps['result']:
        return render_json({'code':True,'count':len(apps['data']), 'msg':u"获取业务信息成功"})
    return render_json({'code':True,'count':0, 'msg':u"获取业务信息失败"})


def search_host(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    hosts = bking_ifc_req.search_host(req)
    if hosts['result']:
        return render_json({'code':True,'count':hosts['data']['count'], 'msg':u"获取业务信息成功"})
    return render_json({'code':True,'count':0, 'msg':u"获取业务信息失败"})


def get_job_list(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    hosts = bking_ifc_req.get_job_list(req)
    if hosts['result']:
        return render_json({'code':True,'count':hosts['data']['count'], 'msg':u"获取业务信息成功"})
    return render_json({'code':True,'count':0, 'msg':u"获取业务信息失败"})


def get_template_list(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    hosts = bking_ifc_req.get_template_list(req)
    if hosts['result']:
        return render_json({'code':True,'count':hosts['data']['count'], 'msg':u"获取业务信息成功"})
    return render_json({'code':True,'count':0, 'msg':u"获取业务信息失败"})


def get_template_info(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    hosts = bking_ifc_req.get_template_info(req)
    if hosts['result']:
        return render_json({'code':True,'count':hosts['data']['count'], 'msg':u"获取业务信息成功"})
    return render_json({'code':True,'count':0, 'msg':u"获取业务信息失败"})

def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]
    
def login_koala(session):
    #session = requests.session()
    ip = get_dict_base_service()
    if ip != None: 
        url = ip+u'/auth/login'
    else:
        url=u'http://192.168.1.50/auth/login'
    #url = 'http://192.168.1.50/auth/login'
    headers = {'User-Agent': 'Koala Admin'}
    data={"username":"test@megvii.com","password":"123456"}
    ret = session.post(url, json=data, headers=headers).content
    data = json.loads(ret)
    return data['code']


def get_koala_user(req):
    session = requests.session()
    code = login_koala(session)
    if code == 0:
        ip = get_dict_base_service()
        if ip != None: 
            url = ip+u'/mobile-admin/subjects'
        else:
            url=u'http://192.168.1.50/mobile-admin/subjects'
        #url = 'http://192.168.1.50/mobile-admin/subjects'
        data = {}
        ret = None
        try:
            ret = session.get(url).content
            data = json.loads(ret)
            if data['code'] == 0:
                for d in data['data']:
                    stu_code=d['id']
                    stu_name=d['name']
                    stu_class=d['department']
                    stu_build=d['department']
                    stu_room=d['company_id']
                    stu_img=d['photos'][0]['url']
                    stu = Students.objects.get(stu_code=stu_code)
                    if not stu:
                        Students.objects.create(stu_code=stu_code,stu_name=stu_name,stu_class=stu_class,stu_build=stu_build,
                                stu_room=stu_room,stu_img=stu_img)
            else:
                print data['code'], data['desc']
        except:
            print ret
            #print traceback.format_exc()
    return render_json({'code':True,'msg':u"操作成功"})

def get_sync_time(curr_time):
    dict_type="base_conf"
    ret = {}
    try: 
        dicts = Dicts.objects.filter(dict_type=dict_type)
        if dicts :
            for d in dicts :
                if d.dict_name == u'async_events_time_pre':
                    m = int(d.dict_value)
                    curr_time1 = (curr_time+datetime.timedelta(minutes=-m)).strftime("%Y-%m-%d %H:%M:%S")
                    curr_time1 = datetime.datetime.strptime(curr_time1,'%Y-%m-%d %H:%M:%S')
                    ret['pre'] = time.mktime(curr_time1.timetuple())
                if d.dict_name == u'async_events_time_next':
                    m = int(d.dict_value)
                    curr_time2 = (curr_time+datetime.timedelta(minutes=m)).strftime("%Y-%m-%d %H:%M:%S")
                    curr_time2 = datetime.datetime.strptime(curr_time2,'%Y-%m-%d %H:%M:%S')
                    ret['next'] = time.mktime(curr_time2.timetuple())
        return {'code':True, 'msg':"查询数据出错","ret":ret}
    except:
        return {'code':False, 'msg':"查询数据出错"}

def get_events(req):
    try :
        curr_time = req.POST.get("curr_time")
        if curr_time == None or curr_time == "":
            curr_time = datetime.datetime.now()
        else:
            curr_time=curr_time.replace(u'&nbsp;', u' ')
            curr_time = datetime.datetime.strptime(curr_time,'%Y-%m-%d %H:%M:%S')
        result = get_sync_time(curr_time)
        if result["code"] == True:
            times = result["ret"]
            session = requests.session()
            code = login_koala(session)
            if code == 0:
                try:
                    para={"start":times["pre"],"end":times["next"]}
                    ip = get_dict_base_service()
                    if ip != None: 
                        url = ip+u'/event/events'
                    else:
                        url=u'http://192.168.1.50/event/events'
                    ret = session.get(url,json=para)
                    data = json.loads(ret.text)
                    if data['code'] != 0:
                        print data['code'], data['desc']
                    elif data['code'] == 0:
                        for record in data['data']:
                            print data
                            stu_code=record['subject_id']
                            stu_flow_date=record['timestamp']
                            dateArray = datetime.datetime.utcfromtimestamp(stu_flow_date)
                            dateArray = dateArray + datetime.timedelta(hours=8)
                            otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
                            stu_img=record['photo']
                            ips = ip_re_format(record['screen']['camera_address'])
                            if ips :
                                dict = get_dict_data_by_type_and_code("base_conf",ips[0])
                            if stu_code != None and stu_code != "":
                                if dict['code']:
                                    list = dict['list'][0]
                                    if list['dict_value'] == 'IN':
                                        in_or_out='归寝'
                                    if list['dict_value'] == 'OUT':
                                        in_or_out='离寝'
                                stus = StuFlows.objects.filter(stu_img=stu_img)
                                if not stus :
                                    StuFlows.objects.create(stu_code=stu_code,stu_flow_date=otherStyleTime,
                                        in_or_out=in_or_out,stu_img=stu_img)
                                #else :
                            else:
                                items = StuOut.objects.filter(stu_out_img=stu_img)
                                if not items :
                                    if dict['code']:
                                        list = dict['list'][0]
                                        if list['dict_value'] == 'IN':
                                            in_or_out='到访'
                                        if list['dict_value'] == 'OUT':
                                            in_or_out='离开'
                                    StuOut.objects.create(type="非人工操作",stu_out_flow_date=otherStyleTime,
                                            in_or_out=in_or_out,stu_out_img=stu_img)
                except:
                    print ret
                    #print traceback.format_exc()
        return render_json({'code':True,'msg':u"操作成功"})
    except Exception,e:
        return render_json({'code':False,'msg':u"操作失败"})


def exp_stu_in(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t1.id,t1.stu_code,t1.stu_name,t1.stu_build,t1.stu_class,t1.stu_room,t2.in_or_out,date_format(t2.stu_flow_date, '%Y-%m-%d %H:%m:%s') as stu_flow_date,t2.stu_img\
            FROM home_application_students t1,home_application_stuflows t2\
            WHERE t1.stu_code=t2.stu_code and t2.in_or_out='归寝'"
    jgCols = req.GET.get("jgCols");
    showNames = req.GET.get("showNames")
    q_date_start = req.GET.get("q_date_start");
    if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
    stu_build = req.GET.get("stu_build");
    stu_class = req.GET.get("stu_class");
    if stu_build !=None and stu_build != "" :
        sql += u" and t1.stu_build like '%%"+stu_build+u"%%'"
    if stu_class !=None and stu_class != "" :
        sql += u" and t1.stu_class like '%%"+stu_class+u"%%'"
    if q_date_start != None and q_date_start != "":
        sqldate = u"select * from (\
            select * from (\
                select t.id,t.stu_code,t.in_or_out,date_format(t.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,\
                    ABS(TIME_TO_SEC(str_to_date('"+q_date_start+u"','%Y-%m-%d %H:%i:%s'))- TIME_TO_SEC(t.stu_flow_date))  AS diffTime\
                FROM home_application_stuflows t,home_application_students s\
                WHERE t.stu_code=s.stu_code\
                order by stu_code,in_or_out,diffTime asc) a\
            group by a.stu_code asc,in_or_out asc,diffTime asc\
            ORDER BY a.stu_code asc,diffTime asc\
            )b\
            group by b.stu_code"
        sql += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
    titles_name= jgCols.split("|")
    titles_code = showNames.split("|")
    titles = formatTitles(titles_name,titles_code)
    cursor.execute(sql)
    dicts =dictfetchall(cursor)
    return export_excel(req,"在寝人员列表",titles,dicts)

def exp_stu_flow_in(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t1.id,t1.stu_code,t1.stu_name,t1.stu_build,t1.stu_class,t1.stu_room,t2.in_or_out,date_format(t2.stu_flow_date, '%Y-%m-%d %H:%m:%s') as stu_flow_date,t2.stu_img\
            FROM home_application_students t1,home_application_stuflows t2\
            WHERE t1.stu_code=t2.stu_code and t2.in_or_out='归寝'"
    jgCols = req.GET.get("jgCols");
    showNames = req.GET.get("showNames")
    q_date_start = req.GET.get("q_date_start");
    if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
    stu_code = req.GET.get("stu_code");
    stu_name = req.GET.get("stu_name");
    if stu_code !=None and stu_code != "" :
        sql += u" and t1.stu_code = '"+stu_code+u"'"
    if stu_name !=None and stu_name != "" :
        sql += u" and t1.stu_name = '"+stu_name+u"'"
    if q_date_start != None and q_date_start != "":
        sqldate = u"select * from (\
            select * from (\
                select t.id,t.stu_code,t.in_or_out,date_format(t.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,\
                    ABS(TIME_TO_SEC(str_to_date('"+q_date_start+u"','%Y-%m-%d %H:%i:%s'))- TIME_TO_SEC(t.stu_flow_date))  AS diffTime\
                FROM home_application_stuflows t,home_application_students s\
                WHERE t.stu_code=s.stu_code\
                order by stu_code,in_or_out,diffTime asc) a\
            group by a.stu_code asc,in_or_out asc,diffTime asc\
            ORDER BY a.stu_code asc,diffTime asc\
            )b\
            group by b.stu_code"
        sql += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
    titles_name= jgCols.split("|")
    titles_code = showNames.split("|")
    titles = formatTitles(titles_name,titles_code)
    cursor.execute(sql)
    dicts =dictfetchall(cursor)
    return export_excel(req,"在寝人员列表",titles,dicts)

def formatTitles(titles_name,titles_code): 
    titles=[]
    i = 0
    for code in titles_code:
        item={}
        item['code']=code
        item['name']=titles_name[i]
        i = i+1
        titles.append(item)
    return titles


def exp_stu_out(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t1.id,t1.stu_code,t1.stu_name,t1.stu_build,t1.stu_class,t1.stu_room,t2.in_or_out,date_format(t2.stu_flow_date, '%Y-%m-%d %H:%m:%s') as stu_flow_date,t2.stu_img\
            FROM home_application_students t1,home_application_stuflows t2\
            WHERE t1.stu_code=t2.stu_code and t2.in_or_out='离寝'"
    jgCols = req.GET.get("jgCols");
    showNames = req.GET.get("showNames")
    q_date_start = req.GET.get("q_date_start");
    if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
    stu_build = req.GET.get("stu_build");
    stu_class = req.GET.get("stu_class");
    if stu_build !=None and stu_build != "" :
        sql += u" and t1.stu_build like '%%"+stu_build+u"%%'"
    if stu_class !=None and stu_class != "" :
        sql += u" and t1.stu_class like '%%"+stu_class+u"%%'"
    if q_date_start != None and q_date_start != "":
        sqldate = u"select * from (\
            select * from (\
                select t.id,t.stu_code,t.in_or_out,date_format(t.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,\
                    ABS(TIME_TO_SEC(str_to_date('"+q_date_start+u"','%Y-%m-%d %H:%i:%s'))- TIME_TO_SEC(t.stu_flow_date))  AS diffTime\
                FROM home_application_stuflows t,home_application_students s\
                WHERE t.stu_code=s.stu_code\
                order by stu_code,in_or_out,diffTime asc) a\
            group by a.stu_code asc,in_or_out asc,diffTime asc\
            ORDER BY a.stu_code asc,diffTime asc\
            )b\
            group by b.stu_code"
        sql += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
    titles_name= jgCols.split("|")
    titles_code = showNames.split("|")
    titles = formatTitles(titles_name,titles_code)
    cursor.execute(sql)
    dicts =dictfetchall(cursor)
    return export_excel(req,"离寝人员列表",titles,dicts)


def exp_stu_flow_out(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t1.id,t1.stu_code,t1.stu_name,t1.stu_build,t1.stu_class,t1.stu_room,t2.in_or_out,date_format(t2.stu_flow_date, '%Y-%m-%d %H:%m:%s') as stu_flow_date,t2.stu_img\
            FROM home_application_students t1,home_application_stuflows t2\
            WHERE t1.stu_code=t2.stu_code and t2.in_or_out='离寝'"
    jgCols = req.GET.get("jgCols");
    showNames = req.GET.get("showNames")
    q_date_start = req.GET.get("q_date_start");
    if q_date_start != None and q_date_start != "":
            q_date_start=q_date_start.replace(u'&nbsp;', u' ')
    stu_code = req.GET.get("stu_code");
    stu_name = req.GET.get("stu_name");
    if stu_code !=None and stu_code != "" :
        sql += u" and t1.stu_code ='"+stu_code+u"'"
    if stu_name !=None and stu_name != "" :
        sql += u" and t1.stu_name = '"+stu_name+u"'"
    if q_date_start != None and q_date_start != "":
        sqldate = u"select * from (\
            select * from (\
                select t.id,t.stu_code,t.in_or_out,date_format(t.stu_flow_date, '%Y-%m-%d %H:%i:%s') as stu_flow_date,\
                    ABS(TIME_TO_SEC(str_to_date('"+q_date_start+u"','%Y-%m-%d %H:%i:%s'))- TIME_TO_SEC(t.stu_flow_date))  AS diffTime\
                FROM home_application_stuflows t,home_application_students s\
                WHERE t.stu_code=s.stu_code\
                order by stu_code,in_or_out,diffTime asc) a\
            group by a.stu_code asc,in_or_out asc,diffTime asc\
            ORDER BY a.stu_code asc,diffTime asc\
            )b\
            group by b.stu_code"
        sql += u" and t2.id in (SELECT tt.id from ("+sqldate+u") tt)"
    titles_name= jgCols.split("|")
    titles_code = showNames.split("|")
    titles = formatTitles(titles_name,titles_code)
    cursor.execute(sql)
    dicts =dictfetchall(cursor)
    return export_excel(req,"离寝人员列表",titles,dicts)
 
 
def exp_stu_out_in(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t2.id,t2.type,date_format(t2.stu_out_flow_date, '%Y-%m-%d %H:%m:%s') as stu_out_flow_date,t2.in_or_out,t2.stu_out_img\
        FROM home_application_stuout t2\
        WHERE t2.in_or_out='到访'"
    jgCols = req.GET.get("jgCols");
    showNames = req.GET.get("showNames")
    q_date_start = req.GET.get("q_date_start")
    q_date_end = req.GET.get("q_date_end")
    if q_date_start != None and q_date_start != "":
        q_date_start=q_date_start.replace(u'&nbsp;', u' ')
    if q_date_end != None and q_date_end != "":
        q_date_end=q_date_end.replace(u'&nbsp;', u' ')
    if q_date_start != None and q_date_end != None:
        sql += u" and t2.stu_out_flow_date between '"+q_date_start+u"' and '"+q_date_end+u"'"
    titles_name= jgCols.split("|")
    titles_code = showNames.split("|")
    titles = formatTitles(titles_name,titles_code)
    cursor.execute(sql)
    dicts =dictfetchall(cursor)
    return export_excel(req,"到访未离开人员列表",titles,dicts) 

def exp_stu_out_unin(req):
    from django.db import connection
    cursor=connection.cursor()
    sql = u"SELECT DISTINCT t2.id,t2.type,date_format(t2.stu_out_flow_date, '%Y-%m-%d %H:%m:%s') as stu_out_flow_date,t2.in_or_out,t2.stu_out_img\
        FROM home_application_stuout t2\
        WHERE t2.in_or_out='离开'"
    jgCols = req.GET.get("jgCols");
    showNames = req.GET.get("showNames")
    q_date_start = req.GET.get("q_date_start")
    q_date_end = req.GET.get("q_date_end")
    if q_date_start != None and q_date_start != "":
        q_date_start=q_date_start.replace(u'&nbsp;', u' ')
    if q_date_end != None and q_date_end != "":
        q_date_end=q_date_end.replace(u'&nbsp;', u' ')
    if q_date_start != None and q_date_end != None:
        sql += u" and t2.stu_out_flow_date between '"+q_date_start+u"' and '"+q_date_end+u"'"
    titles_name= jgCols.split("|")
    titles_code = showNames.split("|")
    titles = formatTitles(titles_name,titles_code)
    cursor.execute(sql)
    dicts =dictfetchall(cursor)
    return export_excel(req,"到访已离开人员列表",titles,dicts)   


def do_uninconfrim(req):
    id = req.POST.get("id")
    if id == None or id == "":
        return render_json({'code':False,'msg':u"操作失败"})
    try:
        stu = StuOut.objects.get(id=id)
        if stu :
            stu.in_or_out = u"离开"
            stu.type = u"人工确认"
        stu.save()
        return render_json({'code':True,'msg':u"操作成功"})
    except Exception,e:
        return render_json({'code':False,'msg':u"操作失败"})


def get_dict_data_by_type_and_code(type,code):
    dict_type=type
    if type == None or type =="":
        return render_json({'code':False, 'msg':"字典类型不能为空"})
    if code == None or code =="":
        return {'code':False, 'msg':"字典编码不能为空"}
    try: 
        dicts = Dicts.objects.filter(dict_type=dict_type,dict_name=code)             
    except:
        return {'code':False, 'msg':"查询数据出错"}
    return {'code':True, 'msg':"查询数据成功",'list':convert_objs_to_dicts(dicts)}

def get_dict_base_service():
    dict_type="base_conf"
    code = "base_service_conf"
    if type == None or type =="":
        return render_json({'code':False, 'msg':"字典类型不能为空"})
    if code == None or code =="":
        return {'code':False, 'msg':"字典编码不能为空"}
    try: 
        dicts = Dicts.objects.filter(dict_type=dict_type,dict_name=code)
        if dicts :
            item = dicts[0]             
            if item :
                return item.dict_value
    except:
        return None


def ip_re_format(url):  
    import re
    compile_rule = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')  
    match_list = re.findall(compile_rule, url)  
    if match_list:  
        return match_list 
    else:  
        return None  