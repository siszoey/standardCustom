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

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'index'),
    (r'^home/$', 'home'),
    (r'^apply_manage/$', 'apply_manage'),
    (r'^edit_apply_info/$', 'edit_apply_info'),
    (r'^add_apply_info/$', 'add_apply_info'),
    (r'^apply_type/$', 'apply_type'),
    (r'^apply_version_manage/$', 'apply_version_manage'),
    (r'^apply_version_query/$', 'apply_version_query'),
    (r'^apply_vm_box/$', 'apply_vm_box'),
    (r'^doAddAPPTypeDict/$', 'doAddAPPTypeDict'),
    (r'^doModifyAppTypeict/$', 'doModifyAppTypeict'),
    (r'^doDelAppTypeDict/$', 'doDelAppTypeDict'),
    (r'^getPagingAPPTypeDictList/$', 'getPagingAPPTypeDictList'),
    (r'^getDictByType/$', 'getDictByType'),
    (r'^getDictById/$', 'getDictById'),
    (r'^doAddAPPConfig/$', 'doAddAPPConfig'),
    (r'^doModifyAPPConfig/$', 'doModifyAPPConfig'),
    (r'^doDelAPPConfig/$', 'doDelAPPConfig'),
    (r'^getPagingAPPConfigList/$', 'getPagingAPPConfigList'),
    (r'^getAPPConfigById/$', 'getAPPConfigById'),
    (r'^getPagingAPPChangeByUnConfirm/$', 'getPagingAPPChangeByUnConfirm'),
    (r'^getPagingAPPChangeByConfirmed/$', 'getPagingAPPChangeByConfirmed'),
    (r'^exec_task_test/$', 'exec_task_test'),
    (r'^get_exec_task_test_result/$', 'get_exec_task_test_result'),
    (r'^getUserIps/$', 'getUserIps'),
    (r'^get_user_biz/$', 'get_user_biz'),
    (r'^confirmCahngeStatus/$', 'confirmCahngeStatus'),
    (r'^recover_his_version/$', 'recover_his_version'),
    (r'^home_type_count/$', 'home_type_count'),
    (r'^home_chart_count/$', 'home_chart_count'),
    (r'^home_chart_count_time/$', 'home_chart_count_time'),
)
