/**
 * Created by scw on 2017/8/2.
 */
$(function () {
    //设置鼠标到table中的行的显示效果的改变
    $('.userinfoshowtab tr').mouseenter(function() {
         $(this).css('background-color','#ffff66');
    })
    $('.userinfoshowtab tr').mouseout(function() {
         $(this).css('background-color','#d4e3e5');
    })

    //显示所有学生信息
    $('#showallstudentinfo').click(function () {
        $('#layoutcenter>div').hide();  //将所有的table隐藏
        $('#tableeasyuishowinfo').show();  //显示对应栏目的table
        $('#tableeasyuishowinfo').tabs('select', 0);
    })
    //显示老师信息
    $('#showallteacherinfo').click(function () {
        $('#layoutcenter>div').hide();  //将所有的table隐藏
        $('#tableeasyuishowinfo').show();  //显示对应栏目的table
        $('#tableeasyuishowinfo').tabs('select', 1);
    })
    //显示助教信息
    $('#showallassistantinfo').click(function () {
        $('#layoutcenter>div').hide();  //将所有的table隐藏
        $('#tableeasyuishowinfo').show();  //显示对应栏目的table
        $('#tableeasyuishowinfo').tabs('select', 2);
    })

    //单个添加学生，老师，助教信息模块功能
    $('#addstudentinfosigle').click(function () {
        $('#layoutcenter>div').hide();  //将所有的table隐藏
        $('#tableeasyuiaddsigle').show();  //显示对应栏目的table
        $('#tableeasyuiaddsigle').tabs('select', 0);
    })
    //单个验证老师添加信息
    $('#addteacherinfosigle').click(function () {
        $('#layoutcenter>div').hide();
        $('#tableeasyuiaddsigle').show();
        $('#tableeasyuiaddsigle').tabs('select', 1);
    })
    //单个验证助教添加
    $('#addassistantsigle').click(function () {
        $('#layoutcenter>div').hide();
        $('#tableeasyuiaddsigle').show();
        $('#tableeasyuiaddsigle').tabs('select', 2);
    })


    //批量添加学生，老师，助教信息
    $('#addstudentinfomore').click(function () {
        $('#layoutcenter>div').hide();
        $('#tableeasyuiaddmore').show();
        $('#tableeasyuiaddmore').tabs('select', 0);
    })
    //批量验证老师信息
    $('#addsteacherinfomore').click(function () {
        $('#layoutcenter>div').hide();
        $('#tableeasyuiaddmore').show();
        $('#tableeasyuiaddmore').tabs('select', 1);
    })
    //批量验证助教信息
    $('#addassistantmore').click(function () {
        $('#layoutcenter>div').hide();
        $('#tableeasyuiaddmore').show();
        $('#tableeasyuiaddmore').tabs('select', 2);
    })

    //单个添加信息表单的验证功能
    //学生验证
    $('#regesterstu').click(function () {
        var number = $('#usernumber').val().trim();
        var name = $('#username').val().trim();
        var stuclass = $('#userclass').val().trim();
        if(name ==""||number == ""|| stuclass==""){
            alert("所填信息不能为空!")
            return;
        }
        $('#siglestudentregester').attr({'action':'/systemmanagement/regesterinfo/'});
        $('#siglestudentregester').submit();
    })
    //助教验证
    $('#regesterass').click(function () {
        var number = $('#usernumber2').val().trim();
        var name = $('#username2').val().trim();
        var stuclass = $('#userclass2').val().trim();
        if(name ==""||number == ""|| stuclass==""){
            alert("所填信息不能为空!")
            return;
        }
        $('#sigleassistantregester').attr({'action':'/systemmanagement/regesterinfo/'});
        $('#sigleassistantregester').submit();
    })
    //老师验证
    $('#regestertea').click(function () {
        var number = $('#usernumber3').val().trim();
        var name = $('#username3').val().trim();
        var stuclass = $('#userclass3').val().trim();
        if(name ==""||number == ""|| stuclass==""){
            alert("所填信息不能为空!")
            return;
        }
        $('#sigleteacherregester').attr({'action':'/systemmanagement/regesterinfo/'});
        $('#sigleteacherregester').submit();
    })


    //学生的分页处理
    $('#studentinfopage').pagination({
        //选择新页面的时候触发pageNumber:选择的页面，pageSize:选择的每页的大小
        onSelectPage: function (pageNumber, pageSize) {
            $(this).pagination('loading');
            $.ajax({
                url:'/systemmanagement/changepagenumber/',
                async:false, //这里不要异步，因为异步的话，如果数据多了，就导致数据显示过慢
                data:{"pagesize":pageSize ,"pagenumber":pageNumber,"type":'1'}, //页面大小,页面索引数和请求的数据类型
                type:"GET",
                success:function (data) {  //请求成功
                    //1:先将之前的表格中的数据进行清除
                    $('#studentbodyinfo').empty();
                    //2:循环拼接需要的类型数据
                    $.each(data.data,function (i , m) {
                        var $std = $('<tr><td>'+m.uid +'</td><td>'+m.name+'</td><td>'+m.student_class_name+'</td>' +
                            '<td>'+m.permission+'</td><td>'+m.contact+'</td><td><a href="#" id="updatatableinfostu" class="'+ m.uid +'">更新</a></td><td><a href="#" id="updatatableinfostu" class="'+m.uid+'">删除</a></td></tr>');
                        //3.将表格内容添加到对应的table中
                        $std.appendTo('#studentbodyinfo');
                    })
                    $('.userinfoshowtab tr').mouseenter(function () {
                        $(this).css('background-color', '#ffff66');
                    })
                    $('.userinfoshowtab tr').mouseout(function () {
                        $(this).css('background-color', '#d4e3e5');
                    })
                },
                errors:function () {
                    alert("信息加载失败，请稍后再试哦！")
                },
                dataType:"json"
            });
            $(this).pagination('loaded');
	    },
        //更改页面大小的时候触发的函数:pageSize:更改的页面大小
	    onChangePageSize:function (pageSize) {
            $.ajax({
                url:'/systemmanagement/changepagesize/',
                async:false, //这里不要异步，因为异步的话，如果数据多了，就导致数据显示过慢
                data:{"pagesize":pageSize ,"type":'1'}, //页面大小和请求的数据类型
                type:"GET",
                success:function (data) {  //请求成功
                    //1:先将之前的表格中的数据进行清除
                    $('#studentbodyinfo').empty();
                    //2:循环拼接需要的类型数据
                    $.each(data.data,function (i , m) {
                        var $std = $('<tr><td>'+m.uid +'</td><td>'+m.name+'</td><td>'+m.student_class_name+'</td>' +
                            '<td>'+m.permission+'</td><td>'+m.contact+'</td><td><a href="#" id="updatatableinfostu" class="'+ m.uid +'">更新</a></td><td><a href="#" id="updatatableinfostu" class="'+m.uid+'">删除</a></td></tr>');
                        //3.将表格内容添加到对应的table中
                        $std.appendTo('#studentbodyinfo');
                    })
                    $('.userinfoshowtab tr').mouseenter(function () {
                        $(this).css('background-color', '#ffff66');
                    })
                    $('.userinfoshowtab tr').mouseout(function () {
                        $(this).css('background-color', '#d4e3e5');
                    })
                },
                errors:function () {
                    alert("信息加载失败，请稍后再试哦！")
                },
                dataType:"json"
            });
        }
    })
    //老师的分页处理
    $('#teacherinfopage').pagination({
        //选择新页面的时候触发pageNumber:选择的页面，pageSize:选择的每页的大小
        onSelectPage: function (pageNumber, pageSize) {
            $(this).pagination('loading');
            $.ajax({
                url:'/systemmanagement/changepagenumber/',
                async:false, //这里不要异步，因为异步的话，如果数据多了，就导致数据显示过慢
                data:{"pagesize":pageSize ,"pagenumber":pageNumber,"type":'3'}, //页面大小,页面索引数和请求的数据类型
                type:"GET",
                success:function (data) {  //请求成功
                    //1:先将之前的表格中的数据进行清除
                    $('#teacherbodyinfo').empty();
                    //2:循环拼接需要的类型数据
                    $.each(data.data,function (i , m) {
                        var $std = $('<tr><td>'+m.uid +'</td><td>'+m.name+'</td><td>'+m.teacher_class_name+'</td>' +
                            '<td>'+m.permission+'</td><td>'+m.contact+'</td><td><a href="#" id="updatatableinfotea" class="'+ m.uid +'">更新</a></td><td><a href="#" id="updatatableinfotea" class="'+m.uid+'">删除</a></td></tr>');
                        //3.将表格内容添加到对应的table中
                        $std.appendTo('#teacherbodyinfo');
                    })
                    $('.userinfoshowtab tr').mouseenter(function () {
                        $(this).css('background-color', '#ffff66');
                    })
                    $('.userinfoshowtab tr').mouseout(function () {
                        $(this).css('background-color', '#d4e3e5');
                    })
                },
                errors:function () {
                    alert("信息加载失败，请稍后再试哦！")
                },
                dataType:"json"
            });
            $(this).pagination('loaded');
	    },
        //更改页面大小的时候触发的函数:pageSize:更改的页面大小
	    onChangePageSize:function (pageSize) {
            $.ajax({
                url:'/systemmanagement/changepagesize/',
                async:false, //这里不要异步，因为异步的话，如果数据多了，就导致数据显示过慢
                data:{"pagesize":pageSize ,"type":'1'}, //页面大小和请求的数据类型
                type:"GET",
                success:function (data) {  //请求成功
                    //1:先将之前的表格中的数据进行清除
                    $('#teacherbodyinfo').empty();
                    //2:循环拼接需要的类型数据
                    $.each(data.data,function (i , m) {
                        var $std = $('<tr><td>'+m.uid +'</td><td>'+m.name+'</td><td>'+m.teacher_class_name+'</td>' +
                            '<td>'+m.permission+'</td><td>'+m.contact+'</td><td><a href="#" id="updatatableinfotea" class="'+ m.uid +'">更新</a></td><td><a href="#" id="updatatableinfotea" class="'+m.uid+'">删除</a></td></tr>');
                        //3.将表格内容添加到对应的table中
                        $std.appendTo('#teacherbodyinfo');
                    })
                    //重新绑定鼠标移动到table的显示css，因为上面清空了之前的，那么就没有了
                    $('.userinfoshowtab tr').mouseenter(function () {
                        $(this).css('background-color', '#ffff66');
                    })
                    $('.userinfoshowtab tr').mouseout(function () {
                        $(this).css('background-color', '#d4e3e5');
                    })
                },
                errors:function () {
                    alert("信息加载失败，请稍后再试哦！")
                },
                dataType:"json"
            });
        }
    })
    //助教的分页处理
    $('#assistantinfopage').pagination({
        //选择新页面的时候触发pageNumber:选择的页面，pageSize:选择的每页的大小
        onSelectPage: function (pageNumber, pageSize) {
            $(this).pagination('loading');
            $.ajax({
                url:'/systemmanagement/changepagenumber/',
                async:false, //这里不要异步，因为异步的话，如果数据多了，就导致数据显示过慢
                data:{"pagesize":pageSize ,"pagenumber":pageNumber,"type":'2'}, //页面大小,页面索引数和请求的数据类型
                type:"GET",
                success:function (data) {  //请求成功
                    //1:先将之前的表格中的数据进行清除
                    $('#assistantbodyinfo').empty();
                    //2:循环拼接需要的类型数据
                    $.each(data.data,function (i , m) {
                        var $std = $('<tr><td>'+m.uid +'</td><td>'+m.name+'</td><td>'+m.student_class_name+'</td>' +
                            '<td>'+m.permission+'</td><td>'+m.contact+'</td><td><a href="#" id="updatatableinfoass" class="'+ m.uid +'">更新</a></td><td><a href="#" id="updatatableinfoass" class="'+m.uid+'">删除</a></td></tr>');
                        //3.将表格内容添加到对应的table中
                        $std.appendTo('#assistantbodyinfo');
                    })
                    $('.userinfoshowtab tr').mouseenter(function () {
                        $(this).css('background-color', '#ffff66');
                    })
                    $('.userinfoshowtab tr').mouseout(function () {
                        $(this).css('background-color', '#d4e3e5');
                    })
                },
                errors:function () {
                    alert("信息加载失败，请稍后再试哦！")
                },
                dataType:"json"
            });
            $(this).pagination('loaded');
	    },
        //更改页面大小的时候触发的函数:pageSize:更改的页面大小
	    onChangePageSize:function (pageSize) {
            $.ajax({
                url:'/systemmanagement/changepagesize/',
                async:false, //这里不要异步，因为异步的话，如果数据多了，就导致数据显示过慢
                data:{"pagesize":pageSize ,"type":'1'}, //页面大小和请求的数据类型
                type:"GET",
                success:function (data) {  //请求成功
                    //1:先将之前的表格中的数据进行清除
                    $('#teacherbodyinfo').empty();
                    //2:循环拼接需要的类型数据
                    $.each(data.data,function (i , m) {
                        var $std = $('<tr><td>'+m.uid +'</td><td>'+m.name+'</td><td>'+m.student_class_name+'</td>' +
                            '<td>'+m.permission+'</td><td>'+m.contact+'</td><td><a href="#" id="updatatableinfoass" class="'+ m.uid +'">更新</a></td><td><a href="#" id="updatatableinfoass" class="'+m.uid+'">删除</a></td></tr>');
                        //3.将表格内容添加到对应的table中
                        $std.appendTo('#teacherbodyinfo');
                    })
                    $('.userinfoshowtab tr').mouseenter(function () {
                        $(this).css('background-color', '#ffff66');
                    })
                    $('.userinfoshowtab tr').mouseout(function () {
                        $(this).css('background-color', '#d4e3e5');
                    })
                },
                errors:function () {
                    alert("信息加载失败，请稍后再试哦！")
                },
                dataType:"json"
            });
        }
    })


    //点击学生table中的更新链接，进行更新操作
    $(document).on('click','#updatatableinfostu',function () {
        alert("我是学生更新！")
    })
    //点击老师table中的更新链接，进行更新操作
     $(document).on('click','#updatatableinfotea',function () {
        alert("我是老师更新！")
    })
    //点击助教table中的更新链接，进行更新操作
     $(document).on('click','#updatatableinfoass',function () {
        alert("我是助教更新！")
    })

    //点击学生table中的删除链接，进行删除操作
     $(document).on('click','#deletetableinfostu',function () {
        alert("我是学生删除！")
    })
    //点击老师table中的删除链接，进行删除操作
     $(document).on('click','#deletetableinfotea',function () {
        alert("我是老师删除！")
    })
    //点击助教table中的删除链接，进行删除操作
     $(document).on('click','#deletetableinfoass',function () {
        alert("我是助教删除！")
    })

})