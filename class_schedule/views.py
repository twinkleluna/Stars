from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from commom.functions import get_checkchars, get_checkimg
from io import BytesIO
from django.contrib.auth.models import User
import json
import pymysql
# Create your views here.

# @login_required
def class_schedule(request):
    context = {}
    return render(request, 'class_schedule/new_timetable.html',context)

# @login_required
def get_schedule(request):
    # username=request.user.username
    username="Twinkle"
    weekday1=['','','','','','','','','','','','']
    weekday2=['','','','','','','','','','','','']
    weekday3=['','','','','','','','','','','','']
    weekday4=['','','','','','','','','','','','']
    weekday5=['','','','','','','','','','','','']
    weekday6=['','','','','','','','','','','','']
    weekday7=['','','','','','','','','','','','']

    if request.is_ajax():

       db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")

       cursor=db.cursor()

       order='select cno from selected_course where sname=\"'+username+"\";"
       print(order)

       try:
            cursor.execute(order)
            db.commit()
            rows=cursor.fetchall()
            print(rows)
       except:
            db.rollback()

       for row in rows:
           order_cname='select cname from course where cno='+(str)(row[0])+";"
           order_weekday='select weekday from course where cno=' + (str)(row[0]) + ";"
           order_start_time='select start_time from course where cno=' + (str)(row[0]) + ";"
           order_duration='select duration from course where cno=' + (str)(row[0]) + ";"
           order_classroom='select classroom from course where cno=' + (str)(row[0]) + ";"
           try:
               cursor.execute(order_cname)
               db.commit()
               cname=cursor.fetchall()
               cname=str(cname[0])
               cname=cname[2:-3]

               cursor.execute(order_weekday)
               db.commit()
               weekday=cursor.fetchall()
               weekday=str(weekday[0])
               weekday=weekday[2]
               print(weekday)

               cursor.execute(order_start_time)
               db.commit()
               start_time=cursor.fetchall()
               start_time=str(start_time[0])
               start_time=int(start_time[1:-2])

               cursor.execute(order_duration)
               db.commit()
               duration=cursor.fetchall()
               duration=str(duration[0])
               duration=int(duration[1:-2])

               cursor.execute(order_classroom)
               db.commit()
               classroom=cursor.fetchall()
               classroom=str(classroom[0])
               print(classroom)
           except:
               db.rollback()
           if weekday == '1':
              for num in range(1, 13):
                   if num in range(start_time,start_time+duration):
                       weekday1[num-1]=cname
           if weekday == '2':
               for num in range(1,13 ):
                   if num in range(start_time, start_time + duration):
                       weekday2[num - 1]=cname
           if weekday == '3':
               for num in range(1, 13):
                   if num in range(start_time, start_time + duration):
                       weekday3[num - 1]=cname
           if weekday == '4':
               for num in range(1, 13):
                   if num in range(start_time,start_time+duration):
                    weekday4[num-1]=cname
           if weekday == '5':
               for num in range(1, 13):
                   if num in range(start_time, start_time + duration):
                       weekday5[num - 1]=cname
           if weekday == '6':
               for num in range(1, 13):
                   if num in range(start_time, start_time + duration):
                       weekday6[num - 1]=cname
           if weekday == '7':
               for num in range(1, 13):
                   if num in range(start_time, start_time + duration):
                       weekday7[num - 1]=cname
       db.close()
       courseList=[weekday1, weekday2, weekday3, weekday4, weekday5,weekday6,weekday7]
       print(courseList)
       content=json.dumps(courseList)
       return HttpResponse(content)

# @login_required
def get_scheduleOther(request):
    if request.is_ajax():
       courseList=[
        ['', '', '', '', '毛概@14208', '毛概@14208', '', '', '', '选修', '', ''],
        ['大学英语(Ⅳ)@10203', '大学英语(Ⅳ)@10203', '', '', '模拟电子技术基础@16204', '模拟电子技术基础@16204', '', '', '', '', '', ''],
        ['', '', '信号与系统@11302', '信号与系统@11302', '', '', '电路、信号与系统实验', '电路、信号与系统实验', '', '', '', ''],
        ['形势与政策(Ⅳ)@15208', '形势与政策(Ⅳ)@15208', '', '', '电装实习@11301', '电装实习@11301', '', '', '', '大学体育', '大学体育', ''],
        ['大学体育(Ⅳ)', '大学体育(Ⅳ)', '', '', '数据结构与算法分析', '数据结构与算法分析', '', '', '信号与系统', '信号与系统', '', ''],
       ]
       content=json.dumps(courseList)
       return HttpResponse(content)

def new_class_schedule(request):
    context = {}
    return render(request, 'class_schedule/new_timetable.html',context)