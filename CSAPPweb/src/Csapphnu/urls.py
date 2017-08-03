from django.conf.urls import url,include;
from . import  views
from . import stugroupviews
from . import modifiinfoviews

urlpatterns = [
    url(r'^assistantmanage/$' , views.managerAssistantInfo),  #教师管理助教信息
    url(r'^addassistantinfodb/$' , views.addInfo),  #添加助教信息
    url(r'^deletassistantinfodb/$' , views.deleteInfo), #删除助教信息
    url(r'^updataassistantinfodb/$', views.updataInfo),  # 更新助教信息
    url(r'^studentgrouping/$' , stugroupviews.studentgrouping),  #学生分组
    url(r'^studentgroupindodb/$' , stugroupviews.studentGrounpToDB), #学生分组信息数据库管理
    url(r'^studentclassandname/$' , stugroupviews.reloadStudentClassAndName), #ajax请求刷新班级和学生的名单
    url(r'^modifyuserinfo/$' , modifiinfoviews.modifyUserInfo), #用户修改个人信息
    url(r'^logininforegester/$' , modifiinfoviews.updateinfo), #更新用户提交过来的个人信息修改
    url(r'^userinfomanage/$', views.jumptoeverymodel), #跳转到各个模块
    url(r'^usertypeverification/$' , views.userTypeVerification), #验证用户的权限是否能够跳转到相应的页面
    url(r'^requestclassnumber/$' , views.getTeacherBelongClass), #ajax请求得到当前登录老师所带的班级信息
]