$(function(){
	$.ajax({
		type: 'get',
	  	url: window.parent.getRootPath()+'getAPPConfigById?id='+window.parent.updateApplyId,
	  	data: {"applyId":window.parent.updateApplyId},
	  	success: function(returnData){
			returnData = window.parent.parseJsonStr(returnData);
			if(returnData.code){
	    		$("#appBakPath").val(returnData.list[0].app_bak_path);
	    		$("#app_name").val(returnData.list[0].app_name);
	    		$("#checkTime").val(returnData.list[0].app_check_cycle);
	    		$("#timeType").val(returnData.list[0].app_check_unit);
	    		loadConfigPath(returnData.list[0].app_config_file_path);
	    		loadHost(returnData.list[0].app_host_ip);
	    		loadApplyType(returnData.list[0].app_type);
	    	}
		},
	  	dataType: 'json'
	});
});
function loadConfigPath(path){
	if(path!=null&&path.length>0){
		var arr=path.split(",");
		for(var i=0;i<arr.length;i++){
			if(i==0){
				$("#topPathInput").val(arr[i]);
			}else{
				var tb = $('#deployPath');
				var tr = $('<tr>');
				$(tr).append('<td><input type="text" class="form-control" value="'+arr[i]+'" placeholder="绝对路径+文件名">');
				$(tr).append('</td>');
				$(tr).append('<td><label class="font_input pic_input"><span class="glyphicon glyphicon-minus" aria-hidden="true" onclick="deleteDeployPath(this);"></span></label>');
				$(tr).append('</td>');
				$(tb).append(tr);
			}
		}
	}
}
//selected="selected"
function loadHost(ip){
	$.ajax({
		type: 'GET',
	  	url: window.parent.getRootPath()+"getUserIps?biz_name="+window.parent.select_busy,
	  	data: null,
	  	success: function(returnData){
			returnData = window.parent.parseJsonStr(returnData);
			var tb = $('#selectHost');
	    	$(tb).empty();
			if(returnData.code && returnData.list.length > 0){
	    		$.each(returnData.list,function(i,row){
	    			var tr;
	    			if(ip==row.host_ip){
	    				tr=$('<option selected="selected" value="'+row.host_ip+'" host_source="'+row.source+'" app_name="'+row.app_name+'" app_id="'+row.app_id+'" os_type="'+row.os_type+'">');
	    			}else{
	    				tr=$('<option value="'+row.host_ip+'" host_source="'+row.source+'" app_name="'+row.app_name+'" app_id="'+row.app_id+'" os_type="'+row.os_type+'">');
	    			}
	    			$(tr).append(row.host_ip);
	    			$(tr).append('</option>');
	    			$(tb).append(tr);
	    		});
	    	}
		},
	  	dataType: 'json'
	});
}
function loadApplyType(type){
	$.ajax({
		type: 'GET',
		url: window.parent.getRootPath()+"getDictByType?dict_type=APP_TYPE",
		data: null,
		success: function(returnData){
		returnData = window.parent.parseJsonStr(returnData);
		var tb = $('#selectApplyType');
		debugger
		$(tb).empty();
		if(returnData.code && returnData.list.length > 0){
			$.each(returnData.list,function(i,row){
				var tr;
				if(type==row.id){
					tr = $('<option selected="selected" value="'+row.id+'">');
				}else{
					tr = $('<option value="'+row.id+'">');
				}
				$(tr).append(row.dict_name);
				$(tr).append('</option>');
				$(tb).append(tr);
			});
		}
	},
	dataType: 'json'
	});
}
function addDeployPath(){
	var tb = $('#deployPath');
	var tr = $('<tr>');
	$(tr).append('<td><input type="text" class="form-control" placeholder="绝对路径+文件名">');
	$(tr).append('</td>');
	$(tr).append('<td><label class="font_input pic_input"><span class="glyphicon glyphicon-minus" aria-hidden="true" onclick="deleteDeployPath(this);"></span></label>');
	$(tr).append('</td>');
	$(tb).append(tr);
}
function deleteDeployPath(obj){
	$(obj).parent("label").parent("td").parent("tr").remove();
}

function getTbodeyInput(){
	var inpus=[];
	$("#deployPath").find("tr").each(function(){
	    var tdArr = $(this).children();
	    var path = tdArr.eq(0).find("input").val();//收入类别
	    if(path!=null&&path!=''){
	    	inpus.push(path);
	    }
	  });
	if(inpus!=null&&inpus.length>0){
		return inpus.join(",");
	}else{
		return null;
	}
}
//save
function updateApplyInfo(){
	var appName=$("#app_name").val();
	if (appName==null || appName=='') { 
		layer.tips('<span style="color:red">应用名称不能为空!</span>', '#app_name',{tips:[1, '#E4E4E4'],time: 2000});
		$("#appBakPath").focus();
		return; 
	}
	var selectApplyType=$("#selectApplyType").val();
	if (selectApplyType==null || selectApplyType=='') { 
		layer.tips('<span style="color:red">应用类型不能为空!</span>', '#selectApplyType',{tips:[1, '#E4E4E4'],time: 2000});
		$("#selectApplyType").focus();
		return; 
	}
	var selectHost=$("#selectHost").val();
	var biz_id,biz_name,host_source,os_type;
	if (selectHost==null || selectHost=='') { 
		layer.tips('<span style="color:red">应用所属主机不能为空!</span>', '#selectHost',{tips:[1, '#E4E4E4'],time: 2000});
		$("#selectHost").focus();
		return; 
	}
	biz_id=$("#selectHost").find("option:selected").attr("app_id");
	biz_name=$("#selectHost").find("option:selected").attr("app_name");
	host_source=$("#selectHost").find("option:selected").attr("host_source");
	os_type=$("#selectHost").find("option:selected").attr("os_type");
	var deployPath=getTbodeyInput();
	if (deployPath==null || deployPath=='') { 
		layer.tips('<span style="color:red">应用文件不能为空!</span>', '#deployPath',{tips:[1, '#E4E4E4'],time: 2000});
		$("#deployPath").focus();
		return; 
	}
	var appBakPath=$("#appBakPath").val();
	if (appBakPath==null || appBakPath=='') { 
		layer.tips('<span style="color:red">应用所属主机不能为空!</span>', '#appBakPath',{tips:[1, '#E4E4E4'],time: 2000});
		$("#appBakPath").focus();
		return; 
	}
	var checkTime=$("#checkTime").val();
	if (!(/(^[1-9]\d*$)/.test(checkTime))) { 
		layer.tips('<span style="color:red">时间必须为整数</span>','#checkTime',{tips:[1, '#E4E4E4'],time: 2000});
		$("#checkTime").focus();
		return; 
	}
	var timeType=$("#timeType").val();
	if (timeType==null || timeType=='') { 
		layer.tips('<span style="color:red">时间单位不能为空!</span>', '#timeType',{tips:[1, '#E4E4E4'],time: 2000});
		$("#timeType").focus();
		return; 
	}
	var params={"id":window.parent.updateApplyId,"selectApplyType":selectApplyType
			,"selectHost":selectHost,"biz_id":biz_id,"biz_name":biz_name,"app_name":appName
			,"host_source":host_source,"os_type":os_type,"deployPath":deployPath
			,"appBakPath":appBakPath,"checkTime":checkTime,"timeType":timeType};
	window.parent.showLayerLoading("正在更新...",60000);
	$.ajax({
		type: 'GET',
	  	url: window.parent.getRootPath()+"doModifyAPPConfig/",
	  	data: params,
	  	success: function(returnData){
	  		window.parent.hideLayerLoading();
			returnData = window.parent.parseJsonStr(returnData);
			window.parent.layer.msg(returnData.text,{icon: 1,time: 2000});
			window.parent.triggerClick('Applicationinformationmanagement',1000);
		},
	  	dataType: 'json'
	});
}