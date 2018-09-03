# -*- coding: utf-8 -*-
from common.mymako import render_mako_context, render_json
from django.shortcuts import render
from django.shortcuts import redirect
from doctest import script_from_examples
from conf.default import STATICFILES_DIRS
from common_utils.model_to_dicts import hash_code

# Create your views here.

def user_view(request):
    """
    账号
    """
    return render_mako_context(request, '/login/sysuser.html')

def login(request):
    """
    登陆页
    """
    from captcha.models import CaptchaStore  
    from captcha.helpers import captcha_image_url  
    hashkey = CaptchaStore.generate_key()  
    imgage_url = captcha_image_url(hashkey)
    if not request.session.get('user_is_login'):
        request.session['user_is_login'] = False
        request.session['user_id'] = ""
        request.session['user_name'] = ""
        request.session['login_code'] = ""
    return render(request, 'login/login.html',context={'hashkey':hashkey,'imgage_url':imgage_url})


def do_captcha_refresh(request):
    from captcha.models import CaptchaStore
    from django.http import JsonResponse
    if  request.is_ajax():
        cs = CaptchaStore.objects.filter(response=request.GET['response'],hashkey=request.GET['hashkey'])
        if cs:
            json_data={'status':1}
        else:
            json_data = {'status':0}
        return JsonResponse(json_data)
    else:
        # raise Http404
        json_data = {'status':0}
        return JsonResponse(json_data) #需要导入  


def do_login(request):
    from captcha.models import CaptchaStore
    from captcha.helpers import captcha_image_url  
    hashkey = CaptchaStore.generate_key()  
    imgage_url = captcha_image_url(hashkey)
    if request.session.get('user_is_login',None):
        return redirect("/index/")
    if request.method == "POST":
        user_name = request.POST.get("username")
        pwd = request.POST.get("password")
        captcha_code = request.POST.get("jcaptchaCode")
        captcha_key = request.POST.get("captchaCode_0")
        cs = CaptchaStore.objects.filter(response=captcha_code,hashkey=captcha_key)
        if not cs:
            message = "验证码错误"
            return render(request, 'login/login.html', locals())
        message = "请检查填写的内容！"
        try:
            #user = BkingOperator.objects.filter(login_code=user_name,op_password=hash_code(pwd,user_name))
            #if user[0].status == "1" :
            #    message = "该用户已锁定，请联系管理员解锁！"
            #    return render(request, 'login/login.html', locals())
            #if user[0].status == "2" :
            #    message = "该用户已失效，请联系管理员解决！"
            #    return render(request, 'login/login.html', locals())
            #if user[0].op_password == hash_code(pwd,user_name):
            request.session['user_is_login'] = True
            request.session['user_id'] = '10001'
            request.session['user_name'] = '管理員'
            request.session['login_code'] = 'admin'
            return redirect('/index/')
            #else:
            #    message = "密码不正确！"
        except:
            message = "账号或密码错误！"
            return render(request, 'login/login.html', locals())
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1,username)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往注册邮箱，进行邮件确认！'
                return render(request, 'login/confirm.html', locals())  # 跳转到等待邮件确认页面。
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
    

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.pst.space的注册确认邮件'

    text_content = '''感谢注册www.pst.space，这里是潘仕摊的站点，专注于技术的分享！\
                                                        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.pst.space</a>，\
                                                                这里是潘仕摊的站点，专注于技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def unLock(req):
    login_code = req.POST.get("userName")
    pwd = req.POST.get("password")
    try:
        user = BkingOperator.objects.filter(login_code=login_code,op_password=hash_code(pwd,login_code))
        if user[0].status == "1" :
            message = "该用户已锁定，请联系管理员解锁！"
            return render_json({'code':False, 'msg':message})
        if user[0].status == "2" :
            message = "该用户已失效，请联系管理员解决！"
            return render_json({'code':False, 'msg':message})
        if user[0].op_password == hash_code(pwd,login_code):
            req.session['user_is_login'] = True
            req.session['user_id'] = user[0].op_id
            req.session['user_name'] = user[0].op_name
            req.session['login_code'] = user[0].login_code
            return render_json({'code':True, 'msg':"验证成功"})
        else:
            message = "密码不正确！"
    except Exception,e:
        message = "账号或密码错误！"
        return render_json({'code':False, 'msg':message})
    return render_json({'code':True, 'msg':message})


def login_out(request):
    if not request.session.get('user_is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")

def do_add_user(req):
    user_name = req.user.username
    if user_name == None or user_name == "":
        return render_json({'code':False, 'msg':u"获取用户信息失败"})
    login_code = req.POST.get("login_code")
    op_name = req.POST.get("op_name")
    op_password = req.POST.get("op_password")
    bill_class = req.POST.get("bill_class")
    region_id = req.POST.get("region_id")
    county_id = req.POST.get("county_id")
    org_id = req.POST.get("org_id")
    email = req.POST.get("email")
    phone_id = req.POST.get("phone_id")
    status = req.POST.get("status")
    mark = req.POST.get("mark")
    try:
        users = BkingOperator.objects.filter(login_code=login_code)
        if users.exists():
            return render_json({'code':False, 'msg':u"登录名已存在"})
        BkingOperator.objects.create(login_code=login_code,op_name=op_name,op_password=hash_code(op_password,login_code)
                                    ,bill_class=bill_class,region_id=region_id,county_id=county_id
                                    ,org_id=org_id,email=email,phone_id=phone_id
                                    ,status=status,mark=mark,create_op=user_name)
        logger.error('insert object to BkingOperator is success')
        return render_json({'code':False, 'msg':u"账号数据新增成功"})
    except Exception , e:
        logger.error('insert object to BkingOperator is error:{}'.format(repr(e)))
        return render_json({'code':False, 'msg':u"账号数据新增失败:{}".format(repr(e))})
    
def get_user(req):
    op_id = req.POST.get("id")
    if op_id == None or op_id == "":
        return render_json({'code':False, 'msg':u"必须传递参数id且值不为空"})
    try: 
        user = BkingOperator.objects.get(op_id=op_id)
        return render_json({'code':True, 'msg':u"查询数据成功",'list':convert_obj_to_dicts(user)})
    except Exception, e:
        logger.error('get object for BkingOperator is error:{}'.format(repr(e))) 
        return render_json({'code':False, 'msg':u"数据查询失败:{}".format(repr(e))})

def do_modify_user(req):
    op_id = req.POST.get("op_id")
    if op_id == None or op_id == "":
        return render_json({'code':False, 'msg':u"必须传递参数id且值不为空"})
    op_name = req.POST.get("op_name")
    bill_class = req.POST.get("bill_class")
    region_id = req.POST.get("region_id")
    county_id = req.POST.get("county_id")
    org_id = req.POST.get("org_id")
    email = req.POST.get("email")
    phone_id = req.POST.get("phone_id")
    status = req.POST.get("status")
    mark = req.POST.get("mark")
    try:
        user = BkingOperator.objects.get(op_id=op_id)
    except Exception, e:
        logger.error('modify object for BkingOperator is error:{}'.format(repr(e))) 
        return render_json({'code':False, 'msg':u"账号不存在:{}".format(repr(e))})
    if op_name == None or op_name == "":
        return render_json({'code':False, 'msg':u"业务名称不能为空"})
    user.op_name = op_name
    user.bill_class = bill_class
    user.region_id = region_id
    user.county_id = county_id
    user.org_id = org_id
    user.email = email
    user.phone_id = phone_id
    user.status = status
    user.mark = mark
    
    try:
        user.save()
        logger.info('modify object for BkingOperator is success:{}') 
        return render_json({'code':True, 'msg':u"数据保存成功"})
    except Exception, e:
        logger.error('modify object for BkingOperator is error:{}'.format(repr(e))) 
        return render_json({'code':False, 'msg':u"数据保存失败:{}".format(repr(e))})
    
    
def do_del_user(req):
    op_ids = req.POST.getlist("userIds")
    if op_ids == None or op_ids == "":
        return render_json({'code':False, 'msg':u"必须传递参数op_id且值不为空"})
    try:
        for op_id in op_ids:
            user = BkingOperator.objects.get(op_id=op_id)
            #删除账号
            BkingOperator.objects.filter(op_id=op_id).delete()
            #删除账号关联的角色信息
            BkingOpRoleGrant.objects.filter(login_code=user.login_code).delete()
            return render_json({'code':True, 'msg':u"数据删除成功"})
    except Exception, e:
        logger.error('delete object for BkingOperator is error:{}'.format(repr(e))) 
        return render_json({'code':False, 'msg':u"数据删除失败:{}".format(repr(e))})
    
def do_lock_user(req):
    op_ids = req.POST.getlist("userIds")
    if op_ids == None or op_ids == "":
        return render_json({'code':False, 'msg':u"必须传递参数op_id且值不为空"})
    try:
        for op_id in op_ids:
            user = BkingOperator.objects.get(op_id=op_id)
            user.status = 1
            user.save()
    except Exception,e:
        logger.error('modify object  BkingOperator is error:{}'.format(repr(e))) 
        return render_json({'code':False, 'msg':u"解锁失败".format(repr(e))})
    return render_json({'code':True, 'msg':u"解锁成功"})


def do_unlock_user(req):
    op_ids = req.POST.getlist("userIds")
    if op_ids == None or op_ids == "":
        return render_json({'code':False, 'msg':u"必须传递参数op_id且值不为空"})
    try:
        for op_id in op_ids:
            user = BkingOperator.objects.get(op_id=op_id)
            user.status = 0
            user.save()
    except Exception,e:
        logger.error('modify object  BkingOperator is error:{}'.format(repr(e))) 
        return render_json({'code':False, 'msg':u"解锁失败".format(repr(e))})
    return render_json({'code':True, 'msg':u"解锁成功"})


def updPwd(req):
    op_id = req.POST.get("op_id")
    if op_id == None or op_id == "":
        return render_json({'code':False, 'msg':u"必须传递参数op_id且值不为空"})
    pwd = req.POST.get("op_password")
    newpwd = req.POST.get("newPassword")
    if pwd != newpwd:
        return render_json({'code':False, 'msg':u"两次输入密码不一致"})
    try: 
        user = BkingOperator.objects.get(op_id=op_id)
        pwd = hash_code(pwd,user.login_code)
        user.op_password = pwd
        user.save()
        return render_json({'code':True, 'msg':u"密码修改成功"})
    except Exception, e:
        logger.error('modify object pwd BkingOperator is error:{}'.format(repr(e))) 
        return render_json({'code':False, 'msg':u"密码修改失败".format(repr(e))})
    
def chgPwd(req):
    op_id = req.POST.get("op_id")
    if op_id == None or op_id == "":
        return render_json({'code':False, 'msg':u"必须传递参数op_id且值不为空"})
    pwd = req.POST.get("op_password")
    newpwd = req.POST.get("newPassword")
    if pwd != newpwd:
        return render_json({'code':False, 'msg':u"两次输入密码不一致"})
    try: 
        user = BkingOperator.objects.get(op_id=op_id)
        pwd = hash_code(pwd,user.login_code)
        user.op_password = pwd
        user.save()
        return render_json({'code':True, 'msg':u"密码修改成功"})
    except Exception, e:
        logger.error('modify object pwd BkingOperator is error:{}'.format(repr(e))) 
        return render_json({'code':False, 'msg':u"密码修改失败".format(repr(e))})


def get_user_paging(req):
    try:
        op_name = req.POST.get("op_name")
        login_code = req.POST.get("login_code")
        phone_id = req.POST.get("phone_id")
        page_size = int(req.POST.get("limit"))
        page_number = int(req.POST.get("page"))
        create_time = req.POST.get("create_time")
    except ValueError:
        page_size=10
        page_number=1
    if page_number > 0:
        startPos = (page_number-1) * page_size
        endPos = startPos + page_size
    start_time=""
    end_time=""
    if create_time != None and create_time != "":
        start_time=create_time.split("~")[0]
        end_time=create_time.split("~")[1]
    searchCondition = {}
    if op_name !=None and op_name != "" :
        searchCondition['op_name__icontains']=op_name
    if login_code !=None and login_code != "" :
        searchCondition['login_code__icontains']=login_code
    if phone_id !=None and phone_id !="":
        searchCondition['phone_id__icontains']=phone_id
    if start_time != None and start_time != "" and end_time != None and end_time !="":
        searchCondition['create_date__range']=(datetime.datetime.strptime(start_time,'%Y-%m-%d'),datetime.datetime.strptime(end_time,'%Y-%m-%d'))#####
    
    kwargs = getKwargs(searchCondition)
    dicts = BkingOperator.objects.filter(**kwargs)[startPos:endPos]
    total = BkingOperator.objects.filter(**kwargs).count()
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


    
