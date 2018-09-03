var grid = $("#jqGrid");
var grid2 = $("#jqGrid2");
$(function () {
    $("#jqGrid").jqGrid({
        url: site_url+'get_stu_in_paging/',
        mtype: 'POST',
        datatype: "json",
        colModel: [			
        	{ label: '学号', name: 'stu_code', index: 'stu_code', width: 50, key: true },
        	{ label: '姓名', name: 'stu_name', index: 'stu_name', width: 80 },	
        	{ label: '楼宇', name: 'stu_build', index: 'stu_build', width: 80 },
        	{ label: '班级', name: 'stu_class', index: 'stu_class', width: 80 }, 
			{ label: '寝室', name: 'stu_room', index: 'stu_room', width: 80 }, 
			{ label: '进出类型', name: 'in_or_out', index: 'in_or_out', width: 80}, 
			{ label: '归寝时间', name: 'stu_flow_date', index: 'stu_flow_date', width: 80},
			/*{ label: '照片', name: 'stu_img', index: 'stu_img',width: 60, formatter: function(value, options, row){
				return '<a> <img class="jqgrid_img" onclick="javascript:window.open(this.src)" src="http://192.168.1.50'+value+'"></img> </a>';
			}}*/
        ],
		viewrecords: true,
        height: $(window).height()-100,
        rowNum: 10,
		rowList : [10,30,50],
        rownumbers: true, 
        rownumWidth: 25, 
        autowidth:true,
        multiselect: true,
        pager: "#jqGridPager",
        //toolbar:[true,"top"],
        jsonReader : {
            root: "list",
            page: "pageNumber",
            total: "totalPage",
            records: "totalRow"
        },
        prmNames : {
            page:"page", 
            rows:"limit", 
            order: "order"
        },
        gridComplete:function(){
        	//隐藏grid底部滚动条
        	$("#jqGrid").closest(".ui-jqgrid-bdiv").css({ "overflow-x" : "hidden" }); 
        },
        loadComplete: function() {
        	debugger
        	$("#jqGrid").setGridHeight($(window).height()-100);
        	var total = $('#jqGrid').jqGrid('getGridParam', 'records'); 
        	$("#zaiqin").html("在寝人数:"+total);
        },
        ajaxGridOptions:{
        	beforeSend:function(xhr, settings){
        		function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
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
        }
    });
   // $('.grid-btn').appendTo('#t_jqGrid');
   // $('#t_jqGrid').append($('.grid-btn').html());
});

function loadOut () {
    $("#jqGrid2").jqGrid({
        url: site_url+'get_stu_out_paging/',
        mtype: 'POST',
        datatype: "json",
        colModel: [			
        	{ label: '学号', name: 'stu_code', index: 'stu_code', width: 50, key: true },
        	{ label: '姓名', name: 'stu_name', index: 'stu_name', width: 80 },	
        	{ label: '楼宇', name: 'stu_build', index: 'stu_build', width: 80 },
        	{ label: '班级', name: 'stu_class', index: 'stu_class', width: 80 }, 
			{ label: '寝室', name: 'stu_room', index: 'stu_room', width: 80 }, 
			{ label: '进出类型', name: 'in_or_out', index: 'in_or_out', width: 80}, 
			{ label: '离寝时间', name: 'stu_flow_date', index: 'stu_flow_date', width: 80}, 
			/*{ label: '照片', name: 'stu_img', index: 'stu_img',width: 60, formatter: function(value, options, row){
				return '<a> <img class="jqgrid_img" onclick="javascript:window.open(this.src)" src="http://192.168.1.50'+value+'"></img> </a>';
			}}*/
        ],
		viewrecords: true,
        height: $(window).height()-100,
        rowNum: 10,
		rowList : [10,30,50],
        rownumbers: true, 
        rownumWidth: 25, 
        autowidth:true,
        multiselect: true,
        pager: "#jqGridPager2",
        //toolbar:[true,"top"],
        jsonReader : {
            root: "list",
            page: "pageNumber",
            total: "totalPage",
            records: "totalRow"
        },
        prmNames : {
            page:"page", 
            rows:"limit", 
            order: "order"
        },
        gridComplete:function(){
        	//隐藏grid底部滚动条
        	$("#jqGrid2").closest(".ui-jqgrid-bdiv").css({ "overflow-x" : "hidden" }); 
        },
        loadComplete: function() {
        	debugger
        	var total = $('#jqGrid2').jqGrid('getGridParam', 'records'); 
        	$("#liqin").html("离寝人数:"+total);
        },
        ajaxGridOptions:{
        	beforeSend:function(xhr, settings){
        		debugger
        		function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
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
        }
    });
   // $('.grid-btn').appendTo('#t_jqGrid');
   // $('#t_jqGrid').append($('.grid-btn').html());
}

/*$(document).ready(function () {
	$(".datetimepicker").datetimepicker({
        language: "zh-CN",
		format: 'yyyy-mm-dd HH:mm:ss',
		weekStart: true,
        todayBtn:  true,
		autoclose: true,
		todayHighlight: true,
		startView: 2,
		forceParse: 0,
        showMeridian: true
    });
    
});*/

var setting = {
    data: {
        simpleData: {
            enable: true,
            idKey: "id",
            pIdKey: "pid",
            rootPId: -1
        },
        key: {
            url:"nourl"
        }
    }
};
var ztree;

//菜单树
var menu_ztree;
var menu_setting = {
    data: {
        simpleData: {
            enable: true,
            idKey: "priv_code",
            pIdKey: "parent_priv_code",
            rootPId: -1
        },
        key: {
            url:"nourl"
        }
    },
    check:{
        enable:true,
        nocheckInherit:true
    }
};

//角色树
var role_ztree;
var role_setting = {
    data: {
        simpleData: {
            enable: true,
            idKey: "role_code",
            pIdKey: "role_code",
            rootPId: 0
        },
        key: {
            url:"nourl"
        }
    },
    check:{
        enable:true,
        nocheckInherit:true
    }
};

var vm = new Vue({
    el:'#rrapp',
    data:{
        q:{
        	op_name: null,
        	login_code: null,
        	phone_id: null
        },
        showList: true,
        title:null,
        roleList:{},
        user:{
            status:0,
            org_id:null,
            bill_class:null,
            region_id:null,
            county_id:null,
        },
        op_password:'',
		newPassword:''
    },
    methods: {
        query: function () {
        	$("#jqGrid").jqGrid('setGridParam',{ 
                postData:{
                	'build_name': vm.q.stu_class,
                	'stu_class': vm.q.stu_class,
                	'q_date_start': $("#q_date_start").val()
                },
                page:1 
            }).trigger("reloadGrid");
        	$("#jqGrid2").jqGrid('setGridParam',{ 
                postData:{
                	'build_name': vm.q.stu_class,
                	'stu_class': vm.q.stu_class,
                	'q_date_start': $("#q_date_start").val()
                },
                page:1 
            }).trigger("reloadGrid");
        },
        exportGrid1:function(){
        	var g_paras=$("#jqGrid").jqGrid("getGridParam","colModel");
        	var names = getJqTitles(g_paras);
        	var showNames = getJqLable(g_paras);
        	var para = getQueryPara();
        	/*$.post(site_url+'exp_stu_in/',{'jgCols':names,'showNames':showNames,'para':JSON.stringify(para)},function(r){
        		
            });*/
        	 try{ 
                 var elemIF = document.createElement("iframe");   
                 elemIF.src = site_url+'exp_stu_in/?jgCols='+names+'&showNames='+showNames+'&para='+para;
                 elemIF.style.display = "none";   
                 document.body.appendChild(elemIF);   
             }catch(e){ 
      
             }
        	//window.frames["frameName"].location.href=
        	//$("body:eq(0)").append('<iframe id="_export_frame" style="display:none" width="500px" src="about:blank"></iframe>');
        	//IframePost.doPost({ Url: site_url+"exp_stu_in/", Target: "_export_frame", PostParams: {jgCols:names,showNames:showNames,para:JSON.stringify(para)} });
        },
        exportGrid2:function(){
        	var g_paras=$("#jqGrid2").jqGrid("getGridParam","colModel");
        	var names = getJqTitles(g_paras);
        	var showNames = getJqLable(g_paras);
        	var para = getQueryPara();
        	try{ 
                var elemIF = document.createElement("iframe");   
                elemIF.src = site_url+'exp_stu_out/?jgCols='+names+'&showNames='+showNames+'&para='+para;  
                elemIF.style.display = "none";   
                document.body.appendChild(elemIF);   
            }catch(e){ 
     
            }
        },
        add: function(){
            vm.showList = false;
            vm.title = "新增";
            vm.roleList = {};
            $("#user_op_password").css("display","");
            $("#login_code").css("readonly","");
            vm.user = {op_id:null, status:0,org_id:'',bill_class:'',region_id:'',county_id:''};
        },
        asyncUser: function(){
        	//同步蓝鲸账号数据
            $.post(site_url+'do_async_operator/', function(r){
            	debugger
                if(r.code){
                	alert('同步账号成功', function(){
                        vm.reload();
                    });
                }else{
                	alert(r.msg, function(){
                        //vm.reload();
                    });
                }
            });
        },
        getDept: function(){
            //加载部门树
            $.get(site_url+'/rest/sysorg/list', function(r){
            	debugger
                ztree = $.fn.zTree.init($("#deptTree"), setting, r);
                var node = ztree.getNodeByParam("id", vm.user.orgId);
                if(node != null){
                    ztree.selectNode(node);

                    vm.user.pName = node.name;
                }
            })
        },
        update: function () {
            var userId = getSelectedRow();
            if(userId == null){
                return ;
            }
            $("#user_op_password").css("display","none");
            $("#login_code").attr("readonly","readonly");
            vm.showList = false;
            vm.title = "修改";
            vm.getUser(userId);
        },
        toLocked: function () {
            var userIds = getSelectedRows();
            if(userIds == null){
                return ;
            }
            confirm('确定要锁定选中的用户吗？', function(){
	            $.ajax({
	                type: "POST",
	                traditional:true,
                    url: site_url+"do_lock_user/",
                    dataType:'json',
                    async: true,
                    data:{userIds:userIds},
	                success: function(r){
	                    if(r.code){
	                        alert('用户锁定成功', function(){
	                            vm.reload();
	                        });
	                    }else{
	                        alert(r.msg);
	                    }
	                }
	            });
            });
        },
        
        toUnLocked: function () {
            var userIds = getSelectedRows();
            if(userIds == null){
                return ;
            }

            $.ajax({
                type: "POST",
                traditional:true,
                url: site_url+"do_unlock_user/",
                dataType:'json',
                async: true,
                data:{userIds:userIds},
                success: function(r){
                    if(r.code){
                        alert('解锁成功', function(){
                            vm.reload();
                        });
                    }else{
                        alert(r.msg);
                    }
                }
            });
        },
        updatePassword: function(){
        	var userId = getSelectedRow();
        	if(userId == null){
                return ;
            }
            vm.getUser(userId);
			layer.open({
				type: 1,
				skin: 'layui-layer-molv',
				title: "修改密码",
				area: ['550px', '270px'],
				shadeClose: false,
				content: jQuery("#passwordLayer"),
				btn: ['修改','取消'],
				btn1: function (index) {
					var data = "op_password="+vm.op_password+"&newPassword="+vm.newPassword+"&op_id="+vm.user.op_id;
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
		},
        del: function () {
            var userIds = getSelectedRows();
            if(userIds == null){
                return ;
            }
            confirm('确定要删除选中的记录？', function(){
                $.ajax({
                    type: "POST",
                    traditional:true,
                    url: site_url+"do_del_user/",
                    dataType:'json',
                    async: true,
                    data:{userIds:userIds},
                    success: function(r){
                        if(r.code == 0){
                            alert('操作成功', function(){
                                vm.reload();
                            });
                        }else{
                            alert(r.msg);
                        }
                    }
                });
            });
        },
        saveOrUpdate: function () {
            var url = vm.user.op_id == null ? "do_add_user/" : "do_modify_user/";
            $.post(site_url+url,vm.user,function(res){
        		if (res.code) {	
        			alert('操作成功', function(){
                        vm.reload();
                    });
        		}else {
        			alert(res.msg);
        		}
        	}, 'json');
        },
        getUser: function(userId){
            $.post(site_url+'get_user/',{id:userId}, function(r){
            	if(r.code){
            		vm.user = r.list[0];
                    vm.user.password = null;
            	}else{
            		alert(r.msg);
            	}
                
            });
        },
        getRoleList: function(){
            $.get(site_url+'/rest/rssysrole/select', function(r){
                vm.roleList = r.list;
            });
        },
        deptTree: function(){
            layer.open({
                type: 1,
                offset: '50px',
                skin: 'layui-layer-molv',
                title: "选择部门",
                area: ['300px', '450px'],
                shade: 0,
                shadeClose: false,
                content: jQuery("#deptLayer"),
                btn: ['确定', '取消'],
                btn1: function (index) {
                    var node = ztree.getSelectedNodes();
                    //选择上级部门
                    debugger
                    vm.user.orgId = node[0].id;
                    vm.user.pName = node[0].name;

                    layer.close(index);
                }
            });
        },
        setRoles:function(){
        	$("#zaiqinlist").css("display","");
        	$("#liqinlist").css("display","none");
        	vm.reload();
        },
        setMenus:function(){
        	loadOut();
        	$("#jqGrid2").setGridWidth($(window).width()-15);
        	$("#liqinlist").css("display","");
        	$("#zaiqinlist").css("display","none");
        	vm.reload();
        },
        getMenuTree: function(user_id) {
            //加载菜单树
            $.post(site_url+'get_user_priv/',{login_code:user_id}, function(r1){
            	debugger
                menu_ztree = $.fn.zTree.init($("#menuTree"), menu_setting, r1.list);
            	var menuIds = r1.list;
                for(var i=0; i<menuIds.length; i++) {
                    var node = menu_ztree.getNodeByParam("priv_code", menuIds[i].priv_code);
                    menu_ztree.checkNode(node, true, false);
                    menu_ztree.expandNode(node, true, false, true);
                }
            });
        },
        getRoleTree: function(user_id) {
            //加载角色树
            $.post(site_url+'get_curr_user_role/',function(r1){
            	debugger
                role_ztree = $.fn.zTree.init($("#roleTree"), menu_setting, r1.list);
            	$.post(site_url+'get_user_role/',{id:user_id},function(r){
            		var roleIds = r.list;
                    for(var i=0; i<roleIds.length; i++) {
                        var node = role_ztree.getNodeByParam("role_code", roleIds[i].role_code);
                        role_ztree.checkNode(node, true, false);
                        role_ztree.expandNode(node, true, false, true);
                    }
                });
            });
        },
        reload: function () {
            vm.showList = true;
            var page = $("#jqGrid").jqGrid('getGridParam','page');
            $("#jqGrid").jqGrid('setGridParam',{
                postData:{'userName': vm.q.userName},
                page:page
            }).trigger("reloadGrid");
            var page2 = $("#jqGrid2").jqGrid('getGridParam','page');
            $("#jqGrid2").jqGrid('setGridParam',{
                postData:{'userName': vm.q.userName},
                page:page2
            }).trigger("reloadGrid");
        }
    }
});

$(document).ready(function () {
	//setSelectData("get_dict_type","bill_class");
	//setSelectData("get_dict_class","region_id");
	//setSelectData("get_dict_type","county_id");
	//setSelectData("get_dict_class","org_id");
});

function setSelectData(code, objId) {
	$.ajax({
		type: "POST",
        url: site_url+code+'/',
        dataType:'json',
        async: true,
        data:{},
	    success : function(r) {    
	    	var data = r.list;  
	    	var opts = "";  
	    	opts += "<option selected value=''>----------请选择----------</option>";
	    	for( var index = 0 ; index < data.length; index++ ){  
	    		var d = data[index];  
	    		opts += "<option value='"+d.dict_code+"'>"+d.dict_name+"</option>";  
	    	}
	    	// 查询界面  
	    	$("."+objId).append(opts);    
	  }    
	});
}
/*$('.form_datetime').datetimepicker({
	format: 'yyyy-mm-dd hh:ii:ss',
    weekStart: 0, //一周从哪一天开始
    todayBtn:  1, //
    autoclose: 1,
    todayHighlight: 1,
    startView: 2,
    forceParse: 0,
    showMeridian: 1
});*/

function getJqTitles(objs){
	var ret = "";
	for(var i=0;i<objs.length;i++){
		var obj = objs[i];
		if(obj.label != undefined){
			if(ret == ""){
				ret +=obj.label;
			}else{
				ret +="|"+obj.label;
			}
			
		}
	}
	return ret;
}

function getJqLable(objs){
	var ret = "";
	for(var i=0;i<objs.length;i++){
		var obj = objs[i];
		if(obj.label != undefined){
			if(ret == ""){
				ret +=obj.name;
			}else{
				ret +="|"+obj.name;
			}
			
		}
	}
	return ret;
}

//查询参数获取
function getQueryPara(){
	var  para = "";
	if(document.getElementById("build_name").value != ''
		&& document.getElementById("build_name").value != undefined){
		para+='&build_name='+document.getElementById("build_name").value;	
	}
	if(document.getElementById("stu_class").value != ''
		&& document.getElementById("stu_class").value != undefined){
		para+='&stu_class='+document.getElementById("stu_class").value;	
	}
	if(document.getElementById("q_date_start").value != ''
		&& document.getElementById("q_date_start").value != undefined){
		para+='&q_date_start='+document.getElementById("q_date_start").value;	
	}
	return para;
}