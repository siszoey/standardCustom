# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

"""
权限管理models.操作员模型
"""
class BkingOperator(models.Model):
    gender = (
        ('0', "正常"),
        ('1', "锁定"),
        ('2', "无效"),
    )
    op_id=models.AutoField(u"操作员ID",primary_key=True)
    op_name=models.CharField(u"操作员名称",max_length=255)
    login_code=models.CharField(u"登录工号",max_length=255)
    op_password=models.CharField(u"工号密码",max_length=255)
    photo=models.CharField(u"头像",max_length=255,null=True,blank=True)
    email=models.CharField(u"邮箱",max_length=255,null=True,blank=True)
    phone_id=models.CharField(u"手机号",max_length=255,null=True,blank=True)
    status=models.IntegerField(u"账号状态",choices=gender, default=0)
    create_date=models.DateTimeField(u"创建时间",auto_now_add=True)
    create_op=models.CharField(u"创建人",max_length=20)
    upd_date=models.DateTimeField(u"修改时间",auto_now = True)
    mark=models.CharField(u"备注",max_length=1000,null=True,blank=True)
   
    
    def __str__(self):
        return self.login_code+'-'+self.op_name

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "操作员"
        verbose_name_plural = "操作员"
