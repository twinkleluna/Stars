from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from commom.functions import get_checkchars, get_checkimg
from io import BytesIO
from django.contrib.auth.models import User


# Create your views here.
def ctf_login(request):
    redirect_to = request.POST.get('next', request.GET.get('next', '/information/information'))

    context = {'next': redirect_to}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        checkcode = request.POST['checkcode']

        if request.session['checkcode'] == "":
            return HttpResponse('Check code time out!')
        elif request.session['checkcode'].upper() != checkcode.upper():
            request.session['checkcode'] = ""
            return HttpResponse('Wrong check code!')

        # 验证密码
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponse(username + ' is not active')
        else:
            return HttpResponse("Invalid user")
    return render(request, 'board/login.html',context)

def ctf_checkimg(request):
    code = get_checkchars()
    checkimg = get_checkimg(code)
    bytes = BytesIO()
    checkimg.save(bytes, 'PNG')
    request.session['checkcode'] = code
    return HttpResponse(bytes.getvalue())


@login_required
def ctf_logout(request):
    logout(request)
    return HttpResponseRedirect('/board/login')


def ctf_register(request):
    redirect_to = '/board/login'

    context = {'next': redirect_to}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        checkcode = request.POST['checkcode']
        check_password=request.POST['check_password']
        sno=request.POST['sno']

        if request.session['checkcode'] == "":
            return HttpResponse('Check code time out!')
        elif request.session['checkcode'].upper() != checkcode.upper():
            request.session['checkcode'] = ""
            return HttpResponse('Wrong check code!')

        # 验证密码
        flag = (check_password == password)
        print(flag)

        if(flag):
            registAdd = User.objects.create_user(username=username, password=password)
        else:
            return HttpResponse("Sorry,两次密码不一致~")

        print(registAdd)

        if registAdd :
            import pymysql
            db=pymysql.connect("140.143.234.60", "Db_team", "TikoTiko", "Class_Schedule")
            cursor=db.cursor()

            order='insert into student(sname,sno) values(\'' + username + '\','+sno+');'
            print(order)
            try:
                cursor.execute(order)
                db.commit()
                is_valid=cursor.fetchall()
                print(is_valid)
            except:
                db.rollback()
                db.close()
                return HttpResponse('sorry,登陆失败！')
            return HttpResponseRedirect(redirect_to)
        else:
            return HttpResponse("Invalid user")
    return render(request, 'board/register.html',context)
