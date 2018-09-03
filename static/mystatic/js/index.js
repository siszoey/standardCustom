/** index.js By Beginner Emain:zheng_jinfan@126.com HomePage:http://www.zhengjinfan.cn */
//加载菜单
var menu_data={};
$(function(){
	//getNavBarData();
});
function getNavBarData() {
	//debugger
	$.ajax({
		type : 'POST',
		async : false,
		url : site_url + 'get_curr_user_priv/',
		processData : true,
		dataType : 'json',
		success : function(data) {
			if (data.code) {
				data = format_json_to_menu(data.list)
				menu_data = JSON.parse(JSON.stringify(data));
				return JSON.stringify(data);
				//mMenu._init(result,"nav-bracket");
			} else {
				///alert('菜单加载失败:'+data.msg);
			}
		},
		error : function() {
			alert('菜单加载失败，已恢复默认菜单');
		},
		beforeSend : function(xhr, settings) {
			function getCookie(name) {
				var cookieValue = null;
				if (document.cookie && document.cookie != '') {
					var cookies = document.cookie.split(';');
					for (var i = 0; i < cookies.length; i++) {
						var cookie = jQuery.trim(cookies[i]);
						// Does this cookie string begin with the name
						// we want?
						if (cookie.substring(0, name.length + 1) == (name + '=')) {
							cookieValue = decodeURIComponent(cookie
									.substring(name.length + 1));
							break;
						}
					}
				}
				return cookieValue;
			}
			function csrfSafeMethod(method) {
				// these HTTP methods do not require CSRF protection
				return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
			}
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				var csrftoken = getCookie('csrftoken');
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
}

/**
 * 格式化后台数据使之符合menu控件的数据格式
 */

function format_json_to_menu(data){
	// debugger
	var menus = [];
	nav1 = {};
	for (var i = 0 ; i < data.length; i++){
		menu = {};
		if (data[i].parent_priv_code == "0" && data[i].type == 1){
			nav1.title=data[i].name;
			nav1.icon=data[i].icon == undefined ? "fa-th-large":data[i].icon;
			nav1.spread=false;
			nav1.href="";
			nav1.children=getMenuChildrens(data,data[i].priv_code);
			//data[i].Childrens = JSON.stringify(getMenuChildrens(data,data[i].priv_code));
			menu = deepClone(nav1);
			//menu[0].Childrens = JSON.stringify(getMenuChildrens(data,data[i].priv_code));
			menus.push(menu);
		}
	}
	return menus;
}
function deepClone(obj){
    let _obj = JSON.stringify(obj),
        objClone = JSON.parse(_obj);
    return objClone
}
/**获得下一及菜单列表*/
nav = {};
function getMenuChildrens(data,priv_code){
	//debugger
	var menus = [];
	for (var i = 0 ; i < data.length; i++){
		menu = {};
		if(data[i].parent_priv_code == priv_code && data[i].type == 1){
			nav.title=data[i].name;
			nav.icon=data[i].icon == undefined ? "fa-th-large":data[i].icon;
			nav.href=data[i].uri == undefined ? "":data[i].uri;
			nav.children=getMenuChildrens(data,data[i].priv_code);
			//data[i].Childrens = JSON.stringify(getMenuChildrens(data,data[i].priv_code));
			menu = deepClone(nav);
			//menu.Childrens = "ssssss";
			menus.push(menu);
		}
	}
	return menus;
}


var tab;

layui.config({
    base: '/static/mystatic/js/',
    version: new Date().getTime()
}).use(['form','element', 'layer', 'navbar', 'tab'], function () {
    var element = layui.element,
    	form=layui.form,
        $ = layui.jquery,
        layer = layui.layer,
        navbar = layui.navbar();
    tab = layui.tab({
        elem: '.admin-nav-card' //设置选项卡容器
        ,
        //maxSetting: {
        //	max: 5,
        //	tipMsg: '只能开5个哇，不能再开了。真的。'
        //},
        contextMenu: true,
        onSwitch: function (data) {
            console.log(data.id); //当前Tab的Id
            console.log(data.index); //得到当前Tab的所在下标
            console.log(data.elem); //得到当前的Tab大容器

            console.log(tab.getCurrentTabId())
        },
        closeBefore: function (obj) { //tab 关闭之前触发的事件
            console.log(obj);
            //obj.title  -- 标题
            //obj.url    -- 链接地址
            //obj.id     -- id
            //obj.tabId  -- lay-id
            if (obj.title === 'BTable') {
                layer.confirm('确定要关闭' + obj.title + '吗?', { icon: 3, title: '系统提示' }, function (index) {
                    //因为confirm是非阻塞的，所以这里关闭当前tab需要调用一下deleteTab方法
                    tab.deleteTab(obj.tabId);
                    layer.close(index);
                });
                //返回true会直接关闭当前tab
                return false;
            }else if(obj.title==='表单'){
                layer.confirm('未保存的数据可能会丢失哦，确定要关闭吗?', { icon: 3, title: '系统提示' }, function (index) {
                    tab.deleteTab(obj.tabId);
                    layer.close(index);
                });
                return false;
            }
            return true;
        }
    });
    //更换皮肤
	function skins(){
		var skin = window.sessionStorage.getItem("skin");
		if(skin){  //如果更换过皮肤
			if(window.sessionStorage.getItem("skinValue") != "自定义"){
				$("body").addClass(window.sessionStorage.getItem("skin"));
			}else{
				$(".layui-layout-admin .layui-header").css("background-color",skin.split(',')[0]);
				$(".layui-bg-black").css("background-color",skin.split(',')[1]);
				$(".hideMenu").css("background-color",skin.split(',')[2]);
			}
		}
	}
	skins();
	$(".changeSkin").click(function(){
		layer.open({
			title : "更换皮肤",
			area : ["350px","300px"],
			shadeClose: true, //点击遮罩关闭
			type : "1",
			content : '<div class="skins_box">'+
						'<form class="layui-form">'+
							'<div class="layui-form-item">'+
								'<input type="radio" name="skin" value="默认" title="默认" lay-filter="default" checked="">'+
								'<input type="radio" name="skin" value="橙色" title="橙色" lay-filter="orange">'+
								'<input type="radio" name="skin" value="蓝色" title="蓝色" lay-filter="blue">'+
								'<input type="radio" name="skin" value="自定义" title="自定义" lay-filter="custom">'+
								'<div class="skinCustom">'+
									'<input type="text" class="layui-input topColor" name="topSkin" placeholder="顶部颜色" />'+
									'<input type="text" class="layui-input leftColor" name="leftSkin" placeholder="左侧颜色" />'+
									'<input type="text" class="layui-input menuColor" name="btnSkin" placeholder="顶部菜单按钮" />'+
								'</div>'+
							'</div>'+
							'<div class="layui-form-item skinBtn">'+
								'<a href="javascript:;" class="layui-btn layui-btn-small layui-btn-normal" lay-submit="" lay-filter="changeSkin">确定更换</a>'+
								'<a href="javascript:;" class="layui-btn layui-btn-small layui-btn-primary" lay-submit="" lay-filter="noChangeSkin">我再想想</a>'+
							'</div>'+
						'</form>'+
					'</div>',
			success : function(index, layero){
				var skin = window.sessionStorage.getItem("skin");
				if(window.sessionStorage.getItem("skinValue")){
					$(".skins_box input[value="+window.sessionStorage.getItem("skinValue")+"]").attr("checked","checked");
				};
				if($(".skins_box input[value=自定义]").attr("checked")){
					$(".skinCustom").css("visibility","inherit");
					$(".topColor").val(skin.split(',')[0]);
					$(".leftColor").val(skin.split(',')[1]);
					$(".menuColor").val(skin.split(',')[2]);
				};
				form.render();
				$(".skins_box").removeClass("layui-hide");
				$(".skins_box .layui-form-radio").on("click",function(){
					
					var skinColor;
					if($(this).find("span").text() == "橙色"){
						
						skinColor = "orange";
						
					}else if($(this).find("span").text() == "蓝色"){
						skinColor = "blue";
					}else if($(this).find("span").text() == "默认"){
						skinColor = "";
					}
					if($(this).find("span").text() != "自定义"){
						$(".topColor,.leftColor,.menuColor").val('');
						$("body").removeAttr("class").addClass("main_body "+skinColor+"");
						$(".skinCustom").removeAttr("style");
						$(".layui-bg-black,.hideMenu,.layui-layout-admin .layui-header").removeAttr("style");
					}else{
						$(".skinCustom").css("visibility","inherit");
					}
				})
				var skinStr,skinColor;
				$(".topColor").blur(function(){
					
					$(".layui-layout-admin .layui-header").css("background-color",$(this).val());
				})
				$(".leftColor").blur(function(){
					
					$(".layui-bg-black").css("background-color",$(this).val());
				})
				$(".menuColor").blur(function(){
					$(".hideMenu").css("background-color",$(this).val());
				})

				form.on("submit(changeSkin)",function(data){
					if(data.field.skin != "自定义"){
						if(data.field.skin == "橙色"){
							skinColor = "orange";
						}else if(data.field.skin == "蓝色"){
							skinColor = "blue";
						}else if(data.field.skin == "默认"){
							skinColor = "";
						}
						window.sessionStorage.setItem("skin",skinColor);
					}else{
						skinStr = $(".topColor").val()+','+$(".leftColor").val()+','+$(".menuColor").val();
						window.sessionStorage.setItem("skin",skinStr);
						$("body").removeAttr("class").addClass("main_body");
						
					}
					window.sessionStorage.setItem("skinValue",data.field.skin);
					
					layer.closeAll("page");
				});
				form.on("submit(noChangeSkin)",function(){
					$("body").removeAttr("class").addClass("main_body "+window.sessionStorage.getItem("skin")+"");
					$(".layui-bg-black,.hideMenu,.layui-layout-admin .layui-header .logo .layui-this .layui-side-scroll").removeAttr("style");
					skins();
					
					layer.closeAll("page");
				});
			},
			cancel : function(){
				$("body").removeAttr("class").addClass("main_body "+window.sessionStorage.getItem("skin")+"");
				
				$(".layui-bg-black,.hideMenu,.layui-layout-admin .layui-header").removeAttr("style");
				skins();
			}
		})
	})

    //iframe自适应
    $(window).on('resize', function () {
        var $content = $('.admin-nav-card .layui-tab-content');
        $content.height($(this).height() - 147);
        $content.find('iframe').each(function () {
            $(this).height($content.height());
        });
    }).resize();

    //设置navbar
    navbar.set({
        spreadOne: true,
        elem: '#admin-navbar-side',
        /*cached: true,*/
        data: navs
		/*url: "{:url('getNavBarData()')}"*/
    });
    
    //debugger	
    //渲染navbar
    navbar.render();
    
    //监听点击事件
    navbar.on('click(side)', function (data) {
        tab.tabAdd(data.field);
    });
    //清除缓存
    $('#clearCached').on('click', function () {
        navbar.cleanCached();
        layer.alert('清除完成!', { icon: 1, title: '系统提示' }, function () {
            location.reload();//刷新
        });
    });

    $('.admin-side-toggle').on('click', function () {
        var sideWidth = $('#admin-side').width();
        if (sideWidth === 200) {
            $('#admin-body').animate({
                left: '0'
            }); //admin-footer
            $('#admin-footer').animate({
                left: '0'
            });
            $('#admin-side').animate({
                width: '0'
            });
        } else {
            $('#admin-body').animate({
                left: '200px'
            });
            $('#admin-footer').animate({
                left: '200px'
            });
            $('#admin-side').animate({
                width: '200px'
            });
        }
    });
    $('.admin-side-full').on('click', function () {
        var docElm = document.documentElement;
        //W3C  
        if (docElm.requestFullscreen) {
            docElm.requestFullscreen();
        }
        //FireFox  
        else if (docElm.mozRequestFullScreen) {
            docElm.mozRequestFullScreen();
        }
        //Chrome等  
        else if (docElm.webkitRequestFullScreen) {
            docElm.webkitRequestFullScreen();
        }
        //IE11
        else if (elem.msRequestFullscreen) {
            elem.msRequestFullscreen();
        }
        layer.msg('按Esc即可退出全屏');
    });

    $('#setting').on('click', function () {
        tab.tabAdd({
            href: '/Manage/Account/Setting/',
            icon: 'fa-gear',
            title: '设置'
        });
    });

    //锁屏
    $(document).on('keydown', function () {
        var e = window.event;
        if (e.keyCode === 76 && e.altKey) {
            //alert("你按下了alt+l");
            lock($, layer);
        }
    });
    $('#lock').on('click', function () {
        lock($, layer);
    });

    //手机设备的简单适配
    var treeMobile = $('.site-tree-mobile'),
        shadeMobile = $('.site-mobile-shade');
    treeMobile.on('click', function () {
        $('body').addClass('site-mobile');
    });
    shadeMobile.on('click', function () {
        $('body').removeClass('site-mobile');
    });
});

var isShowLock = false;
function lock($, layer) {
    if (isShowLock)
        return;
    //自定页
    layer.open({
        title: false,
        type: 1,
        closeBtn: 0,
        anim: 6,
        content: $('#lock-temp').html(),
        shade: [0.9, '#393D49'],
        success: function (layero, lockIndex) {
            isShowLock = true;
            //给显示用户名赋值
            //layero.find('div#lockUserName').text('admin');
            //layero.find('input[name=username]').val('admin');
            layero.find('input[name=password]').on('focus', function () {
                var $this = $(this);
                if ($this.val() === '输入密码解锁..') {
                    $this.val('').attr('type', 'password');
                }
            })
               
            //在此处可以写一个请求到服务端删除相关身份认证，因为考虑到如果浏览器被强制刷新的时候，身份验证还存在的情况			
            //do something...
            //e.g. 

            $.getJSON(site_url+'login_out/', null, function (res) {
                if (!res.rel) {
                    layer.msg(res.msg);
                }
            }, 'json');

            //绑定解锁按钮的点击事件
            layero.find('button#unlock').on('click', function () {
                var $lockBox = $('div#lock-box');

                var userName = $lockBox.find('input[name=lockUser]').val();
                var pwd = $lockBox.find('input[name=lockPwd]').val();
                if (pwd === '输入登录密码解锁..' || pwd.length === 0) {
                    layer.msg('请输入密码..', {
                        icon: 2,
                        time: 1000
                    });
                    return;
                }
                unlock(userName, pwd);
            });
			/**
			 * 解锁操作方法
			 * @param {String} 用户名
			 * @param {String} 密码
			 */
            var unlock = function (un, pwd) {
                console.log(un, pwd);
                //这里可以使用ajax方法解锁
                $.post(site_url+'unLock/', { userName: un, password: pwd }, function (res) {
                	//debugger
                    //验证成功
                    if (res.code) {
                        //关闭锁屏层
                        layer.close(lockIndex);
                        isShowLock = false;
                    } else {
                        layer.msg(res.msg, { icon: 2, time: 1000 });
                    }
                }, 'json');
                //isShowLock = false;
                //演示：默认输入密码都算成功
                //关闭锁屏层
                //layer.close(lockIndex);
            };
        }
    });
}

function chgPwd(){
	layer.open({
        title: "密码修改",
        type: 1,
        closeBtn: 0,
        anim: 6,
        content: jQuery("#changePwd"),
        shade: [0.9, '#393D49'],
        area: ['650px', '470px'],
        shadeClose: false,
        btn: ['修改','取消'],
		btn1: function (index) {
			var data = "op_password="+$("#newPwd").val()+"&newPassword="+$("#confirmPwd").val()+"&op_id="+user_id;
			$.ajax({
				type: "POST",
			    url: site_url+'updPwd/',
			    data: data,
			    dataType: "json",
			    success: function(result){
					if(result.code){
						layer.close(index);
						alert('修改成功', function(index){
							vm.reload();
						});
					}else{
						alert(result.msg);
					}
				}
			});
        }
	});
}