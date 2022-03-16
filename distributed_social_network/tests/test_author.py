from shutil import register_unpack_format
import uuid
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Author, User
from django.utils import timezone
from datetime import datetime
import copy, base64, os, json
from django.db.models import Q
from http.cookies import SimpleCookie

# User Mock Data

user1 = {
    "username":"user1",
    "password":"password1"
}

user2 = {
    "username":"user2",
    "password":"password2"
}

# Author Mock Data

author1 = {
    "url":"testingUrl1",
    "host":"testingHost1",
    "displayName":"testingDisplayName1",
    "github":"testingGithub1",
    "profileImage":"testingProfileImage1"
}

author2 = {
    "url":"testingUrl2",
    "host":"testingHost2",
    "displayName":"testingDisplayName2",
    "github":"testingGithub2",
    "profileImage":"testingProfileImage2"
}

class AuthorTestCase(TestCase):

    def setUp(self):
        self.id = uuid.uuid4()
        self.user = User.objects.create(id=self.id)
        Author.objects.create(id=self.user)

    def test_author_default_values(self):
        author = Author.objects.get(id=self.id)
        self.assertEqual(author.id, self.user)

class AuthorEndpointTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Create 2 new users if they don't already exist
        registerUrl = "/register/"
        cls.client.post(registerUrl, user1, format='json')
        cls.client.post(registerUrl, user2, format='json')
        
        # Save their ids
        user1Id = str(User.objects.get(username=user1["username"]).id)
        user2Id = str(User.objects.get(username=user2["username"]).id)
        author1["id"] = user1Id
        author2["id"] = user2Id
        user1["id"] = user1Id
        user2["id"] = user2Id

        # Update authors
        updateUrl1 = '/authors/' + author1["id"] + '/'
        updateUrl2 = '/authors/' + author2["id"] + '/'
        
        cls.client.post(updateUrl1, author1, format='json')
        cls.client.post(updateUrl2, author2, format='json')

    def test_get_multiple_authors(self):
        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        url = '/authors/'

        # Get multiple authors
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure 2 authors returned
        responseJson = response.json()
        self.assertEqual(len(responseJson['items']), 2)

    def test_update_author(self):
        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        updateUrl = '/authors/' + author1["id"] + '/'

        # Update the author
        author1Updated = copy.deepcopy(author2)
        author1Updated["id"] = author1["id"]
        response = self.client.post(updateUrl, author1Updated, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for updated attributes
        savedAuthor = Author.objects.get(id=author1["id"])
        self.assertEqual(savedAuthor.url, author1Updated["url"])
        self.assertEqual(savedAuthor.host, author1Updated["host"])
        self.assertEqual(savedAuthor.displayName, author1Updated["displayName"])
        self.assertEqual(savedAuthor.github, author1Updated["github"])
        self.assertEqual(savedAuthor.profileImage, author1Updated["profileImage"])

    def test_get_single_author(self):
        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        getUrl = '/authors/' + author1["id"] + '/'

        # Get the author
        response = self.client.get(getUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for correct attributes
        responseJson = response.json()
        self.assertEqual(responseJson["id"], author1["id"])
        self.assertEqual(responseJson["url"], author1["url"])
        self.assertEqual(responseJson["host"], author1["host"])
        self.assertEqual(responseJson["displayName"], author1["displayName"])
        self.assertEqual(responseJson["github"], author1["github"])
        self.assertEqual(responseJson["profileImage"], author1["profileImage"])
