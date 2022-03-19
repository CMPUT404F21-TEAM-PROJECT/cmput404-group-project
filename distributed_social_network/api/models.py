import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Author(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # id = models.CharField(max_length=200, primary_key=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)
    displayName = models.CharField(max_length=30)
    github = models.CharField(max_length=100, null=True, blank=True)
    profileImage = models.CharField(max_length=200, null=True, blank=True) # this will likely be a url or file path

    # objects = AuthorManager()

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    # id = models.CharField(max_length=200, primary_key=True)
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

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE) # When post is deleted, delete the comments
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # When author is deleted so are their comments
    contentType = models.CharField(max_length=20) # Limit to only content types allowed
    comment = models.CharField(max_length=200) # Actual content of the comment
    published = models.DateTimeField() # ISO FORMAT, Time is updated every time the comment is changed

class Inbox(models.Model):
    author = models.OneToOneField(Author,
                                  on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)
    likes = models.ManyToManyField(Like)
    follow_requests = models.ManyToManyField(FollowRequest)
    comments = models.ManyToManyField(Comment)

# class AuthorManager(models.Manager):
#     def get_queryset(self):
#         queryset = super().get_queryset() 
#         # TODO: Iterate through the queryset and for any author with a foreign 'host' field (doesn't match our host name):
#         # 1. do a get request to get the author's latest details from the remote host
#         # 2. update the author in our database if those details are different from what we have
#         #    or if we recieve a 404 response, delete the author from our database 
#         # save all changes to the database then return an updated queryset
#         return super().get_queryset()