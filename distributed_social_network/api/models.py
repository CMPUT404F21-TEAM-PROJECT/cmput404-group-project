import uuid
from django.db import models

class Author(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    url = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=30)
    github = models.CharField(max_length=100)
    profileImage = models.CharField(max_length=200) # this will likely be a url or file path
    password = models.CharField(max_length=100)
    #friends = models.CharField(max_length=200) # not sure about this attribute yet

class FollowRequest(models.Model):
    summary = models.CharField(max_length=200)
    actor = models.ForeignKey('Author',
                              on_delete=models.CASCADE,
                              related_name='actor')
    object = models.ForeignKey('Author',
                               on_delete=models.CASCADE,
                               related_name='object')
    accepted = models.BooleanField(default=False)

class Post(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # When author is deleted so are their posts
    title = models.CharField(max_length=200)
    contentType = models.CharField(max_length=20) # TODO: Limit to only content types allowed
    content = models.TextField()
    description = models.CharField(max_length=500)
    visibility = models.CharField(max_length=10) # TODO: Limit to only 'PUBLIC' or 'FRIENDS'
    published = models.DateField()
    source = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    categories = models.CharField(max_length=200) # Should be stored as space separated list of strings
    unlisted = models.BooleanField(default=False)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # id = models.CharField(max_length=200, primary_key=True) #TODO: Should they be stored as uuidfields?
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE) # When post is deleted, delete the comments
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # When author is deleted so are their comments
    contentType = models.CharField(max_length=20) # Limit to only content types allowed
    comment = models.CharField(max_length=200) # Actual content of the comment
    published = models.DateTimeField() # ISO FORMAT, Time is updated every time the comment is changed
