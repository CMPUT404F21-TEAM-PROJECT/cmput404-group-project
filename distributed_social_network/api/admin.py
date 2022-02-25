from django.contrib import admin
from .models import Author, Post, Comment, User

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
