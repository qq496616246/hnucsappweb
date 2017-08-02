from django.shortcuts import render
from django.http import *
from .models import *
from django.template import *
from django.core.urlresolvers import reverse
import json
from django.core import serializers


def modifyUserInfo(request):
    # 首先判断是否是属于登录中的用户，否则跳转到登录页面中
    isOnlineUser = request.session.get('uid');
    if isOnlineUser == None:  # 表示不是登录中的用户
        return HttpResponseRedirect('/index/');
    else:
        updateResult = request.GET.get('issucess');
        if updateResult == '1':  # 表示是进行了更新操作
            updateResult = "恭喜你，个人信息更新成功"
        elif updateResult == '2': #表示更新失败
            updateResult = "该用户不是合法身份，请确认！"
        else:
            updateResult = '';
        #获取登录用户的信息(从session中获取)
        username = request.session.get('name');
        userregisternumber = request.session.get('uid');
        userclass = ''  #登录用户的班级
        usertype = str(request.session.get('permission')); #1表示学生，2：助教，3：；老师，4：管理员  (session中拿)
        userTypeChange = {"1":"学生" , "2":"助教" , "3":"教师" ,"4":"管理员"};  #将身份进行转变
        usertype = userTypeChange[usertype]
        assistantname = '';  #助教姓名
        if usertype == '学生' : #表示是学生
            userclass = request.session.get('student_class_name') #从session中得到
            assistantInfo = User.objects(student_class_name = userclass , permission = 2)  # 通过user表找到对应班级的助教名字
            if len(assistantInfo) > 0 :  #表示找到对应的信息
                assistantname = assistantInfo[0].name   #得到助教姓名
        elif usertype == '助教' : #表示是助教，那么助教姓名就是自己
            userclass = request.session.get('student_class_name') #从session中得到
            assistantname = username ;
        elif usertype == '教师' : #表示的是老师，那么直接通过查找数据库来找需要的信息
            currentTeacher = User.objects(uid = userregisternumber)[0];
            className = currentTeacher.teacher_class_name;  #该老师所带的班级(返回的是列表类型)
            classAssistantName =currentTeacher.assisant_info;#该老师所带的助教(返回的是字典类型)
            for everyclass in className:  #得到拼接的老师所带的班级信息
                userclass = userclass + ','+everyclass;
            for everyassistantinfo in classAssistantName.values(): #得到拼接的老师所带的助教的信息(因为是字典，key是助教的学号，值是助教的名字)
                assistantname = assistantname + "," +everyassistantinfo ;

        elif usertype == '管理员' : #表示的是管理员，则显示所有助教信息
            userobject = User.objects( permission = 2)  #通过找用户表，权限为2的人
            for everyinfo in userobject:
                assistantname = assistantname +","+everyinfo.name

        logininfo ={"loginname":username , "loginclass":userclass , "loginnumber":userregisternumber ,"usertype":usertype
                    ,"assistantname":assistantname};
        context = {'logininfo':logininfo , 'updateResult':json.dumps(updateResult)}
        return  render(request , 'Csapphnu/modifyUserInfo.html' ,context)

#更新数据的操作
def updateinfo(request):
    loginRegesterNumber = request.POST.get('registrationnumber')   #获取提交过来的学号/工号，因为这个是主键
    loginRegesterPas = request.POST.get('loginuserpassword')  #新的密码
    print(loginRegesterPas)
    loginRegesterTel = request.POST.get('logintelphone')    #新的联系方式
    print(loginRegesterTel)
    #根据主键进行更新
    userinfo = User.objects( uid = loginRegesterNumber)  #拿取所有数据
    addresult = '';
    if len(userinfo) > 0 :  #表示数据库有该用户的信息
        userinfo = User.objects(uid=loginRegesterNumber)[0]  # 拿取一条数据
        userinfo.psw = loginRegesterPas ;
        userinfo.contact = loginRegesterTel ;
        userinfo.save();
        addresult ='1'; #表示更新成功
    else:
        addresult = '2'
    return HttpResponseRedirect("/modifyuserinfo/?issucess="+addresult) #重定向回去