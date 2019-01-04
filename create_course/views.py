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
def show(request):
    if request.method=='GET':
        # username=request.user.username
        username="Twinkle"
        if username=='Twinkle':
            context = {}
            return render(request, 'create_course/create_course.html',context)
        else:
            return HttpResponse("sorry,您不是管理员，没有权限修改课程数据库~")
    else:
        return HttpResponse("???")

# @login_required
def add_course(request):
    if request.method=='POST':
        # username=request.user.username
        username="Twinkle"
    else:
        return HttpResponse("???")

    if username=='Twinkle':
        cname=request.POST['cname']
        weekday=request.POST['weekday']
        start_time=request.POST['start_time']
        duration=request.POST['duration']
        classroom=request.POST['classroom']
        teacher=request.POST['teacher']

        db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
        cursor=db.cursor()

        order="select * from teachers where tname=\'"+teacher+"\';"
        print(order)
        try:
            cursor.execute(order)
            db.commit()
            has_teacher=cursor.fetchall()
            print(has_teacher)
        except:
            db.rollback()
            db.close()
            return HttpResponse('sorry,添加失败！')
        if has_teacher:
            pass
        else:
            db.rollback()
            db.close()
            return HttpResponse("Sorry,没有这个老师~")

        order1="select * from course where teacher=\'"+teacher+"\' and weekday="+weekday+" and cname=\'"+cname+"\';"
        print(order1)
        try:
            cursor.execute(order1)
            db.commit()
            free_teacher=cursor.fetchall()
            print(free_teacher)
        except:
            db.rollback()
            db.close()
            return HttpResponse('sorry,添加失败！')
        if free_teacher:
            db.rollback()
            db.close()
            return HttpResponse("Sorry,"+teacher+"老师周"+weekday+"已经有"+cname+"课了哦~")
        else:
            pass

        order2="select * from course where classroom=\'"+classroom+"\' and weekday="+weekday+";"
        print(order2)
        try:
            cursor.execute(order2)
            db.commit()
            course_classroom=cursor.fetchall()
            print(course_classroom)
        except:
            db.rollback()
            db.close()
            return HttpResponse('sorry,添加失败！')
        if course_classroom:
            for row in course_classroom:
                print(row[4])
                print( int(start_time) + int(duration) -int(1))
                print(start_time)
                print(row[4] + row[5] - 1)
                print(int(row[4]) > int(start_time)+int(duration)-int(1))
                print( int(row[4])+int(row[5])-1 < int(start_time))
                if int(row[4]) > int(start_time)+int(duration)-1 or int(row[4])+int(row[5])-1 < int(start_time):
                    pass
                else:
                    db.rollback()
                    db.close()
                    return HttpResponse("Sorry,周"+weekday+"这节课的classroom"+classroom+"已经被占用了哦~")
        else:
            pass

        order3="insert into course(cname,teacher,weekday,start_time,duration,classroom) values("+"\'"+cname+"\',\'"+teacher+"\',"\
               +weekday+","+start_time+","+duration+",\'"+classroom+"\');"
        print(order3)
        try:
            cursor.execute(order3)
            db.commit()
            insert=cursor.fetchall()
            print(insert)
        except:
            db.rollback()
            db.close()
            return HttpResponse('sorry,添加失败！')
        db.rollback()
        db.close()
        return HttpResponse("OK,添加成功！")

# @login_required
def delete_course(request):
    if request.method=='POST':
        # username=request.user.username
        username="Twinkle"
    else:
        return HttpResponse("???")

    if username=='Twinkle':
        cno=request.POST['cno']

        db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
        cursor=db.cursor()

        order="select * from course where cno="+cno+";"
        print(order)
        try:
            cursor.execute(order)
            db.commit()
            valid_course=cursor.fetchall()
            print(valid_course)
        except:
            db.rollback()
            db.close()
            return HttpResponse('sorry,删除失败！')
        if valid_course:
            pass
        else:
            db.rollback()
            db.close()
            return HttpResponse("Sorry,没有这个课~")

        order1="delete from course where cno="+cno+";"
        print(order1)
        try:
            cursor.execute(order1)
            db.commit()
            db.rollback()
            db.close()
            return HttpResponse("OK,删除成功~")
        except:
            db.rollback()
            db.close()
            return HttpResponse('sorry,删除失败！')