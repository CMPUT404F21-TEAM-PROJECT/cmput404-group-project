from shutil import register_unpack_format
import uuid
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Author, Post, User
from django.utils import timezone
import copy, base64, os, json
from django.db.models import Q
from http.cookies import SimpleCookie
from django.db import connections
from psycopg2.extras import Json


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

textPostPlain = {
    "id": "41111111-1111-1111-1111-111111111111",
    "title":"textPostTitle1",
    "contentType":"text/plain",
    "content":"textPostContent1",
    "description":"textDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10T09:26:03.478039-07:00",
    "source":"textSource1",
    "origin":"textOrigin1",
    "categories":"textCategories1",
    "unlisted":False,
    "viewableBy":'',
}

textPostMarkdown = {
    "id": "51111111-1111-1111-1111-111111111111",
    "title":"textPostTitle2",
    "contentType":"text/markdown",
    "content":"textPostContent2",
    "description":"textDescription2",
    "visibility":"PUBLIC",
    "published":"2022-01-11T09:26:03.478039-07:00",
    "source":"textSource2",
    "origin":"textOrigin2",
    "categories":"textCategories2",
    "unlisted":False,
    "viewableBy":'',
}

os.chdir(os.path.dirname(__file__))
imagePostPng = {
    "id": "11111111-1111-1111-1111-111111111111",
    "title":"imageTitle1",
    "contentType":"image/png;base64",
    "content":base64.b64encode(open(os.getcwd() + "/testing_media/test.png", 'rb').read()),
    "description":"imageDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10T09:26:03.478039-07:00",
    "source":"imageSource1",
    "origin":"imageOrigin1",
    "categories":"imageCategories1",
    "unlisted":False,
    "viewableBy":'',
}

imagePostJpeg = {
    "id": "21111111-1111-1111-1111-111111111111",
    "title":"imageTitle1",
    "contentType":"image/jpeg;base64",
    "content":base64.b64encode(open(os.getcwd() + "/testing_media/test.jpeg", 'rb').read()),
    "description":"imageDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10T09:26:03.478039-07:00",
    "source":"imageSource1",
    "origin":"imageOrigin1",
    "categories":"imageCategories1",
    "unlisted":False,
    "viewableBy":'',
}

imagePostBase64 = {
    "id": "31111111-1111-1111-1111-111111111111",
    "title":"imageTitle1",
    "contentType":"application/base64",
    "content":base64.b64encode(open(os.getcwd() + "/testing_media/test.png", 'rb').read()),
    "description":"imageDescription1",
    "visibility":"PUBLIC",
    "published":"2022-01-10T09:26:03.478039-07:00",
    "source":"imageSource1",
    "origin":"imageOrigin1",
    "categories":"imageCategories1",
    "unlisted":False,
    "viewableBy":'',
}

class PostTestCase(TestCase):
    def setUp(self):
        self.id = uuid.uuid4()
        self.post_id = uuid.uuid4()
        self.user = User.objects.create(id=self.id)
        self.author = Author.objects.create(id=self.user)
        self.post = Post.objects.create(id=self.post_id, author=self.author)

    def test_author_default_values(self):
        post = Post.objects.get(id=self.post_id)
        self.assertEqual(post.id, self.post_id)
        self.assertEqual(post.author, self.author)

class PostEndpointTestCase(APITestCase):
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
        textPostPlain["author"] = user1Id
        textPostMarkdown["author"] = user1Id
        imagePostBase64["author"] = user1Id
        imagePostPng["author"] = user1Id
        imagePostJpeg["author"] = user1Id

        # Update authors
        updateUrl1 = '/authors/' + author1["id"] + '/'
        updateUrl2 = '/authors/' + author2["id"] + '/'
        cls.client.post(updateUrl1, author1, format='json')
        cls.client.post(updateUrl2, author2, format='json')

    def test_get_text_post(self):

        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        postUrl = '/authors/' + author1["id"] + '/posts/' + textPostPlain["id"] + '/'

        # Add a text post
        response = self.client.put(postUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the text post
        response = self.client.get(postUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for correct attributes
        responseJson = response.json()
        self.assertEqual(responseJson["id"], textPostPlain["id"])
        self.assertEqual(responseJson["title"], textPostPlain["title"])
        self.assertEqual(responseJson["contentType"], textPostPlain["contentType"])
        self.assertEqual(responseJson["content"], textPostPlain["content"])
        self.assertEqual(responseJson["description"], textPostPlain["description"])
        self.assertEqual(responseJson["visibility"], textPostPlain["visibility"])
        self.assertEqual(responseJson["published"], textPostPlain["published"])
        self.assertEqual(responseJson["source"], textPostPlain["source"])
        self.assertEqual(responseJson["origin"], textPostPlain["origin"])
        self.assertEqual(responseJson["categories"], textPostPlain["categories"])
        self.assertEqual(responseJson["unlisted"], textPostPlain["unlisted"])
        # Check for correct author object
        self.assertEqual(responseJson["author"]["id"], author1["id"])
        self.assertEqual(responseJson["author"]["url"], author1["url"])
        self.assertEqual(responseJson["author"]["host"], author1["host"])
        self.assertEqual(responseJson["author"]["displayName"], author1["displayName"])
        self.assertEqual(responseJson["author"]["github"], author1["github"])
        self.assertEqual(responseJson["author"]["profileImage"], author1["profileImage"])

    def test_get_multiple_posts(self):
        # This test posts 2 posts of different types to the multiple posts url
        # It then gets both posts using the multiple posts url
        # It then verifies that the id of the post has changed and the content has not
        
        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        postsUrl = '/authors/' + author1["id"] + '/posts/'

        # Add 2 text posts
        response = self.client.post(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(postsUrl, textPostMarkdown, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get multiple posts
        response = self.client.get(postsUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure 2 posts returned
        responseJson = response.json()
        self.assertEqual(len(responseJson['items']), 2)

        # Since Pagenation can return random order, determine which is which
        if responseJson['items'][0]['content'] == textPostPlain['content']:
            plainPost = responseJson['items'][0]
            markdownPost = responseJson['items'][1]
        else:
            plainPost = responseJson['items'][1]
            markdownPost = responseJson['items'][0]
        
        # Assert the id has changed but the content has not
        self.assertNotEqual(plainPost['id'], textPostPlain['id'])
        self.assertEqual(plainPost['content'], textPostPlain['content'])
        self.assertNotEqual(markdownPost['id'], textPostMarkdown['id'])
        self.assertEqual(markdownPost['content'], textPostMarkdown['content'])

    def test_get_image_post_jpeg(self):
        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')
        
        addPostUrl = '/authors/' + author1["id"] + '/posts/' + imagePostJpeg["id"] + '/'
        getPostUrl = '/authors/' + author1["id"] + '/posts/' + imagePostJpeg["id"] + '/image/'

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
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        addPostUrl = '/authors/' + author1["id"] + '/posts/' + imagePostPng["id"] + '/'
        getPostUrl = '/authors/' + author1["id"] + '/posts/' + imagePostPng["id"] + '/image/'

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
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        addPostUrl = '/authors/' + author1["id"] + '/posts/' + imagePostBase64["id"] + '/'
        getPostUrl = '/authors/' + author1["id"] + '/posts/' + imagePostBase64["id"] + '/image/'

        # Add an image post
        response = self.client.put(addPostUrl, imagePostBase64, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.png", 'rb').read())

