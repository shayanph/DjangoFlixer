from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from Flixer.models import *

admin.site.register(UserMovie)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Category)
