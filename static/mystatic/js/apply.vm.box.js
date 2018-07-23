function saveVersion(){
	var applyId=window.parent._update_type;
	var typeSelect=window.parent.update_type_sel;
	var versionMark=$("#versionMark").val();
	/*if (versionMark==null || versionMark=='') { 
		layer.tips('<span style="color:red">请填写更备注信息!</span>', '#versionMark',{tips:[1, '#E4E4E4'],time: 2000});
		$("#timeType").focus();
		return; 
	}*/
	var param={"id":applyId,"changeType":typeSelect,"versionMark":versionMark};
	window.parent.showLayerLoading("正在保存...",60000);
	$.ajax({
		type: 'GET',
	  	url: window.parent.getRootPath()+"confirmCahngeStatus/",
	  	data: param,
	  	success: function(returnData){
	  		window.parent.hideLayerLoading();
			returnData = window.parent.parseJsonStr(returnData);
			window.parent.layer.msg(returnData.text,{icon: 1,time: 2000});
			window.parent.triggerClick('Versionchangeconfirmation',1000);
		},
	  	dataType: 'json'
	});
}