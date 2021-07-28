from django.contrib import admin

# Register your models here.
from Flixer.models import *

admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Rating)
