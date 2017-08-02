/**
 * Created by scw on 2017/7/22.
 */
    //点击温馨提示的超链
    function alertmessage() {
        alert("本页面主要的功能为：（1）助教信息显示（2）添加助教。其中它们可以通过左右滑动表格来显示内容哦！");
    }

    //全选和全不选的控制
    function seleteIsAll(flag) {
  		var checkselecte = document.getElementsByName("addismessage");
  		for(var i = 0 ;i<checkselecte.length;i++){
  			checkselecte[i].checked = flag;
  	    }
    }

