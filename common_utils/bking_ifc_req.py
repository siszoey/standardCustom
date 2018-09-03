# -*- coding: utf-8 -*-
from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request,get_client_by_user
from doctest import script_from_examples
from conf.default import STATICFILES_DIRS
import os,base64,copy,datetime,re,json
from django.core import serializers
from common.log import logger

def get_task_status(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    param = {
        "bk_app_code": "customatoms",
        "bk_app_secret": "386892eb-954f-4838-83ef-b9fbcd0672ce",
        "bk_username":"customatoms",
        "bk_biz_id": 2,
    }
    client = get_client_by_user(req)
    hosts = client.job.get_job_list(param)
    return hosts


def get_template_list(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    param = {
        "bk_app_code": "bk_sops",
        "bk_app_secret": "0b5818c8-720f-4440-ad80-c39c194672c4",
        "bk_username":"admin",
        "bk_biz_id": 2,
    }
    client = get_client_by_user(req)
    hosts = client.sops.get_template_list(param)
    return hosts

def get_template_info(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    param = {
        "bk_app_code": "bk_sops",
        "bk_app_secret": "0b5818c8-720f-4440-ad80-c39c194672c4",
        "bk_username":"admin",
        "bk_biz_id": 2,
        "template_id": 5
    }
    client = get_client_by_user(req)
    hosts = client.sops.get_template_info(param)
    return hosts


def search_business(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    param = {
        "bk_app_code": "customatoms",
        "bk_app_secret": "386892eb-954f-4838-83ef-b9fbcd0672ce",
        "bk_username":"customatoms"
    }
    client = get_client_by_user(req)
    bizs = client.cc.search_business(param)
    return bizs


def get_app_info(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    param = {
        "bk_app_code": "customatoms",
        "bk_app_secret": "386892eb-954f-4838-83ef-b9fbcd0672ce",
        "bk_username":"customatoms"
    }
    client = get_client_by_user(req)
    apps = client.bk_paas.get_app_info(param)
    return apps


def search_host(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    param = {
        "bk_app_code": "customatoms",
        "bk_app_secret": "386892eb-954f-4838-83ef-b9fbcd0672ce",
        "bk_username":"customatoms"
    }
    client = get_client_by_user(req)
    hosts = client.cc.search_host(param)
    return hosts


def get_job_list(req):
    user_name = req.session.get('login_code')
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    param = {
        "bk_app_code": "customatoms",
        "bk_app_secret": "386892eb-954f-4838-83ef-b9fbcd0672ce",
        "bk_username":"customatoms",
        "bk_biz_id": 2,
    }
    client = get_client_by_user(req)
    hosts = client.job.get_job_list(param)
    return hosts




