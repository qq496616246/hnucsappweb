#coding=UTF-8
from mongoengine import *

# Create your models here.
class Messages(Document):
    timeStamp=FloatField()  #时间戳
    publish_date=StringField(max_length=20)    #发布日期
    publisher=StringField(max_length=12)    #发布者
    message_to=StringField(max_length=12)   #消息对象：用户ID（面向单个用户），班级（面向单个班级），all（所有人）
    message_type=IntField() #消息类型：1—课程通知；2—讨论课安排；3—实验课安排；4—大班课安排；
    message_content=StringField(max_length=500) #消息内容
    is_valid=BooleanField() #消息是否过期