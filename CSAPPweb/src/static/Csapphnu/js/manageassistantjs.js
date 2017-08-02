/**
 * Created by scw on 2017/7/22.
 */

$(function() {

    /**
     * 自动生成显示助教信息表格中的编号（这种方法很好）
     */
    var strlength = $('#assistantshow-table-tbody tr').length;
    for(var i= 0 ; i < strlength ; i++){
        $('#assistantshow-table-tbody tr:eq('+i+') td:first').text(i+1);
    }

    var deletNumber = 0;   //存储删除人的学号，方便进行数据传输
    //这里通过事件委托来实现，否则无法监听到其他的点击事件
    $(document).on('click','#deletbtnlianjie',function () {
        deletNumber = $(this).attr('name');  //获取点击删除的对应数据的学号
    })

    //当点击更新的时候，将之前的获取进行存储显示出来
    $(document).on('click','#updatabtnlianjie',function () {
        var updataNumber = document.getElementById('updataNumber');
        var updataName = document.getElementById('updataName');
        var updataClass = document.getElementById('updataClass');
        var content = $(this).attr('name');
        //将数据进行分割(因为之前使用@作为分割符号)
        arrstr = content.split('@');
        updataNumber.value = arrstr[0];  //获取点击更新的学号，姓名，和班级
        updataName.value = arrstr[1];  //获取点击更新的学号，姓名，和班级
        updataClass.value = arrstr[2];  //获取点击更新的学号，姓名，和班级
    })

    //点击按钮，隐藏助教信息显示
    $('#showassistantbtn').click(function () {
        $('#assistantshow-table-tbody').fadeToggle();
    })


    //点击按钮，增加添加助教信息的表格，方便一次添加多条信息
    $('#addassistanttablenumber').click(function () {
        var $str = $('<tr>');//添加一行
        var $content = $('#tablecountid'); //得到目前table条目的个数
        $number = parseInt($content.val()) + 1;

        var currentTeacherClass = new Array();  //当前老师所带的班级信息
        //ajax请求该老师对应所带的班级信息
        $.ajax({
             url:'/requestclassnumber/',
             async:false,  //这里要变为同步，一定要，因为如果用异步请求，这会导致数据还没过来页面已经加载完了
             data:{'message':'1'},
             type:'GET',
             success:function (data) {
                 //判断请求的结果
                if(data.requestResult == 'success'){   //成功
                    for(var i = 0 ;i < data.classNumberData.length ; i++){
                        currentTeacherClass[i] = data.classNumberData[i];
                    }
                }
                else{
                    alert("没有访问到对应的班级信息！")
                }
             },
             error:function () {
                 alert("网络不稳，请稍后再试！")
             },
             dataType:"json"
         });
        //拼接动态条目的内容
        var contentInfo = '<td><input type="checkbox" name="addismessage" value="'+$number+'"></td> ' +
             '<td><input type="text" name="assistantNumber'+$number+'" id="assistantNumber'+$number+'"></td>' +
             '<td><input type="text" name="assistantName'+$number+'" id="assistantName'+$number+'"></td>' +
             '<td>';
        var temp ='';  //select选择框的内容
        for(var i = 0 ;i <currentTeacherClass.length ; i++){
            var optionscon = '<option value="'+currentTeacherClass[i] +'">'+ currentTeacherClass[i]+'</option>';
            temp += optionscon;
        }
        var selectInfo = '<select name="selectClass'+ $number +'">' + temp +'</select>'; //拼接选择框中的html内容
        contentInfo = contentInfo + selectInfo + '</td>' + //拼接所有要显示的htnl内容
             '<td> <a href="#" data-toggle="modal"  data-target="#modal03"><span class="glyphicon glyphicon-ok"></span>添加</a> </td></tr>';

        //拼接增加行的内容
        //  var content = '<td><input type="checkbox" name="addismessage" value="'+$number+'"></td> ' +
        //      '<td><input type="text" name="assistantNumber'+$number+'" id="assistantNumber'+$number+'"></td>' +
        //      '<td><input type="text" name="assistantName'+$number+'" id="assistantName'+$number+'"></td>' +
        //      '<td><input type="text" name="assistantClass'+$number+'" id="assistantClass'+$number+'"></td>' +
        //      '<td> <a href="#" data-toggle="modal"  data-target="#modal03"><span class="glyphicon glyphicon-ok"></span>添加</a> </td>';
        //var $std = $str.html(content);  //添加元素，这里是用所有的输入框的形式，后面进行了修改为了班级是选择框来进行

        var $std = $str.html(contentInfo); //添加元素标签到对应的位置
        $std.appendTo($('#assistantaddd-table-tbody'));
        document.getElementById('tablecountid').value = $number;
        alert("添加条目成功!");
    })

    //模态框中的添加确定的事件
    $('#okaddbtn').click(function () {
        var deleteselecte = document.getElementsByName("addismessage");
    	 //判断哪些被选中
    	 var str = "";
    	 var number = 0; //删除的个数
    	 for(var i = 0 ; i <deleteselecte.length ;i++){
    		 if(deleteselecte[i].checked == true){
    		     //判断选择的内容中是否有填写内容是不符合规范的（比如空）
                var judgeresult = jugdeInputContent( i+1 ); //因为循环是从0开始，而标签得下标自己是从1开始设置
    		 	if(judgeresult == false){ //表示存在不符合规范的内容，则不进行后面的操作了
                    return;
                }
                str = str + deleteselecte[i].value +",";
    		 	number++;
    		 }
    	 }
    	 if(number >=1){
    		//将点击的索引号进行拼接，方便在后台进行处理获取表单提交的数据，进行页面表单提交跳转
             document.getElementById('tableinfoindex').value = str;  //封装好了选中的索引值
             $('#addtable-form').attr({action: '/addassistantinfodb/'});
             $('#addtable-form').submit();
    	 }
    	 else{
    		 alert("添加的个数不能少于一个");
    	 }
    })
    //删除按钮确定的处理
    $('#okdeletebtn').click(function () {
        deleteOption();
    })
    //更新按钮确定的处理
    $('#okupdatabtn').click(function () {
        updataOption();
    })


    /**
     * scw
     * funciton:提交信息的时候，判断输入框中的内容是否符合规范
     * @param index:多选框的下标（从1开始自己设置了）
     */
    function jugdeInputContent( index) {
        //拿到助教学号输入框内容
        var strNumber = '#assistantNumber' + index;
        var strName = '#assistantName' + index;
        var strclass = '#assistantClass' + index;
        var assistansNumber = $(strNumber).val();
        var assistansName = $(strName).val();
        var assistansClass = $(strclass).val();
        //进行判断是否符合规范
        if(assistansNumber == ""){
            alert("其中选择条目("+index+")中,存在填写助教学号不符合规范(注：①不能为空②需要为汉字)，请确认！")
            return false;
        }
        if(assistansName == ""){
            alert("其中选择条目("+index+")中,存在填写助教姓名不符合规范(注：①不能为空②需要为汉字)，请确认！")
            return false;
        }
        if(assistansClass == ""){
            alert("其中选择条目("+index+")中,存在填写助教班级不符合规范(注：①不能为空②需要为汉字)，请确认！")
            return false;
        }
    }

    /**
     * scw
     * function：执行删除操作
     *
     */
    function deleteOption() {
        //进行页面跳转
        window.location = '/deletassistantinfodb/?deletenumber='+ deletNumber;
    }

    /**
     * scw
     * function：进行更新操作的处理
     */
    function updataOption() {
        //拿到更新框中的输入的内容，进行判断是否符合规范
        var stunumber = $('#updataNumber').val();
        var stuname = $('#updataName').val();
        var stuclass = $('#updataClass').val();
        var isSuccess = true;
        //因为学号不可以更新，所以不需要判断了，在添加的时候已经进行了判断
        if(stuname ==''){
            alert("填写的姓名不规范，请确认！");
            isSuccess = false;
        }
        if(stuclass == ''){
            alert("填写的班级不规范，请确认！");
            isSuccess = false;
        }
        //判断是否进行跳转
        if(isSuccess == true){
             $('#updataInfo-form').attr( {action : '/updataassistantinfodb/'});
             $('#updataInfo-form').submit();
        }
    }
})

