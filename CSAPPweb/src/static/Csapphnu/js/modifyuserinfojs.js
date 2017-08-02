/**
 * Created by scw on 2017/7/27.
 */
$(function () {
	var error_password = true;   //密码
	var error_check_password = true; //确定密码
	var error_tel = true;  //联系方式

    //为input输入框添加移除焦点事件
    $('#loginuserpassword').blur(function () {
        checkpassword();  //检查密码是否符合规则
    })
    $('#loginaginpassword').blur(function () {
        checkagainpassword();  //检查确认密码是否符合规则
    })
    $('#logintelphone').blur(function () {
        checktelnumber();  //检查联系方式是否符合规则
    })

    //为input输入框添加获取焦点处理事件
     $('#loginuserpassword').focus(function () {
         $(this).next().hide();
         $(this).next().next().hide();
    })
    $('#loginaginpassword').focus(function () {
        $(this).next().hide();
        $(this).next().next().hide();
    })
    $('#logintelphone').focus(function () {
        $(this).next().hide();
        $(this).next().next().hide();
    })
    //密码检查
    function checkpassword() {
       var val =  $('#loginuserpassword').val();
       var reg = /^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,12}$/;
		if(val==''){
			$('#loginuserpassword').next().next().hide();
			$('#loginuserpassword').next().show();
			error_password = true;
			return;
		}
		if(reg.test(val))
		{
			$('#loginuserpassword').next().hide();
			$('#loginuserpassword').next().next().show();
			error_password = false;
		}
		else
		{
			$('#loginuserpassword').next().next().hide();
			$('#loginuserpassword').next().show();
			error_password = true;
		}
    }
    //密码判断是否一致（两次输入）
    function checkagainpassword() {
        var pass = $('#loginuserpassword').val();
		var cpass = $('#loginaginpassword').val();

		if(pass!=cpass)
		{
			$('#loginaginpassword').next().next().hide();
			$('#loginaginpassword').next().show();
			error_check_password = true;
		}
		else
		{
			$('#loginaginpassword').next().hide();
			$('#loginaginpassword').next().next().show();
			error_check_password = false;
		}
		if(cpass == ''){
			$('#loginaginpassword').next().next().hide();
			$('#loginaginpassword').next().show();
			error_check_password = true;
		}
    }

    //联系方式判断
    function checktelnumber() {
		var telval = $('#logintelphone').val();
		var reg = /^1[34578]\d{9}$/;
		if(reg.test(telval)){  //匹配正确
			$('#logintelphone').next().hide();
			$('#logintelphone').next().next().show();
			error_tel = false;
		}
		else{
			$('#logintelphone').next().next().hide();
			$('#logintelphone').next().show();
			error_tel = true;
		}
    }

    //提交所有信息，当所填的所有信息都符合规范的时候
	$('.reg_form').submit(function () {
		checkpassword();
		checkagainpassword();
		checktelnumber()
		if(error_password==false && error_check_password==false && error_tel==false){  //表示都符合规范
			return true ; //进行提交
		}
		else{
			return false;
		}
    })
})