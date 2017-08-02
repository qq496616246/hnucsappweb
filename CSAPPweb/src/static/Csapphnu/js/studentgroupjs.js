/**
 * Created by scw on 2017/7/24.
 */

$(function () {
    //拿到点击切换班级的内容，即要切换的班级
    var changeClassValue = '';
    $(document).on('click' , '#changeClassList' , function () {
        changeClassValue = $(this).attr('name');
    })

    //点击显示不显示，来控制分组的显示效果
    $('#showgrounpstudentinfo').click(function () {
        $('#studentgrounp-table-tbody').toggle();
    })

    //设置切换班级的模态框点击确定的事件
    $('#okselectbtn').click(function () {
        //传送点击的班级的信息过去后台，来获取内容。
        window.location = '/studentgrouping/?classnumber='+ changeClassValue;
        //用ajax异步刷新页面
        // $.ajax({
        //     url:'/studentclassandname/',
        //     async:true,
        //     type:"GET",
        //     data:{'classnumber': changeClassValue},
        //     success:function (data) {
        //         alert(data.result)
        //     },
        //     error:function () {
        //         alert("选择失败！请重新选择!（保持网络稳定）")
        //     },
        //     dataType:"json"
        // });
    })


    //点击输入分组数目的确定按钮的监听，实现下拉框生成对应的分组数目
    $('#okstudentmaxgroupnumber').click(function () {
        //获取输入框中填写的数值
        var valueinput = $('.input-groupnumber').val();
        if(valueinput == ''){
            alert('请输入学生分组的最大数目');
            return;
        }
        if(parseInt(valueinput) > 12 ) {
            alert('学生分组的最大数目不能超过12组!');
            return;
        }

        //进行判断是否是数字
        var reg = /^[0-9]*$/;
        if(!reg.test(valueinput)){
            alert('请输入数字!');
            return;
        }
        //判断成功后，自动生成下拉列表中对应的数值
        //先清空之前存在的内容
        selectvalue = 1; //默认第一个选择
        $('#select-option').html('');
        $('#student-grounp-detail').html('');
        for(var i = 0 ; i <parseInt(valueinput) ; i++){
            //添加下拉框的内容
            var $soption = $('<option value="'+ (i+1) +'">小组'+ (i+1) +'</option>');
            $soption.appendTo('#select-option');
             //添加相应小组信息框
            var $sli = $('<li><a href="#" class="grounp1">小组'+ (i+1) +'</a><ul  id="grounp'+ (i+1)+'"></ul></li>');
            $sli.appendTo('#student-grounp-detail');
        }
        //将学生分组显示中，默认显示第一个，所以需要加个class属性
        $('#student-grounp-detail li').first().children("ul:eq(0)").addClass('current');
        alert("小组创建信息完成，请进行分组操作!");
    })

    /**
     * scw
     * function:获取选择框选中的小组信息
     * @type {number}
     */
    var selectvalue = 0; //选择框选中的内容的值，默认不给，方便判断是否有进行选择
    //监听选择下拉框中的内容的时候的监听，用来提示给用户将要进行的操作
    $('#select-option').change(function () {
        selectvalue =  $(this).children('option:selected').val(); //选择框选中的内容
    })


    /**
     * 分组详情的展开显示效果，点击的监听，需要通过事件委托来实现
     */
    $('#student-grounp-detail').on('click' ,'.grounp1',function () {
          $(this).next().slideDown().parent().siblings().children('ul').slideUp();
    } )


    /**
     * scw
     * function:学生名单中的选择的监听事件
     * 1:判断是否有选择进行分组的序号
     * 2:获取点击的学生按钮的内容
     * 3:先隐藏点击的那个学生按钮
     * 4：将点击按钮的学生加入到对应要进行分组的小组中（这个对应小组的值在其他的地方获取了，只要判断是否为空就行，否则不进行操作，而提示）
     */
    $('#student-select-btn').on('click' , '#studentbtn' , function () {
        //判断要进行分组的序号是否为空，为空表示还没选择小组序号
         if(selectvalue == 0){  //表示还没进行选择学生要进行分组的序号
             alert("请选择要分组的序号，分组序号不能为空！");
          }
          else{
             var $clickStuNumber = $(this).attr('value'); //这里是得到点击按钮学生的学号，这是主键
             var $clickStuName = $(this).text();  //这里是得到点击学生的名字，主要是用来进行显示的
             $(this).hide();    //隐藏点击的那个学生按钮
             //拿取一起存了多少个数据了，方便进行输入框中的name赋值
             var countnumber = $('#savecountnumber').val();
             //转为整型
             var countnumberInter = parseInt(countnumber);
             //个数+1
             countnumberInter += 1;
             //再把个数的值赋值回去，下次使用
             document.getElementById('savecountnumber').value = countnumberInter;
             //将内容添加到分组详情中
             var $addsli = $('<li><input type="text" readonly id="inputStudentitem" name="submitcontent'+ countnumberInter +'" value="'+selectvalue+'-'+$clickStuName+'-'+$clickStuNumber+'">' +
                 '<button data-toggle="modal"  data-target="#modal03" id="-'+$clickStuNumber +'" name="'+$clickStuNumber+'" class="deletebtn" value="'+ countnumberInter +'">删除</button></li>')
             //得到需要加入到对应的分组的ul值
             var $ulvalue = '#grounp'+ selectvalue ;
             $addsli.appendTo( $ulvalue );
             alert('分组成功!')
         }
    })

    /**
     * 点击提交分组情况的确定按钮的监听事件
     */
    $('#oksubmitBtn').click(function () {
        //判断是否有分组信息
        if(selectvalue == 0){ //表示没有分组信息
            alert("没有分组信息，无法进行分组操作！")
        }
        else {
            //判断分组名单中是否有添加人数
            //判断分组的ul中的子元素li的子元素ul中的子元素的个数即表示添加了多少个
            var countnumber = $('#student-grounp-detail').children('li').children('ul').children('li').length;
            if(countnumber == 0){  //表示没有添加人数
                alert("没有分组名单信息，无法进行分组，请确认！")
                return;
            }
            else {
                //赋值该次选择的班级
                if (changeClassValue == '') { //表示是用第一次进来的班级，而没有进行班级切换，则不需要更改班级的提交内容

                }
                else {
                    //进行了班级切换，那么就把新的班级信息进行赋值，便于form传过来
                    document.getElementById('studentSelectClass').value = changeClassValue;
                }
                //进行页面跳转
                $('#submitgrounp-form').attr({action: '/studentgroupindodb/'});
                $('#submitgrounp-form').submit();
            }
        }
    })


     /**
     * scw
     * function：点击删除分组信息的监听，进行删除操作
      * 事件委托实现
     */
     var deletbtnName = '';
     var removelibtnId = '';
     var removerlibtnValue = '';
    $(document).on('click','.deletebtn',function (){
        deletbtnName = $(this).attr('name');  //得到点击按钮的name值
        removelibtnId = $(this).attr('id');  //得到点击按钮的id值
        removerlibtnValue = $(this).attr('value');  //得到点击按钮的value值（表示的是第几个按钮）
        return false;     //这个一定要，因为来防止冒泡事件的产生
    })


    /**
     * 点击确定删除学生分组信息的监听
     * (1):恢复点击的按钮的学生的名字
     * (2)：将点击的信息把输入框对应的位置进行删除
     */
    $('#deletesubmitBtn').click(function () {
        //恢复点击删除的学生信息的按钮
        var $sbtnaddname = '.'+deletbtnName;
        $($sbtnaddname).show();  //这个按钮在之前是hide了的，所以现在show出来就可以了
        //下面的显示方法也可以，只是麻烦了点，
        // var $sbtn =$('<button id="studentbtn" value="{{ studentinfo.student_number }}">'+ deletbtnName+'</button>')
        // $sbtn.appendTo($('#addstudentinfodiv'));

        //将对应点击的删除按钮的输入框的父元素进行删除，从而达到删除效果
        var $sli = '#'+removelibtnId;  //拿到点击按钮的ID来进行操作
        $($sli).parent('li').remove();

        //将删除的按钮的value值进行记录
        var getValue = $('#savedeletenumber').val();  //取之前的值，下面进行拼接为0-N-N的形式
        document.getElementById('savedeletenumber').value = getValue +"-"+removerlibtnValue ;
        alert("删除成功！")
    })

})