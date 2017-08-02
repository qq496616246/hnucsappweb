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
    context ={}
    return render(request , 'Csapphnu/csappstudentmanage.html' ,context)


#将上传过来的文件进行保存到服务器中
def addUserInfomation(request):
    # 拿到上传过来的文件
    fileInfo = request.FILES['picl'];
    # 拼凑保存到服务器中文件的名字
    filename = os.path.join(settings.MEDIA_ROOT, fileInfo.name)
    # 解析传过来的图片并且写到服务器对应的目录media下
    with open(filename, 'wb+') as readcontent:  # 注意这里的读取方式要为'wb+',否则会有问题
        for con in fileInfo.chunks():  # 这是读取的方式
            readcontent.write(con);

    #当上传到服务器后，读取文件，并将信息保存到数据库中
    readUserInfomationFile(request , fileInfo.name);
    # 返回上传成功的信息
    return HttpResponse("成功");

def readUserInfomationFile(request , filename):
    #写服务器的上传过来的文件路径
    webFileName = os.path.join(settings.MEDIA_ROOT, filename)
    # 打开文件
    workbook = xlrd.open_workbook(r''+webFileName)
    # 获取所有sheet
    #workbook.sheet_names()
    #获取第一个sheet名字
    sheet2_name = workbook.sheet_names()[0]
    # 根据sheet索引或者名称获取sheet内容
    sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始，第一个sheet就是为0，因为一个excl表里面可以有多个sheet
    # sheet2 = workbook.sheet_by_name('sheet2') #这是直接通过名字进行获取

    # sheet的名称，行数，列数
    print (sheet2.name, sheet2.nrows, sheet2.ncols)

    # 获取指定的整行和整列的值（返回的是数组类型）
    rows = sheet2.row_values(3)  # 获取第四行内容
    cols = sheet2.col_values(2)  # 获取第三列内容
    print (rows)
    print (cols)

    # 获取指定某个单元格内容(三种方法)
    print (sheet2.cell(1, 0).value)
    print (sheet2.cell_value(1, 0))
    print (sheet2.row(1)[0].value)
    # 获取单元格内容的数据类型
    #ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
    print (sheet2.cell(1,0).ctype)
