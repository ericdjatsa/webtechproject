/**
 * Tip模块,用于在百科页面中显示弹出提示层
 * <publish> 
 * 	<Namespace name="Tip">
 * 		<Method name="showBeside">
 * 			<argv name="element"></argv>
 * 			<argv name="*argvs" optional></argv>
 * 		</Method>
 * 	</Namespace>	
 */
(function(){
	
//向window对象发布的命名空间名称
var PUBLISHNAME = 'Tip';

var isIE7 = (navigator.appName == "Microsoft Internet Explorer") && (navigator.appVersion.match(/7./i)=='7.');

//$函数
function $(s){
	return document.getElementById(s);
	}

function $show(el){
	el.style.display = 'block';
	}

function $hide(el){
	el.style.display = 'none';
	}	

//配置管理类
function Ini(){
	var _inisettings = {};
	function _wrap(name){
		return '{' + '}';
		}
	this.set = function(name,value){
		var sname = _wrap(name);
		_inisettings[sname] = value;
		};
	this.get = function(name){
		var sname = _wrap(name);
		var ret = _inisettings[sname];
		ret = ret ? ret : '';
		return ret;
		};
	}

//将Arguments对象转化为一个Array对象
function Arg2Arr(arg){
	var ret = [];
	for(var i=0,ilen=arg.length;i<ilen;i++){
		ret.push(arg[i]);
		}
	return ret;	
	}

//获取元素位置对象	
var Position = new function(){
	this.getAbsRect=function(el){
		var oriObj=el;
		var y1=x1=isHide=0;
		if(oriObj.style.display=='none'){
			oriObj.style.display='';
			isHide=1;
			}
		do{
			if(el.className == 'col3_wrap1'){
				y1+=el.offsetTop||0;
				el=el.offsetParent;
				continue;
				}
			y1+=el.offsetTop||0;
			x1+=el.offsetLeft||0;
			el=el.offsetParent;
			}
		while(el);
		a=[x1,(x1+oriObj.offsetWidth),y1,(y1+oriObj.offsetHeight)];
		if(isHide){
			oriObj.style.display='none';
			}
		return a;
		};	
	};

var PageSize = new function(){
	var isCSS1Dom = document.compatMode && (document.compatMode != "BackCompat");
	this.getWidth = function(){
		var x1=document.body.clientWidth;
		var x2=document.documentElement.clientWidth;
		return isCSS1Dom ? x2 : x1;};

	this.getHeight = function(){
		var y1=document.body.clientHeight;
		var y2=document.documentElement.clientHeight;
		return isCSS1Dom ? y2 : y1;};

	this.getScrollTop = function(){
		return isCSS1Dom ? 
			document.documentElement.scrollTop : document.body.scrollTop;};
			
	this.getScrollLeft = function(){
		return isCSS1Dom ? 
			document.documentElement.scrollLeft : document.body.scrollLeft;};					
	};

//Core
var Tip = new function(){
	//__init__ BEGIN
	var _ini = new Ini();
	_ini.set('tip_container_id','bk_tip_container');
	//__init__ END

	function _getTipDiv(){
		return $(_ini.get('tip_container_id'));
		}

	function _show(pos,html){
		var tip_con = _getTipDiv();//$(_ini.get('tip_container_id'));
		if(!tip_con){
			return false;
			}
		tip_con.style.left = pos.x + 'px';
		tip_con.style.top = pos.y + 'px';	
		tip_con.innerHTML = html;
		$show(tip_con);
		tip_con.style.zIndex = '9999';
		}	
	
	function _hide(){
		var tip_con = _getTipDiv();//$(_ini.get('tip_container_id'));
		if(!tip_con){
			return false;
			}
		$hide(tip_con);		
		}
	
	//获取相对element的显示Tip位置
	function _getBesidePos(element){
		var area = Position.getAbsRect(element);
		var pos = {x : area[0],y : area[3]};
		var tip_con = _getTipDiv();
		$show(tip_con);
		var maxRight = pos.x + tip_con.offsetWidth;
		$hide(tip_con);
		var deltaX = 0;
		var pageWidth = PageSize.getWidth();
		if(maxRight > pageWidth){
			deltaX = maxRight - pageWidth;
			pos.x -= deltaX; 
			}			
		return pos;
		}
	
	//获取页面居中位置
	function _getCenterPos(html){
		var tip = _getTipDiv();
		var ori_top = tip.style.top;
		var ori_left = tip.style.left;
		var ori_display = tip.style.display;
		var ori_html = tip.innerHTML;
		tip.style.top = '-9999px';
		tip.style.left = '-9999px';
		tip.innerHTML = html;
		tip.style.display = 'block';
		var tw = tip.clientWidth;
		var th = tip.clientHeight;
		tip.style.top = ori_top;
		tip.style.left = ori_left;
		tip.innerHTML = ori_html;
		tip.style.display = ori_display;
		return {
			x : PageSize.getScrollLeft() + (PageSize.getWidth() - tw)/2,
			y : PageSize.getScrollTop() +(PageSize.getHeight() - th)/2
			};
		}
	
	function _adjust(){
		
		}
		
	//设置初始参数
	this.ini_set = function(name,value){
		_ini.set(name,value);
		};
	
	/*
	 * TODO : showBeside和showCenter中的代码重用问题
	 */
	
	//在element旁边显示Tip层
	this.showBeside = function(element,argvs){
		var arg = Arg2Arr(arguments);
		var el = arg.shift();
		var opt = {offsetX : 0,offsetY : 0};
		if(typeof(arg[0]) == 'object'){
			opt = arg.shift();
			}
		var html = [];
		for(var i=0,ilen=arg.length;i<ilen;i++){
			html.push(arg[i]);
			}
		html = html.join('');
		var pos = _getBesidePos(element);
		_show(pos,html);
		return false;
		};
	
	//居中显示Tip层
	this.showCenter = function(src,argvs){
		var arg = Arg2Arr(arguments);
		var src = arg.shift();
		var opt = {offsetX : 0,offsetY : 0};
		if(typeof(arg[0]) == 'object'){
			opt = arg.shift();
			}
		var html = [];
		for(var i=0,ilen=arg.length;i<ilen;i++){
			html.push(arg[i]);
			}
		html = html.join('');
		var pos = _getCenterPos(html);
		_show(pos,html);
		//_adjust('center');
		return false;		
		}
	
	//隐藏Tip层
	this.hide = function(){
		_hide();
		return false;
		};
	};

//组织标题 html
Tip.title = function(title){
	var ret = ['<h5 class="fc-red tc">',title,'</h5>'].join('');
	return ret;
	};

//组织内容 html
Tip.tip = function(tip){
	var ret = ['<p class="tc">',tip,'</p>'].join('');
	return ret;
	};
	
//组织关闭按钮 html	
Tip.close = function(){
	var ret = ['<p class="fr fc-gray">',
		'<a href="#" onclick="return ',PUBLISHNAME,'.hide();">[关闭]</a>',
		'</p>'].join('');
	return ret;
	};

Tip.iframe = function(src){
	var ret = [
		'<iframe width="100%" height="90%" src=',src,
		' frameborder="0" scrolling="no"',
		'></iframe>'
		].join('');
	return ret;	
	};

//发布命名空间
window[PUBLISHNAME] = Tip;	
})();
