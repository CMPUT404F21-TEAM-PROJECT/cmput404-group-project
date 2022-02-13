from django.contrib import admin
from .models import Author, Like


myModels = [Author, Like]
admin.site.register(myModels)