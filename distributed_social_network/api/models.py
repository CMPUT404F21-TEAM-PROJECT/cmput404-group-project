from django.db import models

class Author(models.Model):
    id = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    displayName = models.CharField(max_length=30)
    github = models.CharField(max_length=100)
    profileImage = models.CharField(max_length=200) # this will likely be a url or file path
    #friends = models.CharField(max_length=200) # not sure about this attribute yet