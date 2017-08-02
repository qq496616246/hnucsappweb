#coding=UTF-8
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import time

def classSchedule(request) :
    return render(request, "ClassSchedule/classSchedule.html")

def ajaxQuery(request):
#     currenttime=time.time()
#     date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
#     Messages(timeStamp=currenttime, publish_date=date, publisher=request.session.get("name",None),
#         message_to='s123', message_type=int((request.GET['opt'])[-1]), message_content='dhhhhhhh',
#             is_valid=True).save()
    if request.is_ajax():
        opt=int(request.GET['opt'])
        data={'opt':'s'}
        
        if opt==1:
            messages=Messages.objects(message_type=opt).order_by('-timeStamp')
            i=1
            for message in messages:
                getter=message["message_to"]
                if (getter=='all'  or getter==request.session.get("student_class_name",-1)\
                    or getter==request.session.get("uid",-1) or (getter in (request.session.get("teacher_class_name",[]))))\
                        and message["is_valid"] :
                    data[i]=message["publish_date"]+":"+message["message_content"]
                    i+=1
                    
        elif request.session.get("permission",-1)==3 :
            messages=Messages.objects(message_type=opt).order_by('timeStamp')
            i=1
            data['opt']='t'
            class_collection=request.session.get("teacher_class_name",[])
            for tmp_class in class_collection:
                data[tmp_class]={}
            for message in messages:
                getter=message["message_to"]
                if (getter in class_collection) and message["is_valid"] :
                    data[getter][i]=message["message_content"]
                    i+=1
                    
        else :
            messages=Messages.objects(message_type=opt).order_by('timeStamp')
            i=1
            for message in messages:
                getter=message["message_to"]
                if getter==request.session.get("student_class_name",-1) and message["is_valid"] :
                    data[i]=message["message_content"]
                    i+=1
            
        print(data)
        return JsonResponse(data)
    
def ajaxQuery2(request):
    permission=request.session.get("permission",-1)
    if request.is_ajax() and (permission in [2,3,4]):
        opt=int(request.GET['opt'])
        data={"class_name":[],"message":[]}
        
        if opt==1:
            if permission==2:
                data["class_name"]=[request.session.get("student_class_name",-1)]
                messages=Messages.objects(publisher=request.session.get("uid",None)).order_by('timeStamp')
                for message in messages:
                    if message["message_type"]==opt:
                        data["message"].append(message["publish_date"]+"#"+message["message_to"]+"@内容："+message["message_content"])
            elif permission==3:
                teacher_class_name=request.session.get("teacher_class_name",[])
                teacher_class_name.append("all(自己所带的小班课的所有班)")
                teacher_class_name.append("all(上大班课的所有班)")
                data["class_name"]=teacher_class_name
                teacher_class_name.append("all")
                messages=Messages.objects(message_type=opt).order_by("timeStamp")
                for message in messages:
                    if message["message_to"] in teacher_class_name :
                        data["message"].append(message["publish_date"]+"#"+message["message_to"]+"@内容："+message["message_content"])
            else:
                pass
        
        else:
            if permission==2:
                class_tmp=request.session.get("student_class_name",-1)
                data["class_name"]=[class_tmp]
                messages=Messages.objects(message_type=opt).order_by('timeStamp')
                for message in messages:
                    if message['message_to']==class_tmp:
                        data["message"].append(message["message_to"]+"@"+message["message_content"])
            elif permission==3:
                teacher_class_name=request.session.get("teacher_class_name",[])
                teacher_class_name.append("all(自己所带的小班课的所有班)")
                data["class_name"]=teacher_class_name
                messages=Messages.objects(message_type=opt).order_by("timeStamp")
                for message in messages:
                    if message["message_to"] in teacher_class_name :
                        data["message"].append(message["message_to"]+"@"+message["message_content"])
            
            else:
                pass
            
        print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({"class":{},"message":{"权限错误"}})