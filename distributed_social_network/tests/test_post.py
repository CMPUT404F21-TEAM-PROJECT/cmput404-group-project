from shutil import register_unpack_format
import uuid
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Author, Post, User
from django.utils import timezone
import copy, base64, os, json, environ
from django.db.models import Q
from http.cookies import SimpleCookie
from django.db import connections
from psycopg2.extras import Json

env = environ.Env()
environ.Env.read_env()

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
    "id": str(uuid.uuid4()),
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
    "id": str(uuid.uuid4()),
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

textPostPlainFriends = {
    "id": str(uuid.uuid4()),
    "title":"textPostTitle2",
    "contentType":"text/plain",
    "content":"textPostContent2",
    "description":"textDescription2",
    "visibility":"FRIENDS",
    "published":"2022-01-10T09:26:03.478039-07:00",
    "source":"textSource2",
    "origin":"textOrigin2",
    "categories":"textCategories2",
    "unlisted":False,
    "viewableBy":'',
}

os.chdir(os.path.dirname(__file__))
imagePostPng = {
    "id": str(uuid.uuid4()),
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
    "id": str(uuid.uuid4()),
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
    "id": str(uuid.uuid4()),
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
        textPostPlainFriends["author"] = user1Id
        imagePostBase64["author"] = user1Id
        imagePostPng["author"] = user1Id
        imagePostJpeg["author"] = user1Id

    def test_get_text_post(self):

        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        postUrl = author1["id"].replace(env("LOCAL_HOST"), "") + "/posts/" + textPostPlain['id'] + "/"

        # Add a text post
        response = self.client.put(postUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the text post
        response = self.client.get(postUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for correct attributes
        responseJson = response.json()
        self.assertEqual(responseJson["id"], author1["id"] + "/posts/" + textPostPlain["id"])
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

    def test_get_multiple_posts(self):
        # This test posts 2 posts of different types to the multiple posts url
        # It then gets both posts using the multiple posts url
        # It then verifies that the id of the post has changed and the content has not
        
        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        postsUrl = author1["id"] + '/posts/'

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
        
        addPostUrl = author1["id"].replace(env("LOCAL_HOST"), "") + "/posts/" + imagePostJpeg['id'] + "/"
        getPostUrl = author1["id"].replace(env("LOCAL_HOST"), "") + '/posts/' + imagePostJpeg["id"] + '/image/'

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

        addPostUrl = author1["id"].replace(env("LOCAL_HOST"), "") + "/posts/" + imagePostPng['id'] + "/"
        getPostUrl = author1["id"].replace(env("LOCAL_HOST"), "") + '/posts/' + imagePostPng["id"] + '/image/'

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

        addPostUrl = author1["id"].replace(env("LOCAL_HOST"), "") + "/posts/" + imagePostBase64['id'] + "/"
        getPostUrl = author1["id"].replace(env("LOCAL_HOST"), "") + '/posts/' + imagePostBase64["id"] + '/image/'

        # Add an image post
        response = self.client.put(addPostUrl, imagePostBase64, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the image post
        response = self.client.get(getPostUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the image matches the posted image
        self.assertEqual(response.content, open(os.getcwd() + "/testing_media/test.png", 'rb').read())

    def test_get_public_posts(self):
        # This test posts 2 public posts of different types to the multiple posts url
        # It then posts 1 friends only post
        # It then gets all public posts using the public posts url
        # It then verifies that the id of the post has changed and the content has not
        
        # Log in as user1
        loginUrl = "/login/"
        self.client.post(loginUrl, user1, format='json')

        postsUrl = author1["id"] + '/posts/'
        publicPostsUrl = '/public-posts/'

        # Add 2 text posts
        response = self.client.post(postsUrl, textPostPlain, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(postsUrl, textPostMarkdown, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(postsUrl, textPostPlainFriends, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get public posts
        response = self.client.get(publicPostsUrl)
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
        self.assertEqual(plainPost['visibility'], "PUBLIC")
        self.assertNotEqual(markdownPost['id'], textPostMarkdown['id'])
        self.assertEqual(markdownPost['content'], textPostMarkdown['content'])
        self.assertEqual(markdownPost['visibility'], "PUBLIC")
