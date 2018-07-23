var busy_arr,select_busy,updateApplyId,_update_type,update_type_sel,_home_click=false,_home_click_id,_apply_m_query=false;
function showLayerLoading(con,time){
	layer.msg(con,{icon: 16,shade: 0.2,time: time});
}
function hideLayerLoading(){
	layer.closeAll();
}
function strShowManage(con,len){
	if(con!=null&&con.length>len){
		return con.substring(0,len)+"...";
	}else{
		return con;
	}
}
function parseJsonStr(con){
	//return JSON.parse(con);
	return con;
}
function triggerClick(_id,_time){
	setTimeout(function(){
		var _new_id="#"+_id;
		$(_new_id).trigger("click");
	},_time);
}
function getRootPath() {
	/*var pathName = window.location.pathname.substring(1);
	var webName = pathName == '' ? '' : pathName.substring(0, pathName
			.indexOf('/'));
	if (webName == "") {
		return window.location.protocol + '//' + window.location.host;
	} else {
		return window.location.protocol + '//' + window.location.host + '/'
				+ webName;
	}*/
	return site_url;
}
$(".sidebar-title").live('click', function() {
	if ($(this).parent(".sidebar-nav").hasClass("sidebar-nav-fold")) {
		$(this).next().slideDown(200);
		$(this).parent(".sidebar-nav").removeClass("sidebar-nav-fold");
	} else {
		$(this).next().slideUp(200);
		$(this).parent(".sidebar-nav").addClass("sidebar-nav-fold");
	}
});
$(function(){
	$.ajax({
		type: 'GET',
	  	url: getRootPath()+"get_user_biz/",
	  	data: null,
	  	success: function(returnData){
			returnData = parseJsonStr(returnData);
			busy_arr = returnData;
			var tb = $('#dropdown_busy');
	    	$(tb).empty();
			if(returnData.code && returnData.list.length > 0){
	    		$.each(returnData.list,function(i,row){
	    			if(i==0){
	    				$("#busy_select").text(row.buseName);
	    				select_busy=row.buseId;
	    			}else{
	    				var tr = $('<li>');
		    			$(tr).append('<a href="javascript:void(0);" onclick="selectBusy(this);" name="'+row.buseId+'">'+row.buseName+'</a>');
		    			$(tr).append('</li>');
		    			$(tb).append(tr);
	    			}
	    		});
	    	}
		},
	  	dataType: 'json'
	});
});
function selectBusy(obj){
	var id=$(obj).attr("name");
	var tb = $('#dropdown_busy');
	$(tb).empty();
	if(busy_arr.code && busy_arr.list.length > 0){
		$.each(busy_arr.list,function(i,row){
			if(row.buseId==id){
				$("#busy_select").text(row.buseName);
				select_busy=row.buseId;
			}else{
				var tr = $('<li>');
    			$(tr).append('<a href="javascript:void(0);" onclick="selectBusy(this);" name="'+row.buseId+'">'+row.buseName+'</a>');
    			$(tr).append('</li>');
    			$(tb).append(tr);
			}
		});
	}
	$("#busy_select").trigger("click");
}

function copyPath(obj){
    var oInput = document.createElement('input');
    oInput.value = obj;
    document.body.appendChild(oInput);
    oInput.select(); // 选择对象
    document.execCommand("Copy"); // 执行浏览器复制命令
    oInput.className = 'oInput';
    oInput.style.display='none';
	layer.msg("已复制到剪切板!");
}