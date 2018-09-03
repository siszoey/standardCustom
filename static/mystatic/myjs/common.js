/***一些公公方法**/
/**
 * ServletContext路径
 * 
 * @returns
 */
function getContext()
{
	return site_url;
}

/**
 * 客户端当前时间
 * 
 * @returns
 */
function currentDate()
{
	return now;
}

/**
 * 
 * 获取当前时间
 */
function p(s) {
    return s < 10 ? '0' + s: s;
}

var myDate = new Date();
//获取当前年
var year=myDate.getFullYear();
//获取当前月
var month=myDate.getMonth()+1;
//获取当前日
var date=myDate.getDate(); 
var h=myDate.getHours();       //获取当前小时数(0-23)
var m=myDate.getMinutes();     //获取当前分钟数(0-59)
var s=myDate.getSeconds();  

var now=year+'-'+p(month)+"-"+p(date)+" "+p(h)+':'+p(m)+":"+p(s);

/**
 * 注册自己
 * 
 * @param _r
 */
function register(_r)
{
	for ( var n in _r)
	{
		var i = _r[n];
		if (i instanceof Function)
		{
			i.$ = _r;
		}
	}
}

/**
 * 计算Frame高度
 * 
 * @param obj
 */
function setFrameHeightAsPage(obj)
{   
	var height = $(window).height();
	height = height==0?490:height;
	var top = 0;
	if($("#content_div").length > 0){
		top = $("#content_div").offset().top;
	}
	$("#" + obj.id).css("height", height - top -20);
}




/**
 * 字符串自动URL参数化处理
 * 
 * @author pst
 * 
 */
function urlPara(u)
{
	//var u = this;
	if (u.indexOf("?") == -1)
	{
		u += "?";
	} else
	{
		u += "&";
	}

	u += "OLMTTIMESTAMP=" + currentDate();

	return getContext() + u;
}

/**
 * 方法:Array.remove(dx) 通过遍历,重构数组 功能:删除数组元素. 参数:dx删除元素的下标.
 */
Array.prototype.remove = function(dx)
{
	if (isNaN(dx) || dx > this.length)
	{
		return false;
	}
	for ( var i = 0, n = 0; i < this.length; i++)
	{
		if (this[i] != this[dx])
		{
			this[n++] = this[i];
		}
	}
	this.length -= 1;
};

/*********Json 数据操作*********/



/*********frame 导出***********/

function getParaMap(url)
{
   var intPos = url.indexOf("?");
   var strRight = url.substr(intPos + 1);//==========获取到右边的参数部分
   var arrTmp = strRight.split("&");//=============以&分割成数组
   var map =""; 
   for(var i = 0; i < arrTmp.length; i++ ) //===========循环数组
   {
     var dIntPos = arrTmp[i].indexOf("=");
     var paraName= arrTmp[i].substr(0,dIntPos);
     var paraData= arrTmp[i].substr(dIntPos+1);
    
     map+=',"'+paraName+'":"'+paraData+'"';
   }
   map = map.substr(1);
   return "{"+map+"}";
}

IframePost = function() {
    var 
        
        createForm = function(obj) {
            var oForm = document.createElement("form");
            oForm.id = "forPost";
            oForm.method = "post";
            oForm.action = obj.Url;
            oForm.target = "_self";
            var oIpt, arrParams;
            arrParams = obj.PostParams;
            for (var tmpName in arrParams) {
                oIpt = document.createElement("input");
                oIpt.type = "hidden";
                oIpt.name = tmpName;
                oIpt.value = arrParams[tmpName];
                oForm.appendChild(oIpt);
            }
            xhr = new XMLHttpRequest();
        	oIpt = document.createElement("input");
            oIpt.type = "hidden";
            oIpt.name = "csrftoken";
            oIpt.value = showRequest(xhr,oForm);
            oForm.appendChild(oIpt);
            
            return oForm;
        },
        deleteForm = function() {
            var oOldFrm = document.getElementById("forPost");
            if (oOldFrm) {
                document.body.removeChild(oOldFrm);
            }
        }
        showRequest = function(xhr, settings){
        	//debugger
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
                //xhr.setRequestHeader("X-CSRFToken", csrftoken);
                return csrftoken;
            }
            
        }

    return {
        //功能：给嵌套的Iframe界面Post值
        //参数：obj - 传递对象
        //     {Url - 页面地址, Target - Iframe对象, PostParams - Post参数,{ 参数名1 : 值1, 参数名2 : 值2 } }
        //例：{ Url: "aicf/gridExportComponent.action", Target: 'myiframe', PostParams: { type: 'excel',gridcode:'alarList'} }
        doPost: function(obj) {
            deleteForm();
            var oForm = createForm(obj);
            //var doc = window.frames[obj.Target].document.appendChild(oForm);
            var doc = document.getElementById(obj.Target).document || document.getElementById(obj.Target).contentWindow.document;
            doc.body.appendChild(oForm);
            oForm.submit();
            deleteForm();
        }
    }
} ();



