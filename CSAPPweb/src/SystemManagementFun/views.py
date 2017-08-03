from django.shortcuts import render
from django.http import *
from .models import *
from django.template import *
from django.core.urlresolvers import reverse
import json
from django.conf import settings   #引入配置文件
import os         #引入配置文件
import xlrd   #引入读取excl表格的库

def showFunciton(request):
    try: #抛个异常判断，防止出现意外情况
        #首先判断是否是属于登录中的用户并且是否有足够的权限（这个模块只有老师可以进），否则跳转到登录页面中
        isOnlineUser = request.session.get('uid');
        isEnoughtPermission = request.session.get('permission');
        if isOnlineUser == None: #表示不是登录中的用户
            return HttpResponseRedirect('/index/');
        else:
            if isEnoughtPermission == 3: #表示是管理员
                sigleaddResult = request.GET.get('addresult'); #单个添加用户信息的操作结果
                moreaddResult = request.GET.get('more'); #批量添加用户信息的操作结果
                if moreaddResult == None: #表示没有进行批量信息添加
                    moreaddResult = '';
                if sigleaddResult == None: #表示没有进行单个信息添加
                    sigleaddResult = '';

                allstudentinfo = User.objects.filter(permission = 1).limit(10);  # 查询所有学生用户的信息，默认查询10条
                allteacherinfo = User.objects.filter(permission = 3).limit(10);  # 查询所有学生用户的信息
                allassistantinfo = User.objects.filter(permission = 2).limit(10);  # 查询所有学生用户的信息
                allstudentinfoNumber = len(User.objects.filter(permission = 1));  #学生信息的条数
                allteacherinfoNumber = len(User.objects.filter(permission = 3)); #老师信息的条数
                allassistantinfoNumber = len(User.objects.filter(permission = 2)); #助教信息的条数

                #(1)sigleResult:单个添加用户信息操作的结果 (2)moreaddResult:批量添加信息的结果   (3)allstudentinfo:所有学生的信息
                #(4)allteacherinfo:所有老师信息(5)所有助教信息(6)allstudentinfoNumber,allteacherinfoNumber,allassistantinfoNumber每种用户的信息条数
                context ={'sigleResult':json.dumps(sigleaddResult) ,'moreaddResult':json.dumps(moreaddResult),'allstudentinfo':allstudentinfo,
                          'allteacherinfo':allteacherinfo,'allassistantinfo':allassistantinfo,
                          'allstudentinfoNumber':allstudentinfoNumber,'allteacherinfoNumber':allteacherinfoNumber,'allassistantinfoNumber':allassistantinfoNumber}
                return render(request , 'SystemManagementFun/csappstudentmanage.html' ,context)
            else:  #权限不够则，回到主界面
                return HttpResponseRedirect('/index/');
    except Exception as  errors:
        return HttpResponseRedirect('/index/');

#将上传过来的文件进行保存到服务器中
def addUserInfomation(request):
    try:
        # 拿到上传过来的文件
        fileInfo = request.FILES['picl'];
        #拿到要进行添加的类型，1表示学生，2表示助教，3表示老师
        addUserType = request.POST.get('addusertype');
        # 拼凑保存到服务器中文件的名字
        filename = os.path.join(settings.MEDIA_ROOT, fileInfo.name)
        # 解析传过来的图片并且写到服务器对应的目录media下
        with open(filename, 'wb+') as readcontent:  # 注意这里的读取方式要为'wb+',否则会有问题
            for con in fileInfo.chunks():  # 这是读取的方式
                readcontent.write(con);
        #判断这次需要添加的用户类型
        if addUserType == '1':
            #当上传到服务器后，读取文件，并将信息保存到数据库中(学生)
            successAddNumber = readStudentInfomationFile(request , fileInfo.name );  #添加学生信息的操作
        elif addUserType == '2':  #添加助教
            successAddNumber = readAssistantInfomationFile(request , fileInfo.name );  #添加助教信息的操作
        elif addUserType == '3': #添加老师
            successAddNumber = readTeacherInfomationFile(request , fileInfo.name );  #添加老师信息的操作
        # 返回上传成功的信息
        return HttpResponseRedirect('/systemmanagement/csappstudentmanage?more='+str(successAddNumber));
    except Exception as errors:  #防止异常情况出现
        return render(request ,'SystemManagementFun/csappstudentmanage.html');

#批量添加学生基本信息
def readStudentInfomationFile(request , filename ):
    #写服务器的上传过来的文件路径
    webFileName = os.path.join(settings.MEDIA_ROOT, filename)
    # 打开文件
    workbook = xlrd.open_workbook(r''+webFileName)
    # 根据sheet索引或者名称获取sheet内容
    sheet = workbook.sheet_by_index(0)  # sheet索引从0开始，第一个sheet就是为0，因为一个excl表里面可以有多个sheet

    studentNumber = -1; #记录excl表中学生学号对应的列号
    studentName = -1;  #记录excl表中学生名字对应的列号
    studentClass = -1 ; #记录excl表中学生班级对应的列号

    exclcol = 0;  # 当前列数
   #得到excl表中对应的学号，姓名，班级的索引，便于后于插入数据
    while exclcol < sheet.ncols: #如果当前的列数小于总的列数
        if sheet.cell_value(0, exclcol) == '学号':
            studentNumber = exclcol;
        elif sheet.cell_value(0, exclcol) == '姓名':
            studentName = exclcol;
        elif sheet.cell_value(0, exclcol) == '班级':
            studentClass = exclcol;
        exclcol += 1;

    #以行进行读取数据，插入数据到数据库中
    exclcol = 0; #初始化当前列索引
    exclrow = 1;  # 当前行数，第一行的数据是标志，不需要进行数据查询判断，第二行开始才是数据
    thisOpAddStudentNumber = 0 #记录当前执行添加excl添加成功的人数
    while exclrow < sheet.nrows:  #以行进行读取
        currentNumber = '';  # 记录当前添加信息的学号的内容
        adduser = User();
        while exclcol < sheet.ncols:
            #得到当前行当前列的值
            currentContent = sheet.cell_value(exclrow, exclcol);
            if exclcol == studentNumber:
                adduser.uid = currentContent;  #学号
                currentNumber = currentContent ; #记录一下学号，后面便于判断是否该学生重复添加了
                adduser.psw = currentContent;  #默认初始密码为学号
            elif exclcol == studentName:
                adduser.name = currentContent;     #姓名
            elif exclcol == studentClass:
                adduser.student_class_name = currentContent;  #班级
            exclcol += 1;  # 当前读取列数+1
        #判断当前学生是否已经添加过在数据库中已经存在
        print(currentNumber)
        judgeIsAdd = User.objects(uid = currentNumber);
        if len(judgeIsAdd) > 0 : #表示已经添加过，则这次不要添加
            exclrow += 1;  # 当前读取行数+1
            exclcol = 0;  # 初始化当前列索引
            continue;    #后面的不会执行
        #注意要让user的其他字段为空，否则会在判断的时候出问题
        adduser.permission = 1 ; #权限为学生
        adduser.teacher_class_name = [];
        adduser.assisant_info = {};
        adduser.contact = '';
        adduser.is_valid = True;
        adduser.student_grounp = '';
        adduser.save();   #插入到数据库中
        thisOpAddStudentNumber += 1; #成功添加人数+1
        exclrow += 1;  #当前读取行数+1
        exclcol = 0 ; #初始化当前列索引
    return thisOpAddStudentNumber;  #返回本次添加成功的人数

# 批量添加助教基本信息
def readAssistantInfomationFile(request, filename):
        # 写服务器的上传过来的文件路径
        webFileName = os.path.join(settings.MEDIA_ROOT, filename)
        # 打开文件
        workbook = xlrd.open_workbook(r'' + webFileName)
        # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_index(0)  # sheet索引从0开始，第一个sheet就是为0，因为一个excl表里面可以有多个sheet

        studentNumber = -1;  # 记录excl表中助教学号对应的列号
        studentName = -1;  # 记录excl表中助教名字对应的列号
        studentClass = -1;  # 记录excl表中助教班级对应的列号

        exclcol = 0;  # 当前列数
        # 得到excl表中对应的学号，姓名，班级的索引，便于后于插入数据
        while exclcol < sheet.ncols:  # 如果当前的列数小于总的列数
            if sheet.cell_value(0, exclcol) == '学号':
                studentNumber = exclcol;
            elif sheet.cell_value(0, exclcol) == '姓名':
                studentName = exclcol;
            elif sheet.cell_value(0, exclcol) == '班级':
                studentClass = exclcol;
            exclcol += 1;

        # 以行进行读取数据，插入数据到数据库中
        exclcol = 0;  # 初始化当前列索引
        exclrow = 1;  # 当前行数，第一行的数据是标志，不需要进行数据查询判断，第二行开始才是数据
        thisOpAddStudentNumber = 0  # 记录当前执行添加excl添加成功的人数
        while exclrow < sheet.nrows:  # 以行进行读取
            currentNumber = '';  # 记录当前添加信息的学号的内容
            adduser = User();
            while exclcol < sheet.ncols:
                # 得到当前行当前列的值
                currentContent = sheet.cell_value(exclrow, exclcol);
                if exclcol == studentNumber:
                    adduser.uid = currentContent;  # 学号
                    currentNumber = currentContent;  # 记录一下学号，后面便于判断是否该学生重复添加了
                    adduser.psw = currentContent;  # 默认初始密码为学号
                elif exclcol == studentName:
                    adduser.name = currentContent;  # 姓名
                elif exclcol == studentClass:
                    adduser.student_class_name = currentContent;  # 班级
                exclcol += 1;  # 当前读取列数+1
            # 判断当前学生是否已经添加过在数据库中已经存在
            print(currentNumber)
            judgeIsAdd = User.objects(uid=currentNumber);
            if len(judgeIsAdd) > 0:  # 表示已经添加过，则这次不要添加
                exclrow += 1;  # 当前读取行数+1
                exclcol = 0;  # 初始化当前列索引
                continue;  # 后面的不会执行
            # 注意要让user的其他字段为空，否则会在判断的时候出问题
            adduser.permission = 2;  # 权限为助教
            adduser.teacher_class_name = [];
            adduser.assisant_info = {};
            adduser.contact = '';
            adduser.is_valid = True;
            adduser.student_grounp = '';
            adduser.save();  # 插入到数据库中
            thisOpAddStudentNumber += 1;  # 成功添加人数+1
            exclrow += 1;  # 当前读取行数+1
            exclcol = 0;  # 初始化当前列索引
        return thisOpAddStudentNumber;  # 返回本次添加成功的人数

# 批量添加老师基本信息
def readTeacherInfomationFile(request, filename):
        # 写服务器的上传过来的文件路径
        webFileName = os.path.join(settings.MEDIA_ROOT, filename)
        # 打开文件
        workbook = xlrd.open_workbook(r'' + webFileName)
        # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_index(0)  # sheet索引从0开始，第一个sheet就是为0，因为一个excl表里面可以有多个sheet

        teacherNumber = -1;  # 记录excl表中老师学号对应的列号
        teacherName = -1;  # 记录excl表中老师名字对应的列号
        teacherClass = -1;  # 记录excl表中老师所带班级对应的列号

        exclcol = 0;  # 当前列数
        # 得到excl表中对应的学号，姓名，班级的索引，便于后于插入数据
        while exclcol < sheet.ncols:  # 如果当前的列数小于总的列数
            if sheet.cell_value(0, exclcol) == '学号':
                teacherNumber = exclcol;
            elif sheet.cell_value(0, exclcol) == '姓名':
                teacherName = exclcol;
            elif sheet.cell_value(0, exclcol) == '班级':
                teacherClass = exclcol;
            exclcol += 1;

        #以行进行读取数据，插入数据到数据库中
        exclcol = 0;  # 初始化当前列索引
        exclrow = 1;  # 当前行数，第一行的数据是标志，不需要进行数据查询判断，第二行开始才是数据
        thisOpAddStudentNumber = 0  # 记录当前执行添加excl添加成功的人数
        while exclrow < sheet.nrows:  # 以行进行读取
            currentNumber = '';  # 记录当前添加信息的学号的内容
            adduser = User();
            while exclcol < sheet.ncols:
                # 得到当前行当前列的值
                currentContent = sheet.cell_value(exclrow, exclcol);
                if exclcol == teacherNumber:
                    adduser.uid = currentContent;  # 工号
                    currentNumber = currentContent;  # 记录一下工号，后面便于判断是否该学生重复添加了
                    adduser.psw = currentContent;  # 默认初始密码为学号
                elif exclcol == teacherName:
                    adduser.name = currentContent;  # 姓名
                elif exclcol == teacherClass:  # 由于老师所带的班级可能是多个，则是列表形式，这里需要自己拼接
                    classlist = currentContent.split('-');  #这要求excl中以-为分割符
                    if len(classlist) == 1: #表示分割就一个班级，那么班级内容就是读取到的内容
                         adduser.teacher_class_name.append(currentContent);
                    else:
                        for everyclass in classlist:
                            adduser.teacher_class_name.append(everyclass);
                exclcol += 1;  # 当前读取列数+1
            # 判断当前学生是否已经添加过在数据库中已经存在
            judgeIsAdd = User.objects(uid=currentNumber);
            if len(judgeIsAdd) > 0:  # 表示已经添加过，则这次不要添加
                exclrow += 1;  # 当前读取行数+1
                exclcol = 0;  # 初始化当前列索引
                continue;  # 后面的不会执行
            # 注意要让user的其他字段为空，否则会在判断的时候出问题
            adduser.permission = 3;  # 权限为老师
            adduser.student_class_name = '';
            adduser.assisant_info = {};
            adduser.contact = '';
            adduser.is_valid = True;
            adduser.student_grounp = '';
            adduser.save();  # 插入到数据库中
            thisOpAddStudentNumber += 1;  # 成功添加人数+1
            exclrow += 1;  # 当前读取行数+1
            exclcol = 0;  # 初始化当前列索引
        return thisOpAddStudentNumber;  # 返回本次添加成功的人数
    # 获取第一个sheet名字
    # sheet2_name = workbook.sheet_names()[0]
    # sheet2 = workbook.sheet_by_name('sheet2') #这是直接通过名字进行获取
    # sheet的名称，行数，列数
    # print (sheet.name, sheet.nrows, sheet.ncols)
    # 获取所有sheet
    #workbook.sheet_names()
    # 获取指定的整行和整列的值（返回的是数组类型）
    #rows = sheet.row_values(0)  # 获取第四行内容
    # cols = sheet.col_values(2)  # 获取第三列内容
    #print (rows)
    # print (cols)
    #
    # # 获取指定某个单元格内容(三种方法)
    # print (sheet.cell(1, 0).value)
    # print (sheet.cell_value(1, 0))
    # print (sheet.row(1)[0].value)
    # # 获取单元格内容的数据类型
    # #ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
    # print (sheet.cell(1,0).ctype)
#单个添加用户信息
def regesterUserInfoSigle(request):
    addInfoResult = '';
    usernumber = request.POST.get('usernumber');
    username = request.POST.get('username');
    userclass = request.POST.get('userclass');
    usertype = request.POST.get('usertype'); #用户权限
    #判断该用户是否已经添加过了
    currentUser = User.objects.filter( uid = usernumber);
    if len(currentUser) > 0 : #表示已经添加过
        addInfoResult = '0';
    else:
        addUser = User();
        #判断是老师，还是助教和学生
        if usertype == '1' or usertype == '2':
            addUser.uid = usernumber;
            addUser.psw = usernumber;
            addUser.name = username;
            addUser.permission = usertype;
            addUser.is_valid = True;
            addUser.student_class_name = userclass;
            addUser.contact = '';
            addUser.teacher_class_name = [];
            addUser.assisant_info = {};
            addUser.student_grounp = '';
            addUser.save();
        elif usertype == '3':
            addUser.uid = usernumber;
            addUser.psw = usernumber;
            addUser.name = username;
            addUser.permission = usertype;
            addUser.is_valid = True;
            addUser.student_class_name = '';
            addUser.contact = '';
            addUser.teacher_class_name = [];
            addUser.assisant_info = {};
            addUser.student_grounp = '';
            addUser.save();
        addInfoResult = '1'
    return  HttpResponseRedirect('/systemmanagement/csappstudentmanage/?addresult='+addInfoResult);

#分页大小发生变化
def changepagesize(request):
    thispagesize = request.GET.get('pagesize'); #得到请求的分页的大小
    thistype = request.GET.get('type'); #得到请求的分页的用户类型，1是学生，2是助教，3是老师
    #返回对应条数的数据内容
    if thistype == '1':#请求学生数据,返回一定数量的数据
       currentInfo = User.objects.filter(permission = 1 ).limit(int(thispagesize)); #限制返回的数据条数
    elif thistype == '2': #请求的是助教信息
        currentInfo = User.objects.filter(permission=2).limit(int(thispagesize));  # 限制返回的数据条数
    elif thistype == '3': #请求的是老师的信息
        currentInfo = User.objects.filter(permission=3).limit(int(thispagesize));  # 限制返回的数据条数
    #由于返回的类型不能被直接序列化，所以需要自己进行处理
    data = [];
    if thistype== '1' or thistype == '2':
        for everydata in currentInfo:
            data.append({"uid":everydata.uid ,"name":everydata.name,"permission":everydata.permission,
                         "student_class_name":everydata.student_class_name,"contact":everydata.contact});
    elif thistype == '3': #表示的是老师，老师要显示的数据不一样
        for everydata in currentInfo:
            data.append({"uid":everydata.uid ,"name":everydata.name,"permission":everydata.permission,
                         "teacher_class_name":everydata.teacher_class_name,"contact":everydata.contact});
    data ={"data":data};
    return JsonResponse(data);

#分页的索引发生变化
def changepagenumber(request):
    thispagesize = request.GET.get('pagesize');  # 得到请求的分页的大小
    thistype = request.GET.get('type');  # 得到请求的分页的用户类型，1是学生，2是助教，3是老师
    thisnumber = request.GET.get('pagenumber'); #得到需要请求的数据的页面索引数
    # 返回对应条数的数据内容
    if thistype == '1':  # 请求学生数据,返回一定数量的数据
        currentInfo = User.objects.filter(permission=1);  # 返回的数据条数
    elif thistype == '2':  # 请求的是助教信息
        currentInfo = User.objects.filter(permission=2);  # 返回的数据条数
    elif thistype == '3':  # 请求的是老师的信息
        currentInfo = User.objects.filter(permission=3);  # 返回的数据条数
    #寻找到对应的页面的数据
    startindex = (int(thisnumber)-1)*int(thispagesize);
    endindex = int(thisnumber)*int(thispagesize);
    currentInfo = currentInfo[startindex : endindex]; #分割到对应数据的内容数据
    # 由于返回的类型不能被直接序列化，所以需要自己进行处理
    data = [];
    if thistype == '1' or thistype == '2':
        for everydata in currentInfo:
            data.append({"uid": everydata.uid, "name": everydata.name, "permission": everydata.permission,
                         "student_class_name": everydata.student_class_name, "contact": everydata.contact});
    elif thistype == '3': #因为老师要显示的数据不一样，所以需要分开
        for everydata in currentInfo:
            data.append({"uid": everydata.uid, "name": everydata.name, "permission": everydata.permission,
                         "teacher_class_name": everydata.teacher_class_name, "contact": everydata.contact});
    data = {"data": data};
    return JsonResponse(data);
