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

    weekday_table=[
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""]
    ]

    if request.is_ajax():

       db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
       cursor=db.cursor(cursor=pymysql.cursors.DictCursor)
       order='select cno from selected_course where sname=\"'+username+"\" and D_S='D';"
       print(order)

       try:
            cursor.execute(order)
            db.commit()
            rows=cursor.fetchall()
            print(rows)
       except:
            db.rollback()

       for row in rows:

           cSQL = "SELECT * FROM course WHERE cno=" + str(row['cno']) + ";"
           try:
               cursor.execute(cSQL)
               db.commit()
               con = cursor.fetchall()
               print(con)
               cname = con[0]['cname']
               weekday = con[0]['weekday']
               start_time = con[0]['start_time']
               duration = con[0]['duration']
               classroom = con[0]['classroom']


           except:
               db.rollback()

           for num in range(1, 13):
               if num in range(start_time, start_time + duration):
                   weekday_table[int(weekday)-1][num - 1] = cname+'('+classroom+')'

       db.close()
       print(weekday_table)
       content = json.dumps(weekday_table)
       return HttpResponse(content)

# @login_required
def get_scheduleOther(request):
    # username=request.user.username
    username="Twinkle"

    weekday_table=[
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", ""]
    ]

    if request.is_ajax():

       db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
       cursor=db.cursor(cursor=pymysql.cursors.DictCursor)
       order='select cno from selected_course where sname=\"'+username+"\" and D_S='S';"
       print(order)

       try:
            cursor.execute(order)
            db.commit()
            rows=cursor.fetchall()
            print(rows)
       except:
            db.rollback()

       for row in rows:

           cSQL = "SELECT * FROM course WHERE cno=" + str(row['cno']) + ";"
           try:
               cursor.execute(cSQL)
               db.commit()
               con = cursor.fetchall()
               print(con)
               cname = con[0]['cname']
               weekday = con[0]['weekday']
               start_time = con[0]['start_time']
               duration = con[0]['duration']
               classroom = con[0]['classroom']


           except:
               db.rollback()

           for num in range(1, 13):
               if num in range(start_time, start_time + duration):
                   weekday_table[int(weekday)-1][num - 1] = cname+'('+classroom+')'

       db.close()
       print(weekday_table)
       content = json.dumps(weekday_table)
       return HttpResponse(content)

def new_class_schedule(request):
    context = {}
    return render(request, 'class_schedule/new_timetable.html',context)