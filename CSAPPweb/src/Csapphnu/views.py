from django.shortcuts import render
from django.http import *
from .models import *
from django.template import *
from django.core.urlresolvers import reverse
import json



class showAssistanInfo(object):
    def __init__(self, assistantNumber, assistantName, assistantClass):
        self.assistantNumber = assistantNumber
        self.assistantName = assistantName
        self.assistantClass = assistantClass
    #返回助教的学号
    def get_Number(self):
        return self.assistantNumber
    #返回助教的名字
    def get_Name(self):
        return self.assistantName
    #返回助教的所带的班级
    def get_Class(self):
        return self.assistantClass

#显示助教信息
def managerAssistantInfo(request):
    try: #抛个异常判断，防止出现意外情况
        #首先判断是否是属于登录中的用户并且是否有足够的权限（这个模块只有老师可以进），否则跳转到登录页面中
        isOnlineUser = request.session.get('uid');
        isEnoughtPermission = request.session.get('permission');
        if isOnlineUser == None: #表示不是登录中的用户
            return HttpResponseRedirect('/index/');
        else:
            if isEnoughtPermission == 3:  #权限等于3（老师）的才能进入
                # 判断添加是否成功，拿取添加操作传递过来的数据
                addresult = request.GET.get('addresult');
                allnumber = request.GET.get('allnumber');
                if addresult == None:  # 这个表示是并没有执行添加操作
                    addresult = "";
                    addresultPrintf = "";
                else:
                    addresult = "总添加条数为" + str(allnumber) + ";其中成功添加" + str(addresult) + "条，添加失败" + str(int(allnumber) - int(addresult)) + "条(注：无法重复添加已存在信息或不存在的数据信息)"
                    addresultPrintf = addresult;

                # 得到删除操作后，传过来的内容
                deleteresult = request.GET.get('del');
                if deleteresult == 'success':
                    deleteresult = '删除成功!';
                else:
                    deleteresult = '';

                # 得到删除操作后，传过来的内容
                updataresult = request.GET.get('upd');
                if updataresult == 'success':
                    updataresult = '更新成功!';
                else:
                    updataresult = '';

                #得到当前登录老师的姓名和工号(session获取)
                contentOne = request.session.get('name');
                teacherUid = request.session.get('uid');
                # 得到user数据库中的对应老师对应的助教数据
                currentTeacherInfo = User.objects(uid = teacherUid);
                dictInfo = [];  #对应老师的助教学生的信息
                if len(currentTeacherInfo) > 0 : #找到对应的老师信息
                    currentTeacherInfo = User.objects(uid=teacherUid)[0];
                    belongtoClassNumber = currentTeacherInfo.teacher_class_name; #老师所带的学生的班级，返回是列表
                    content = currentTeacherInfo.assisant_info ; #得到助教的信息，返回的是字典
                    for everyInfo in content.keys():  #得到助教的学号
                        stuNumber = everyInfo ;
                        #通过学号找助教的姓名
                        currentUser = User.objects(uid = stuNumber)[0];
                        stuName = currentUser.name;
                        stuClass = currentUser.student_class_name;
                        #封装到对象里面
                        currentContext = showAssistanInfo(stuNumber,stuName,stuClass);
                        #添加到列表中，进行传送
                        dictInfo.append(currentContext);
                else:
                    dictInfo = [''];

                #（1）dbinfoDatda：对应老师所带的助教信息（2）addresult：进行添加操作的结果（3）addresultPrintf：进行添加操作打印信息的内容
                #（4）teacherinfo：当前登录老师的姓名（5）deleteResult：删除操作的结果（6）updataResult：更新操作的结果
                #(6)belongtoClassNumber:当前登录老师所带的班级
                context = {'dbinfoDatda': dictInfo, 'addresult': addresult ,'addresultPrintf':json.dumps(addresultPrintf), 'teacherinfo':contentOne,
                       'deleteResult': json.dumps(deleteresult) , 'updataResult':json.dumps(updataresult),
                        'belongtoClassNumber':belongtoClassNumber};
                return render(request, 'Csapphnu/managerassistantinfo.html', context);
            else: #没有足够权限的则显示到主界面
                return HttpResponseRedirect('/index/');
    except Exception as  errors:
        return HttpResponseRedirect('/index/');

#添加助教信息
def addInfo(request):
    #得到传送过来选择的索引值
    index = request.POST.get('tableinfoindex');
    #执行添加数据到数据库操作，返回添加的数目
    successresult , allnumber= addAssistantInfo2DB(index ,request);
    #重定向到最初的显示页面
    return HttpResponseRedirect('/assistantmanage/?addresult=' + str(successresult)+'&allnumber='+str(allnumber));

#将传送过来的数据添加到数据库中
def addAssistantInfo2DB(index , request):
    #分割传送过来的索引值，以逗号进行分割
    isSucess = 0;
    index = index[0:len(index)-1] #因为最后多了一个逗号，先将其进行截取
    indexlist = index.split(',');
    for con in indexlist:
        #获取输入框和选择框中填写的内容
        stuNumber = request.POST.get('assistantNumber'+con);
        stuName = request.POST.get('assistantName' + con);
        stuClass = request.POST.get('selectClass' + con);
       # stuClass = request.POST.get('assistantClass' + con);  //之前版本中的输入框的添加信息
        #判断要添加的数据是否已经在数据库中了(用学号为主键来判断)
        # 得到数据库中的数据，根据学号来进行判断
        #得到该老师的uid，来得到该老师的信息
        teacherUid = request.session.get('uid');
        currentTeacherInfo = User.objects(uid = teacherUid)[0];
        if len(currentTeacherInfo) > 0 : #表示找到对应的老师的信息
            #判断添加的助教是否在user表中，否则不能无中生有加助教的信息
            addAssistanStudent = User.objects(uid = stuNumber ,name = stuName ,permission = 2);
            if len(addAssistanStudent) > 0 :#表示该助教的信息符合
                #判断添加的助教是否已经存在对应的该老师的信息中
                dictAssistantInfo = currentTeacherInfo.assisant_info; #返回的是字典
                isNoFind = True;
                for everyassistant in dictAssistantInfo.keys():
                    if everyassistant == stuNumber:
                        isNoFind = False;
                        break;
                if isNoFind == True:  #表示没有重复，则进行添加操作
                    #添加对应的助教信息
                    currentTeacherInfo.assisant_info[stuNumber] = stuName;
                    #更新对应助教的个人信息
                    addAssistant = User.objects(uid = stuNumber, name=stuName)[0];
                    addAssistant.student_class_name = stuClass;
                    addAssistant.save();
                    currentTeacherInfo.save();
                    isSucess += 1;
                else:
                    continue;
            else:
                continue;
        else:
            continue;
    #返回添加的条数，一个为成功添加的数目，第二个为总数目
    return isSucess ,len(indexlist);

#进行删除操作
def deleteInfo(request):
    #获取要删除的学号
    deletenumber =  request.GET.get('deletenumber');
    print(deletenumber+"@@@@@@@@")
    #将对应的学号的信息中的所带班级进行删除
    deleteResult = User.objects(uid = deletenumber);
    if len(deleteResult) > 0 :  #表示查找到信息
        #更新User中对应的个人信息中的班级内容
        deleteResult = User.objects(uid=deletenumber)[0];
        deleteResult.student_class_name = '';
        #删除对应老师中的助教信息中的内容
        teachUid = request.session.get('uid');
        currentInfo = User.objects(uid = teachUid );
        if len(currentInfo) > 0 :
            currentInfo = User.objects(uid=teachUid)[0];
            dictInfoDel = currentInfo.assisant_info;
            del dictInfoDel[deletenumber];
            currentInfo.save();
            deleteResult.save();  #更新数据
    return HttpResponseRedirect('/assistantmanage/?del='+ 'success'); #重定向回主页面

#进行更新操作
def updataInfo(request):
    #拿到传送过来的数据
    updataNumber = request.POST.get('updataNumber');
    updataName = request.POST.get('updataName');
    updataClass =  request.POST.get('updataClass');

    #更新数据
    updataresult = User.objects(uid = updataNumber);
    if len(updataresult) != 0 :
        updataresult = User.objects(uid=updataNumber)[0]; #更新对应助教的个人信息数据库
        updataresult.uid = updataNumber; #学号
        updataresult.name = updataName; #姓名
        updataresult.student_class_name = updataClass;#所带班级
        #更新对应老师中的助教内容
        teachUid = request.session.get('uid');  #当前老师的uid
        currentInfo = User.objects(uid = teachUid);
        if len(currentInfo) > 0:
            currentInfo = User.objects(uid=teachUid)[0];
            dictInfoDel = currentInfo.assisant_info;
            dictInfoDel[updataNumber] = updataName;
            currentInfo.save();
            updataresult.save();  # 更新数据
    return HttpResponseRedirect('/assistantmanage/?upd='+ 'success');

#ajax请求得到当前老师所带的班级信息，用来动态生成选择框中的内容
def getTeacherBelongClass(request):
    requestResult = ''; #请求的结果
    requestClass = []; #请求得到的班级
    teacherUid = request.session.get('uid'); #得到当前老师的uid信息
    try:
       currentInfo =  User.objects(uid = teacherUid)[0];
       requestClass = currentInfo.teacher_class_name ; #得到所带的班级信息，返回的是列表
       requestResult = 'success';
    except Exception as  errors:
        requestResult = 'fail';
    data = {'requestResult':requestResult , 'classNumberData':requestClass};
    return HttpResponse(JsonResponse(data), content_type="application/json")

#跳转到对应的视图
def jumptoeverymodel(request):
    # 首先判断是否是属于登录中的用户，否则跳转到登录页面中
    isOnlineUser = request.session.get('uid');
    if isOnlineUser == None:  # 表示不是登录中的用户
        return HttpResponseRedirect('/index/');
    else:
        return render(request , 'Csapphnu/userinfomanage.html');

#权限验证各个模块
def userTypeVerification(request):
    if request.method == 'GET':
        #得到要访问的是哪个模块
        modelType = request.GET.get('currentmodeltype');
        usertype = request.session.get('permission');  #从session中得到该用户的权限
        result = '';
        if modelType == 'grounpmodel':      #访问学生分组模块，学生权限不能进
            if int(usertype) <= 1:
                result = 'fail';
            else:
                result = 'success';
        elif modelType == 'assistantmange': #访问老师管理助教模块，学生和助教权限不能进
            if int(usertype) <= 2:
                result = 'fail';
            else:
                result = 'success';
        data = {'result':result};
    return HttpResponse(JsonResponse(data), content_type="application/json")