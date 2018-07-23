$(function(){
	//query apply type
	$.ajax({
		type: 'GET',
		url: window.parent.getRootPath()+"getDictByType?dict_type=APP_TYPE",
		data: null,
		async:false,
		success: function(returnData){
			returnData = window.parent.parseJsonStr(returnData);
			var tb = $('#applyType');
			$(tb).empty();
			if(returnData.code && returnData.list.length > 0){
				$(tb).append('<option value="0" selected="selected">-全部-</option>');
				$.each(returnData.list,function(i,row){
					var tr;// = $('<option value="'+row.id+'">');
					if(window.parent._home_click&&window.parent._home_click_id==row.id){
						tr = $('<option selected="selected" value="'+row.id+'">');
					}else{
						tr = $('<option value="'+row.id+'">');
					}
					$(tr).append(row.dict_name);
					$(tr).append('</option>');
					$(tb).append(tr);
				});
			}
			window.parent._home_click=false;
		},
		dataType: 'json'
	});
	//end 
	laydate.render({
		 elem: '#checkTime'
		 ,range: true
		 ,range: '~'
	});
	if(window.parent._apply_m_query){
		window.parent._apply_m_query=false;
		searchVersion();
	}
});
function getInfo(id,name,result){
	if(removeAllSpace(result) != "成功"){
		layer.msg("版本备份未成功，不能提取历史版本",{icon: 2,time: 5000});
		return;
	}
	layer.confirm('确认提取  '+name+'?', {
		  btn: ['确定','取消'] //按钮
	}, function(index){
		layer.close(index);
	  	var indd=window.parent.showLayerLoading("正在提取...",60000);
		$.ajax({
			type: 'GET',
		  	url: window.parent.getRootPath()+"recover_his_version/",
		  	data: {"id":id,"name":name},
		  	success: function(returnData){
		  		window.parent.hideLayerLoading();
				returnData = window.parent.parseJsonStr(returnData);
				/*if(returnData.code){
					layer.msg(returnData.text,{icon: 1,time: 6000});
				}else{
					layer.msg(returnData.text,{icon: 2,time: 6000});
				}*/
				if(returnData.code){
					var con="<div style='font-size:14px;margin-left:15px;margin-top:8px;word-break:break-all;'><b>"+returnData.text+"</b></div>"+
			  		"<div style='font-size:14px;margin-left:15px;margin-top:8px;'><b>IP:<span style='color:red'>"+returnData.IP+"</span></b></div>"+
			  		"<div style='font-size:14px;margin-left:15px;margin-top:8px;word-break:break-all;'><b>路径:<span style='color:red'>"+returnData.path+"</span></b></div>"+
			  		"<div style='margin-top:5px;' align='center'><input type='button' style='text-decoration:none;background:#1D689C;color:#f2f2f2;padding: 5px 5px 5px 5px;font-size:13px;"+
			  		"font-family: 微软雅黑,宋体,Arial,Helvetica,Verdana,sans-serif;font-weight:bold;border-radius:3px;-webkit-transition:all linear 0.30s;"+
			  		"moz-transition:all linear 0.30s;transition:all linear 0.30s;' value='复制路径' onclick='copyPath(\""+returnData.path+"\");'></div>";
					var index = parent.layer.open({
						type: 1,
						title: name+'  提取结果',
						maxmin: false,
						resize:false,
						scrollbar: false,
						area: ['515px', '250px'],
						content: con
					});
		  		}else{
		  			var con="<div style='font-size:14px;margin-left:15px;margin-top:8px;word-break:break-all;'><b>"+returnData.text+"</b></div>";
					var index = parent.layer.open({
						type: 1,
						title: name+'  提取结果',
						maxmin: false,
						resize:false,
						scrollbar: false,
						area: ['515px', '250px'],
						content: con
					});
		  		}
			},
		  	dataType: 'json'
		});
	}, function(){
	  //layer.msg('取消');
	});
}

function searchVersionKey(event){
   var e = event || window.event || arguments.callee.caller.arguments[0];
   if(e && e.keyCode==13){ // enter 键
	  searchVersion();
   }
}
function removeAllSpace(str) {
    return str.replace(/\s+/g, "");
}
function searchVersion(){
	var queryUrl=window.parent.getRootPath()+"getPagingAPPChangeByConfirmed/";
	var checkTimeStr=$("#checkTime").val();
	if(checkTimeStr!=null&&checkTimeStr!=''){
		checkTimeStr=removeAllSpace(checkTimeStr);
	}
	$("#checkTimeQuery").val(checkTimeStr);
	$('#page3').empty();
	$('#page3').scroPage({
	    url : queryUrl,
	    asyncLoad : true,
	    asyncType : 'GET',
	    serverSidePage : false,
	    render : function(data){
	    	var tb = $('#dataGridTableJson tbody');
	    	$(tb).empty();
	    	window.parent.hideLayerLoading();
	    	if(data && data.list && data.list.length > 0){
	    		$.each(data.list,function(i,row){
	    			var tr = $('<tr>');
	    			$(tr).append('<td>'+row.app_id+'</td>');
	    			$(tr).append('<td title='+row.app_name+'>'+window.parent.strShowManage(row.app_name,9)+'</td>');
	    			$(tr).append('<td>'+row.app_in_host+'</td>');
	    			$(tr).append('<td>'+row.app_type+'</td>');
	    			$(tr).append('<td title='+row.app_name+'>'+window.parent.strShowManage(row.change_file,9)+'</td>');
	    			$(tr).append('<td title='+row.bak_path+'>'+window.parent.strShowManage(row.bak_path,9)+'</td>');
	    			$(tr).append('<td title='+row.bak_result+'>'+window.parent.strShowManage(row.bak_result,9)+'</td>');
	    			$(tr).append('<td>'+row.app_last_bak_time+'</td>');
	    			if(row.change_type==0){
	    				$(tr).append('<td>未知</td>');
	    			}else if(row.change_type==1){
	    				$(tr).append('<td>上线变化</td>');
	    			}else if(row.change_type==2){
	    				$(tr).append('<td>受控变化</td>');
	    			}else if(row.change_type==3){
	    				$(tr).append('<td>异常变化</td>');
	    			}else{
	    				$(tr).append('<td></td>');
	    			}
	    			$(tr).append('<td>'+row.check_time+'</td>');
	    			$(tr).append('<td title='+row.confirm_mark+'>'+window.parent.strShowManage(row.confirm_mark,9)+'</td>');
	    			$(tr).append('<td>'+row.confirm_time+'</td>');
	    			$(tr).append('<td><input type="button" value="提取" onclick="getInfo(\''+row.id+'\',\''+row.app_name+'\',\''+row.bak_result+'\');" class="button" style="margin-left: 15px;"/></td>');
	    			$(tb).append(tr);
	    		});
	    	}
	    	$("#pagerAddBtn").hide();
	    },
	    params : function(){
	        return {
	        	appName : $("#appName").val(),
	        	appIp : $("#appIp").val(),
	        	applyType : $("#applyType").val(),
	        	checkTime : $("#checkTimeQuery").val(),
	        	changeResult : $("#changeResult").val(),
	        	changeType : $("#changeType").val()
	        };
	    }
	});
}