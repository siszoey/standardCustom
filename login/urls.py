# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'login.views',
    (r'^login/$', 'login'),
    (r'^login/$', 'login'),
    (r'^user_view/$', 'user_view'),
    (r'^login_out/$', 'login_out'),
    (r'^unLock/$', 'unLock'),
    (r'^do_captcha_refresh/$', 'do_captcha_refresh'),
    (r'^do_login/$', 'do_login'),  
    (r'^do_add_user/$', 'do_add_user'),
    (r'^get_user/$', 'get_user'),
    (r'^do_modify_user/$', 'do_modify_user'),
    (r'^do_del_user/$', 'do_del_user'),
    (r'^do_lock_user/$', 'do_lock_user'),
    (r'^do_unlock_user/$', 'do_unlock_user'),
    (r'^updPwd/$', 'updPwd'),
    (r'^chgPwd/$', 'chgPwd'),  
    
)