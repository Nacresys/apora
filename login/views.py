from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect
from login.models import userreg
# Create your views here.

def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        try:
            check_user = userreg.objects.get(uname=user, pwd=password)
            request.session['user'] = str(check_user.uname)
            request.session['user_id'] = str(check_user.id)
            request.session['role'] = str(check_user.role_id)
            role_id = request.session['role']
            userid = check_user.id
            cc = connection.cursor()
            cc.execute("call login('" + str(userid) + "')")
            try:
                if role_id == '2':
                    return redirect('supervisor:supervisor_login')
                elif role_id == '3':
                    return redirect('picker:picker_login')
                else:
                    return redirect('home')
            except:
                messages.error(request, 'Sorry, You were not assigned a role!!')
        except:
            messages.error(request, 'Please enter valid Username and Password !!!')
    return render(request,"login.html")