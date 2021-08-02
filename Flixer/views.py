from django.db.models import Sum
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
                    return userHome(request)
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
        categories = Category.objects.all()
        return render(request, 'admin_pages/moviesData.html', {'moviesData': moviesData,
                                                               'added': added,
                                                               'categories': categories})
    else:
        return start(request)


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
            new_movie.category = Category.objects.filter(category_id=request.POST.get('select1')).get()
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
        categories = Category.objects.all()
        return render(request, "admin_pages/editMovie.html", {'movie_obj': movie_object,
                                                              'categories': categories})
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
            new_movie.category = Category.objects.filter(category_id=request.POST.get('select1')).get()
            new_movie.save()
            return moviePage(request, 'updated')
    else:
        return start(request)


def addCat(request):
    if request.session.get('admin', False):
        if request.method == 'POST':
            catname = request.POST.get('category')
            category = Category()
            category.cat_name = catname

            category.save()

            return moviePage(request)


def logoutadmin(request):
    try:
        del request.session['admin']
    except KeyError:
        pass
    return start(request)


# -------------------------------------USER PART------------------------------- #
def userHome(request, found='True'):
    if request.session.get('user', False):
        movies = Movie.objects.all()
        ratings = []
        users = []
        for obj in movies:
            total = findRating(obj.movie_id)
            total_user = Rating.objects.filter(movie_id=obj.movie_id).count()
            users.append(total_user)
            if total == 0:
                ratings.append(0)
            else:
                avgrate = total / total_user
                ratings.append(avgrate)

        zippedlist = zip(movies, users, ratings)
        zippedlist = sorted(zippedlist, key=lambda x: x[len(x) - 1], reverse=True)

        if len(zippedlist) < 10:
            sliced = zippedlist
        else:
            sliced = zippedlist[0:10]
        category = Category.objects.all()
        return render(request, 'user.html', {'found': found, 'moviesTop': sliced, 'categories': category})
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


def findRating(movie):
    total = 0
    for i in range(5):
        total_user_rating = Rating.objects.filter(movie_id=movie,
                                                  rating_value=i + 1).count()
        if total_user_rating == 0:
            rating_val = 0
        else:
            rating_val = (i + 1) * total_user_rating
        total = total + rating_val

    return total


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
                total = findRating(obj.movie_id)
                total_user = Rating.objects.filter(movie_id=obj.movie_id).count()

                if total == 0:
                    rating_list.append(0)
                    total_users.append(total_user)
                else:
                    avgrate = total / total_user
                    rating_list.append(avgrate)
                    total_users.append(total_user)
            if len(movieList) >= 1:
                found = True
            else:
                found = False

            zipped_List = zip(movieList, rating_list, total_users)
            category = Category.objects.all()

            return render(request, 'user_pages/movie_search.html', {'movie': zipped_List,
                                                                    'found': found,
                                                                    'categories': category})
        return userHome(request, 'False')
    else:
        return start(request)


def viewMovie(request):
    if request.session.get('admin', False) or request.session.get('user', False):
        if request.method == 'GET':
            new_movie = Movie.objects.filter(movie_id=request.GET.get('movieId')).get()
            rating = Rating.objects.filter(movie_id=new_movie.movie_id).aggregate(Sum('rating_value'))
            total_user = Rating.objects.filter(movie_id=new_movie.movie_id).count()
            user_rating = Rating.objects.filter(movie_id=new_movie.movie_id,
                                                user_id=request.session['userId']).count()
            if user_rating == 0:
                user_rating = 0
            else:
                user_rating = Rating.objects.filter(movie_id=new_movie.movie_id,
                                                    user_id=request.session['userId']).get().rating_value
            total = findRating(new_movie.movie_id)

            total_user = Rating.objects.filter(movie_id=new_movie.movie_id).count()
            if total_user == 0:
                rating_send = 0
            else:
                rating_send = total / total_user
            return render(request, 'user_pages/showMovie.html', {'movie': new_movie,
                                                                 'rating': rating_send,
                                                                 'total': total_user,
                                                                 'userrating': user_rating})
        else:
            return start(request)
    else:
        return start(request)


def viewMovieAgain(request, movie_id, rat):
    new_movie = Movie.objects.filter(movie_id=movie_id).get()
    total = findRating(movie_id)

    total_user = Rating.objects.filter(movie_id=movie_id).count()
    if total_user == 0:
        rating_send = 0
    else:
        rating_send = total / total_user
    return render(request, 'user_pages/showMovie.html', {'movie': new_movie,
                                                         'rating': rating_send,
                                                         'total': total_user,
                                                         'userrating': rat})


def saveRating(request):
    if request.session.get('admin', False) or request.session.get('user', False):
        if request.method == 'POST':
            ratingvalue = request.POST.get('star')
            movie_id = request.POST.get('movie_id')
            user_id = request.session['userId']

            if Rating.objects.filter(user_id=user_id, movie_id=movie_id).count() == 0:
                rating_obj = Rating()
                rating_obj.movie_id = movie_id
                rating_obj.user_id = user_id
                rating_obj.rating_value = ratingvalue
                rating_obj.save()
            else:
                obj = Rating.objects.filter(user_id=user_id, movie_id=movie_id).get()
                obj.rating_value = ratingvalue
                obj.save()
            return viewMovieAgain(request, movie_id, ratingvalue)
    else:
        return start(request)


def viewMoviegenre(request):
    if request.session.get('admin', False) or request.session.get('user', False):
        cat_obj = Category.objects.filter(category_id=request.GET.get('cat_id')).get()
        movies = Movie.objects.filter(category=cat_obj)

        rating_list = []
        total_users = []
        for obj in movies:
            total = findRating(obj.movie_id)
            total_user = Rating.objects.filter(movie_id=obj.movie_id).count()

            if total == 0:
                rating_list.append(0)
                total_users.append(total_user)
            else:
                avgrate = total / total_user
                rating_list.append(avgrate)
                total_users.append(total_user)

        if len(movies) >= 1:
            found = True
        else:
            found = False

        zipped_List = zip(movies, rating_list, total_users)
        category = Category.objects.all()

        return render(request, 'user_pages/movie_search.html', {'movie': zipped_List,
                                                                'found': found,
                                                                'categories': category})
    else:
        return start(request)
