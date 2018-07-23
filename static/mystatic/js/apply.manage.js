function updateInfo(id,name){
	window.parent.updateApplyId=id;
	var index = parent.layer.open({
		type: 2,
		title: '修改应用  '+name+'  配置信息',
		maxmin: true,
		scrollbar: false,
		area: ['45%', '60%'],
		content: window.parent.getRootPath()+'edit_apply_info/',
	});
}
function deleteInfo(id,name){
	layer.confirm(name+' 删除后不可恢复!', {
		  btn: ['确定','取消'] //按钮
	}, function(index){
		layer.close(index);
	  	window.parent.showLayerLoading("正在删除...",60000);
		$.ajax({
			type: 'get',
		  	url: window.parent.getRootPath()+"doDelAPPConfig/",
		  	data: {"id":id},
		  	success: function(returnData){
		  		window.parent.hideLayerLoading();
				returnData = window.parent.parseJsonStr(returnData);
				window.parent.layer.msg(returnData.text,{icon: 1,time: 2000});
				window.parent.triggerClick('Applicationinformationmanagement',1000);
			},
		  	dataType: 'json'
		});
	}, function(){
	  //layer.msg('取消');
	});
}
function addInfo(){
	var index = parent.layer.open({
		type: 2,
		title: '添加应用配置信息',
		maxmin: true,
		scrollbar: false,
		area: ['45%', '60%'],
		content: window.parent.getRootPath()+'add_apply_info/',
	});
}
$(function(){
	$.ajax({
		type: 'get',
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
					var tr;
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
	searchApplyInfo();
});

function getTypeName(id){
	msg = "";
	$.ajax({
		type: 'get',
		async:false,
	  	url: window.parent.getRootPath()+"getDictById/",
	  	data: {"id":id},
	  	success: function(returnData){
	  		debugger
	  		if(returnData.code){
	  			data = returnData.list;
	  			msg = data[0].dict_name;
	  		}
		},
	  	dataType: 'json'
	});
	return msg;
}

function searchApplyInfo(){
	$('#page3').empty();
	$('#page3').scroPage({
	    url : window.parent.getRootPath()+"getPagingAPPConfigList/",
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
	    			$(tr).append('<td>'+row.id+'</td>');
	    			$(tr).append('<td>'+row.app_name+'</td>');
	    			$(tr).append('<td>'+row.app_host_ip+'</td>');
	    			$(tr).append('<td>'+getTypeName(row.app_type)+'</td>');
	    			if(row.app_check_unit=='day'){
	    				$(tr).append('<td>'+row.app_check_cycle+'(天)</td>');
	    			}else if(row.app_check_unit=='hour'){
	    				$(tr).append('<td>'+row.app_check_cycle+'(时)</td>');
	    			}else if(row.app_check_unit=='minute'){
	    				$(tr).append('<td>'+row.app_check_cycle+'(分)</td>');
	    			}else{
	    				$(tr).append('<td></td>');
	    			}
	    			if(row.app_status==0){
	    				$(tr).append('<td>有效</td>');
	    			}else{
	    				$(tr).append('<td>无效</td>');
	    			}
	    			$(tr).append('<td>'+row.app_creator+'</td>');
	    			$(tr).append('<td>'+row.app_create_time+'</td>');
	    			$(tr).append('<td><input type="button" value="修改" onclick="updateInfo(\''+row.id+'\',\''+row.app_name+'\');" class="button" style="margin-left: 15px;"/><input type="button" value="删除" onclick="deleteInfo(\''+row.id+'\',\''+row.app_name+'\');" class="button" style="margin-left: 15px;"/></td>');
	    			$(tb).append(tr);
	    		});
	    	}
	    	$("#pagerAddBtn").show();
	    },
	    params : function(){
	        return {
	        	applyType:$("#applyType").val(),
	        	appName:$("#appName").val(),
	        	appIp:$("#appIp").val()
	        };
	    }
	});
	
}