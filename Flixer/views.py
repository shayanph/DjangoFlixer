from django.http import HttpResponse
from django.shortcuts import render
from Flixer.models import *


def start(request):
    return render(request, 'login.html')


def login(request):
    admin_id = 'admin'
    admin_pass = 'admin'
    if request.method == 'POST':
        login_id = request.POST.get('id')
        login_pass = request.POST.get('pass')

        if login_id == admin_id and login_pass == admin_pass:
            return render(request, 'admin.html')
        else:
            return HttpResponse('hello world')


def userPage(request, added='no'):
    userData = User.objects.all()
    return render(request, 'admin_pages/usersData.html', {'userData': userData, 'added': added})


def home(request):
    return render(request, 'admin.html')


def moviePage(request):
    return render(request, 'admin_pages/moviesData.html')


def searchMovie(request):
    return HttpResponse(request.POST.get('search'))


def deleteUser(request):
    if request.method == 'POST':
        User.objects.filter(user_id=request.POST.get('user_id')).delete()
        return userPage(request, 'deleted')


def addUser(request):
    if request.method == 'POST':
        new_user = User()
        new_user.user_id = request.POST.get('user_id')
        new_user.name = request.POST.get('user_name')
        new_user.password = request.POST.get('pass')
        new_user.email = request.POST.get('emaill')
        new_user.gender = request.POST.get('radio1')
        new_user.save()
        return userPage(request, 'yes')


def editUser(request):
    if request.method == 'POST':
        new_user = User.objects.filter(user_id=request.POST.get('user_id1')).get()
        new_user.name = request.POST.get('user_name1')
        new_user.password = request.POST.get('pass1')
        new_user.email = request.POST.get('emaill1')
        new_user.gender = request.POST.get('rad')

        new_user.save()
        return userPage(request, 'updated')
