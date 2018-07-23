function updateType(id,name){
	layer.prompt({title: '应用类型修改', formType: 3,value: name}, function(text, index){
		layer.close(index);
	  	window.parent.showLayerLoading("正在更新...",60000);
		$.ajax({
			type: 'get',
		  	url: window.parent.getRootPath()+"doModifyAppTypeict/",
		  	data: {"id":id,"name":text},
		  	success: function(returnData){
		  		window.parent.hideLayerLoading();
				returnData = window.parent.parseJsonStr(returnData);
				window.parent.layer.msg(returnData.text,{icon: 1,time: 2000});
				window.parent.triggerClick('Applicationtypemanagement',1000);
			},
		  	dataType: 'json'
		});
	});
}
function deleteType(id,name){
	layer.confirm(name+' 删除后不可恢复!', {
		  btn: ['确定','取消'] //按钮
	}, function(index){
	  layer.close(index);
	  window.parent.showLayerLoading("正在删除...",60000);
	  $.ajax({
			type: 'GET',
		  	url: window.parent.getRootPath()+"doDelAppTypeDict/",
		  	data: {"id":id},
		  	success: function(returnData){
		  		window.parent.hideLayerLoading();
				returnData = window.parent.parseJsonStr(returnData);
				window.parent.layer.msg(returnData.text,{icon: 1,time: 2000});
				window.parent.triggerClick('Applicationtypemanagement',1000);
			},
		  	dataType: 'json'
		});
	}, function(){
	  //layer.msg('取消');
	});
}
function addInfo(){
	layer.prompt({title: '应用类型添加', formType: 3}, function(text, index){
		layer.close(index);
		window.parent.showLayerLoading("正在添加...",60000);
		  $.ajax({
			 type: 'GET',
		  	 url: window.parent.getRootPath()+"doAddAPPTypeDict/",
		  	 data: {"name":text},
		  	 success: function(returnData){
		  		window.parent.hideLayerLoading();
				returnData = window.parent.parseJsonStr(returnData);
				window.parent.layer.msg(returnData.text,{icon: 1,time: 2000});
				window.parent.triggerClick('Applicationtypemanagement',1000);
			 },
		  	 dataType: 'json'
		  });
	});
}
$(function(){
	var queryUrl=window.parent.getRootPath()+"getPagingAPPTypeDictList/";
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
	    			//$(tr).append('<td><label><input type="checkbox"></label></td>');
	    			$(tr).append('<td>'+row.id+'</td>');
	    			$(tr).append('<td>'+row.dict_name+'</td>');
	    			$(tr).append('<td><input type="button" value="修改" onclick="updateType(\''+row.id+'\',\''+row.dict_name+'\');" class="button" style="margin-left: 15px;"/><input type="button" value="删除" onclick="deleteType(\''+row.id+'\',\''+row.dict_name+'\');" class="button" style="margin-left: 15px;"/></td>');
	    			$(tb).append(tr);
	    		});
	    	}
	    	$("#pagerAddBtn").show();
	    },
	    params : function(){
	        return {
	            userName : null
	        };
	    }
	});
});