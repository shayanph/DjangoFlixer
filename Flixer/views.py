from django.http import HttpResponse
from django.shortcuts import render

from Flixer.models import Movie


def start(request):
    return render(request, 'login.html')


def login(request):
    admin_id = 'admin'
    admin_pass = 'admin'
    if request.method == 'POST':
        login_id = request.POST.get('id')
        login_pass = request.POST.get('pass')
        
        if login_id == admin_id and login_pass == admin_pass:
            return render(request , 'admin.html')
        else:
            return HttpResponse('hello world')
