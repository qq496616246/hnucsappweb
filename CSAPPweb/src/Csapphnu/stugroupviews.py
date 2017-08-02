from django.shortcuts import render
from django.http import *
from .models import *
from django.template import *
from django.core.urlresolvers import reverse
import json
from django.core import serializers

#显示分组情况
def studentgrouping(request):
    # 首先判断是否是属于登录中的用户并且是否有足够的权限（老师和助教），否则跳转到登录页面中
    isOnlineUser = request.session.get('uid');
    isEnoughtPermission = request.session.get('permission');
    if isOnlineUser == None:  # 表示不是登录中的用户
        return HttpResponseRedirect('/index/');
    else:
        if isEnoughtPermission >= 2: #表示是助教和老师等级权限
            userType = request.session.get('permission'); #这个权限从session中直接获取即可
            username = request.session.get('name');  # 从session获取，拿到登录者的名字
            userGonghao = request.session.get('uid'); #从session获取，拿到登录者的公号

            #判断是否是从添加分组的页面过来的信息
            grounpResult = request.GET.get('issuccess');
            if grounpResult == '1':
                grounpResult = '分组成功！';
            else:
                grounpResult = '';
            #拿到进入该模块的用户（助教和老师）所属的班级，没有的话则显示session中保存的即可（这整合项目的时候修改）
            currentClassNumberInfo = request.GET.get('classnumber');
            if currentClassNumberInfo == None:
                # 得到该用户的班级信息，然后方便填充到页面中的班级选择框中
                #如果是助教，直接拿对应班级属性中的值
                if userType == 2:
                    currentClassNumberInfo = request.session.get('student_class_name');
                elif userType == 3: #是老师,而老师可能有多个，到时候默认显示第一个就好了
                    currentClassNumberInfo = request.session.get('teacher_class_name')[0];

            #得到对应班级中的分组信息和学生的信息，方便显示到页面
            grounpInfo = User.objects(student_class_name = currentClassNumberInfo , permission = 1);

            #获取助教或者老师登录者数据中包含的对应的班级信息，从登录者的权限来判断，如果是助教，那么只有一个班级，如果是老师，则从数据库中进行获取
            infoAssistantOrTeacherClass = [];
            if userType == 2 : #是助教，直接拿取所带的班级就可以了
                infoAssistantOrTeacherClass.append(currentClassNumberInfo);
            elif userType == 3: #是老师，则要从数据库中进行（根据登录老师的名字获取）
                currentTeacher = User.objects(uid = userGonghao)[0];#老师是通过工号找带的班级(返回的是对应的对象)
                teacherclass = currentTeacher.teacher_class_name;
                for everyclass in teacherclass:
                    infoAssistantOrTeacherClass.append(everyclass);
            #（1）grounpResult:进行当前分组操作的结果（2）grounpInfo：对应当前选择的班级分组详细信息（3）currentClassNumberInfo：当前选择的班级
            #（4）infoAssistantOrTeacherClass：助教或者老师所带的班级 （5）username:登录人的名字
            context ={'grounpResult':json.dumps(grounpResult) , 'grounpInfo':grounpInfo  ,'currentClassNumberInfo':currentClassNumberInfo,
                      'infoAssistantOrTeacherClass':infoAssistantOrTeacherClass ,'username':username};
            return render(request , 'Csapphnu/studentGroupingInfo.html',context);
        else:#没有足够权限的则显示到主界面
            return HttpResponseRedirect('/index/');

#将页面传过来的分组情况进行数据库处理
def studentGrounpToDB(request):
    #得到传送过来的学生的个数，以此来进行数据的获取
    countNumber = request.POST.get('savecountnumber');
    #得到传送过来进行了删除后又添加的数值，并进行分割，以“-”，因为拼接是按这样的方式
    deletNumber = request.POST.get('savedeletenumber');
    deletlist = '';
    if deletNumber == '0':   #表示里面进行删除内容
        deletlist = ['0'];
    else:
        deletlist = deletNumber.split('-');
    #进行循环，拿取提交过来的数据
    everyNumber = 1;
    #得到需要进行分组的班级
    studentClass  = request.POST.get('studentSelectClass');
    while everyNumber < (int(countNumber)+1):  #注意加1，因为比较我这是从1开始
        isAreadyExist = False;
        #比较该数值是否在删除编号列表中出现，出现了则不进行操作，因为这个内容已经不存在了
        for everyValueDelete in deletlist:
            if everyValueDelete == str(everyNumber):
                isAreadyExist = True;
                break;
        if isAreadyExist == True:   #表示当前的这个数值已经被删除了，不用进行添加操作
            everyNumber += 1;  # 操作个数+1
            continue;
        else:
            strStudent = 'submitcontent';
            # 得到输入框中的内容
            inputContent = request.POST.get(strStudent + str(everyNumber));
            # 分割数据，因为在传入的时候进行了处理，其中形式是：组号-姓名-学号
            fengelist = inputContent.split('-');
            grounpNumber = fengelist[0];  # 得到小组号
            studentName = fengelist[1];  # 得到姓名
            studentNumber = fengelist[2];  # 得到学号
            # 存入到数据库中(user表中)
            studentop = User.objects(uid = studentNumber);
            if len(studentop) > 0:  # 则进行更新操作
              studentop = User.objects(uid = studentNumber)[0];  #拿到对应的学号人的信息
              studentop.name = studentName;
              studentop.student_class_name = studentClass;
              studentop.student_grounp = grounpNumber;
              studentop.save();
            else:  # 如果数据库中没有这个学号的学生，则进行添加操作（其实不会出现，因为添加的学生都是从学生用户得到的，但是防止其他的情况出现）
              addstudentinfo = User();
              addstudentinfo.name = studentName;
              addstudentinfo.uid = studentNumber;
              addstudentinfo.student_class_name = studentClass;
              addstudentinfo.student_grounp = grounpNumber;
              addstudentinfo.save();
            everyNumber += 1;  # 操作个数+1
    return  HttpResponseRedirect('/studentgrouping/?issuccess=1&classnumber='+ studentClass);

#处理ajax的班级刷新操作（没用到这里）
def reloadStudentClassAndName(request):
    response_data = {}
    result = {'result': 101}
    if request.method == 'GET':
        # 得到要刷新的班级信息
        classnumber = request.GET.get('classnumber');
        # 查询数据库返回对应班级学生的分组数据
        allGrounpInfo = StudentGrounp.objects(student_class = classnumber);
        response_data['result'] = 'Success'
        response_data['message'] = serializers.serialize('json', allGrounpInfo)
        print(response_data['message'])
        return render(request ,'Csapphnu/helloworld.html')
   # return HttpResponse(JsonResponse(result), content_type="application/json")
