$(function() {
	// 图标信息加载
	$.ajax( {
		type : 'GET',
		url : window.parent.getRootPath() + "home_type_count/",
		data : null,
		success : function(returnData) {
			var box=$("#iconBox");
			box.empty();
			returnData = window.parent.parseJsonStr(returnData);
			if (returnData.code && returnData.list.length > 0) {
				$.each(returnData.list, function(i, row) {
					var ll='<li class="fl margin-large-35">'+
						'<a class="class-detail fl" onclick="querySkip(\''+row.type_id+'\')" href="javascript:void(0);" style="text-decoration:none">'+
						'<div class="class-detail-top">'+
							'<div class="text-center indentify-icon" style="margin-top: -8px;">'+
								'<span style="margin-left: 5px;"><img src="'+static_url+'mystatic/image/icon-data.png"></span>'+
								'<span class="badge badge-info" style="margin-top: -53px;margin-left: 60px;">'+row.change_totle+'</span>'+
							'</div>'+
							'<h5 class="text-center" stye="font-size: 14px;">'+row.type_name+'</h5>'+
						'</div><p class="continue text-small">查看详细</p></a></li>';
					box.append(ll);
				});
			}
		},
		dataType : 'json'
	});
	var bartitle=[],nochange=[],alreadychange=[];
	// 柱状图信息加载
	$.ajax( {
		type : 'GET',
		url : window.parent.getRootPath() + "home_chart_count/",
		data : null,
		success : function(returnData) {
		returnData = window.parent.parseJsonStr(returnData);
		if (returnData.code && returnData.list.length > 0) {
			$.each(returnData.list, function(i, row) {
				bartitle.push(row.type_name);
				nochange.push(row.no_changes);
			//	alreadychange.push(row.already_change);
			});
		}
		loadBarInfo(bartitle,nochange,alreadychange);
	},
	dataType : 'json'
	});
	var bartitleBottom=[],nochangeBottom=[],alreadychangeBottom=[];
	$.ajax( {
		type : 'GET',
		url : window.parent.getRootPath() + "home_chart_count_time/",
		data : null,
		success : function(returnData) {
		returnData = window.parent.parseJsonStr(returnData);
		if (returnData.code && returnData.list.length > 0) {
			$.each(returnData.list, function(i, row) {
				bartitleBottom.push(row.type_name);
				nochangeBottom.push(row.no_changes);
				alreadychangeBottom.push(row.already_change);
			});
		}
		$("#totle_container").height((42*returnData.list.length+85));
		loadBottomBarInfo(bartitleBottom,nochangeBottom,alreadychangeBottom);
	},
	dataType : 'json'
	});
});

function querySkip(id){
	window.parent._home_click=true;
	window.parent._home_click_id=id;
	window.parent._apply_m_query=true;
	window.parent.triggerClick('Applicationinformationmanagement',100);
}
function loadBarInfo(bartitle,nochange,alreadychange) {
	var dom = document.getElementById("data_container");
	var myChart = echarts.init(dom);
	option = null;
	option = {
		title: {
	        text: '当前异动文件未确认情况',
	        x:'center',
	        subtext: ''
	    },
		color : [ '#C23531'],//, '#91C7AE' ],
		tooltip : {
			trigger : 'axis',
			axisPointer : {
				type : 'shadow'
			}
		},
		/*legend : {
			data : [ '未知']//, '已确认' ]
		},*/
		calculable : true,
		xAxis : [ {
			type : 'category',
			axisTick : {
				show : false
			},
			data : bartitle
		} ],
		yAxis : [ {
			type : 'value'
		} ],
		series : [ {
			name : '未知',
			type : 'bar',
			barWidth : 35,
			data : nochange
		}
//		, {
//			name : '已确认',
//			type : 'bar',
//			barWidth : 35,
//			data : alreadychange
//		} 
		]
	};
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
	myChart.on('click',function(a,b){
		window.parent.triggerClick('Versionchangeconfirmation',100);
	});
}

function loadBottomBarInfo(bartitle,nochange,alreadychange){
	var dom = document.getElementById("totle_container");
	var myChart = echarts.init(dom);
	option = {
		title: {
	        text: '最近一个月内变更数据',
	        x:'center',
	        subtext: ''
	    },
		color : ['#91C7AE','#C23531'],
	    tooltip : {
	        trigger: 'axis',
	        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
	            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
	        }
	    },
	    legend: {
	        data: ['已确认','未知'],
	        x:'right',
	    },
	    grid: {
	        left: '3%',
	        right: '4%',
	        bottom: '3%',
	        containLabel: true
	    },
	    xAxis:  {
	        type: 'value'
	    },
	    yAxis: {
	        type: 'category',
	        data: bartitle
	    },
	    series: [
			{
			    name: '已确认',
			    type: 'bar',
			    stack: '总量',
			    label: {
			        normal: {
			            show: true,
			            position: 'insideRight'
			        }
			    },
			    data: alreadychange
			},
	        {
	            name: '未知',
	            type: 'bar',
	            stack: '总量',
	            label: {
	                normal: {
	                    show: true,
	                    position: 'insideRight'
	                }
	            },
	            data: nochange
	        }
	    ]
	};
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}
}
