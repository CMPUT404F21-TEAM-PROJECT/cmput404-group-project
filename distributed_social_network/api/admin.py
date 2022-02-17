from django.contrib import admin
from .models import Author, FollowRequest, Post

myModels = [Author,
            FollowRequest,
            Post]
admin.site.register(myModels)
