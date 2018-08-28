# -*- coding: utf-8 -*-
from common.mymako import render_mako_context, render_json
from home_application.models import BkingBusiness,BkingBisApplicationRel,BkingApplication,Dicts,BkingBisApplicationRel,BkingApplicationHostRel
from system_permission.models import BkingOperator,BkingRole,BkingPriv,BkingRolePrivGrant,BkingOpRoleGrant
from doctest import script_from_examples
from conf.default import STATICFILES_DIRS


def is_has_menu_priv(priv_code,login_code):
    return False


def is_has_menu_btn_priv(priv_code,login_code):
    return False


def is_has_data_priv(data_code,login_code):
    return False
