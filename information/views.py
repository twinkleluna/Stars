import os
import struct
import io
import json
import magic
from PIL import Image
import pymysql

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required()
def information(request):
    print('request', request.POST)
    if request.method == 'POST':
            sname=request.user.username
            # sname='Twinkle'
            sno=request.POST['sno']
            signature=request.POST.get('signature','')
            email=request.POST.get('email','')
            sex=request.POST['sex']

            db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
            cursor=db.cursor()

            order='insert into student(sname,sno,email,signature,sex) values(\'' +sname+ '\',' + sno + ',\'' + email + '\',\'' + signature + '\',\'' + sex + '\');'
            print(order)

            try:
                cursor.execute(order)
                db.commit()
                showinfo=cursor.fetchall()
            except:
                db.rollback()
                db.close()
                return HttpResponse('sorry,添加个人信息失败！')

            return render(request, 'information/information.html',{'information':showinfo} )

    else:
        sname=request.user.username
        print(sname)
        # sname='Twinkle'
        db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
        cursor=db.cursor()

        order='select * from student where sname=\''+sname+'\';'
        print(order)

        try:
            cursor.execute(order)
            db.commit()
            showinfo=cursor.fetchall()
            if showinfo:
                pass
            else:
                order='select * from student where sname=\'' + 'moren'+ '\';'
                print(order)
                cursor.execute(order)
                db.commit()
                showinfo=cursor.fetchall()
        except:
            db.rollback()

        db.close()
        print(showinfo[0])
        showinfo=showinfo[0]
        return render(request, 'information/information.html',{'sname':showinfo[0],'sno':showinfo[1],'email':showinfo[2],'signature':showinfo[3],'sex':showinfo[4],'photo':showinfo[5]} )

@csrf_exempt
def submitphoto(request):
    print('fileElementId', request.FILES)
    if request.method == 'POST':
        sname=request.user.username
        # sname='Twinkle'
        photo=request.FILES.get("submitphoto", None)  # 获取上传的文件，如果没有文件，则默认为None
        with open('C:\workspace\PythonProject\Stars\static\photos\\' + photo.name, 'wb') as f:
            for line in photo:
                f.write(line)
        type = magic.from_file('C:\workspace\PythonProject\Stars\static\photos\\' + photo.name, mime=True)
        content=json.dumps(type)
        type=content[1:-1]

        if type == "image/png" or type == "image/jpeg":
             db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
             cursor=db.cursor()

             order='select photo from student where sname=\''+ sname + '\';'
             print(order)
             cursor.execute(order)
             db.commit()
             repitition=cursor.fetchall()
             print(repitition)
             if repitition:
               repitition=repitition[0]
               if repitition[0]!=photo.name:
                try:
                    order='update student set photo=\'' + photo.name + '\' where sname=\'' + sname + '\';'
                    print(order)
                    cursor.execute(order)
                    db.commit()
                    result=cursor.fetchall()
                    print(result)
                except:
                    db.rollback()
                    db.close()
                    return HttpResponse('sorry,上传失败！')
                db.close()
                string = 0
                content = json.dumps(string)
                return HttpResponse(content)
               else:
                 db.close()
                 string=3
                 content=json.dumps(string)
                 return HttpResponse(content)
             else:
              db.close()
              string=2
              content=json.dumps(string)
              return HttpResponse(content)

        os.remove('C:\workspace\PythonProject\Stars\static\photos\\' + photo.name)
        string = "-1"
        content = json.dumps(string)
        return HttpResponse(content)
    else:
         return HttpResponse("wrong!")


@login_required
def ctf_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

