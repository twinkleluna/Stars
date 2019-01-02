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
def update_schedule(request):
    context = {}
    return render(request, 'update_schedule/new_update.html',context)

# @login_required
def add_course(request):
    # username=request.user.username
    username="Twinkle"

    if request.method=='POST':

        db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
        cursor=db.cursor()

        cno=request.POST['cno']
        D_S=request.POST['optionsRadios']
        print(D_S)

        if D_S!='DS':
            order='select * from selected_course where sname=\'' + username + '\' and cno=' + cno + ' and D_S=\''+D_S+'\';'
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

            order1='select * from course where cno=' + cno + ';'
            print(order1)
            try:
                cursor.execute(order1)
                db.commit()
                is_valid=cursor.fetchall()
                print(is_valid)
            except:
                db.rollback()
                db.close()
                return HttpResponse('sorry,添加课程失败！')
            if is_valid:
                pass
            else:
                db.rollback()
                db.close()
                return HttpResponse("sorry,不存在此课程！")
            order2='insert into selected_course(sname,cno,D_S) values (\''+username+'\','+cno+',\''+D_S+'\');'
            print(order2)
            try:
                cursor.execute(order2)
                db.commit()
            except:
                db.rollback()
                db.close()
                return HttpResponse('sorry,添加课程失败！')
            db.close()
            return HttpResponse('添加成功！')
        else:
            order1="select * from selected_course where sname=\'" + username + "\'"+" and cno=" + cno + " and D_S='D';"
            print(order1)
            cursor.execute(order1)
            db.commit()
            has_danzhou=cursor.fetchall()
            print(has_danzhou)

            order2="select * from selected_course where sname=\'" + username + "\'" + " and cno=" + cno + " and D_S='S';"
            print(order2)
            cursor.execute(order2)
            db.commit()
            has_shuangzhou=cursor.fetchall()
            print(has_shuangzhou)
            if has_danzhou and has_shuangzhou:
                db.close()
                return HttpResponse('您已添加该课程！')
            elif has_danzhou:
                order3="insert into selected_course(sname,cno,D_S) values (\'" + username + "\'," + cno + ",'S');"
                print(order3)
                cursor.execute(order3)
                db.commit()
                db.close()
                return HttpResponse('添加成功！')
            elif has_shuangzhou:
                order4="insert into selected_course(sname,cno,D_S) values (\'" + username + "\'," + cno + ",'D');"
                print(order4)
                cursor.execute(order4)
                db.commit()
                db.close()
                return HttpResponse('添加成功！')
            else:
                order3="insert into selected_course(sname,cno,D_S) values (\'" + username + "\'," + cno + ",'S');"
                order4="insert into selected_course(sname,cno,D_S) values (\'" + username + "\'," + cno + ",'D');"
                print(order3)
                print(order4)
                cursor.execute(order3)
                cursor.execute(order4)
                db.commit()
                db.close()
                return HttpResponse('添加成功！')

# @login_required
def sub_course(request):
    # sname=request.user.username
    sname="Twinkle"

    if request.method == 'POST':

        db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
        cursor=db.cursor()

        cno=request.POST['cno']
        D_S=request.POST['optionsRadios']
        print(D_S)

        if D_S!='DS':
            order1='select * from selected_course where sname=\'' + sname + '\' and cno=' + cno + ' and D_S=\''+D_S+'\';'
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
                order2='delete from selected_course where cno=' + cno + ' and sname=\'' + sname + '\' and D_S=\'' + D_S + '\';'
                print(order2)
                try:
                    cursor.execute(order2)
                    db.commit()
                    db.close()
                    return HttpResponse('删除成功！')
                except:
                    db.rollback()
                    db.close()
                    return HttpResponse('sorry,删除课程失败！')
            else:
                db.rollback()
                db.close()
                return HttpResponse('sorry,您并没有选择该课程！')
        else:
            order1="select * from selected_course where sname=\'" + sname + "\' and cno=" + cno + " and D_S='D';"
            print(order1)
            cursor.execute(order1)
            db.commit()
            has_danzhou=cursor.fetchall()
            print(has_danzhou)

            order2="select * from selected_course where sname=\'" + sname + "\' and cno=" + cno + " and D_S='S';"
            print(order2)
            cursor.execute(order2)
            db.commit()
            has_shuangzhou=cursor.fetchall()
            print(has_shuangzhou)
            if has_danzhou and has_shuangzhou:
                order3="delete from selected_course where cno="+ cno + " and sname=\'" + sname + "\' and D_S= 'D';"
                order4="delete from selected_course where cno="+ cno + " and sname=\'" + sname + "\' and D_S= 'S';"
                print(order3)
                print(order4)
                cursor.execute(order3)
                cursor.execute(order4)
                db.commit()
                db.close()
                return HttpResponse('删除成功！')
            elif has_danzhou:
                order3="delete from selected_course where cno="+ cno + " and sname=\'" + sname + "\' and D_S= 'S';"
                print(order3)
                cursor.execute(order3)
                db.commit()
                db.close()
                return HttpResponse('删除成功！')
            elif has_shuangzhou:
                order4="delete from selected_course where cno="+ cno + " and sname=\'" + sname + "\' and D_S= 'D';"
                print(order4)
                cursor.execute(order4)
                db.commit()
                db.close()
                return HttpResponse('删除成功！')
            else:
                db.close()
                return HttpResponse('您并未添加该课程！')

