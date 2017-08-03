from django.db import models
from mongoengine import *

class User(Document):
    uid = StringField(max_length=12)  # 用户id（学号/工号）
    psw = StringField(max_length=12)  # 用户密码
    name = StringField(max_length=12)  # 用户姓名
    permission = IntField()  # 用户身份：1—学生；2—助教；3—老师；4—管理员；
    student_class_name = StringField(max_length=12)  # 学生和助教所在班级，老师为空；
    teacher_class_name = ListField()  # 老师所带班级的列表，学生助教为空；
    assisant_info = DictField()  # 老师所带助教的列表，学生助教为空；
    contact = StringField(max_length=30)  # 联系方式；
    is_valid = BooleanField()  # True表示是该学期有效用户，False表示往学期的无效用户；
    student_grounp = StringField(max_length=10);   #学生分组信息
    class Meta:
        db_table = 'User';
