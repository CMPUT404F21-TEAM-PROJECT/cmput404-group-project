from shutil import register_unpack_format
import uuid
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Post, Comment, User
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

# Post Mock Data

os.chdir(os.path.dirname(__file__))
imagePostPng = {
    "id": "11111111-1111-1111-1111-111111111111",
    "title":"imageTitle1",
    "contentType":"image/png;base64",
    "content":base64.b64encode(open(os.getcwd() + "/testing_media/test.png", 'rb').read()),
    "description":"imageDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10",
    "source":"imageSource1",
    "origin":"imageOrigin1",
    "categories":"imageCategories1",
    "unlisted":False
}

imagePostJpeg = {
    "id": "21111111-1111-1111-1111-111111111111",
    "title":"imageTitle1",
    "contentType":"image/jpeg;base64",
    "content":base64.b64encode(open(os.getcwd() + "/testing_media/test.jpeg", 'rb').read()),
    "description":"imageDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10",
    "source":"imageSource1",
    "origin":"imageOrigin1",
    "categories":"imageCategories1",
    "unlisted":False
}

imagePostBase64 = {
    "id": "31111111-1111-1111-1111-111111111111",
    "title":"imageTitle1",
    "contentType":"application/base64",
    "content":base64.b64encode(open(os.getcwd() + "/testing_media/test.png", 'rb').read()),
    "description":"imageDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10",
    "source":"imageSource1",
    "origin":"imageOrigin1",
    "categories":"imageCategories1",
    "unlisted":False
}

# Create your tests here.
class AuthorTestCase(TestCase):

    def setUp(self):
        self.id = uuid.uuid4()
        self.user = User.objects.create(id=self.id)
        Author.objects.create(id=self.user)

    def test_author_default_values(self):
        author = Author.objects.get(id=self.id)
        self.assertEqual(author.id, self.user)


class PostTestCase(TestCase):
    def setUp(self):
        self.id = uuid.uuid4()
        self.post_id = uuid.uuid4()
        self.user = User.objects.create(id=self.id)
        self.author = Author.objects.create(id=self.user)
        self.post = Post.objects.create(id=self.post_id, author=self.author, published=datetime.now())

    def test_author_default_values(self):
        post = Post.objects.get(id=self.post_id)
        self.assertEqual(post.id, self.post_id)
        self.assertEqual(post.author, self.author)

class AuthorEndpointTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Create 2 new users if they don't already exist
        registerUrl = "/service/register/"
        cls.client.post(registerUrl, user1, format='json')
        cls.client.post(registerUrl, user2, format='json')
        
        # Save their ids
        user1Id = str(User.objects.get(username=user1["username"]).id)
        user2Id = str(User.objects.get(username=user2["username"]).id)
        author1["id"] = user1Id
        author2["id"] = user2Id
        user1["id"] = user1Id
        user2["id"] = user2Id
        imagePostBase64["author"] = user1Id
        imagePostPng["author"] = user1Id
        imagePostJpeg["author"] = user1Id

        # Update authors
        updateUrl1 = '/service/authors/' + author1["id"] + '/'
        updateUrl2 = '/service/authors/' + author2["id"] + '/'
        
        cls.client.post(updateUrl1, author1, format='json')
        cls.client.post(updateUrl2, author2, format='json')

    def test_get_multiple_authors(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        url = '/service/authors/'

        # Get multiple authors
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure 2 authors returned
        responseJson = response.json()
        self.assertEqual(len(responseJson['items']), 2)

    def test_update_author(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        updateUrl = '/service/authors/' + author1["id"] + '/'

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
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        getUrl = '/service/authors/' + author1["id"] + '/'

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

class PostEndpointTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Create 2 new users if they don't already exist
        registerUrl = "/service/register/"
        cls.client.post(registerUrl, user1, format='json')
        cls.client.post(registerUrl, user2, format='json')
        
        # Save their ids
        user1Id = str(User.objects.get(username=user1["username"]).id)
        user2Id = str(User.objects.get(username=user2["username"]).id)
        author1["id"] = user1Id
        author2["id"] = user2Id
        user1["id"] = user1Id
        user2["id"] = user2Id
        imagePostBase64["author"] = user1Id
        imagePostPng["author"] = user1Id
        imagePostJpeg["author"] = user1Id

        # Update authors
        updateUrl1 = '/service/authors/' + author1["id"] + '/'
        updateUrl2 = '/service/authors/' + author2["id"] + '/'
        cls.client.post(updateUrl1, author1, format='json')
        cls.client.post(updateUrl2, author2, format='json')

    def test_get_image_post_jpeg(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')
        
        addPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostJpeg["id"] + '/'
        getPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostJpeg["id"] + '/image/'

        # Add an image post
        response = self.client.put(addPostUrl, imagePostJpeg, format='json', )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.jpeg", 'rb').read())

    def test_get_image_post_png(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        addPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostPng["id"] + '/'
        getPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostPng["id"] + '/image/'

        # Add an image post
        response = self.client.put(addPostUrl, imagePostPng, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.png", 'rb').read())

    def test_get_image_post_base64(self):
        # Log in as user1
        loginUrl = "/service/login/"
        self.client.post(loginUrl, user1, format='json')

        addPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostBase64["id"] + '/'
        getPostUrl = '/service/authors/' + author1["id"] + '/posts/' + imagePostBase64["id"] + '/image/'

        # Add an image post
        response = self.client.put(addPostUrl, imagePostBase64, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.png", 'rb').read())

class CommentTestCase(TestCase):

    def setUp(self):
        self.id = uuid.uuid4()
        self.post_id = uuid.uuid4()
        self.comment_id = uuid.uuid4()
        self.user = User.objects.create(id=self.id)
        self.author = Author.objects.create(id=self.user)
        self.post = Post.objects.create(id=self.post_id, author=self.author, published=datetime.now())
        Comment.objects.create(id=self.comment_id, post_id=self.post, author=self.author, published=timezone.now())

    def test_comment_default_values(self):
        comment = Comment.objects.get(id=self.comment_id)
        self.assertEqual(comment.id, self.comment_id)
        self.assertEqual(comment.author, self.author)