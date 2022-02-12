from django.contrib import admin
from .models import Author, FollowRequest

myModels = [Author, FollowRequest]
admin.site.register(myModels)
