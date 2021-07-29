from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from Flixer.models import *


def start(request, defaurg='ok'):
    return render(request, 'login.html', {'defAurg': defaurg})


def login(request):
    admin_id = 'admin'
    admin_pass = 'admin'
    if request.method == 'POST':
        login_id = request.POST.get('id')
        login_pass = request.POST.get('pass')

        if login_id == admin_id and login_pass == admin_pass:
            request.session['admin'] = True
            return render(request, 'admin.html')
        else:
            try:
                userObject = User.objects.filter(user_id=login_id).get()
                if userObject is None or userObject.password != login_pass:
                    return start(request, 'logged')
                else:
                    request.session['user'] = True
                    request.session['userId'] = login_id
                    return render(request, 'user.html')
            except Exception:
                return start(request, 'nouser')


# -------------------------------------Admin PART------------------------------- #

def userPage(request, added='no'):
    if request.session.get('admin', False):
        userData = User.objects.all()
        return render(request, 'admin_pages/usersData.html', {'userData': userData, 'added': added})
    else:
        return start(request)


def home(request):
    if request.session.get('admin', False):
        return render(request, 'admin.html')
    else:
        return start(request)


def moviePage(request, added='no'):
    if request.session.get('admin', False):
        moviesData = Movie.objects.all()
        return render(request, 'admin_pages/moviesData.html', {'moviesData': moviesData, 'added': added})
    else:
        return start(request)


def searchMovie(request):
    return HttpResponse(request.POST.get('search'))


def deleteUser(request):
    if request.session.get('admin', False):
        if request.method == 'POST':
            User.objects.filter(user_id=request.POST.get('user_id')).delete()
            return userPage(request, 'deleted')
    else:
        return start(request)


def addUser(request):
    if request.session.get('admin', False):
        if request.method == 'POST':
            new_user = User()
            new_user.user_id = request.POST.get('user_id')
            new_user.name = request.POST.get('user_name')
            new_user.password = request.POST.get('pass')
            new_user.email = request.POST.get('emaill')
            new_user.gender = request.POST.get('radio1')
            new_user.save()
            return userPage(request, 'yes')
    else:
        return start(request)


def editUser(request):
    if request.session.get('admin', False):
        if request.method == 'POST':
            new_user = User.objects.filter(user_id=request.POST.get('user_id1')).get()
            new_user.name = request.POST.get('user_name1')
            new_user.password = request.POST.get('pass1')
            new_user.email = request.POST.get('emaill1')
            new_user.gender = request.POST.get('rad')

            new_user.save()
            return userPage(request, 'updated')
    else:
        return start(request)


def addMovie(request):
    if request.session.get('admin', False):
        if request.method == 'POST':
            new_movie = Movie()
            new_movie.movie_id = request.POST.get('movie_id')
            new_movie.name = request.POST.get('movie_name')
            new_movie.link = request.POST.get('link')
            new_movie.year = request.POST.get('year1')
            new_movie.description = request.POST.get('des')

            new_movie.save()
            return moviePage(request, 'yes')
    else:
        return start(request)


def delMovie(request):
    if request.session.get('admin', False):
        if request.method == 'POST':
            Movie.objects.filter(movie_id=request.POST.get('movie_id')).delete()
            return moviePage(request, 'deleted')
    else:
        return start(request)


def editMovie(request):
    if request.session.get('admin', False):
        movie_object = Movie.objects.filter(movie_id=request.POST.get('movie_id')).get()
        return render(request, "admin_pages/editMovie.html", {'movie_obj': movie_object})
    else:
        return start(request)


def saveeditMovie(request):
    if request.session.get('admin', False):
        if request.method == 'POST':
            new_movie = Movie.objects.filter(movie_id=request.POST.get('movie_id')).get()
            new_movie.name = request.POST.get('movie_name')
            new_movie.link = request.POST.get('link')
            new_movie.year = request.POST.get('year1')
            new_movie.description = request.POST.get('des')

            new_movie.save()
            return moviePage(request, 'updated')
    else:
        return start(request)


def logoutadmin(request):
    try:
        del request.session['admin']
    except KeyError:
        pass
    return start(request)


# -------------------------------------USER PART------------------------------- #
def userHome(request, found='True'):
    if request.session.get('user', False):
        return render(request, 'user.html', {'found': found})
    else:
        return start(request)


def userLogout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return start(request)


def userProfile(request):
    if request.session.get('admin', False) or request.session.get('user', False):
        user_data = User.objects.filter(user_id=request.session['userId']).get()
        return render(request, 'user_pages/editUser.html', {'user_data': user_data})
    else:
        return start(request)


def saveUserEdit(request):
    if request.session.get('admin', False) or request.session.get('user', False):
        if request.method == 'POST':
            new_user = User.objects.filter(user_id=request.POST.get('user_id')).get()
            new_user.name = request.POST.get('user_name')
            new_user.password = request.POST.get('pass1')
            new_user.email = request.POST.get('email1')
            new_user.gender = request.POST.get('rad')

            new_user.save()
            return userHome(request)
    else:
        return start(request)


def movieSearch(request):
    if request.session.get('admin', False) or request.session.get('user', False):
        movie_name = request.POST.get('movie_name').lower()
        movieList = []

        for obj in Movie.objects.all():
            if obj.name.lower() == movie_name:
                movieList.append(obj)

        for obj in Movie.objects.all():
            if obj.name.split(' ')[0].lower() == movie_name.split(' ')[0]:
                if obj not in movieList:
                    movieList.append(obj)

        for obj in Movie.objects.all():
            if obj.name.split(' ')[0][0].lower() == movie_name.split(' ')[0][0]:
                if obj not in movieList:
                    movieList.append(obj)

        if len(movieList) != 0:
            rating_list = []
            total_users = []
            for obj in movieList:
                rating = Rating.objects.filter(movie_id=obj.movie_id).aggregate(Sum('rating_value'))
                total_user = Rating.objects.filter(movie_id=obj.movie_id).count()
                if rating['rating_value__sum'] is None:
                    rating_list.append(0)
                else:
                    avgrate = rating['rating_value__sum'] / (5 * total_user)
                    rating_list.append(avgrate)
                total_users.append(total_user)
            if len(movieList) == 1:
                found = True
            else:
                found = False

            zipped_List = zip(movieList, rating_list, total_users)
            return render(request, 'user_pages/movie_search.html', {'movie': zipped_List,
                                                                    'found': found})
        return userHome(request, 'False')
    else:
        return start(request)


def viewMovie(request):
    if request.session.get('admin', False) or request.session.get('user', False):
        if request.method == 'GET':
            new_movie = Movie.objects.filter(movie_id=request.GET.get('movieId')).get()
            rating = Rating.objects.filter(movie_id=new_movie.movie_id).aggregate(Sum('rating_value'))
            total_user = Rating.objects.filter(movie_id=new_movie.movie_id).count()
            if rating['rating_value__sum'] is None:
                rating_val = 0
            else:
                rating_val = rating['rating_value__sum'] / (5 * total_user)
            return render(request, 'user_pages/showMovie.html', {'movie': new_movie,
                                                                 'rating': rating_val,
                                                                 'total': total_user})
        else:
            return start(request)
    else:
        return start(request)
