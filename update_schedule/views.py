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

@login_required
def update_schedule(request):
    context = {}
    return render(request, 'update_schedule/update.html',context)

@login_required
def add_course(request):
    username=request.user.username
    # username="Twinkle"

    if request.method=='POST':

       db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
       cursor=db.cursor()

       cno=request.POST['cno']
       cname=request.POST['cname']
       teacher=request.POST['teacher']
       weekday=request.POST['weekday']
       lesson1=request.POST['lesson1']
       lesson2=request.POST['lesson2']
       lesson3=request.POST['lesson3']
       lesson4=request.POST['lesson4']

       order='select * from selected_course where sname=\'' + username + '\' and cno=' + cno + ';'
       print(order)

       try:
           cursor.execute(order)
           db.commit()
           has_chosen=cursor.fetchall()
           print(has_chosen)
       except:
           db.rollback()
           db.close()
           return HttpResponse('sorry,添加课程失败！')

       if has_chosen:
           db.rollback()
           db.close()
           return HttpResponse("sorry,您已添加该课程！")

       order1='insert into course(cno,cname,teacher,weekday,lesson1,lesson2,lesson3,lesson4) values('+cno+',\''+cname+'\',\''+teacher+'\','+weekday+','+lesson1+','+lesson2+','+lesson3+','+lesson4+");"
       print(order1)
       order2='insert into selected_course(sname,cno,cname) values (\''+username+'\','+cno+',\''+cname+'\');'
       print(order2)

       try:
           cursor.execute(order1)
           db.commit()
       except:
            db.rollback()
            db.close()
            return HttpResponse('sorry,添加课程失败！')

       try:
           cursor.execute(order2)
           db.commit()
       except:
            db.rollback()
            db.close()
            return HttpResponse('sorry,添加课程失败！')

       db.close()
       return HttpResponse('添加成功！')

@login_required
def sub_course(request):
    sname=request.user.username
    # sname="Twinkle"

    if request.method == 'POST':

        db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
        cursor=db.cursor()

        cno=request.POST['cno']

        order1='select * from selected_course where sname=\''+sname+'\' and cno='+cno+';'
        print(order1)

        try:
            cursor.execute(order1)
            db.commit()
            is_valid=cursor.fetchall()
            print(is_valid)
        except:
            db.rollback()
            db.close()
            return HttpResponse('sorry,删除课程失败！')

        if is_valid:
           order2='delete from selected_course where cno=' + cno + ' and sname=\'' + sname + '\';'
           print(order2)

           try:
             cursor.execute(order2)
             db.commit()
           except:
             db.rollback()
             db.close()
             return HttpResponse('sorry,删除课程失败！')

           order3='delete from course where cno=' + cno + ';'
           print(order3)

           try:
             cursor.execute(order3)
             db.commit()
           except:
             db.rollback()
             db.close()
             return HttpResponse('sorry,删除课程失败！')

           db.close()
           return HttpResponse('删除成功！')
        else:
            db.rollback()
            db.close()
            return HttpResponse('sorry,您并没有选择该课程！')