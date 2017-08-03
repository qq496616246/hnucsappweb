from django.conf.urls import url, include
from . import views

urlpatterns = [
 url(r'^csappstudentmanage/$' , views.showFunciton),#显示管理员功能
 url(r'^addinfomationuser/$' , views.addUserInfomation), #批量添加用户的信息（学生，老师，管理员）
 url(r'^regesterinfo/$' ,views.regesterUserInfoSigle),#单个添加用户信息
 url(r'^changepagesize/$', views.changepagesize), #选择分页的页面大小发生变化
 url(r'^changepagenumber/$' , views.changepagenumber) #选择分页的页面索引发生变化
]