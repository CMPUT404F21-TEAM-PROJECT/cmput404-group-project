import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone
import environ, requests

env = environ.Env()
environ.Env.read_env()

class AuthorManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
#         # TODO: Iterate through the queryset and for any author with a foreign 'host' field (doesn't match our host name):
#         # 1. do a get request to get the author's latest details from the remote host
#         # 2. update the author in our database if those details are different from what we have
#         #    or if we recieve a 404 response, delete the author from our database 
#         # save all changes to the database then return an updated queryset
        localHost = env("LOCAL_HOST")
        for author in queryset:
            if not (localHost in author.id):
                response = requests.get(author.id)
                if response.status_code == 200 or response.status_code == 201 or response.status_code == 204 or response.status_code == 304:
                    newData = response.json()
                    author.url = newData["url"]
                    author.host = newData["host"]
                    author.displayName = newData["displayName"]
                    author.github = newData["github"]
                    author.profileImage = newData["profileImage"]
                    author.save()
                elif response.status_code == 404:
                    author.delete()
        
        return super().get_queryset()

class PostManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        localHost = env("LOCAL_HOST")
        for post in queryset:
            if not (localHost in post.id):
                response = requests.get(post.id)
                if response.status_code == 200 or response.status_code == 201 or response.status_code == 204 or response.status_code == 304:
                    newData = response.json()
                    # Intentionally left out viewableBy since it is not in spec so other teams may not have implemented
                    post.author = newData["author"]
                    post.title = newData["title"]
                    post.contentType = newData["contentType"]
                    post.content = newData["content"]
                    post.description = newData["description"]
                    post.visibility = newData["visibility"]
                    post.published = newData["published"]
                    post.source = newData["source"]
                    post.origin = newData["origin"]
                    post.categories = newData["categories"]
                    post.unlisted = newData["unlisted"]
                    post.save()
                elif response.status_code == 404:
                    post.delete()
        
        return super().get_queryset()

class CommentManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        localHost = env("LOCAL_HOST")
        for comment in queryset:
            if not (localHost in comment.id):
                response = requests.get(comment.id)
                if response.status_code == 200 or response.status_code == 201 or response.status_code == 204 or response.status_code == 304:
                    newData = response.json()
                    # Intentionally left out post_id since it is not in spec so other teams may not have implemented
                    comment.author = newData["author"]
                    comment.contentType = newData["contentType"]
                    comment.comment = newData["comment"]
                    comment.published = newData["published"]
                    comment.save()
                elif response.status_code == 404:
                    comment.delete()
        
        return super().get_queryset()

class User(AbstractUser):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(max_length=200, primary_key=True)

class Author(models.Model):
    #id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    id = models.CharField(max_length=200, primary_key=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)
    displayName = models.CharField(max_length=30)
    github = models.CharField(max_length=100, null=True, blank=True)
    profileImage = models.CharField(max_length=200, null=True, blank=True) # this will likely be a url or file path

    objects = AuthorManager()

class Like(models.Model):
    summary = models.CharField(max_length=200) #Description of like
    author = models.ForeignKey(Author, on_delete=models.CASCADE) #Sender of the like
    object = models.CharField(max_length=200) #URL of the post or comment being liked

    class Meta:
        unique_together = ('author', 'object')

    
class FollowRequest(models.Model):
    summary = models.CharField(max_length=200)
    actor = models.ForeignKey(Author,
                              on_delete=models.CASCADE,
                              related_name='fr_sent')
    object = models.ForeignKey(Author,
                               on_delete=models.CASCADE,
                               related_name='fr_received')
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('actor', 'object')

class Post(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    id = models.CharField(max_length=200, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # When author is deleted so are their posts
    title = models.CharField(max_length=200)
    contentType = models.CharField(max_length=20) # TODO: Limit to only content types allowed
    content = models.TextField()
    description = models.CharField(max_length=500)
    visibility = models.CharField(max_length=10) # TODO: Limit to only 'PUBLIC' or 'FRIENDS'
    published = models.DateTimeField(default=django.utils.timezone.now)
    source = models.CharField(default='', max_length=200)
    origin = models.CharField(default='', max_length=200)
    categories = models.CharField(max_length=200) # Should be stored as space separated list of strings
    unlisted = models.BooleanField(default=False)
    viewableBy = models.CharField(default='', max_length=200, blank=True)

    objects = PostManager()

class Comment(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    id = models.CharField(max_length=200, primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE) # When post is deleted, delete the comments
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # When author is deleted so are their comments
    contentType = models.CharField(max_length=20) # Limit to only content types allowed
    comment = models.CharField(max_length=200) # Actual content of the comment
    published = models.DateTimeField() # ISO FORMAT, Time is updated every time the comment is changed

    objects = CommentManager()

class Inbox(models.Model):
    author = models.OneToOneField(Author,
                                  on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)
    likes = models.ManyToManyField(Like)
    follow_requests = models.ManyToManyField(FollowRequest)
    comments = models.ManyToManyField(Comment)