from django.db import models

class Author(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    url = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=30)
    github = models.CharField(max_length=100)
    profileImage = models.CharField(max_length=200) # this will likely be a url or file path
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
    description = models.CharField(max_length=500)
    visibility = models.CharField(max_length=10) # TODO: Limit to only 'PUBLIC' or 'FRIENDS'
    published = models.DateField()
