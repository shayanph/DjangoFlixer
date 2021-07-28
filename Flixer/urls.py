from django.urls import path
from . import views

app_name = "Flixer"

urlpatterns = [
    path('', views.start),
    path('login/', views.login, name="login"),
    path('home/', views.home, name="home"),

    # ADMIN MODULE URLS
    path('home/logout/', views.logoutadmin, name="logout-admin"),
    path('home/users/', views.userPage, name="user-page"),
    path('home/movies/', views.moviePage, name="movie-page"),
    path('home/searchMovie', views.searchMovie, name="movie-search"),
    path('home/delUser', views.deleteUser, name="user-delete"),
    path('home/addUser', views.addUser, name="add-user"),
    path('home/editUser', views.editUser, name="edit-user"),
    path('home/addMovie', views.addMovie, name="add-movie"),
    path('home/delMovie', views.delMovie, name="del-movie"),
    path('home/editMovie', views.editMovie, name="edit-movie"),
    path('home/saveeditMovie', views.saveeditMovie, name="save-edit-movie"),

    # USER MODULE URLS
]
