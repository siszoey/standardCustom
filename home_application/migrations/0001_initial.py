# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buid_name', models.CharField(max_length=255, null=True, verbose_name='\u697c\u5b87', blank=True)),
                ('service_addr', models.CharField(max_length=255, null=True, verbose_name='\u63a5\u53e3\u5730\u5740', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dicts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dict_class', models.CharField(max_length=255, verbose_name='\u5b57\u5178\u7c7b\u522b')),
                ('dict_type', models.CharField(max_length=255, verbose_name='\u5b57\u5178\u7c7b\u578b')),
                ('dict_name', models.CharField(max_length=255, verbose_name='\u5b57\u5178\u540d\u79f0')),
                ('dict_value', models.CharField(max_length=255, verbose_name='\u5b57\u5178\u503c')),
                ('dict_status', models.IntegerField(verbose_name='\u5b57\u5178\u72b6\u6001')),
                ('dict_mark', models.CharField(max_length=1000, null=True, verbose_name='\u5b57\u5178\u5907\u6ce8', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stu_code', models.CharField(unique=True, max_length=255, verbose_name='\u5b66\u53f7')),
                ('stu_name', models.CharField(max_length=255, verbose_name='\u59d3\u540d')),
                ('stu_class', models.CharField(max_length=255, verbose_name='\u73ed\u7ea7')),
                ('stu_build', models.CharField(max_length=255, verbose_name='\u697c\u5b87')),
                ('stu_room', models.CharField(max_length=255, verbose_name='\u5bdd\u5ba4')),
                ('stu_img', models.CharField(max_length=255, verbose_name='\u7167\u7247')),
                ('stu_status_date', models.DateTimeField(auto_now=True, verbose_name='\u72b6\u6001\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='StuFlows',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stu_code', models.CharField(max_length=255, verbose_name='\u5b66\u53f7')),
                ('stu_flow_date', models.DateTimeField(verbose_name='\u6293\u62cd\u65f6\u95f4')),
                ('stu_img', models.CharField(max_length=255, verbose_name='\u7167\u7247')),
                ('in_or_out', models.CharField(max_length=255, verbose_name='\u8fdb\u51fa\u7c7b\u578b')),
            ],
        ),
        migrations.CreateModel(
            name='StuOut',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stu_out_flow_date', models.DateTimeField(verbose_name='\u6293\u62cd\u65f6\u95f4')),
                ('stu_out_img', models.CharField(max_length=255, verbose_name='\u7167\u7247')),
                ('in_or_out', models.CharField(max_length=255, verbose_name='\u8fdb\u51fa\u7c7b\u578b')),
                ('type', models.CharField(max_length=255, verbose_name='\u662f\u5426\u4eba\u5de5\u5904\u7406')),
            ],
        ),
    ]
