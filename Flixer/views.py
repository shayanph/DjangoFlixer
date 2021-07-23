from django.http import HttpResponse
from django.shortcuts import render


def say(request):
    return HttpResponse('Hello world')
