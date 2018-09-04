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
    (r'^stus_view/$', 'stus_view'),
    (r'^stu_view/$', 'stu_view'),
    (r'^stu_out_view/$', 'stu_out_view'),
    (r'^build_view/$', 'build_view'),
    (r'^dict_view/$', 'dict_view'),
    (r'^home_page/$', 'home_page'),
    (r'^do_add_build/$', 'do_add_build'),
    (r'^get_build/$', 'get_build'),
    (r'^login_koala/$', 'login_koala'),
    (r'^get_koala_user/$', 'get_koala_user'),
    (r'^get_events/$', 'get_events'),
    (r'^web_socket/$', 'web_socket'),
    (r'^do_modify_build/$', 'do_modify_build'),
    (r'^do_del_build/$', 'do_del_build'),
    (r'^get_build_paging/$', 'get_build_paging'),
    (r'^get_stu_in_paging/$', 'get_stu_in_paging'),
    (r'^get_stu_out_paging/$', 'get_stu_out_paging'),
    (r'^get_stu_flow_in_paging/$', 'get_stu_flow_in_paging'),
    (r'^get_stu_flow_out_paging/$', 'get_stu_flow_out_paging'),
    (r'^get_stu_out_in_paging/$', 'get_stu_out_in_paging'),
    (r'^get_stu_out_unin_paging/$', 'get_stu_out_unin_paging'),
    (r'^exp_stu_in/$', 'exp_stu_in'),
    (r'^exp_stu_out/$', 'exp_stu_out'),
    (r'^exp_stu_flow_in/$', 'exp_stu_flow_in'),
    (r'^exp_stu_flow_out/$', 'exp_stu_flow_out'),
    (r'^exp_stu_out_unin/$', 'exp_stu_out_unin'),
    (r'^exp_stu_out_in/$', 'exp_stu_out_in'),
    (r'^get_dict_class/$', 'get_dict_class'),
    (r'^get_dict_type/$', 'get_dict_type'),
    (r'^do_add_application_type/$', 'do_add_application_type'),
    (r'^do_modify_application_type/$', 'do_modify_application_type'),
    (r'^do_del_application_type/$', 'do_del_application_type'),
    (r'^get_paging_application_type/$', 'get_paging_application_type'),
    (r'^get_dict_by_id/$', 'get_dict_by_id'),
    (r'^async_koala_data/$', 'async_koala_data'),
    (r'^do_uninconfrim/$', 'do_uninconfrim'),
    #(r'^test_add_student/$', 'test_add_student'),
    #(r'^test_add_student_in/$', 'test_add_student_in'),
    #(r'^test_add_student_out/$', 'test_add_student_out'),
    #(r'^search_business/$', 'search_business'),
    #(r'^search_app_info/$', 'search_app_info'),
    #(r'^search_host/$', 'search_host'),
    #(r'^get_job_list/$', 'get_job_list'),
    #(r'^get_template_list/$', 'get_template_list'),
    #(r'^get_template_info/$', 'get_template_info'),
)
