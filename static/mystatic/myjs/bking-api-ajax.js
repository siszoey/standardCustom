$(function(){
	//search_business();
	//search_app_info();
	//search_host();
	//get_job_list();
	//get_template_list();
	//get_template_info();
	//addstu2();
	asyncKoalaData();
});

function asyncKoalaData(){
	$.post(site_url+'async_koala_data/',function(r){
		if(r.code){
			for(var i = 0;i < r.list.length; i ++){
				if(r.list[i].dict_name == 'async_event_time_aging'){
					var m = parseInt(r.list[i].dict_value)
					ref = setInterval(syncDataByEvents,60*1000*m);
				}
			}
		}
    });
}

function syncDataByEvents(){
	$.post(site_url+'get_events/',{'curr_time':currentDate()},function(r){
		/*if(r.code){
			//$("#biz_count").html(r.count);
		}*/
    });
}

function loginKuoShi(){
	/*$.ajax({
		 url: 'http://192.168.1.50/auth/login',
		 headers: {
			 'User-Agent':'Koala Admin',
			 'Content-Type':'application/JSONP;charset=UTF-8'
		 },
		 type: 'POST',
		 dataType: 'JSONP',
		 data: {"username":"test@megvii.com","password":"123456"},
		 success: function(ret){
			 alert(ret);
			 debugger
			 console.log('succes: '+ret);
		 },error:function(ret){
			 debugger
	         alert("error");
	     }
	});*/
	$.post(site_url+'get_events/',function(r){
		/*if(r.code){
			//$("#biz_count").html(r.count);
		}*/
    });
}

function addstu2(){
	for(var i = 1 ;i <= 100;i++){
		for(var j=1;j<=10;j++){
			var stu_img = "/test"+i+".png";
			var type = "非人工";
			var in_or_out = "离开";
			debugger
			var stu_flow_date = new Date().Format("yyyy-MM-dd hh:mm:ss",5*j);//Format("输入你想要的时间格式:yyyy-MM-dd,yyyyMMdd")
				$.post(site_url+'test_add_student_out/',{
					"type":type,
					"in_or_out":in_or_out,
					"stu_flow_date":stu_flow_date,
					"stu_img":stu_img
				},function(r){
					debugger
					if(r.code){
						//$("#biz_count").html(r.count);
					}
			    });
		}
		
	}
	
}
function addstu(){
	for(var i = 1 ;i <= 50;i++){
		for(var j=1;j<=10;j++){
			var stu_img = "/test"+i+".png";
			var stu_code = "1000"+i;
			var in_or_out = "离寝";
			debugger
			var stu_flow_date = new Date().Format("yyyy-MM-dd hh:mm:ss",5*j);//Format("输入你想要的时间格式:yyyy-MM-dd,yyyyMMdd")
				$.post(site_url+'test_add_student_in/',{
					"stu_code":stu_code,
					"in_or_out":in_or_out,
					"stu_flow_date":stu_flow_date,
					"stu_img":stu_img
				},function(r){
					debugger
					if(r.code){
						//$("#biz_count").html(r.count);
					}
			    });
		}
		
	}
	
}
Date.prototype.Format = function (fmt,m) {
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes()+m, //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
 
function addstu1(){
	for(var i = 1 ;i <= 2000;i++){
		var stu_img = "/test"+i+".png";
		var stu_code = "1000"+i;
		var stu_name = "张三"+i;
		var stu_class = "高三"+i+"班";
		var stu_build = "一栋";
		var stu_room = "1楼10"+i+"室";
			$.post(site_url+'test_add_student/',{
				"stu_code":stu_code,
				"stu_name":stu_name,
				"stu_class":stu_class,
				"stu_build":stu_build,
				"stu_room":stu_room,
				"stu_img":stu_img
			},function(r){
				debugger
				if(r.code){
					//$("#biz_count").html(r.count);
				}
		    });
	}
	
}

/**
 * 查询模板
 */
function get_template_info(){
	$.post(site_url+'get_template_info/',function(r){
		debugger
		if(r.code){
			//$("#biz_count").html(r.count);
		}
    });
}
/**
 * 查询模板
 */
function get_template_list(){
	$.post(site_url+'get_template_list/',function(r){
		debugger
		if(r.code){
			//$("#biz_count").html(r.count);
		}
    });
}

/**
 * 查询业务
 */
function search_business(){
	$.post(site_url+'search_business/',function(r){
		debugger
		if(r.code){
			$("#biz_count").html(r.count);
		}
    });
}

/**
 * 查询应用
 */
function search_app_info(){
	$.post(site_url+'search_app_info/',function(r){
		debugger
		if(r.code){
			$("#app_count").html(r.count);
		}
    });
}

/**
 * search_host 查询主机
 **/
function search_host(){
	$.post(site_url+'search_host/',function(r){
		debugger
		if(r.code){
			$("#host_count").html(r.count);
		}
    });
}

/**
 * get_job_list查询作业模板
 */
function get_job_list(){
	$.post(site_url+'get_job_list/',function(r){
		debugger
		if(r.code){
			$("#job_count").html(r.count);
		}
    });
}