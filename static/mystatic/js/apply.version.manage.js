function updateType(obj,id,name){
	window.parent._update_type=id;
	window.parent.update_type_sel=$(obj).val();
	parent.layer.open({
		type: 2,
		title: name+' 版本确认',
		maxmin: false,
		scrollbar: false,
		area: ['320px', '240px'],
		content: window.parent.getRootPath()+'apply_vm_box/',
		end:function(){
			$(obj).children("option").each(function(){
		        var temp_value = $(this).val();
		        if(temp_value == '0'){
		             $(this).attr("selected","selected");
		        }
			});
		}
	});
}
$(function(){
	var queryUrl=window.parent.getRootPath()+"getPagingAPPChangeByUnConfirm/";
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
	    			$(tr).append('<td>'+row.app_name+'</td>');
	    			$(tr).append('<td>'+row.app_in_host+'</td>');
	    			$(tr).append('<td>'+row.change_file+'</td>');
	    			$(tr).append('<td>'+row.bak_path+'</td>');
	    			$(tr).append('<td>'+row.bak_result+'</td>');
	    			$(tr).append('<td>'+row.app_last_bak_time+'</td>');
	    			$(tr).append('<td><select onchange="updateType(this,\''+row.id+'\',\''+row.app_name+'\');" style="margin-left: 15px;"><option value="0">未知</option><option value="1">上线变化</option><option value="2">受控变化</option><option value="3">异常变化</option></select></td>');
	    			$(tb).append(tr);
	    		});
	    	}
	    	$("#pagerAddBtn").hide();
	    },
	    params : function(){
	        return {
	            userName : null
	        };
	    }
	});
});