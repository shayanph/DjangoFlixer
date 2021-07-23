from django.urls import path
from . import views

urlpatterns = [
    path('', views.start),
    path('home/' , views.login)
]
