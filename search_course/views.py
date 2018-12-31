from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from io import BytesIO
from django.contrib.auth.models import User
import pymysql
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# @login_required
def search_static(request):
    context = {}
    return render(request, 'search_course/search_static.html',context)

def search_teacher(request):
    teacher=request.POST.get('teacher')
    print(teacher)

    if teacher:
        db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
        cursor=db.cursor()

        order='select * from course where teacher=\'' + teacher + '\';'
        print(order)

        try:
            cursor.execute(order)
            db.commit()
            rows=cursor.fetchall()
            print(rows)
        except:
            db.rollback()
            db.close()
            return HttpResponse("Sorry,查询失败！")

        num=0
        if rows:
          showinfo=dict()
          showinfo['cno']=[]
          showinfo['cname']=[]
          showinfo['weekday']=[]
          showinfo['start_time']=[]
          showinfo['duration']=[]
          showinfo['classroom']=[]
          for row in rows:
            showinfo['cno'].append(row[0])
            showinfo['cname'].append(row[1])
            showinfo['weekday'].append(row[3])
            showinfo['start_time'].append(row[4])
            showinfo['duration'].append(row[5])
            showinfo['classroom'].append(row[6])
            print(showinfo)
            num+=1
        else:
            db.rollback()
            db.close()
            return HttpResponse("Sorry,没有该老师的课！")

        db.close()
        return render(request, 'search_course/search_static.html', {'showinfo': showinfo})
    else:
        return HttpResponse("请输入任课教师！")

def search_classroom(request):
    classroom=request.POST.get('classroom')
    print(classroom)

    if classroom:
        db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
        cursor=db.cursor()

        order='select * from course where classroom=\'' + classroom + '\';'
        print(order)

        try:
            cursor.execute(order)
            db.commit()
            rows=cursor.fetchall()
            print(rows)
        except:
            db.rollback()
            db.close()
            return HttpResponse("Sorry,查询失败！")

        num=0
        if rows:
          showinfo=dict()
          showinfo['cno']=[]
          showinfo['cname']=[]
          showinfo['teacher']=[]
          showinfo['weekday']=[]
          showinfo['start_time']=[]
          showinfo['duration']=[]
          for row in rows:
            showinfo['cno'].append(row[0])
            showinfo['cname'].append(row[1])
            showinfo['teacher'].append(row[2])
            showinfo['weekday'].append(row[3])
            showinfo['start_time'].append(row[4])
            showinfo['duration'].append(row[5])
            print(showinfo)
            num+=1
        else:
            db.rollback()
            db.close()
            return HttpResponse("Sorry,没有该教室的课！")

        db.close()
        return render(request, 'search_course/search_static.html', {'showinfo': showinfo})
    else:
        return HttpResponse("请输入上课教室！")


def search_data(request):
    month=request.POST.get('month')
    day=request.POST.get('day')
    print(month+' '+day)

    if month and day:
        db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
        cursor=db.cursor()

        import datetime;
        weekday=datetime.datetime(2018, int(month), int(day)).strftime("%w");
        print(weekday)
        order='select * from course where weekday=\'' + weekday+ '\';'
        print(order)

        try:
            cursor.execute(order)
            db.commit()
            rows=cursor.fetchall()
            print(rows)
        except:
            db.rollback()
            db.close()
            return HttpResponse("Sorry,查询失败！")

        num=0
        if rows:
          showinfo=dict()
          showinfo['cno']=[]
          showinfo['cname']=[]
          showinfo['teacher']=[]
          showinfo['start_time']=[]
          showinfo['duration']=[]
          showinfo['classroom']=[]
          for row in rows:
            showinfo['cno'].append(row[0])
            showinfo['cname'].append(row[1])
            showinfo['teacher'].append(row[2])
            showinfo['start_time'].append(row[4])
            showinfo['duration'].append(row[5])
            showinfo['classroom'].append(row[6])
            print(showinfo)
            num+=1
        else:
            db.rollback()
            db.close()
            return HttpResponse("Sorry,该日期没有课！")

        db.close()
        return render(request, 'search_course/search_static.html', {'showinfo': showinfo})
    else:
        return HttpResponse("请输入月份和日期！")
