from django.urls import path
from . import views

app_name = "Flixer"

urlpatterns = [
    path('', views.start),
    path('login/', views.login, name="login"),
    path('home/', views.home, name="home"),
    path('home/users/', views.userPage, name="user-page"),
    path('home/movies/', views.moviePage, name="movie-page"),
    path('home/searchMovie', views.searchMovie, name="movie-search"),
    path('home/delUser', views.deleteUser, name="user-delete"),
    path('home/addUser', views.addUser, name="add-user"),
    path('home/editUser', views.editUser, name="edit-user"),

]
