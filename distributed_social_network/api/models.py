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