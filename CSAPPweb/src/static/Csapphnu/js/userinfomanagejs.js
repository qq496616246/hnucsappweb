/**
 * Created by scw on 2017/7/27.
 */
$(function () {
    /*为条目设置点击事件
    $('#accordion li').click(function() {
			$(this).animate({left:$(this).index()*20});

			$(this).prevAll().each(function(){
				$(this).animate({left:$(this).index()*20});
			});

			$(this).nextAll().each(function(){
				$(this).animate({left:(327-(3-$(this).index())*20)});
			});
		});*/

    //动态调整图片轮播的位置(这个用来进行屏幕适配功能)
    var windowSize = $(window).width();
    if(windowSize > 768 ){  //当是用PC进行浏览页面的时候，如果是手机的时候，已经是居中显示
        $('#pictureposition').attr('align','center');  //将轮播图居中
    }

    //为图片设置点击事件（三张图）
    //个人信息模块
    $('#imgselete1').click(function () {
       window.location = '/modifyuserinfo/'
    })
    //学生课程分组(需要判断权限)
    $('#imgselete2').click(function () {
          //用ajax异步刷新页面
        $.ajax({
            url:'/usertypeverification/',
            async:true,
            type:"GET",
            data:{'currentmodeltype': 'grounpmodel'},
            success:function (data) {
                if(data.result == 'success'){  //权限验证成功
                     window.location = '/studentgrouping/'  ;
                     alert("欢迎您访问该模块！")
                }
                else{
                    alert("对不起，权限不够，您无法访问该模块")
                }
            },
            error:function () {
                alert("网络不稳定，请确认！")
            },
            dataType:"json"
        });

    })
    //助教信息管理(需要判断权限)
    $('#imgselete3').click(function () {
        //用ajax异步刷新页面
        $.ajax({
            url: '/usertypeverification/',
            async: true,
            type: "GET",
            data: {'currentmodeltype': 'assistantmange'},
            success: function (data) {
                if (data.result == 'success') {  //权限验证成功
                    window.location = '/assistantmanage/';
                    alert("欢迎您访问该模块！")
                }
                else {
                    alert("对不起，权限不够，您无法访问该模块")
                }
            },
            error: function () {
                alert("网络不稳定，请确认！")
            },
            dataType: "json"
        });
    })

})