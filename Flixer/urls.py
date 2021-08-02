from django.urls import path
from . import views

app_name = "Flixer"

urlpatterns = [
    path('', views.start),
    path('login/', views.login, name="login"),

    # ADMIN MODULE URLS
    path('home/', views.home, name="home"),
    path('home/logout/', views.logoutadmin, name="logout-admin"),
    path('home/users/', views.userPage, name="user-page"),
    path('home/movies/', views.moviePage, name="movie-page"),
    path('home/delUser', views.deleteUser, name="user-delete"),
    path('home/addUser', views.addUser, name="add-user"),
    path('home/editUser', views.editUser, name="edit-user"),
    path('home/addMovie', views.addMovie, name="add-movie"),
    path('home/delMovie', views.delMovie, name="del-movie"),
    path('home/editMovie', views.editMovie, name="edit-movie"),
    path('home/saveeditMovie', views.saveeditMovie, name="save-edit-movie"),
    path('home/addCat', views.addCat, name="add-category-movie"),

    # USER MODULE URLS
    path('user/', views.userHome, name="user-home"),
    path('user/logout', views.userLogout, name="user-logout"),
    path('user/profile', views.userProfile, name="user-profile"),
    path('home/saveeditUser', views.saveUserEdit, name="save-edit-user"),
    path('home/movieSearch', views.movieSearch, name="search-movie"),
    path('home/viewMovie', views.viewMovie, name="see-movie"),
    path('home/saveRating', views.saveRating, name="rate-movie"),
    path('home/genre', views.viewMoviegenre, name="see-movie-genre"),
]
