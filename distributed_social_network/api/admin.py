from django.contrib import admin
from .models import Author, Like, Node, Post, Comment, User, FollowRequest, Inbox

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(FollowRequest)
admin.site.register(Inbox)
admin.site.register(Node)

