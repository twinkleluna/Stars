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
    return render(request, 'class_schedule/timetable.html',context)

# @login_required
def get_schedule(request):
    # username=request.user.username
    username="Twinkle"
    weekday1=['','','','','','','','','','','','']
    weekday2=['','','','','','','','','','','','']
    weekday3=['','','','','','','','','','','','']
    weekday4=['','','','','','','','','','','','']
    weekday5=['','','','','','','','','','','','']

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
           order_lesson1='select lesson1 from course where cno=' + (str)(row[0]) + ";"
           order_lesson2='select lesson2 from course where cno=' + (str)(row[0]) + ";"
           order_lesson3='select lesson3 from course where cno=' + (str)(row[0]) + ";"
           order_lesson4='select lesson4 from course where cno=' + (str)(row[0]) + ";"
           order_teacher='select teacher from course where cno=' + (str)(row[0]) + ";"
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

               cursor.execute(order_lesson1)
               db.commit()
               lesson1=cursor.fetchall()
               lesson1=str(lesson1[0])
               lesson1=int(lesson1[1:-2])

               cursor.execute(order_lesson2)
               db.commit()
               lesson2=cursor.fetchall()
               lesson2=str(lesson2[0])
               lesson2=int(lesson2[1:-2])

               cursor.execute(order_lesson3)
               db.commit()
               lesson3=cursor.fetchall()
               lesson3=str(lesson3[0])
               lesson3=int(lesson3[1:-2])

               cursor.execute(order_lesson4)
               db.commit()
               lesson4=cursor.fetchall()
               lesson4=str(lesson4[0])
               lesson4=int(lesson4[1:-2])

               cursor.execute(order_teacher)
               db.commit()
               teacher=cursor.fetchall()
               teacher=str(teacher[0])
               print(teacher)
           except:
               db.rollback()
           if weekday=='1':
              for num in range(1, 13):
                 if lesson1 == num or num == lesson2 or num == lesson3 or num == lesson4:
                    weekday1[num-1]=cname
           if weekday == '2':
               for num in range(1,13 ):
                 if lesson1 == num or num == lesson2 or num == lesson3 or num == lesson4:
                      weekday2[num-1]=cname
           if weekday == '3':
               for num in range(1, 13):
                   if lesson1==num or num == lesson2 or num == lesson3 or num == lesson4:
                       weekday3[num-1]=cname
           if weekday == '4':
               for num in range(1, 13):
                   if lesson1 == num or num == lesson2 or num == lesson3 or num == lesson4:
                       weekday4[num - 1]=cname
           if weekday == '5':
               for num in range(1, 13):
                   if lesson1 == num or num == lesson2 or num == lesson3 or num == lesson4:
                       weekday5[num-1]=cname
       db.close()
       courseList=[weekday1, weekday2, weekday3, weekday4, weekday5]
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