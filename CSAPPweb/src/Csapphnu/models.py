from django.db import models
from mongoengine import *
#from CSAPPweb.settings import DBNAME


#连接数据库的名字
#connect(DBNAME)

class TeachersAssistantInfo(Document):
    #老师姓名
    teacher_name = StringField(max_length=120, required=True);
    #助教姓名
    assistant_name = StringField(max_length=120, required=True);
    # 助教学号
    assistant_number = StringField(max_length=120, required=True);
    #助教班级
    class_number = StringField(max_length=120, required=True);
    class Meta:
        db_table = 'TeachersAssistantInfo';

#学生分组的表
class StudentGrounp(Document):
    # 学生姓名
    student_name = StringField(max_length=30, required=True);
    # 学生学号
    student_number = StringField(max_length=20, required=True);
    # 学生班级
    student_class = StringField(max_length=20, required=True);
    #学生所属的小组
    student_grounp = StringField(max_length=10);
    class Meta:
        db_table = 'StudentGrounp';
    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

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
